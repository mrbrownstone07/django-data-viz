import json
import random
from django.utils import timezone
from django.db.models import Sum, Q, ExpressionWrapper, FloatField, Value, Avg
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

from data.models.mrp_data import MarketPriceData
from .models.product_inouts import ProductInOut, OUT_ORDER


KPI_TIMEDELTA = 7
MRP_TIMEDELTA = 30

class HomeView(RedirectView):
    pattern_name = "admin:index"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(days=n+1)
        

def dashboard_callback(request, context):
    out_orders = ProductInOut.objects.select_related(
        'product').filter(
            order_type=OUT_ORDER,
            order_initiated_on__lte=datetime.now(tz=timezone.get_current_timezone()),
            order_initiated_on__gt=datetime.now(tz=timezone.get_current_timezone()) + timedelta(days=-KPI_TIMEDELTA)
        ).values('product__name').annotate(total_sales=Sum('total_price'), total_units_sold=Sum('units')).order_by('total_sales')
        
        
    mrp_data = MarketPriceData.objects.select_related(
        'product').filter(
            created__lte=datetime.now(tz=timezone.get_current_timezone()),
            created__gt=datetime.now(tz=timezone.get_current_timezone()) + timedelta(days=-MRP_TIMEDELTA)
        ).values('product__name', 'created__date').annotate(avg_price=Avg('price'))

    
    mrp_data_dict = {}
    for product in mrp_data:
        if not mrp_data_dict.get(product['product__name']):
            mrp_data_dict[product['product__name']] = []
        mrp_data_dict[product['product__name']].append(float("{:.2f}".format(product['avg_price'])))          
    
    print(mrp_data_dict)
    
    thrity_days_labels = [ date.strftime('%d %b') for date in daterange(date.today() + timedelta(days=-MRP_TIMEDELTA), date.today()) ]
    
    COLORS = ["#b30000", "#7c1158", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]
               
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]
    performance_positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    performance_negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]

    context.update(
        {
            "navigation": [
                {"title": _("Sales"), "link": "/", "active": True},
                {"title": _("Prices"), "link": "#"},
                {"title": _("Settings"), "link": "#"},
            ],
            "filters": [
                {"title": _("All"), "link": "#", "active": True},
                {
                    "title": _("New"),
                    "link": "#",
                },
            ],
            "kpi": [
                {   
                    "name": f"Last {KPI_TIMEDELTA} Days",
                    "title": f"{out_order['product__name']}",
                    "sales_volume": f"{float(out_order['total_sales'])} BDT",
                    "sales_units": f"{float(out_order['total_units_sold'])}",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                } for out_order in out_orders
            ],
            "mrp_data": {                
                "title": f"Market Price Data for Last {MRP_TIMEDELTA} Days",
                "chart": json.dumps(
                    {
                        "labels": thrity_days_labels,
                        "datasets": [ 
                            {
                                "label": f"{key}",
                                "type": "line",
                                "data": mrp_data_dict[key],
                                "backgroundColor": COLORS[index],
                                "borderColor": COLORS[index],
                            } for key, index in zip(mrp_data_dict.keys(), range(len(mrp_data_dict)))
                        ],
                    }
                ),
            },             
            "performance": [
                {
                    "title": _("Last week revenue"),
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                            "datasets": [
                                {"data": performance_positive, "borderColor": "#9333ea"}
                            ],
                        }
                    ),
                },
                {
                    "title": _("Last week expenses"),
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                            "datasets": [
                                {"data": performance_negative, "borderColor": "#f43f5e"}
                            ],
                        }
                    ),
                },
            ],
            "options": json.dumps(
                {
                    "animation": True,
                    "barPercentage": 1,
                    "base": 0,
                    "grouped": False,
                    "maxBarThickness": 4,
                    "responsive": True,
                    "maintainAspectRatio": False,
                    "datasets": {
                        "bar": {
                            "borderRadius": 12,
                            "border": {
                                "width": 0,
                            },
                            "borderSkipped": "middle",
                        },
                        "line": {
                            "borderWidth": 2,
                            "pointBorderWidth": 0,
                            "pointStyle": False,
                        },
                    },
                    "plugins": {
                        "legend": {
                            "align": "end",
                            "display": True,
                            "position": "top",
                            "labels": {
                                "boxHeight": 5,
                                "boxWidth": 5,
                                "color": "#9ca3af",
                                "pointStyle": "circle",
                                "usePointStyle": True,
                            },
                        },
                        "tooltip": {
                            "enabled": True,
                            "mode": "index",
                            "intersect": False,
                        },
                    },
                    "scales": {
                        "x": {
                            "border": {
                                "dash": [5, 5],
                                "dashOffset": 5,
                                "width": 0,
                            },
                            "ticks": {
                                "color": "#9ca3af",
                                "display": True,
                                "font": {
                                    "size": 9,
                                },
                            },
                            "grid": {
                                "display": True,
                                "tickWidth": 0,
                            },
                        },
                        "y": {
                            "border": {
                                "dash": [5, 5],
                                "dashOffset": 5,
                                "width": 0,
                            },
                            "ticks": {
                                "display": True,
                                "font": {
                                    "size": 10,
                                },   
                            },
                            "beginAtZero": False,
                            "grid": {
                                "lineWidth": "function (context) {if (context.tick.value === 0) {return 1;}return 0;}",
                                "tickWidth": 0,
                            },
                        },
                    },
                },
            ),   
        },
             
    )

    return context