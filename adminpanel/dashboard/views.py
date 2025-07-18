import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.utils.timezone import now, timedelta
from .models import Orders

def sales_chart(request):
    """функция для отрисовки графика продаж за последний месяц"""
    last_month = now() - timedelta(days=30)
    data = (
        Orders.objects.filter(created_at__gte=last_month)
        .values("created_at__date")
        .annotate(total=Sum("final_price"))
        .order_by("created_at__date")
    )

    dates = [str(d["created_at__date"]) for d in data]
    totals = [float(d["total"]) for d in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, totals, marker='o', color='blue')
    plt.title("Продажи за последний месяц")
    plt.xlabel("Дата")
    plt.ylabel("Сумма заказов (BYN)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return HttpResponse(buffer, content_type="image/png")

