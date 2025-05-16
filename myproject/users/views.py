from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer