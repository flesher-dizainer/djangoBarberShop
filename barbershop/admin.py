from django.contrib import admin
from .models import Master, Service, Visit, MasterReview

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_info')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'master', 'service', 'date')

@admin.register(MasterReview)
class MasterReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'rating', 'is_approved')
