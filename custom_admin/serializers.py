from rest_framework import serializers

from custom_admin.models import Angel


class AngelViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Angel
        fields = ('types', 'url', 'pic', 'name')
