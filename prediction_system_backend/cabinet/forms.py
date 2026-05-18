from django import forms

from cabinet.models import PredictionRun, MedicalCard, PredictionUser


class MedicalCardForm(forms.ModelForm):
    """Форма для медицинской карты"""

    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-input',
            },
            format='%Y-%m-%d',
        ),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = MedicalCard
        fields = '__all__'


class PredictionRunForm(forms.ModelForm):
    """Форма создания запуска прогнозирования"""

    class Meta:
        model = PredictionRun
        fields = [
            'anesthesist',
            'medical_card',
            'occlusion_time',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anesthesist'].queryset = PredictionUser.objects.filter(groups__name='anesthetist_group')
