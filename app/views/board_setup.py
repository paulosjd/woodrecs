import json
import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import ProfileBoard
from app.views.profile_data import ProfileDataView

log = logging.getLogger(__name__)


class BoardSetupView(APIView):

    def post(self, request):
        profile = request.user.profile
        board_id = request.data.get('board_id')
        board_name = request.data.get('board_name')
        edit_name = request.data.get('edit_name')
        if edit_name:
            return self.edit_name(request.user.profile, board_id, board_name)

        delete_board = request.data.get('delete_board')
        if delete_board:
            return self.delete_board(request.user.profile, board_id)

        height = int(request.data.get('board_height', 0))
        width = int(request.data.get('board_width', 0))
        hold_set = request.data.get('hold_set', {})
        if not all([
            height in range(10, 19), width in range(6, 13), board_name
        ]):
            return Response({'error': 'missing data'},
                            status=status.HTTP_400_BAD_REQUEST)

        board_dim = f'{str(width).zfill(2)}{str(height).zfill(2)}'
        if board_id:
            try:
                profile_board = ProfileBoard.objects.get(id=board_id)
            except ProfileBoard.DoesNotExist:
                return Response({'error': 'Record not found'},
                                status=status.HTTP_400_BAD_REQUEST)
            profile_board.name = board_name
            profile_board.board_dim = board_dim
        else:
            try:
                profile_board = ProfileBoard.objects.create(
                    profile=profile, name=board_name, board_dim=board_dim
                )
            except IntegrityError as e:
                log.error(e)
                return Response({'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

        profile_board.hold_set = json.dumps(hold_set)
        try:
            profile_board.save()
        except IntegrityError as e:
            log.error(e)
            return Response({'error': e},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(
            ProfileDataView.get_profile_data(
                request.user.profile
            ),
            status=status.HTTP_200_OK
        )

    @staticmethod
    def edit_name(profile, board_id, board_name):
        if board_id:
            try:
                profile_board = ProfileBoard.objects.get(id=board_id)
            except ProfileBoard.DoesNotExist:
                return Response({'error': 'Record not found'},
                                status=status.HTTP_400_BAD_REQUEST)
            profile_board.name = board_name
            profile_board.save()
            return Response(
                ProfileDataView.get_profile_data(
                    profile
                ),
                status=status.HTTP_200_OK
            )
        return Response({'error': 'board_id not provided'},
                        status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_board(profile, board_id):
        if board_id:
            try:
                profile_board = ProfileBoard.objects.get(id=board_id)
            except ProfileBoard.DoesNotExist:
                return Response({'error': 'Record not found'},
                                status=status.HTTP_400_BAD_REQUEST)
            profile_board.delete()
            return Response(
                ProfileDataView.get_profile_data(
                    profile
                ),
                status=status.HTTP_200_OK
            )
        return Response({'error': 'board_id not provided'},
                        status=status.HTTP_400_BAD_REQUEST)
