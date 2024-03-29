from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.core.files.base import File
from django.core.validators import MinValueValidator

from ad_surface.models import Surface


class Company(models.Model):
    """
    A model representing a company.

    Fields:
    - name: The name of the company.
    - phone: The phone number of the company.
    - legal_address: The legal address of the company.
    - actual_address: The actual address of the company.
    - is_agency: Indicates if the company is an agency.
    - agency: The agency associated with the company.
    - placements: The list of surfaces associated with the company's placements.
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    name: str = models.CharField(verbose_name="название", max_length=100)
    phone: str = models.CharField(verbose_name="номер телефона", max_length=10)
    legal_address: str = models.CharField(
        verbose_name="юридический адрес", max_length=100
    )
    actual_address: str = models.CharField(
        verbose_name="фактический адрес", max_length=100
    )
    inn: int = models.CharField(max_length=12, verbose_name="ИНН")
    kpp = models.CharField(max_length=9, verbose_name="КПП")
    ogrn = models.CharField(max_length=13, verbose_name="ОГРН")
    checking_account = models.CharField(max_length=20, verbose_name="Расчётный счёт")
    correspondent_account = models.CharField(
        max_length=20, verbose_name="Корреспондентский счёт"
    )
    bik = models.CharField(max_length=9, verbose_name="БИК")
    bank_name = models.CharField(max_length=100, verbose_name="Название банка")
    bank_address: str = models.CharField(max_length=100, verbose_name="Адрес банка")
    is_agency: bool = models.BooleanField(verbose_name="агенство", default=False)
    agency: "Company" = models.ForeignKey(
        "self", on_delete=models.PROTECT, verbose_name="агенство", null=True, blank=True
    )
    placements: list[Surface] = models.ManyToManyField(
        Surface, through="Placement", verbose_name="размещение"
    )


class Placement(models.Model):
    surface: Surface = models.ForeignKey(
        Surface,
        on_delete=models.PROTECT,
        verbose_name="поверхность",
        related_name="orders",
    )
    company: Company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        verbose_name="организация",
        related_name="placements_data",
    )
    start_at: datetime = models.DateField(verbose_name="начало размещения")
    duration: timedelta = models.DurationField(
        verbose_name="продолжительность размещения",
        validators=[MinValueValidator(timedelta(days=1))],
    )
    invoice: File = models.FileField(null=True, blank=True, upload_to="files")
    reconciliation: File = models.FileField(null=True, blank=True, upload_to="files")
    contract_number: str = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="номер договора"
    )
    installation_cost: int = models.IntegerField(
        null=True, blank=True, verbose_name="стоимость монтажа"
    )
    dismantling_cost: int = models.IntegerField(
        null=True, blank=True, verbose_name="стоимость демонтажа"
    )
    production_cost: int = models.IntegerField(
        null=True, blank=True, verbose_name="стоимость производства"
    )
    placement_cost: int = models.IntegerField(
        null=True, blank=True, verbose_name="стоимость размещения"
    )
    accruals: int = models.IntegerField(
        null=True, blank=True, verbose_name="начисления"
    )

    def finish_at(self) -> datetime:
        return self.start_at + self.duration

    def __str__(self):
        return f'{self.company.name} - {self.surface.name} - {self.start_at.strftime("%d.%m.%Y")} - {(self.start_at + self.duration).strftime("%d.%m.%Y")}'


class PlacementFile(models.Model):
    file: File = models.FileField(upload_to="files")
    placement: Placement = models.ForeignKey(Placement, on_delete=models.CASCADE)
