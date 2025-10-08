from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Avg
from decimal import Decimal
import jdatetime  # 📅 برای تاریخ شمسی

from .models import Indicator, IndicatorData, ActiveMonth, IndicatorTarget
from .forms import IndicatorDataForm

User = get_user_model()


# ----------------------------------------------------------------
# 📌 ورود داده‌های شاخص‌ها (برای کاربران عادی)
# ----------------------------------------------------------------
@login_required
def monthly_data_entry(request):
    active_month = ActiveMonth.objects.filter(is_active=True).first()
    editable = False

    if active_month:
        current_year = active_month.year
        current_month = active_month.month
        editable = True
    else:
        today_jalali = jdatetime.date.today()
        current_year = today_jalali.year
        current_month = today_jalali.month

    indicators = Indicator.objects.filter(owner=request.user)

    month_field_map = {
        1: "jan_target", 2: "feb_target", 3: "mar_target",
        4: "apr_target", 5: "may_target", 6: "jun_target",
        7: "jul_target", 8: "aug_target", 9: "sep_target",
        10: "oct_target", 11: "nov_target", 12: "dec_target",
    }

    form_data = []

    for indicator in indicators:
        obj, created = IndicatorData.objects.get_or_create(
            indicator=indicator,
            month=current_month,
            year=current_year,
            defaults={'value': None}
        )

        form = IndicatorDataForm(
            request.POST or None if editable else None,
            instance=obj,
            prefix=str(indicator.id)
        )

        target = IndicatorTarget.objects.filter(indicator=indicator, year=current_year).first()
        month_target = None
        if target:
            month_field = month_field_map.get(current_month)
            if month_field:
                month_target = getattr(target, month_field, None)

        percent = None
        if obj.value and month_target:
            try:
                percent = round((obj.value / month_target) * 100, 2)
            except ZeroDivisionError:
                percent = None

        form_data.append({
            'indicator': indicator,
            'form': form,
            'target': month_target,
            'percent': percent,
        })

    if request.method == 'POST' and editable:
        all_valid = True
        for item in form_data:
            form = item['form']
            if form.is_valid():
                form.save()
            else:
                all_valid = False

        if all_valid:
            return redirect('indicators:monthly_data')

    return render(request, 'indicators/monthly_data_entry.html', {
        'form_data': form_data,
        'month': current_month,
        'year': current_year,
        'editable': editable,
    })


# ----------------------------------------------------------------
# 📊 داشبورد مدیریتی (فقط برای ادمین‌ها)
# ----------------------------------------------------------------
@staff_member_required
def admin_dashboard(request):
    """📊 داشبورد مدیریتی شاخص‌ها - فقط برای مدیران"""

    from jdatetime import date as jdate  # ✅ اضافه شد

    # 🔹 لیست مالکان شاخص‌ها
    owners = User.objects.filter(indicators__isnull=False).distinct()

    # 🔹 دریافت owner و ماه از query params
    selected_owner_id = request.GET.get('owner')
    selected_month = request.GET.get('month')

    # 🔹 سال شمسی جاری
    today_jalali = jdate.today()
    current_year = today_jalali.year

    # 🔹 تعریف نام ماه‌های شمسی
    month_map = {
        1: "فروردین", 2: "اردیبهشت", 3: "خرداد",
        4: "تیر", 5: "مرداد", 6: "شهریور",
        7: "مهر", 8: "آبان", 9: "آذر",
        10: "دی", 11: "بهمن", 12: "اسفند",
    }

    # 🔹 فیلتر شاخص‌ها
    indicators = Indicator.objects.all()
    if selected_owner_id:
        indicators = indicators.filter(owner_id=selected_owner_id)

    dashboard_data = []

    for indicator in indicators:
        # 📊 داده‌های واقعی شاخص در سال جاری
        data_qs = IndicatorData.objects.filter(indicator=indicator, year=current_year)
        if selected_month:
            data_qs = data_qs.filter(month=selected_month)

        latest_data = data_qs.order_by('-year', '-month').first()

        # 🎯 هدف ماه مربوطه
        target = IndicatorTarget.objects.filter(indicator=indicator, year=current_year).first()
        target_value = None
        percent = None

        if target and latest_data and latest_data.month:
            # نام فیلد هدف ماهیانه را بر اساس ماه انتخابی پیدا کن
            month_field_map = {
                1: "jan_target", 2: "feb_target", 3: "mar_target",
                4: "apr_target", 5: "may_target", 6: "jun_target",
                7: "jul_target", 8: "aug_target", 9: "sep_target",
                10: "oct_target", 11: "nov_target", 12: "dec_target",
            }
            month_field = month_field_map.get(int(latest_data.month))
            if month_field and hasattr(target, month_field):
                target_value = getattr(target, month_field, None)

            if target_value and latest_data.value:
                try:
                    percent = round((latest_data.value / target_value) * 100, 2)
                except ZeroDivisionError:
                    percent = None

        dashboard_data.append({
            'indicator': indicator,
            'latest_value': latest_data.value if latest_data else None,
            'target': target_value,
            'percent': percent,
            'month': int(latest_data.month) if latest_data and latest_data.month else None,
        })

    # 🔹 میانگین درصد تحقق
    valid_percents = [d['percent'] for d in dashboard_data if d['percent'] is not None]
    avg_percent = round(sum(valid_percents) / len(valid_percents), 2) if valid_percents else 0

    # 🔹 داده‌ها برای قالب
    context = {
        'owners': owners,
        'selected_owner_id': selected_owner_id,
        'dashboard_data': dashboard_data,
        'avg_percent': avg_percent,
        'total_indicators': indicators.count(),
        'year': current_year,  # ✅ حالا مقدار سال به قالب می‌فرستد
        'now': today_jalali.strftime("%Y/%m/%d"),
        'month_map': month_map,
        'month_choices': month_map.items(),  # ✅ برای dropdown فیلتر
        'selected_month': int(selected_month) if selected_month else '',
    }

    # 🧩 برای تست: چاپ در کنسول
    print("📅 YEAR SENT TO TEMPLATE:", current_year)
    print("🗓️ MONTH CHOICES:", month_map)

    return render(request, 'indicators/admin_dashboard.html', context)
