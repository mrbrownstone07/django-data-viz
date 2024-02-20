from django.db.models import Sum
from django.shortcuts import render
from .models.product_inouts import ProductInouts, IN_ORDER, OUT_ORDER
import json
import random

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView


class HomeView(RedirectView):
    pattern_name = "admin:index"


def dashboard_callback(request, context):    
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
                {"title": _("Dashboard"), "link": "/", "active": True},
                {"title": _("Analytics"), "link": "#"},
                {"title": _("Settings"), "link": "#"},
            ],
        }
    )

    return context
