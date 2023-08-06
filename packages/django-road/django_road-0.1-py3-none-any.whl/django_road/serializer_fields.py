from rest_framework import serializers

'''
    Make the field compatible with jsonb postgres
    store binary strings, but return json, not text
    returns json as simple data structure instead of text, even if binary is set to True
'''
class RemoteDBJSONField(serializers.JSONField):

    def to_representation(self, value):
        return value
