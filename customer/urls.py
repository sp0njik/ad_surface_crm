from django.urls import path
from customer import views

urlpatterns = [
    path('add_placement/', views.add_placement),
    path('profile/', views.get_profile),
    path('company/<int:company_id>/', views.get_company_page)
]
