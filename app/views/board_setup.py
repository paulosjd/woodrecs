from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.utils.board_setup import BoardSetup


class BoardSetupView(APIView):

    def post(self, request):
        profile = request.user.profile
        print(request.data)
        height = int(request.data.get('board_height', 0))
        width = int(request.data.get('board_width', 0))
        if height in range(10, 19) and width in range(6, 13):
            profile.board_height = height
            profile.board_width = width
            profile.save()
            board_setup = BoardSetup(x_num=width, y_num=height)
            return Response({f'{s}_coords': getattr(board_setup, f'{s}_coords') for s in ['x', 'y']},
                            status=status.HTTP_200_OK)
        print(type(width))
        print(width)
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        return Response({'status': 'Bad request', 'errors': 'Invalid'},
                        status=status.HTTP_400_BAD_REQUEST)
