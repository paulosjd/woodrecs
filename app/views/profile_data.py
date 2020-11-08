import json
import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import ProfileBoard, User
from app.serializers import ProfileSerializer
from app.utils.board_setup import BoardSetup

log = logging.getLogger(__name__)


class ProfileDataView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_params = []

    @staticmethod
    def get_profile_data(profile):
        profile_ser = ProfileSerializer(instance=profile)
        profile_data = profile_ser.data
        boards_data = []
        profile_boards = ProfileBoard.objects.filter(
            profile=profile).prefetch_related('routes').order_by('-id')
        for board in profile_boards:

            routes_set = board.routes.all()
            grades = set(a.grade for a in routes_set)
            problems = {
                grade: [
                    {'board_id': board.id,
                     'x_holds': rec.x_holds.split(','),
                     'y_holds': rec.y_holds.split(','),
                     **{k: getattr(rec, k) for k in
                        ['id', 'name', 'ticked', 'rating', 'notes']}}
                    for rec in routes_set if rec.grade == grade
                ]
                for grade in grades
            }

            board_setup = BoardSetup(
                x_num=int(board.board_dim[:2]),
                y_num=int(board.board_dim[2:])
            )

            boards_data.append({
                'board_id': str(board.id),
                'grades': list(grades),
                'problems': problems,
                'hold_set': json.loads(board.hold_set),
                'board_name': board.name,
                **{f'{s}_coords': getattr(board_setup, f'{s}_coords')
                   for s in ['x', 'y']}
            })

        boards_data.reverse()
        profile_data.update({
            'boards': boards_data
        })

        return profile_data

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            user = get_object_or_404(User, username='demo')
        profile_data = self.get_profile_data(user.profile)
        return Response(profile_data, status=status.HTTP_200_OK)
