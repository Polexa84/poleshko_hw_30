import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    """
    Фильтр для модели Payment.
    """
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHODS, label='Способ оплаты')
    paid_course = django_filters.NumberFilter(field_name='paid_course', lookup_expr='exact', label='ID курса')
    paid_lesson = django_filters.NumberFilter(field_name='paid_lesson', lookup_expr='exact', label='ID урока')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('payment_date', 'payment_date'),
        ),
        label='Сортировка'
    )

    class Meta:
        model = Payment
        fields = ['payment_method', 'paid_course', 'paid_lesson', 'ordering'] # перечисляем поля по которым идет фильтрация