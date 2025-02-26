from django import forms
from .models import Visit, Service, MasterReview


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['name', 'phone', 'master', 'service', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш телефон'}),
            'master': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                self.fields['service'].queryset = Service.objects.filter(masters__id=master_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['service'].queryset = self.instance.master.services.all()

class MasterReviewForm(forms.ModelForm):
    class Meta:
        model = MasterReview
        fields = ['author', 'text', 'rating']
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш отзыв', 'rows': 4}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }

