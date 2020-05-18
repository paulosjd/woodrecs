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
        hold_set = request.data.get('hold_set', {})
        board_name = request.data.get('board_name')
        board_id = request.data.get('board_id')
        print([
            height in range(10, 19), width in range(6, 13), board_name
        ])
        if not all([
            height in range(10, 19), width in range(6, 13), board_name
        ]):
            return Response({'error': 'missing data'},
                            status=status.HTTP_400_BAD_REQUEST)
        print(board_id)
        board_dim = f'{str(width).zfill(2)}{str(height).zfill(2)}'
        if board_id:
            try:
                profile_board = ProfileBoard.objects.get(id=board_id)
                profile_board.name = board_name
                profile_board.board_dim = board_dim
            except ProfileBoard.DoesNotExist:
                return Response({'error': 'Record not found'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                profile_board = ProfileBoard.objects.create(
                    profile=profile, name=board_name, board_dim=board_dim
                )
            except IntegrityError as e:
                print('except on create')
                print(e)
                return Response({'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

        profile_board.hold_set = json.dumps(hold_set)
        # TODO catch/handle integrity error
        try:
            profile_board.save()
        except IntegrityError as e:
            return Response({'error': e},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(
            ProfileDataView.get_profile_data(
                request.user.profile
            ),
            status=status.HTTP_200_OK
        )
