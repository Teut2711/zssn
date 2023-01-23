import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Survivor(models.Model):
    class GenderTypes(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")

    id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=False)
    age = models.PositiveIntegerField(null=False)
    gender = models.CharField(
        max_length=1,
        choices=GenderTypes.choices,
    )
    lat = models.FloatField(null=False)
    lon = models.FloatField(null=False)
    contamination = models.PositiveIntegerField(default=0)


class Item(models.Model):
    id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=False)
    points = models.PositiveIntegerField(default=0, null=False)


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4)
    survivor_id = models.ForeignKey(to=Survivor, on_delete=models.CASCADE)
    item_id = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
