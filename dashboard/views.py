from django.shortcuts import render
from evaluations.models import Evaluation
from django.db.models import Avg
from datetime import date
import calendar

def home(request):
    # داده‌های ساده برای تست نمودار
    evaluations = Evaluation.objects.all().order_by('-date')[:10]
    labels = [e.date.strftime("%Y-%m-%d") for e in evaluations]
    scores = [e.score for e in evaluations]

    context = {
        'labels': labels[::-1],  # برعکس برای ترتیب زمانی درست
        'scores': scores[::-1],
    }
    return render(request, 'dashboard/home.html', context)

def dashboard_view(request):
    evaluations = Evaluation.objects.all()
    avg_score = evaluations.aggregate(Avg('score'))['score__avg'] or 0
    total_evals = evaluations.count()

    # آرایه آخرین 6 ماه (label به شکل YYYY-MM)
    labels = []
    data = []
    today = date.today()
    for i in range(5, -1, -1):
        y = today.year
        m = today.month - i
        while m <= 0:
            m += 12
            y -= 1
        labels.append(f"{y}-{m:02d}")
        month_avg = evaluations.filter(date__year=y, date__month=m).aggregate(Avg('score'))['score__avg'] or 0
        data.append(round(month_avg, 2))

    context = {
        'avg_score': round(avg_score, 2),
        'total_evals': total_evals,
        'chart_labels': labels,
        'chart_data': data,
    }
    return render(request, 'dashboard/dashboard.html', context)
