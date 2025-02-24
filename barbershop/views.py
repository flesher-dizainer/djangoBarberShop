from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Master, Service
from .forms import VisitForm

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