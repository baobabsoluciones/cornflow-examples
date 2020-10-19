from typing import List

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomApiView(APIView):
    """
    Class to handle the API endpoints
    """

    def get_list(self, request, queryset, model_serializer):
        """
        Function that gives back all the results that match the queryset

        :param request: the request done to the API, needed to check the auth.
        :param queryset: the queryset object that performs the query.
        :param model_serializer: the serializer to serialize the json result file.
        :return: a response to the request with the results.
        """
        data = queryset
        if data.count() > 0:
            serializer = model_serializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No available data'}, status=status.HTTP_204_NO_CONTENT)

    def get_detail(self, request, model, model_serializer, key, value):
        """
        Function that gives back the result of a single row on the database identified by the primary key value.

        :param request: the request done to the API, needed to check the auth.
        :param model: the database model that is going to be searched.
        :param model_serializer: the serializer to serialize the json result file.
        :param key: the primary key column in the database table.
        :param value: the value for the primary key that has to be searched.
        :return: a response to the request with the results.
        """
        try:
            instance = getattr(model.objects, 'get')([key, value])
        except model.DoesNotExist:
            return Response({'message': 'No available data'}, status=status.HTTP_204_NO_CONTENT)

        serializer = model_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post_list(self, request, queryset, model_serializer, date_fields: List[str] = None):
        """
        Function that allows to POST new data to the database.

        :param request: the request done to the API, needed to check the auth.
        :param queryset: the queryset object that performs the query and gives back the data again.
        :param model_serializer: the serializer to serialize the json result file. 
        :param date_fields: list with the names of the fields that are dates that come from the frontend.
        :return: a response to the request with the results.
        """
        data = JSONParser().parse(request)
        serializer = model_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put_list(self, request, model, queryset, model_serializer,  key: str = 'id', date_fields: List[str] = None):
        """
        Function that allows to perform a PUT to an endpoint without telling the pk value to the API.

        :param request: the request done to the API, needed to check the auth.
        :param model: the database model that is going to be searched.
        :param queryset: the queryset object that performs the query and gives back the data again.
        :param model_serializer: the serializer to serialize the json result file.
        :param key: the column name for the primary key.
        :param date_fields: list with the names of the fields that are dates that come from the frontend.
        :return: a response to the request with the results.
        """
        data = JSONParser().parse(request)

        try:
            instance = getattr(model.objects, 'get')([key, data[key]])
        except model.DoesNotExist:
            return Response({'message': 'No available data'}, status=status.HTTP_204_NO_CONTENT)

        serializer = model_serializer(instance, data)

        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put_detail(self, request, model, queryset, model_serializer, key, value, date_fields: List[str] = None):
        """
        Function that allows to perform a PUT given a primary key value.

        :param request: the request done to the API, needed to check the auth.
        :param model: the database model that is going to be searched.
        :param queryset: the queryset object that performs the query and gives back the data again.
        :param model_serializer: the serializer to serialize the json result file.
        :param key: the column name for the primary key.
        :param value: the value for the primary key that has to be searched.
        :param date_fields: list with the names of the fields that are dates that come from the frontend.
        :return: a response to the request with the results.
        """
        data = JSONParser().parse(request)

        try:
            instance = getattr(model.objects, 'get')([key, value])
        except model.DoesNotExist:
            return Response({'message': 'No available data'}, status=status.HTTP_204_NO_CONTENT)

        serializer = model_serializer(instance, data=data)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_detail(self, request, model, key, value):
        """
        Function to perform a DELETE given a primary key value

        :param request: the request done to the API, needed to check the auth.
        :param model: the database model that is going to be searched.
        :param key: the column name for the primary key.
        :param value: the value for the primary key that has to be searched.
        :return:
        """
        try:
            instance = getattr(model.objects, 'get')([key, value])
        except model.DoesNotExist:
            return Response({'message': 'No available data'}, status=status.HTTP_204_NO_CONTENT)
        if instance is None:
            return Response({'message': 'No available data'}, status=status.HTTP_204_NO_CONTENT)
        instance.delete()
        return Response({'message': 'Data has been deleted'}, status=status.HTTP_200_OK)

    @staticmethod
    def get_page(queryset, page, num):
        """
        Function to get the objects in each page given a query, a page number and a number of elements per page

        :param queryset: the queryset object that performs the query and gives back the data again.
        :param page: the page number that has to be given back.
        :param num: the number of elements per page.
        :return: the objects read and an error code
        """
        error = None
        try:
            n_rows = queryset.count()
        except Exception as e:
            print("It is a raw query: ", e)
            n_rows = len(queryset)

        if num > n_rows or num <= 0:
            num = n_rows

        try:
            paginator = Paginator(queryset, num, allow_empty_first_page=True)
        except Exception as e:
            print("It is a raw query: ", e)
            paginator = Paginator(queryset, 10, allow_empty_first_page=True)

        try:
            queryset_page = paginator.page(page)
        except PageNotAnInteger:
            queryset_page = paginator.page(1)
        except EmptyPage:
            queryset_page = paginator.page(paginator.num_pages)
        except ZeroDivisionError:
            queryset_page = queryset
            error = -1

        return queryset_page, error

    def get_list_page(self, request, queryset, model_serializer, page, num):
        """
        Function to return the results in pages given a page number and a number of elements per page

        :param request: the request done to the API, needed to check the auth.
        :param queryset: the queryset object that performs the query and gives back the data again.
        :param model_serializer: the serializer to serialize the json result file.
        :param page: the number of the page that needs to be given back.
        :param num: the number of elements in each page.
        :return: a response to the request with the results.
        """

        queryset_page, error = self.get_page(queryset, page, num)

        if error == -1:
            return Response({'message': 'No available data'}, status=status.HTTP_204_NO_CONTENT)

        data = queryset_page.object_list

        try:
            n_rows = data.count()
        except Exception as e:
            print("It is a raw query: ", e)
            n_rows = len(data)

        if n_rows > 0:
            serializer = model_serializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No available data'}, status=status.HTTP_204_NO_CONTENT)
