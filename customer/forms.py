from django import forms
from django.core.exceptions import ValidationError

from ad_surface.models import Surface


class CompanyForm(forms.Form):
    phone = forms.CharField(label='Телефон')
    legal_address = forms.CharField(label='Юридический адрес')
    actual_address = forms.CharField(label='Фактический адрес')


    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit() or len(phone) < 10:
            raise ValidationError("Некорректный номер телефона")
        return phone


class PlacementForm(forms.Form):
    # surface = forms.ModelChoiceField(field=Surface.objects.get(name="name"), label="Поверхность")
    start_at = forms.DateTimeField(label="Начало размещения")
    reconciliation = forms.FileField(label="Акты")
    contract_number = forms.CharField(label="Номер договора")
    installation_cost = forms.IntegerField(label="Стоимость монтажа")
    dismantling_cost = forms.IntegerField(label="Стоимость демонтажа")
    production_cost = forms.IntegerField(label="Стоимость производства")
    placement_cost = forms.IntegerField(label="Стоимость размещения")
    accruals = forms.IntegerField(label="Начисления")