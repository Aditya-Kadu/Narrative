from django.urls import path
from . import views

urlpatterns = [
    path('book-demo/', views.book_demo, name='book_demo'),
    path('available-slots/', views.get_available_slots, name='available_slots'),
    path('confirm-booking/', views.confirm_booking, name='confirm_booking'),
]
