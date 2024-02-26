from rest_framework import generics
from rest_framework.response import Response
from .serializers import StaffProfileSerializer
from ..accounts.models import Profile

class StaffProfileAPIView(generics.RetrieveAPIView):
    serializer_class = StaffProfileSerializer
    def get_queryset(self):
        profile_id = self.kwargs['pk']
        queryset = Profile.objects.filter(id=profile_id)
        return queryset

    def get(self, request, *args, **kwargs):
        profile_instance = self.get_object()
        serializer = self.get_serializer(profile_instance)
        return Response(serializer.data)
