from django.shortcuts import render
from orders.models import Order, OrderItem
from django.db.models import Sum
from django.utils.timezone import now
import matplotlib.pyplot as plt
import io
import base64
import calendar
from django.db.models.functions import TruncMonth
from django.db.models import Sum, F, FloatField
import numpy as np 
from django.db.models import Count
from users.models import User
from main.models import Product, Category
from django.db.models.functions import TruncDate


def sales_by_order():
    orders = (
        Order.objects.filter(paid=True)
        .annotate(total=Sum(F('items__price') * F('items__quantity'), output_field=FloatField()))
        .order_by('id')
    )

    order_ids = []
    totals = []

    for order in orders:
        order_ids.append(str(order.id))
        totals.append(order.total)

    plt.figure(figsize=(12, 5))
    plt.bar(order_ids, totals, color='orange', label='Сумма заказа')

    plt.title('Сумма по каждому заказу')
    plt.xlabel('Номер заказа')
    plt.ylabel('Сумма')
    plt.xticks(rotation=45)
    plt.legend()

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    return graphic

def sales_by_day():
    current_date = now()
    current_year = current_date.year
    current_month = current_date.month

    data = (
        Order.objects.filter(created__year=current_year, created__month=current_month, paid=True)
        .values('created__day')
        .annotate(total=Sum(F('items__price') * F('items__quantity'), output_field=FloatField()))
        .order_by('created__day')
    )

    days = []
    totals = []
    day_indices = []

    for idx, entry in enumerate(data):
        day = entry['created__day']
        days.append(str(day))
        totals.append(entry['total'])
        day_indices.append(idx)

    plt.figure(figsize=(10, 5))
    plt.bar(days, totals, color='lightgreen', label='Продажи по дням')

    # Линия тренда
    if len(day_indices) > 1:
        z = np.polyfit(day_indices, totals, 1)
        p = np.poly1d(z)
        trendline = p(day_indices)
        plt.plot(days, trendline, color='darkgreen', linewidth=2, label='Тренд')

    plt.title(f'Объём продаж по дням ({calendar.month_name[current_month]}, {current_year})')
    plt.xlabel('День')
    plt.ylabel('Сумма продаж')
    plt.xticks(rotation=45)
    plt.legend()

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    return graphic

def sales_by_month(request):
    current_year = now().year

    data = (
        Order.objects.filter(created__year=current_year, paid=True)
        .annotate(month=TruncMonth('created'))  
        .values('month')
        .annotate(total=Sum(F('items__price') * F('items__quantity'), output_field=FloatField()))
        .order_by('month')
    )

    months = []
    totals = []
    month_indices = []

    for idx, entry in enumerate(data):
        month_number = entry['month'].month
        months.append(calendar.month_name[month_number])
        totals.append(entry['total'])
        month_indices.append(idx)

    plt.figure(figsize=(10, 5))
    plt.bar(months, totals, color='skyblue', label='Продажи по месяцам')

    if len(month_indices) > 1:
        z = np.polyfit(month_indices, totals, 1)
        p = np.poly1d(z)
        trendline = p(month_indices)
        plt.plot(months, trendline, color='red', linewidth=2, label='Тренд')

    plt.title(f'Объём продаж по месяцам, {current_year}')
    plt.xlabel('Месяц')
    plt.ylabel('Сумма продаж')
    plt.xticks(rotation=45)
    plt.legend()

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic_month = base64.b64encode(image_png).decode('utf-8')

     # Добавляем график по дням
    graphic_day = sales_by_day()
    # Добавляем график по заказам
    graphic_orders = sales_by_order()

    return render(request, 'analytics/sales_chart.html', {
        'graphic_month': graphic_month,
        'graphic_day': graphic_day,
        'graphic_orders': graphic_orders
    })

def customer_analytics(request):
    # Получаем пользователей и их заказы
    customers = User.objects.filter(role='customer').annotate(
        orders_count=Count('order'),
        total_spent=Sum(F('order__items__price') * F('order__items__quantity'), output_field=FloatField())
    )

    # Топ-5 по покупкам
    top_customers = customers.order_by('-total_spent')[:5]
    names = [c.username for c in top_customers]
    totals = [c.total_spent or 0 for c in top_customers]

    # График: Топ-5 покупателей
    plt.figure(figsize=(10, 5))
    plt.bar(names, totals, color='purple')
    plt.title('Топ-5 покупателей по сумме покупок')
    plt.xlabel('Пользователь')
    plt.ylabel('Сумма заказов')
    plt.xticks(rotation=45)

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'analytics/customer_analytics.html', {
        'graphic': graphic,
        'customers': customers,
    })

def product_demand_analytics(request):
    # Самый популярный товар
    most_popular = Product.objects.annotate(
        order_count=Count('order_items')
    ).order_by('-order_count').first()

    # Товар, который не был заказан ни разу
    least_popular = Product.objects.annotate(
        order_count=Count('order_items')
    ).filter(order_count=0).first()

    context = {
        'most_popular': most_popular,
        'least_popular': least_popular,
    }
    return render(request, 'analytics/product_demand.html', context)


def category_analytics(request):
    category_data = (
        Category.objects.annotate(
            total_quantity=Sum('products__order_items__quantity')
        ).filter(total_quantity__gt=0)
    )

    labels = [c.name for c in category_data]
    sizes = [c.total_quantity for c in category_data]

    # Круговая диаграмма
    fig1, ax1 = plt.subplots(figsize=(6,6))
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax1.axis('equal')

    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    plt.close(fig1)
    buf1.seek(0)
    pie_chart = base64.b64encode(buf1.getvalue()).decode('utf-8')

    # --- Подготовка данных для остальных графиков ---
    daily_data = (
        OrderItem.objects
        .annotate(order_date=TruncDate('order__created'))
        .values('order_date', 'product__category__name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('order_date')
    )

    dates_set = set()
    data_by_category = {}
    for entry in daily_data:
        cat = entry['product__category__name']
        date = entry['order_date']
        qty = entry['total_quantity']
        dates_set.add(date)
        data_by_category.setdefault(cat, {})[date] = qty

    dates = sorted(dates_set)
    categories = sorted(data_by_category.keys())

    if not dates or not categories:
        # Если данных нет, вернуть только круговую диаграмму
        return render(request, 'analytics/category_analytics.html', {
            'pie_chart': pie_chart,
            'grouped_bar_chart': '',
            'heatmap': '',
            'stacked_area_chart': '',
        })

    import numpy as np
    import pandas as pd

    data_array = np.array([
        [data_by_category.get(cat, {}).get(date, 0) for date in dates]
        for cat in categories
    ])

    date_labels = [d.strftime('%d-%m') for d in dates]

    # --- Сгруппированный столбчатый график ---
    fig2, ax2 = plt.subplots(figsize=(8,4))
    width = 0.25
    x = np.arange(len(dates))
    for i, cat in enumerate(categories):
        ax2.bar(x + i*width, data_array[i], width, label=cat)
    ax2.set_xticks(x + width*(len(categories)-1)/2)
    ax2.set_xticklabels(date_labels)
    ax2.set_title('Сгруппированный столбчатый график')
    ax2.legend()
    plt.tight_layout()

    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    plt.close(fig2)
    buf2.seek(0)
    grouped_bar_chart = base64.b64encode(buf2.getvalue()).decode('utf-8')

    # --- Тепловая карта ---
    fig3, ax3 = plt.subplots(figsize=(8,3))
    im = ax3.imshow(data_array, aspect='auto', cmap='YlOrRd')
    ax3.set_yticks(np.arange(len(categories)))
    ax3.set_yticklabels(categories)
    ax3.set_xticks(np.arange(len(dates)))
    ax3.set_xticklabels(date_labels)
    for i in range(len(categories)):
        for j in range(len(dates)):
            ax3.text(j, i, data_array[i, j], ha='center', va='center', color='black')
    ax3.set_title('Тепловая карта заказов')
    fig3.colorbar(im)
    plt.tight_layout()

    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png')
    plt.close(fig3)
    buf3.seek(0)
    heatmap = base64.b64encode(buf3.getvalue()).decode('utf-8')

    # --- Накопленный график ---
    fig4, ax4 = plt.subplots(figsize=(8,4))
    ax4.stackplot(dates, data_array, labels=categories, alpha=0.8)
    ax4.set_title('Накопленный график заказов по категориям')
    ax4.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf4 = io.BytesIO()
    plt.savefig(buf4, format='png')
    plt.close(fig4)
    buf4.seek(0)
    stacked_area_chart = base64.b64encode(buf4.getvalue()).decode('utf-8')

    return render(request, 'analytics/category_analytics.html', {
        'pie_chart': pie_chart,
        'grouped_bar_chart': grouped_bar_chart,
        'heatmap': heatmap,
        'stacked_area_chart': stacked_area_chart,
    })

