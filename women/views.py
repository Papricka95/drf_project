from django.forms import model_to_dict
from rest_framework import generics
from django.shortcuts import render

# Create your views here.
#Dictionary modify to JSON
from rest_framework.response import Response
#Base class
from rest_framework.views import APIView

from .models import Women
from .serializers import WomenSerializer


# class WomenApiView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


# Создание API с наследованием базового класса
#  определением CRUD операций
class WomenApiView(APIView):

    def get(self, request):
        # получаем queryset данных
        w = Women.objects.all()
        # many=True - сериал-р обрабывает СПИСОК записей
        # WomenSerializer преобразует список в соответствующий список из словаря (поэтому в конце data).
        # а Response(...)  - преобразует в байтовую JSON строку
        return Response({'posts': WomenSerializer(w, many=True).data})

    def post(self, request):
        '''
        Чтоб проверить, что все данные были переданы корректно и что все парам-ы переданы, делаем валидацию
        В самом сериализаторе WomenSerializer указаны типы данных, которые должны быть (собственно это и есть валидация)
        raise_exception=False - при нарушении валидации будет возвращаться django html страница с ошибкой :(
        а если оставить True, то не будет возвращаться такая страничка :)

        Вместо ниже закомменченых строк вызываем метод save().
        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )
        Метод, преобразующий модель в словарь, который потом функцией Response
        преобразуется в JSON для отправки клиенту.
        return Response({'post': model_to_dict(post_new)})

        Метод save() вызывает автоматически метод create в сериализаторе и
        будет добавлена новая запись.
        '''

        serializer = WomenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        # return Response({'post': WomenSerializer(post_new).data})
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs: С помощью этой коллекции можем определить
        значение pk - идентификатор записи, которую нужно поменять.
        :return:
        '''
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            # по какому ключу будем менять нашу запись
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "Method PUT not allowed"})

        # в классе WomenSerializer первым аргументом идет изменяемые данные, а второй - где будем менять - модель Women
        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        # метод save вызывает наш метод update в сериализаторе WomenSerializer.
        # Именно update, потому что в сериализатор мы передали ДВА аргумента data и instance
        serializer.save()
        return Response({"post": serializer.data})


    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "Method DELETE not allowed"})

        instance.delete()

        return Response({"post": instance})