from . import models


class Geobase:
    regex = '[0-9]+'

    def to_python(self, identifier: int):
        result = models.Geobase.objects.filter(id=identifier)[:1]
        if not result.exists():
            raise ValueError('Geobase not found')
        return result.get()

    @staticmethod
    def to_url(value):
        return value
