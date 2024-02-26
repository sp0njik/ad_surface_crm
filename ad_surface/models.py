from django.db import models
from django.core.files.images import ImageFile
from django.db.models import ExpressionWrapper, OuterRef, Exists, F, DateField
from django.utils import timezone


class Surface(models.Model):
    name: str = models.CharField(verbose_name='наименование', max_length=255)
    description: str = models.TextField(verbose_name='описание')
    width: int = models.IntegerField(verbose_name='ширина')
    height: int = models.IntegerField(verbose_name='высота')
    price: int = models.IntegerField(verbose_name='цена')
    address: str = models.CharField(verbose_name='адрес', max_length=255)
    place: str = models.CharField(verbose_name='расположнение', max_length=255)
    is_active: bool = models.BooleanField(default=False, verbose_name='активно')

    def __str__(self):
        return self.name

    def get_area(self) -> int:
        """
        Calculate the area of a rectangle.
        """
        return self.width * self.height


class SurfaceImage(models.Model):
    image: ImageFile = models.ImageField(upload_to='surfaces', verbose_name='изображение')
    surface: Surface = models.ForeignKey(Surface, on_delete=models.CASCADE)
