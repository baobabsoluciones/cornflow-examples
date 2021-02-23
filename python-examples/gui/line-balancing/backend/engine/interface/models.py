from django.db import models


# Create your models here.
class Stations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    no_position = models.PositiveIntegerField()
    order = models.PositiveIntegerField()

    class Meta:
        db_table = 'm_stations'


class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    duration = models.FloatField()

    class Meta:
        db_table = "m_tasks"


class Precedences(models.Model):
    id = models.AutoField(primary_key=True)
    before = models.ForeignKey("Tasks", db_column="before", on_delete=models.CASCADE, related_name='before')
    after = models.ForeignKey("Tasks", db_column="after", on_delete=models.CASCADE, related_name='after')

    class Meta:
        db_table = "r_precedences"


class Solution(models.Model):
    id = models.AutoField(primary_key=True)
    station = models.ForeignKey("Stations", db_column="station", on_delete=models.CASCADE)
    task = models.ForeignKey("Tasks", db_column="task", on_delete=models.CASCADE)

    class Meta:
        db_table = "r_solution"