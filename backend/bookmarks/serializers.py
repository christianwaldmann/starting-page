from rest_framework import serializers
from .models import Bookmarks


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = None
        try:
            request = self.context['request']
            if request.method != 'GET':
                return
            fields = request.query_params.get('fields')
        except:
            pass

        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class BookmarksSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Bookmarks
        fields = ("id", "text", "url", "category")
