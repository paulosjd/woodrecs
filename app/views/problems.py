import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Route
from app.models import ProfileBoard
from app.views.profile_data import ProfileDataView

log = logging.getLogger(__name__)


class ProblemsView(APIView):

    def post(self, request):
        try:
            problem_id = int(request.data.get('problem_id', 0))
        except ValueError:
            return Response({'error': 'invalid data'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update problem ticked bool
        if 'is_ticked' in request.data and problem_id:
            return self.set_problem_ticked(request.data['is_ticked'],
                                           request.user.profile, problem_id)

        # Delete existing problem
        if request.data.get('delete_problem') and problem_id:
            return self.delete_problem(request.user.profile, problem_id)

        data = {k: request.data.get(k) for k in
                ['name', 'grade', 'board_id', 'x_holds', 'y_holds']}
        if not all(data.values()):
            return Response({'error': 'missing data'},
                            status=status.HTTP_400_BAD_REQUEST)

        data['rating'] = request.data.get('rating') or 0
        data['notes'] = request.data.get('notes', '')
        try:
            data['board_id'] = int(data['board_id'])
            data['rating'] = int(data['rating'])
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
            data['profile_board'] = ProfileBoard.objects.get(
                id=data.pop('board_id')
            )
        except ProfileBoard.DoesNotExist:
            return Response({'error': 'no record for board_id'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create new problem
        if not problem_id:
            try:
                route = Route.objects.create(**data)
            except IntegrityError as e:
                log.error(e)
                return Response({'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {'problem_id': route.id,
                 **ProfileDataView.get_profile_data(request.user.profile)},
                status=status.HTTP_200_OK
            )

        # Update existing problem
        try:
            problem = Route.objects.get(id=problem_id)
        except Route.DoesNotExist:
            return Response({'error': 'no record for problem_id'},
                            status=status.HTTP_400_BAD_REQUEST)
        for k, v in data.items():
            setattr(problem, k, v)
        try:
            problem.save()
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

    @staticmethod
    def delete_problem(profile, problem_id):
        try:
            problem = Route.objects.get(id=problem_id)
        except Route.DoesNotExist:
            return Response({'error': 'Record not found'},
                            status=status.HTTP_400_BAD_REQUEST)
        problem.delete()
        return Response(
            ProfileDataView.get_profile_data(
                profile
            ),
            status=status.HTTP_200_OK
        )

    @staticmethod
    def set_problem_ticked(tick_bool, profile, problem_id):
        try:
            problem = Route.objects.get(id=problem_id)
        except Route.DoesNotExist:
            return Response({'error': 'Record not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        should_update = False
        if tick_bool and not problem.ticked:
            problem.ticked = True
            should_update = True
        if not tick_bool and problem.ticked:
            problem.ticked = False
            should_update = True

        if should_update:
            problem.save()

            return Response(ProfileDataView.get_profile_data(profile),
                            status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_200_OK)
