import json

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import ProfileBoard
from app.views.profile_data import ProfileDataView


class BoardSetupView(APIView):

    def post(self, request):
        profile = request.user.profile
        height = int(request.data.get('board_height', 0))
        width = int(request.data.get('board_width', 0))
        hold_set = request.data.get('hold_set')

        if height in range(10, 19) and width in range(6, 13):
            profile.board_height = height
            profile.board_width = width
            profile.save()

            profile_board = None
            if isinstance(hold_set, dict):
                pb_data = dict(profile=profile,
                               board_dim=f'{str(width).zfill(2)}{str(height).zfill(2)}')
                profile_board, _ = ProfileBoard.objects.get_or_create(**pb_data)
                profile_board.hold_set = json.dumps(hold_set)
                # TODO catch/handle integrity error
                try:
                    profile_board.save()
                except IntegrityError as e:
                    return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

            profile_data = ProfileDataView.get_profile_data(request.user.profile, profile_board=profile_board)
            return Response(profile_data, status=status.HTTP_200_OK)

        return Response({'status': 'Bad request', 'errors': 'Invalid'},
                        status=status.HTTP_400_BAD_REQUEST)
