from django.contrib import admin

# Register your models here.
from .models import Women

#регистрируем приложение Women
admin.site.register(Women)