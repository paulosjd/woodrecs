from rest_framework import serializers

from app.models import Route


class RouteSerializer(serializers.ModelSerializer):
    board_id = serializers.IntegerField(required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Route
        fields = (
            'id', 'name', 'grade', 'x_holds', 'y_holds', 'ticked', 'notes',
            'board_id'
        )

# Example usage
# ser = RouteSerializer(data={
#     'board_id': request.data.get('board_id'),
#     **{k: getattr(route_obj, k) for k in
#        ['id', 'name', 'grade', 'x_holds', 'y_holds', 'ticked',
#         'notes']}
# })
# if ser.is_valid():
#     return Response(ser.data,
#                     status=status.HTTP_200_OK)
# return Response({'error': ''},
#                 status=status.HTTP_400_BAD_REQUEST)