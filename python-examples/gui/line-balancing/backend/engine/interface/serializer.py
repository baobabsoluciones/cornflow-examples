from rest_framework import serializers

from interface.models import Stations, Tasks, Precedences, Solution


class StationSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Stations
        fields = '__all__'

    def create(self, validated_data):
        return Stations.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.no_position = validated_data.get('no_position', instance.no_position)
        instance.order = validated_data.get('order', instance.order)
        instance.save()

        return instance


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = '__all__'

    def create(self, validated_data):
        return Tasks.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.save()

        return instance


class PrecedenceSerializer(serializers.ModelSerializer):

    before_name = serializers.CharField(source='before.name', read_only=True)
    after_name = serializers.CharField(source='after.name', read_only=True)

    class Meta:
        model = Precedences
        fields = '__all__'

    def create(self, validated_data):
        return Precedences.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.before = validated_data.get('before', instance.before)
        instance.after = validated_data.get('after', instance.after)
        instance.save()

        return instance


class SolutionSerializer(serializers.ModelSerializer):

    station_name = serializers.CharField(source='station.name', read_only=True)
    task_name = serializers.CharField(source='task.name', read_only=True)

    class Meta:
        model = Solution
        fields = '__all__'

    def create(self, validated_data):
        return Solution.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.station = validated_data.get('station', instance.station)
        instance.task = validated_data.get('task', instance.task)
        instance.save()

        return instance