from dataclasses import asdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from cabinet.forms import PredictionRunForm, MedicalCardForm
from cabinet.models import PredictionRun, MedicalCard, Prediction, StentingType
from cabinet.serializer import PredictionRunFilterSerializer
from cabinet.utils import convert_medical_card_to_medical_card_data
from prediction_system_backend.tasks import task_run_prediction


class PredictionRunListAPIView(APIView):
    """Запуски прогнозов"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cabinet/prediction_run_list.html'

    def get(self, request):
        """GET-запрос"""
        filters_serializer = PredictionRunFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        filters = filters_serializer.validated_data
        qs_filter = Q()
        if status := filters.get('status'):
            qs_filter &= Q(status=status)

        if stenting_type_id := filters.get('stenting_type_id'):
            qs_filter &= Q(stenting_type_id=stenting_type_id)

        if date_start := filters.get('date_start'):
            qs_filter &= Q(created_at__gte=date_start)

        if date_end := filters.get('date_end'):
            qs_filter &= Q(created_at__lt=date_end)

        prediction_runs = (
            PredictionRun.objects.select_related('medical_card').filter(
                qs_filter,
                Q(surgeon=request.user) | Q(anesthesist=request.user),
                medical_card__isnull=False,
            )
            .order_by('status', '-created_at')
        )
        paginator = Paginator(prediction_runs, 25)
        page_number = request.query_params.get('page', 1)
        page = paginator.get_page(page_number)
        stenting_types_key = 'stenting_types:filter'
        stenting_types = cache.get(stenting_types_key)
        if not stenting_types:
            stenting_types = dict(StentingType.objects.values_list('id', 'name'))
            cache.set(stenting_types_key, stenting_types, timeout=24 * 60 * 60)
        
        context = {
            'predictions': page.object_list,
            'page_obj': page,
            'is_paginated': page.has_other_pages(),
            'available_statuses': PredictionRun.STATUS_CHOICES,
            'stenting_types': dict(StentingType.objects.values_list('id', 'name')),
            'filters': filters,
        }
        return TemplateResponse(
            request,
            self.template_name,
            context,
        )


@require_GET
@login_required(login_url=reverse_lazy('login'))
def medical_cards(request):
    """View медицинских карт"""
    medical_cards_qs = (
        MedicalCard.objects.filter(
            Q(predictionrun__surgeon=request.user)
            | Q(predictionrun__anesthesist=request.user)
            | Q(created_by=request.user),
        )
        .order_by('last_name', 'first_name', 'middle_name')
        .distinct()
    )
    paginator = Paginator(medical_cards_qs, 25)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'medical_cards': page.object_list,
        'page_obj': page,
        'is_paginated': page.has_other_pages(),
    }
    return render(request, 'cabinet/medical_cards_list.html', context)


class UserLoginView(LoginView):
    """View для авторизации пользователя"""

    template_name = 'auth/login.html'
    next_page = reverse_lazy('cabinet')


class UserLogoutView(LogoutView):
    """View для выхода пользователя из профиля"""

    next_page = reverse_lazy('login')


class PredictionRunCreateView(UserPassesTestMixin, CreateView):
    """VIew создания запуска прогноза"""

    model = PredictionRun
    form_class = PredictionRunForm
    template_name = 'cabinet/prediction_run_create.html'
    success_url = reverse_lazy('cabinet')

    object: PredictionRun

    def form_valid(self, form):
        """Проверить валидность формы"""
        self.object = form.save(commit=False)
        self.object.surgeon = self.request.user
        if self.request.user.is_staff:
            self.object.is_test = True

        self.object.save()
        form = super().form_valid(form)
        result = task_run_prediction.apply_async(
            args=(
                self.object.id,
                asdict(
                    convert_medical_card_to_medical_card_data(
                        self.object.medical_card,
                        self.object.occlusion_time,
                    ),
                ),
            ),
        )
        self.object.task_id = result.id
        self.object.save()
        return form

    def test_func(self):
        """Проверить наличие нужной группы"""
        return self.request.user.groups.filter(
            name__in=[
                'admin_group',
                'surgeon_group',
                'ml_engineer_group',
            ]
        ).exists()

    def handle_no_permission(self):
        """Отловить, что пользователь не может попасть на эту страницу"""
        return redirect(str(reverse_lazy('cabinet')))


class MedicalCardCreateView(UserPassesTestMixin, CreateView):
    """View создания новой медкарты"""

    model = MedicalCard
    form_class = MedicalCardForm
    template_name = 'cabinet/medical_card_create_or_update.html'
    success_url = reverse_lazy('prediction_new')

    new_medical_card_id: int

    def get_success_url(self):
        if self.new_medical_card_id:
            return f'{reverse_lazy("prediction_new")}?medical_card_id={self.new_medical_card_id}'

        return reverse_lazy('prediction_new')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        if self.request.user.is_staff:
            self.object.is_test = True

        self.object.save()
        self.new_medical_card_id = self.object.id
        return super().form_valid(form)

    def test_func(self):
        """Проверить наличие нужной группы"""
        return self.request.user.groups.filter(
            name__in=[
                'admin_group',
                'surgeon_group',
                'ml_engineer_group',
            ]
        ).exists()

    def handle_no_permission(self):
        """Отловить, что пользователь не может попасть на эту страницу"""
        return redirect(str(reverse_lazy('cabinet')))


class MedicalCardUpdateView(UpdateView):
    """View - детальная информация о медицинской карте"""

    model = MedicalCard
    form_class = MedicalCardForm
    success_url = reverse_lazy('medical_card_list')
    template_name = 'cabinet/medical_card_create_or_update.html'
    context_object_name = 'medical_card'

    object: MedicalCard

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        if self.request.user.is_staff:
            self.object.is_test = True

        self.object.save()
        return super().form_valid(form)


class PredictionRunDetailView(DetailView):
    """Детальная информация о запуске прогнозирования"""

    model = PredictionRun
    context_object_name = 'prediction_run'
    template_name = 'cabinet/prediction_run_detail.html'

    def get_context_data(self, **kwargs):
        """Получить контекстные данные"""
        context = super().get_context_data(**kwargs)
        context['predictions'] = Prediction.objects.filter(
            prediction_run=self.object
        ).order_by('ml_model__order')
        return context


class MedicalCardDeleteView(DeleteView):
    """View - удалить медицинскую карту"""

    model = MedicalCard
    success_url = reverse_lazy('medical_card_list')
