from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from indicators.models import Indicator, IndicatorData, ActiveMonth
from django.contrib import messages
from .models import Evaluation
from .forms import EvaluationForm

@login_required
def evaluation_list(request):
    evaluations = Evaluation.objects.select_related('employee').order_by('-date')
    return render(request, 'evaluations/evaluation_list.html', {'evaluations': evaluations})

@login_required
def evaluation_create(request):
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ارزیابی با موفقیت ذخیره شد.")
            return redirect('evaluations:list')
    else:
        form = EvaluationForm()
    return render(request, 'evaluations/evaluation_form.html', {'form': form, 'title': 'ثبت ارزیابی'})

@login_required
def evaluation_edit(request, pk):
    ev = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=ev)
        if form.is_valid():
            form.save()
            messages.success(request, "ویرایش با موفقیت انجام شد.")
            return redirect('evaluations:list')
    else:
        form = EvaluationForm(instance=ev)
    return render(request, 'evaluations/evaluation_form.html', {'form': form, 'title': 'ویرایش ارزیابی'})

@login_required
def evaluation_delete(request, pk):
    ev = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        ev.delete()
        messages.success(request, "حذف انجام شد.")
        return redirect('evaluations:list')
    return render(request, 'evaluations/evaluation_confirm_delete.html', {'obj': ev})

@login_required
def dashboard(request):
    user = request.user
    indicators = Indicator.objects.filter(owner=user)
    active_month = ActiveMonth.objects.filter(is_active=True).first()

    context = {
        'indicators_count': indicators.count(),
        'active_month': active_month,
    }
    return render(request, 'dashboard.html', context)
