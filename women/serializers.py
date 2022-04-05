import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Women

# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


# class WomenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Women
#         fields = ('title', 'cat_id')

# исходная модель
class WomenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    # read_only=True - только для чтения, т.е при валидации учитываться не будут!
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()

    def create(self, validated_data):
        '''
        Создание объекта при POST запросе
        и словарь validate_data будет состоять из всех проверенных данных,
        которые пришли с POST запроса.
        ! При вызове метода is_valid как раз формируется ЭТОТ словарь
        '''
        return Women.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''
        instance - ссылка на объект модели Women
        validate_data - словарь из проверенных данных,
        который нужно изменить в БД
        После получения новых данных из словаря, который нам пришел.
        Второй аргумент в get это значение по умолчанию, т.е вставляется то, которое было до изменения
        '''
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.time_update = validated_data.get("time_update", instance.time_update)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.cat_id = validated_data.get("cat_id", instance.cat_id)

        instance.save()
        return instance


# функция, которая преобразует исходную модель в JSON формат
# def encode():
#     # Исходная модель
#     model = WomenModel('Angelina Jolie', 'Content: Angelina Jolie')
#     # Модель пропущенная через сериализатор - получаем словарь!
#     model_sr = WomenSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     # тут получаем JSON
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# # Ф-ия, которая преобразует JSON в словарь Python
# def decode():
#     # Поток данных, имитируется, что пришли такие данные, которые надо преобразовать в словарь обратно
#     stream = io.BytesIO(b'{"title": "Angelina Jolie", "content": "Content: Angelina Jolie"}')
#     # Само преобразование
#     data = JSONParser().parse(stream)
#     # передаем объект data, чтоб получить объект сериализация
#     # т.е чтоб сериализатор декодировал данные, надо передавать в именованный параметр data.
#     serializer = WomenSerializer(data=data)
#     # надо проверить валидность принятых данных
#     serializer.is_valid()
#     print(serializer.validated_data)