from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'  # Или можно указать конкретные поля: ['id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'payment_amount', 'payment_method']