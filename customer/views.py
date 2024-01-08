from django.shortcuts import render, redirect
from django.db.models import QuerySet, Prefetch
from customer.models import Company, Placement

from ad_surface.views import get_free_surfaces
from ad_surface.models import Surface


def add_placement(request):
    companies: QuerySet[Company] = Company.objects.filter(is_agency=False)
    surfaces: QuerySet[Surface] = get_free_surfaces()
    print(companies)
    return render(request, 'add_placement.html', {'companies': companies, 'surfaces': surfaces})


def get_profile(request):
    """
    Retrieves the user's profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered profile HTML page.

    Raises:
        None
    """
    if not request.user.is_authenticated:
        return redirect('/login/')
    clients_list: QuerySet[Company] = Company.objects.all()
    return render(request, 'profile.html', {'clients_list': clients_list})


def get_company_page(request, company_id):
    company: Company = Company.objects\
                                .prefetch_related(
                                    Prefetch(
                                        'placements_data', 
                                        queryset=Placement.objects\
                                                            .prefetch_related(Prefetch('surface', queryset=Surface.objects.only('name').all()))\
                                                            .only('start_at', 'duration', 'reconciliation', 'invoice', 'surface', 'company')\
                                                            .all()))\
                                .only('name', 'phone', 'legal_address', 'actual_address')\
                                .get(id=company_id)
    # company_placements: QuerySet[Placement] = Placement.objects.filter(company=company)
    return render(request, 'company.html', {'company': company})



def get_placement_page(request, placement_id):
    placement: Placement = Placement.objects.get(id=placement_id)
    return render(request, 'placement.html', {'placement': placement})