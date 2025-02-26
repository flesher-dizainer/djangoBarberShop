from datetime import datetime, timedelta

from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Master, Service, Visit
from .forms import VisitForm, MasterReviewForm
from .utils import get_available_slots


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.all()  # Добавляем мастеров в контекст
        context['form'] = VisitForm()  # Добавляем форму в контекст
        return context

    def post(self, request, *args, **kwargs):
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barbershop:thank_you')  # Перенаправляем на страницу благодарности
        # Если форма невалидна, возвращаем страницу с ошибками
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ThankYouView(TemplateView):
    template_name = 'thank_you.html'


class BookingFormView(FormView):
    template_name = 'index.html'
    form_class = VisitForm
    success_url = reverse_lazy('thank_you')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.all()
        return context


class GetServicesView(View):
    def get(self, request, *args, **kwargs):
        master_id = request.GET.get('master_id')
        services = Service.objects.filter(masters__id=master_id).values('id', 'name')
        return JsonResponse({'services': list(services)})


class MasterDetailView(View):
    def get(self, request, master_id):
        master = get_object_or_404(Master, id=master_id)
        review_form = MasterReviewForm()
        reviews = master.reviews.all().order_by('-created_at')
        return render(request, 'master_detail.html', {
            'master': master,
            'review_form': review_form,
            'reviews': reviews
        })

    def post(self, request, master_id):
        master = get_object_or_404(Master, id=master_id)
        form = MasterReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.master = master
            review.save()
            return redirect('barbershop:master_detail', master_id=master_id)
        return render(request, 'master_detail.html', {
            'master': master,
            'review_form': form,
            'reviews': master.reviews.all()
        })

class ScheduleView(View):
    def get(self, request):
        master_id = request.GET.get('master_id')
        date = request.GET.get('date')
        service_id = request.GET.get('service_id')

        if not date:
            return JsonResponse({
                'available_slots': [],
                'min_date': datetime.now().strftime('%Y-%m-%dT%H:%M'),
                'max_date': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%dT%H:%M')
            })

        try:
            service_duration = Service.objects.get(id=service_id).duration
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Service not found'}, status=404)

        busy_slots = Visit.objects.filter(
            master_id=master_id,
            date__date=datetime.strptime(date, '%Y-%m-%d').date()
        ).values_list('date', 'service__duration')

        available_slots = get_available_slots(busy_slots, date, service_duration)

        return JsonResponse({
            'available_slots': available_slots,
            'min_date': datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'max_date': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%dT%H:%M')
        })
