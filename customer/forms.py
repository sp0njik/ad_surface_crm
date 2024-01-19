from django import forms
from django.core.exceptions import ValidationError


class CompanyForm(forms.Form):
    phone = forms.CharField(label='Телефон')
    legal_address = forms.CharField(label='Юридический адрес')
    actual_address = forms.CharField(label='Фактический адрес')


    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit() or len(phone) < 10:
            raise ValidationError("Некорректный номер телефона")
        return phone
