from django.shortcuts import render

from rest_framework.response import Response

# Create your views here.
from rest_framework import viewsets
from survivors.serializers import (
    SurvivorSerializer,
    ResourceSerializer,
)

from survivors.models import Survivor, Resource
from rest_framework.decorators import action


def is_infected(survivor):
    return survivor.reported_infected_count >= 3


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


from django.db.models import Sum, Count


class GenerateReportViewSet(viewsets.ViewSet):
    def list(self, request):
        infected = Survivor.objects.filter(
            reported_infected_count__gte=3
        ).count()
        total = Survivor.objects.all().count()
        percentage_infected = round((infected / total) * 100, 3)
        percentage_not_infected = 100 - percentage_infected
        grouped = (
            Resource.objects.filter(survivor_id__reported_infected_count__lt=3)
            .values("id")
            .annotate(sums=Sum("quantity"), counts=Count("quantity"))
            .order_by()
        )
        grouped = list(
            map(lambda g: {g["id"]: g["sums"] / g["counts"]}, grouped)
        )

        return Response(
            {
                "percentage_infected": percentage_infected,
                "percentage_not_infected": percentage_not_infected,
                "average_resources": grouped,
            }
        )


class TradeViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        survivor = Survivor.objects.get(pk=pk)
        return Response(
            ResourceSerializer(
                Resource.objects.filter(survivor_id=survivor)
            ).data
        )

    def create(self, request):
        if len(request.data.keys()) != 2:
            raise ValueError("Unsupported number of traders")
        p1, p2 = list(request.data.keys())
        resources_p1 = request.data[p1]
        resources_p2 = request.data[p2]
        p1 = Survivor.objects.get(pk=p1)
        p2 = Survivor.objects.get(pk=p2)

        def update_records(p, resources_p, resources_other):
            for entry in Resource.objects.filter(survivor_id=p):
                entry.quantity += resources_other.get(
                    entry.id, 0
                ) - resources_p.get(entry.id, 0)
                entry.save()

        if not is_infected(p1) and not is_infected(p2):
            update_records(p1, resources_p1, resources_p2)
            update_records(p2, resources_p2, resources_p1)

            return Response({"status": "updated"})
        else:
            return Response({"status": "Failed due to person infected"})
