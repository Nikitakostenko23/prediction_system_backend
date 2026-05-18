from django.urls import path

from cabinet.views import (
    UserLoginView,
    UserLogoutView,
    PredictionRunCreateView,
    MedicalCardCreateView,
    medical_cards,
    MedicalCardUpdateView,
    MedicalCardDeleteView,
    PredictionRunDetailView,
    PredictionRunListAPIView,
)

urlpatterns = [
    path('', PredictionRunListAPIView.as_view(), name='cabinet'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path(
        'medical_cards/new/', MedicalCardCreateView.as_view(), name='medical_card_new'
    ),
    path(
        'medical_cards/<int:pk>/',
        MedicalCardUpdateView.as_view(),
        name='medical_card_update',
    ),
    path(
        'medical_cards/<int:pk>/delete',
        MedicalCardDeleteView.as_view(),
        name='medical_card_delete',
    ),
    path('medical_cards/', medical_cards, name='medical_card_list'),
    path('prediction/new/', PredictionRunCreateView.as_view(), name='prediction_new'),
    path(
        'prediction/<int:pk>/',
        PredictionRunDetailView.as_view(),
        name='prediction_detail',
    ),
]
