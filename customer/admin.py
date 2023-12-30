from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ad_surface.models import Surface
from customer.models import Company, Placement, PlacementFile


class CompanyAdmin(UserAdmin):
    model: Company = Company
    # fieldsets = UserAdmin.fieldsets + ((None, {'fields': [field.name for field in Company._meta.fields][1:]}),)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ['name', 'phone', 'legal_address', 'actual_address', 'is_agency']}),)


class PlacementFileInlineAdmin(admin.TabularInline):
    model = PlacementFile
    extra = 0


class PlacementAdmin(admin.ModelAdmin):
    inlines = [PlacementFileInlineAdmin]
    list_display = ['id', 'company', 'surface', 'start_at_date', 'finish_at_date']
    list_filter = ['company', 'surface']

    def start_at_date(self, placement):
        return placement.start_at.strftime("%d.%m.%Y")

    def finish_at_date(self, placement):
        return (placement.start_at + placement.duration).strftime("%d.%m.%Y")


admin.site.register(Surface)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Placement, PlacementAdmin)
