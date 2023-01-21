from django.shortcuts import render

from rest_framework.response import Response

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.views import APIView
from survivors.serializers import (
    UserSerializer,
    GroupSerializer,
    SurvivorSerializer,
    ResourceSerializer,
)

from survivors.models import Survivor, Resource
from rest_framework.decorators import action


def is_infected(survivor):
    return survivor.reported_infected_count >= 3


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer


class SurvivorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer

    @action(
        methods=["get"],
        detail=True,
        url_path="increase-contamination",
    )
    def increase_contamination(self, _, pk):
        survivor = Survivor.objects.get(pk=pk)
        survivor_contamination = survivor.reported_infected_count
        survivor.reported_infected_count = survivor_contamination + 1
        survivor.save()
        return Response(
            {pk: {"reported_infected_count": survivor_contamination + 1}}
        )


class GenerateReportViewSet(viewsets.ViewSet):
    def list(self, request):
        infected = Survivor.objects.filter(
            reported_infected_count__gte=3
        ).count()
        total = Survivor.objects.all().count()
        percentage_infected = round((infected / total) * 100, 3)
        percentage_not_infected = 100 - percentage_infected
        return Response(
            {
                "percentage_infected": percentage_infected,
                "percentage_not_infected": percentage_not_infected,
                "average_resouces": [0],
            }
        )


class TradeViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        survivor = Survivor.objects.get(pk=pk)
        return Response(ResourceSerializer(Resource.objects.filter(survivor_id=survivor)))

    def create(self, request):
        print(request.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
