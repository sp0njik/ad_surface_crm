from django.shortcuts import render
from ad_surface.models import Surface
from django.utils import timezone
from customer.models import Placement
from django.db.models import Prefetch, F, ExpressionWrapper, DateField, OuterRef, Exists


def get_free_surfaces():
    """
    Retrieves a list of free surfaces.

    This function queries the database to retrieve a list of surfaces that are currently free and available for use. It does this by performing the following steps:

    1. Annotates the Placement objects with the finish_at field, which represents the datetime when the placement finishes. This is done by adding the duration to the start_at field.
    2. Filters the annotated Placement objects to only include those that have a finish_at datetime greater than the current datetime and have a surface ID matching the ID of the current surface being considered.
    3. Queries the Surface objects to retrieve the surfaces that do not have any not_finished_placements and are marked as active.
    4. Returns the retrieved list of free surfaces.

    Returns:
        list[Surface]: A list of Surface objects representing the free surfaces.

    """
    not_finished_placements = Placement.objects.annotate(
        finish_at =ExpressionWrapper(F('start_at') + F('duration'), output_field=DateField())).filter(
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
