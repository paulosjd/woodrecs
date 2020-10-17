import json
import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Route
from app.models import ProfileBoard
from app.serializers.route_ser import RouteSerializer
from app.views.profile_data import ProfileDataView

log = logging.getLogger(__name__)


class ProblemsView(APIView):

    def post(self, request):
        print(request.data)

        data = {k: request.data.get(k) for k in
                ['name', 'grade', 'board_id', 'x_holds', 'y_holds']}
        if not all(data.values()):
            return Response({'error': 'missing data'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            data['board_id'] = int(data['board_id'])
        except ValueError:
            return Response({'error': 'invalid data'},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(data['x_holds']) != len(data['y_holds']):
            return Response({'error': 'x_holds y_holds len not equal'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            data['x_holds'] = ','.join(data['x_holds'])
            data['y_holds'] = ','.join(data['y_holds'])
        except TypeError:
            return Response({'error': 'x_holds or y_holds invalid'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            problem_id = int(request.data.get('problem_id', 0))
        except ValueError:
            return Response({'error': 'invalid data'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            data['profile_board'] = ProfileBoard.objects.get(
                id=data.pop('board_id')
            )
        except ProfileBoard.DoesNotExist:
            return Response({'error': 'no record for board_id'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not problem_id:
            try:
                Route.objects.create(**data)
            except IntegrityError as e:
                log.error(e)
                return Response({'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(
                ProfileDataView.get_profile_data(
                    request.user.profile
                ),
                status=status.HTTP_200_OK
            )

        board_id = request.data.get('board_id')
        board_name = request.data.get('board_name')
        edit_name = request.data.get('edit_problem')
        # if edit_problem:
        #     return self.edit_problem(request.user.profile, board_id, board_name)
        return Response({'error': 'missing data'},
                        status=status.HTTP_400_BAD_REQUEST)

        delete_problem = request.data.get('delete_problem')
        if delete_problem:
            return self.delete_problem(request.user.profile, board_id)

        height = int(request.data.get('board_height', 0))
        width = int(request.data.get('board_width', 0))
        hold_set = request.data.get('hold_set', {})
        # print([
        #     height in range(10, 19), width in range(6, 13), board_name
        # ])
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
    def edit_problem(profile, board_id, board_name):
        pass
        # if board_id:
        #     try:
        #         profile_board = ProfileBoard.objects.get(id=board_id)
        #     except ProfileBoard.DoesNotExist:
        #         return Response({'error': 'Record not found'},
        #                         status=status.HTTP_400_BAD_REQUEST)
        #     profile_board.name = board_name
        #     profile_board.save()
        #     return Response(
        #         ProfileDataView.get_profile_data(
        #             profile
        #         ),
        #         status=status.HTTP_200_OK
        #     )
        # return Response({'error': 'board_id not provided'},
        #                 status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_problem(profile, board_id):
        pass
        # if board_id:
        #     try:
        #         profile_board = ProfileBoard.objects.get(id=board_id)
        #     except ProfileBoard.DoesNotExist:
        #         return Response({'error': 'Record not found'},
        #                         status=status.HTTP_400_BAD_REQUEST)
        #     profile_board.delete()
        #     return Response(
        #         ProfileDataView.get_profile_data(
        #             profile
        #         ),
        #         status=status.HTTP_200_OK
        #     )
        # return Response({'error': 'board_id not provided'},
        #                 status=status.HTTP_400_BAD_REQUEST)
