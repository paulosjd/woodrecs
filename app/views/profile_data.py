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
    def get_profile_data(profile, profile_board=None):
        profile_ser = ProfileSerializer(instance=profile)
        profile_data = profile_ser.data
        x_num, y_num = [profile_data[f'board_{s}']
                        for s in ['width', 'height']]
        board_setup = BoardSetup(
            x_num=x_num, y_num=y_num
        )

        # try:
        #     profile_board = ProfileBoard.objects.get(
        #         profile=profile,
        #         board_dim=f'{str(x_num).zfill(2)}{str(y_num).zfill(2)}'
        #     )
        #     hold_set = json.loads(profile_board.hold_set)
        # except ProfileBoard.DoesNotExist:
        #     hold_set = {}

        boards = []
        if not profile_board:
            profile_board = ProfileBoard.objects.first()
            # profile_board = ProfileBoard.objects.first()  . order_by  -- make preference main board first if set
        if profile_board:
            hold_set, board_name = json.loads(profile_board.hold_set), profile_board.name
        else:
            hold_set, board_name = {}, ''

        boards.append(
            {'hold_set': hold_set,
             'board_name': board_name,
             **{f'{s}_coords': getattr(board_setup, f'{s}_coords') for s in ['x', 'y']}}
        )
        profile_data.update({
            'boards': boards
        })
        print(profile_data)
        return profile_data

    def get(self, request):
        # TODO app or db-level validation that board width and height are numbers within range ...
        profile_data = self.get_profile_data(request.user.profile)
        return Response({'status': 'OK', 'data': profile_data},
                        status=status.HTTP_200_OK)
        # return Response({'status': 'Bad request', 'error': ''},
        #                  # 'errors': serializers['profile_summary'].errors},
        #                 status=status.HTTP_400_BAD_REQUEST)
