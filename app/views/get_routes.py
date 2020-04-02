import logging
from collections import namedtuple

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Profile, Route
from app.serializers import (

)

log = logging.getLogger(__name__)


class ProfileSummaryData(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_params = []


    def dispatch(self, request, *args, **kwargs):
        # profile_id = kwargs.pop('profile_id', '')
        # if profile_id.isdigit():
        #     self.shared_profile = get_object_or_404(Profile, id=profile_id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        profile = request.user.profile

        serializers = dict(zip(
            ['profile_summary', 'all_params', 'datapoints', 'bookmarks'],
            self.get_serializers(profile)
        ))
        if all([ser.is_valid() for ser in serializers.values()]):
            resp_data = {k: v.data for k, v in serializers.items()}
            resp_data.update({
                'share_requests_received': profile.get_share_requests(),
                'is_shared_view': self.shared_profile is not None,
                'date_formats': Parameter.date_formats,
                'linked_parameters': profile.get_linked_profile_parameters(),
                'blank_params':
                    [{**{field: getattr(obj.parameter, field)
                         for field in self.param_fields},
                      **ProfileParamUnitOption.param_unit_opt_dct(
                          obj.unit_option)}
                     for obj in null_data_params],
            })
            return Response(resp_data, status=status.HTTP_200_OK)
        return Response({'status': 'Bad request',
                         'errors': serializers['profile_summary'].errors},
                        status=status.HTTP_400_BAD_REQUEST)
