from django.db import models
from django.core.files.images import ImageFile
from django.db.models import ExpressionWrapper, OuterRef, Exists, F, DateField
from django.utils import timezone


class ActiveSurfaceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Surface(models.Model):
    name: str = models.CharField(verbose_name='наименование', max_length=255)
    description: str = models.TextField(verbose_name='описание')
    width: int = models.IntegerField(verbose_name='ширина, мм')
    height: int = models.IntegerField(verbose_name='высота, мм')
    price: int = models.IntegerField(verbose_name='цена')
    address: str = models.CharField(verbose_name='адрес', max_length=255)
    place: str = models.CharField(verbose_name='расположнение', max_length=255)
    is_active: bool = models.BooleanField(default=True, verbose_name='активно')
    active_surfaces = ActiveSurfaceManager()
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_area(self) -> int:
        """
        Calculate the area of a rectangle in square meters
        """
        return round((self.width * self.height) / 1000000, 2)


class SurfaceImage(models.Model):
    image: ImageFile = models.ImageField(upload_to='surfaces', verbose_name='изображение')
    surface: Surface = models.ForeignKey(Surface, on_delete=models.CASCADE)
