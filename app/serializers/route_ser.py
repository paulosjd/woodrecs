from rest_framework import serializers

from app.models import Route


class RouteSerializer(serializers.ModelSerializer):
    # available_unit_options = serializers.ListField(required=False)
    # name = serializers.CharField()
    # unit_name = serializers.CharField(required=False)
    # unit_symbol = serializers.CharField(required=False)
    # ideal_info = serializers.CharField(required=False, allow_blank=True)
    # ideal_info_url = serializers.CharField(required=False, allow_blank=True)
    # num_values = serializers.CharField(required=False, allow_blank=True)
    # id = serializers.IntegerField(required=False)

    class Meta:
        model = Route
        fields = (
            'name',
        )
