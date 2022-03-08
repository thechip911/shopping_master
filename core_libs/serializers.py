from rest_framework.serializers import ModelSerializer


class MetaObj:
    pass


class BaseModelSerializer(ModelSerializer):
    meta_obj = MetaObj()

    def __init__(self, *args, **kwargs):
        self.Meta = self.meta_obj  # pylint: disable=invalid-name
        super().__init__(*args, **kwargs)
