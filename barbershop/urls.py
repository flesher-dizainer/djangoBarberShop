# booking/urls.py
from django.urls import path
from .views import IndexView, ThankYouView, BookingFormView, GetServicesView, MasterDetailView, ScheduleView

app_name = 'barbershop'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Главная страница
    path('thank-you/', ThankYouView.as_view(), name='thank_you'),  # Страница благодарности
    path('booking/', BookingFormView.as_view(), name='booking'),  # Форма записи
    path('get-services/', GetServicesView.as_view(), name='get_services'),
    path('master/<int:master_id>/', MasterDetailView.as_view(), name='master_detail'),
    path('get-available-slots/', ScheduleView.as_view(), name='get_available_slots'),

]