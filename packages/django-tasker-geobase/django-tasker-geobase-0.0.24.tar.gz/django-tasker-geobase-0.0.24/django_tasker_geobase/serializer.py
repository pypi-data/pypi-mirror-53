from rest_framework import serializers


class Type(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)


class Structure(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    ru = serializers.CharField()
    en = serializers.CharField()
    timezone = serializers.CharField(allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    openweathermap = serializers.IntegerField(allow_null=True)
    zipcode = serializers.CharField(allow_null=True)
    type = Type()


class GeoBase(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    ru = serializers.CharField()
    en = serializers.CharField()
    timezone = serializers.CharField(allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    openweathermap = serializers.IntegerField(allow_null=True)
    zipcode = serializers.CharField(allow_null=True)
    type = Type()
    structure = Structure(many=True)


class Search(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    query = serializers.CharField()
    locality = serializers.CharField(required=False)
    street = serializers.CharField(required=False)
