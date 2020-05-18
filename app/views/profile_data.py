import json
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import ProfileBoard, Route
from app.serializers import ProfileSerializer
from app.utils.board_setup import BoardSetup

log = logging.getLogger(__name__)


class ProfileDataView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_params = []

    def dispatch(self, request, *args, **kwargs):
        # profile_id = kwargs.pop('profile_id', '')
        # if profile_id.isdigit():
        #     self.shared_profile = get_object_or_404(Profile, id=profile_id)
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def get_profile_data(profile):
        profile_ser = ProfileSerializer(instance=profile)
        profile_data = profile_ser.data

        boards_data = []
        profile_boards = ProfileBoard.objects.filter(
            profile=profile).order_by('-id').all()
        for board in profile_boards:
            board_setup = BoardSetup(
                x_num=int(board.board_dim[:2]), y_num=int(board.board_dim[2:])
            )
            boards_data.append({
                'board_id': str(board.id),
                'hold_set': json.loads(board.hold_set),
                'board_name': board.name,
                **{f'{s}_coords': getattr(board_setup, f'{s}_coords')
                   for s in ['x', 'y']}
            })
        profile_data.update({
            'boards': boards_data
        })
        print(profile_data)
        return profile_data

    def get(self, request):
        profile_data = self.get_profile_data(request.user.profile)
        return Response(profile_data, status=status.HTTP_200_OK)
