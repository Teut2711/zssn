from django.contrib.auth.models import User, Group
from survivors.models import Survivor, Item, Resource
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ["quantity", "id"]


class SurvivorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Survivor
        read_only_fields = ["id"]
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "lat",
            "lon",
            "reported_infected_count",
        ]






class CountSerializer(serializers.HyperlinkedModelSerializer):
    count = serializers.IntegerField(min_value=0)
    class Meta:
        model = Item
        fields = ["name" ]

class TradeSerializer(serializers.HyperlinkedModelSerializer):
    survivor_1 = CountSerializer(many=True)
    survivor_2 = CountSerializer(many=True)
 


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
