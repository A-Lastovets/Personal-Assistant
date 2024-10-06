from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacts_home, name='contact_home'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/add/', views.add_contact, name='add_contact'),
    path('contacts/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:contact_id>/edit/', views.edit_contact, name='edit_contact'),
    path('contacts/<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),
    path('contacts/search/', views.contact_search, name='contact_search'),
    path('contacts/upcoming_birthdays/', views.upcoming_birthdays, name='upcoming_birthdays'),
]
