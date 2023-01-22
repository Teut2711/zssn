from django.db.models import Count, F, Sum
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from survivors.models import Resource, Survivor
from survivors.serializers import ResourceSerializer, SurvivorSerializer


def is_infected(survivor):
    return survivor.contamination >= 3


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
        survivor_contamination = survivor.contamination
        survivor.contamination = survivor_contamination + 1
        survivor.save()
        return Response({pk: {"contamination": survivor_contamination + 1}})


class GenerateReportViewSet(viewsets.ViewSet):
    def list(self, request):
        infected = Survivor.objects.filter(contamination__gte=3).count()
        total = Survivor.objects.all().count()
        percentage_infected = round((infected / total) * 100, 3)
        percentage_not_infected = 100 - percentage_infected
        grouped = (
            Resource.objects.filter(survivor_id__contamination__lt=3)
            .values("item_id__name")
            .annotate(sums=Sum("quantity"), counts=Count("quantity"))
            .order_by()
        )
        grouped = list(
            map(
                lambda g: {g["item_id__name"]: g["sums"] / g["counts"]},
                grouped,
            )
        )
        infected_people_points_lost = (
            Resource.objects.filter(survivor_id__contamination__gte=3)
            .annotate(
                infected_people_points=F("quantity") * F("item_id__points")
            )
            .first()
            .infected_people_points
        )

        return Response(
            {
                "percentage_infected": percentage_infected,
                "percentage_not_infected": percentage_not_infected,
                "average_resources": grouped,
                "infected_people_points": infected_people_points_lost,
            }
        )


class TradeViewSet(viewsets.ViewSet):
    def retrieve(self, _, pk=None):
        survivor = Survivor.objects.get(pk=pk)
        return Response(
            {
                i["item_id__name"]: i["quantity"]
                for i in Resource.objects.filter(survivor_id=survivor).values(
                    "quantity", "item_id__name"
                )
            }
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
