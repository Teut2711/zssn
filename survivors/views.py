from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins

from survivors.serializers import (
    UserSerializer,
    GroupSerializer,
    SurvivorSerializer,
    TradeSerializer,
)

from survivors.models import Survivor
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework.response import Response
class SurvivorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

    @action(
        methods=["get"], detail=True, url_path="increase-reported-infected-count"
    )
    def increase_infected_reported_count(self, request, pk):
        survivor = Survivor.objects.get(pk=pk)
        survivor_contamination = survivor.reported_infected_count 
        survivor.reported_infected_count = survivor_contamination+ 1
        survivor.save()
        return Response({pk:{"reported_infected_count": survivor_contamination + 1}})


class TradeViewSet(viewsets.GenericViewSet,  mixins.UpdateModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    

    serializer_class = TradeSerializer
    def update(request, *args, **kwargs):
        print(args, request)

# @api_view(http_method_names=["post"] )
# def trade_view(request):
#     serializer = TradeSerializer(data=request.data)
#     print(serializer)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
