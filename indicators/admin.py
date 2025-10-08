from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import Indicator, IndicatorData, ActiveMonth, IndicatorTarget


# -----------------------------
# مدل شاخص‌ها
# -----------------------------
try:
    @admin.register(Indicator)
    class IndicatorAdmin(admin.ModelAdmin):
        list_display = ('code', 'name', 'owner', 'evaluation_period', 'unit')
        search_fields = ('code', 'name', 'owner__username')
        list_filter = ('evaluation_period', 'unit')
except AlreadyRegistered:
    pass


# -----------------------------
# مدل اهداف شاخص‌ها (جدید)
# -----------------------------
try:
    @admin.register(IndicatorTarget)
    class IndicatorTargetAdmin(admin.ModelAdmin):
        list_display = ('indicator', 'year', 'annual_target')
        list_filter = ('year', 'indicator__owner')
        search_fields = ('indicator__name', 'indicator__code')
        fieldsets = (
            ('مشخصات کلی', {
                'fields': ('indicator', 'year', 'annual_target')
            }),
            ('اهداف ماهانه', {
                'fields': (
                    'jan_target', 'feb_target', 'mar_target', 'apr_target',
                    'may_target', 'jun_target', 'jul_target', 'aug_target',
                    'sep_target', 'oct_target', 'nov_target', 'dec_target'
                ),
                'classes': ('collapse',),  # بخش شکست ماهانه به صورت جمع‌شونده
            }),
        )
except AlreadyRegistered:
    pass


# -----------------------------
# مدل داده‌های شاخص‌ها
# -----------------------------
try:
    @admin.register(IndicatorData)
    class IndicatorDataAdmin(admin.ModelAdmin):
        list_display = ('indicator', 'year', 'month', 'value')
        list_filter = ('year', 'month', 'indicator__owner')
        search_fields = ('indicator__name', 'indicator__code')
except AlreadyRegistered:
    pass


# -----------------------------
# مدل ماه فعال
# -----------------------------
class ActiveMonthAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'is_active')
    list_filter = ('year', 'month')

    def has_add_permission(self, request):
        # فقط اجازهٔ ثبت یک رکورد فعال در هر سال را داشته باشیم
        if ActiveMonth.objects.filter(is_active=True).exists():
            return False
        return True


# ثبت امن ActiveMonth
try:
    admin.site.register(ActiveMonth, ActiveMonthAdmin)
except AlreadyRegistered:
    pass
except Exception:
    raise
