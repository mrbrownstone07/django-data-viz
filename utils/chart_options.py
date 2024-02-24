CUSTOM_OPTIONS =  {
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