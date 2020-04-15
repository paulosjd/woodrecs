import logging
from collections import namedtuple

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Profile, Route
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

    def get(self, request):
        # TODO app or db-level validation that board width and height are numbers within range ...

        profile = request.user.profile
        profile_ser = ProfileSerializer(instance=profile)
        profile_data = profile_ser.data
        profile_data['f'] = 3
        board_setup = BoardSetup(x_num=profile_data['board_width'], y_num=profile_data['board_height'])
        profile_data.update({f'{s}_coords': getattr(board_setup, f'{s}_coords') for s in ['x', 'y']})
        return Response({'status': 'OK', 'data': profile_data},
                        status=status.HTTP_200_OK)
        # return Response({'status': 'Bad request', 'error': ''},
        #                  # 'errors': serializers['profile_summary'].errors},
        #                 status=status.HTTP_400_BAD_REQUEST)
