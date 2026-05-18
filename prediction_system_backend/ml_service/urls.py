from django.urls import path

from ml_service.views import UpdatePredictionRun

urlpatterns = [
    path(
        'prediction_runs/<int:pk>/',
        UpdatePredictionRun.as_view(),
        name='prediction_run',
    ),
]
