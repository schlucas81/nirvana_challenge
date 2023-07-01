from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from .serializers import GetDataSerializer
from .helpers import process_data
from rest_framework import status


class GetDataView(ListModelMixin, GenericAPIView):
    serializer_class = GetDataSerializer

    # GET endpoint, requires 'member_id' and optional 'strategy' both validated by serializer
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        member_id = serializer.validated_data['member_id']
        strategy = serializer.validated_data['strategy']
        try:
            res = process_data(member_id, strategy)
            return Response(res)
        except Exception:
            return Response({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
