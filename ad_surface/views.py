from django.shortcuts import render
from ad_surface.models import Surface
from django.utils import timezone
from customer.models import Placement
from django.db.models import Prefetch, F, ExpressionWrapper, DateField, OuterRef, Exists


def get_free_surfaces():
    not_finished_placements = Placement.objects.annotate(
        finish_at=ExpressionWrapper(F('start_at') + F('duration'), output_field=DateField())).filter(
        finish_at__gt=timezone.now().date(), surface=OuterRef('id'))
    free_surfaces: list[Surface] = Surface.objects.only('name').filter(~Exists(not_finished_placements),
                                                                       is_active=True)
    return free_surfaces


def index(request):
    free_surfaces = get_free_surfaces()
    # for surface in free_surfaces:
    #     # placement_list = Placement.objects.filter(surface=surface)
    #     for placement in surface.orders.all():
    #         if placement.finish_at() >= timezone.now().date():
    #             break
    #     else:
    #         free_surfaces.append(surface)

    return render(request, 'index.html', {'free_surfaces': free_surfaces})
