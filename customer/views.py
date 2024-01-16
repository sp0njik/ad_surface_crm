from django.shortcuts import render, redirect
from django.db.models import QuerySet, Prefetch
from customer.models import Company, Placement
from django.core.files.storage import FileSystemStorage

from ad_surface.views import get_free_surfaces
from ad_surface.models import Surface


def add_placement(request):
    """
    A function that adds a placement.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response containing the 'add_placement.html' template,
        with the 'companies' and 'surfaces' context variables.
    """
    companies: QuerySet[Company] = Company.objects.filter(is_agency=False)
    surfaces: QuerySet[Surface] = get_free_surfaces()
    print(companies)
    return render(
        request, "add_placement.html", {"companies": companies, "surfaces": surfaces}
    )


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
        return redirect("/login/")
    clients_list: QuerySet[Company] = Company.objects.all()
    return render(request, "profile.html", {"clients_list": clients_list})


def get_company_page(request, company_id):
    """
        Retrieves the company page with the given company ID.
        Args:
            request (HttpRequest): The HTTP request object.
            company_id (int): The ID of the company.
    +"""
    company: Company = (
        Company.objects.prefetch_related(
            Prefetch(
                "placements_data",
                queryset=Placement.objects.prefetch_related(
                    Prefetch("surface", queryset=Surface.objects.only("name").all())
                )
                .only(
                    "start_at",
                    "duration",
                    "reconciliation",
                    "invoice",
                    "surface",
                    "company",
                )
                .all(),
            )
        )
        .only("name", "phone", "legal_address", "actual_address")
        .get(id=company_id)
    )
    if request.method == "POST":
        company.phone = request.POST.get("phone")

        company.legal_address = request.POST.get("legal_address")

        company.actual_address = request.POST.get("actual_address")

        company.save()
    return render(request, "company.html", {"company": company})


def get_placement_page(request, placement_id):
    placement: Placement = Placement.objects.prefetch_related(
        Prefetch("surface", queryset=Surface.objects.only("name").all()),
        Prefetch("company", queryset=Company.objects.only("name")),
    ).get(id=placement_id)
    surface_list: QuerySet[Surface] = Surface.objects.all()
    if request.method == "POST":
        surface_id = request.POST.get("surface")
        start_at = request.POST.get("start_at")
        recconiliation = request.FILES.get("reconciliation")
        placement.surface = Surface.objects.get(id=surface_id)
        placement.start_at = start_at
        storage = FileSystemStorage()
        filename = storage.save(f"files/{recconiliation.name}", recconiliation)
        placement.reconciliation = filename
        placement.save()
    return render(
        request,
        "placement.html",
        {"placement": placement, "surface_list": surface_list},
    )
