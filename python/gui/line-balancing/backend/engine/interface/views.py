
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from interface.custom_class_view import CustomApiView
from interface.models import Stations, Tasks, Precedences, Solution
from interface.serializer import StationSerializer, TaskSerializer, PrecedenceSerializer, SolutionSerializer
from interface.solve_model import solve


# Create your views here.
class StationsView(CustomApiView):

    def __init__(self):
        self.model = Stations
        self.queryset = Stations.objects.all()
        self.serializer = StationSerializer
        self.date_fields = []
        self.key = 'id'
        super().__init__()

    def get(self, request):
        return self.get_list(request, Stations.objects.all(), StationSerializer)

    def post(self, request):
        return self.post_list(request, self.queryset, self.serializer, self.date_fields)

    def put(self, request):
        return self.put_list(request, self.model, self.queryset, self.serializer, self.key, self.date_fields)


class TasksView(CustomApiView):

    def __init__(self):
        self.model = Tasks
        self.queryset = Tasks.objects.all()
        self.serializer = TaskSerializer
        self.date_fields = []
        self.key = 'id'
        super().__init__()

    def get(self, request):
        return self.get_list(request, self.queryset, self.serializer)

    def post(self, request):
        return self.post_list(request, self.queryset, self.serializer, self.date_fields)

    def put(self, request):
        return self.put_list(request, self.model, self.queryset, self.serializer, self.key, self.date_fields)


class PrecedenceViews(CustomApiView):

    def __init__(self):
        self.model = Precedences
        self.queryset = Precedences.objects.all()
        self.serializer = PrecedenceSerializer
        self.date_fields = []
        self.key = 'id'
        super().__init__()

    def get(self, request):
        return self.get_list(request, self.queryset, self.serializer)

    def post(self, request):
        return self.post_list(request, self.queryset, self.serializer, self.date_fields)

    def put(self, request):
        return self.put_list(request, self.model, self.queryset, self.serializer, self.key, self.date_fields)


class SolutionView(CustomApiView):

    def __init__(self):
        self.model = Solution
        self.queryset = Solution.objects.all()
        self.serializer = SolutionSerializer
        self.date_fields = []
        self.key = 'id'
        super().__init__()

    def get(self, request):
        return self.get_list(request, self.queryset, self.serializer)


class SolveView(APIView):

    def get(self, request):
        print('HERE WE ARE')
        solve()
        data = Solution.objects.all()
        if data.count() > 0:
            serializer = SolutionSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No available solution'}, status=status.HTTP_204_NO_CONTENT)
