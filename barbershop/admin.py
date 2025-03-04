from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Master, Service, Visit, MasterReview


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_info', 'get_rating')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'contact_info')
    list_filter = ('services',)

    def get_rating(self, obj):
        return obj.get_rating()

    get_rating.short_description = _("Рейтинг")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'display_masters')
    list_display_links = ('name',)
    list_editable = ('price', 'duration')
    search_fields = ('name',)
    list_filter = ('price', 'duration', 'masters')

    def display_masters(self, obj):
        return ", ".join([f"{master.first_name} {master.last_name}" for master in obj.masters.all()])

    display_masters.short_description = _("Мастера")


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'master', 'service', 'date')
    list_display_links = ('name', 'phone')
    search_fields = ('name', 'phone')
    list_filter = ('master', 'service', 'date')
    date_hierarchy = 'date'


@admin.register(MasterReview)
class MasterReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'master', 'rating', 'created_at', 'is_approved')
    list_display_links = ('author',)
    list_editable = ('is_approved',)
    search_fields = ('author', 'text')
    list_filter = ('rating', 'is_approved', 'created_at', 'master')
    date_hierarchy = 'created_at'

    actions = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, _("Выбранные отзывы были одобрены"))

    approve_reviews.short_description = _("Одобрить выбранные отзывы")

    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, _("Выбранные отзывы были отклонены"))

    reject_reviews.short_description = _("Отклонить выбранные отзывы")
