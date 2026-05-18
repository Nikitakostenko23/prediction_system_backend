from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cabinet.models import PredictionRun
from ml_service.services import PredictionInterface


class UpdatePredictionRun(APIView):
    """Обновить запуск прогнозирования"""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def patch(request, pk):
        """Отменить запуск прогнозирования (если он еще не был завершен)"""
        prediction_run = get_object_or_404(PredictionRun, pk=pk, surgeon=request.user)
        PredictionInterface(prediction_run).cancel_prediction_run()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk):
        """Удалить запуск прогнозирования"""
        prediction_run = get_object_or_404(PredictionRun, pk=pk, surgeon=request.user)
        prediction_run.delete()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)
