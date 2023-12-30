from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.base import File
from django.core.validators import MinValueValidator

from ad_surface.models import Surface


class Company(AbstractUser):
    '''
        Модель
    '''
    name: str = models.CharField(verbose_name='название', max_length=100)
    phone: str = models.CharField(verbose_name='номер телефона', max_length=10)
    legal_address: str = models.CharField(verbose_name='юридический адрес', max_length=100)
    actual_address: str = models.CharField(verbose_name='фактический адрес', max_length=100)
    is_agency: bool = models.BooleanField(verbose_name='агенство', default=False)
    agency: 'Company' = models.ForeignKey('self', on_delete=models.PROTECT, verbose_name='агенство', null=True,
                                          blank=True)
    placements: list[Surface] = models.ManyToManyField(Surface, through='Placement', verbose_name='размещение')


class Placement(models.Model):
    surface: Surface = models.ForeignKey(Surface, on_delete=models.PROTECT, verbose_name='поверхность',
                                         related_name='orders')
    company: Company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='организация',
                                         related_name='placements_data')
    start_at: datetime = models.DateField(verbose_name='начало размещения')
    duration: timedelta = models.DurationField(verbose_name='продолжительность размещения',
                                               validators=[MinValueValidator(timedelta(days=1))])
    invoice: File = models.FileField(null=True, blank=True, upload_to='files')
    reconciliation: File = models.FileField(null=True, blank=True, upload_to='files')

    def finish_at(self) -> datetime:
        return self.start_at + self.duration

    def __str__(self):
        return f'{self.company.name} - {self.surface.name} - {self.start_at.strftime("%d.%m.%Y")} - {(self.start_at + self.duration).strftime("%d.%m.%Y")}'


class PlacementFile(models.Model):
    file: File = models.FileField(upload_to='files')
    placement: Placement = models.ForeignKey(Placement, on_delete=models.CASCADE)
