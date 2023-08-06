from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django.core.exceptions import FieldDoesNotExist
    
from rest_framework.generics import GenericAPIView
from rest_framework import exceptions, status
from rest_framework.response import Response

from .pagination import RoadModelPagination

'''
    ROAD RemoteDBAPI
    - the default permissions are: reading without auth, writing only for owner
    - object permissions (has_object_permission method of PermissionClass) have to be checked after retrieving the object
    - permissions are checked on initial (has_permission method of PermissionClass)
'''

'''
    import the permissions and serializers for the remotedb from settings
'''
def import_module(module):
    module = str(module)
    d = module.rfind(".")
    module_name = module[d+1:len(module)]
    m = __import__(module[0:d], globals(), locals(), [module_name])
    return getattr(m, module_name)


ROAD_MODEL_PERMISSIONS = import_module(settings.ROAD_MODEL_PERMISSIONS)
SERIALIZERS = import_module(settings.ROAD_MODEL_SERIALIZERS)

class RemoteDBAPI(GenericAPIView):

    pagination_class = RoadModelPagination

    # overrides APIView get_permissions
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires based on the model and the method
        """
        if self.model_name in ROAD_MODEL_PERMISSIONS:
            model_permissions = ROAD_MODEL_PERMISSIONS[self.model_name]
            if self.action in model_permissions:
                return [permission() for permission in model_permissions[self.action]]
            elif 'default' in model_permissions:
                return [permission() for permission in model_permissions['default']]
 
        message='The action -%s- for the model -%s- is not supported by RemoteDB' % (self.action, self.model_name)
        raise exceptions.ParseError(detail=message)


    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """

        serializer_name = '%sSerializer' % self.model_name
        
        if not hasattr(SERIALIZERS, serializer_name):
            raise ValueError('Serializer missing for %s' % self.model_name)

        serializer_class = getattr(SERIALIZERS, serializer_name)

        return serializer_class

    # called in the beginning
    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        self.Model = self.get_model(kwargs['model_name'])
        self.model_name = kwargs['model_name']
        self.action = kwargs['action']
        return request

    def get_model(self, model_name):
        ct = ContentType.objects.get(model=model_name.lower()) 
        Model = ct.model_class()
        return Model

    # route to the appropriate orm method
    def get(self, request, *args, **kwargs):
        method = getattr(self, '_%s' % self.action)
        return method(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        method = getattr(self, '_%s' % self.action)
        return method(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        method = getattr(self, '_%s' % self.action)
        return method(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        method = getattr(self, '_%s' % self.action)
        return method(request, *args, **kwargs)

    # extract filters from request
    def _get_filters(self, request):
        
        filters = {}

        for key, value in request.data.items():
            try:
                field = self.Model._meta.get_field(key)
                filters[key] = value
            except FieldDoesNotExist:
                pass

        return filters

    # orm actions
    def _get(self, request, *args, **kwargs):
        filters = self._get_filters(request)
        obj = self.Model.objects.get(**filters)
        self.check_object_permissions(request, obj)

        SerializerClass = self.get_serializer_class()

        serializer = SerializerClass(obj)
        
        return Response(serializer.data)

    def _first(self, request, *args, **kwargs):

        filters = self._get_filters(request)
        
        obj = self.Model.objects.filter(**filters).first()
        self.check_object_permissions(request, obj)

        SerializerClass = self.get_serializer_class()

        serializer = SerializerClass(obj)
        
        return Response(serializer.data)

    def _exists(self, request, *args, **kwargs):
        filters = self._get_filters(request)
        exists = self.Model.objects.filter(**filters).exists()
        return Response({'exists':exists})

    def _count(self, request, *args, **kwargs):
        filters = self._get_filters(request)
        count = self.Model.objects.filter(**filters).count()
        return Response({'count':count})

    
    # filter has to support pagination
    def _filter(self, request, *args, **kwargs):
        filters = self._get_filters(request)

        queryset = self.Model.objects.filter(**filters)

        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response([])
        
    # probably redundant to _filter
    def _fetch(self, request, *args, **kwargs):
        filters = self._get_filters(request)

        queryset = self.Model.objects.filter(**filters)

        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response([])
        

    def _save(self):
        # check if it is create or update and redirect to the appropriate method
        # for example, the client may update a user but not create users
        # registering a new user is not done by RemoteDB but by a different api instead
        pass

    def create(self, request, *args, **kwargs):
        return self._insert(request, *args, **kwargs)

    def _insert(self, request, *args, **kwargs):

        # validate the input
        SerializerClass = self.get_serializer_class()

        deserializer = SerializerClass(data=request.data)
        
        if deserializer.is_valid():
            
            data = deserializer.validated_data.copy()

            if request.user.is_authenticated == True:
                if hasattr(SerializerClass, 'assign_authenticated_user'):
                    data[SerializerClass.assign_authenticated_user] = request.user
            
            instance = self.Model(**data)
            instance.save()
        
            serializer = SerializerClass(instance)
        
            return Response(serializer.data)

        # return the error
        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _update(self, request, *args, **kwargs):

        pk = kwargs['pk']
        instance = self.Model.objects.get(pk=pk)

        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def _delete(self, request, *args, **kwargs):

        pk = kwargs['pk']
        obj = self.Model.objects.get(pk=pk)

        self.check_object_permissions(request, obj)

        # if the user has permission to delete the object, do so
        obj.delete()

        return Response({'deleted':True})
        
