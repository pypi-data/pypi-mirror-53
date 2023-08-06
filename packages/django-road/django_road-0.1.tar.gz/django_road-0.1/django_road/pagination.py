from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

# return just a list of dictionaries to make the road JS ORM work
class RoadModelPagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        return Response(data)

    
