from rest_framework import serializers

class PersonSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)



class UpdatePersonSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)


class GetPersonSerializer(serializers.Serializer):
    person_id = serializers.CharField(source='_id')
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()


class DeletePersonSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)