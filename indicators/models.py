from django.db import models
from users.models import User

# -----------------------------
# مدل شاخص‌ها
# -----------------------------
class Indicator(models.Model):
    PERIOD_CHOICES = [
        ('monthly', 'ماهانه'),
        ('quarterly', 'سه ماهه'),
        ('semiannual', 'شش ماهه'),
        ('annual', 'سالانه'),
    ]

    UNIT_CHOICES = [
        ('day', 'روز'),
        ('percent', 'درصد'),
        ('count', 'تعداد'),
        ('million_rial', 'میلیون ریال'),
        ('billion_rial', 'میلیارد ریال'),
        ('toman', 'تومان'),
        ('other', 'سایر'),
    ]

    code = models.CharField(max_length=50, unique=True, verbose_name="کد شاخص")
    name = models.CharField(max_length=255, verbose_name="نام شاخص")
    evaluation_period = models.CharField(max_length=20, choices=PERIOD_CHOICES, verbose_name="دوره ارزیابی")
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, verbose_name="واحد سنجش")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="indicators", verbose_name="مالک شاخص")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "شاخص"
        verbose_name_plural = "شاخص‌ها"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


# -----------------------------
# 🎯 مدل اهداف شاخص‌ها (جدید)
# -----------------------------
class IndicatorTarget(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name="targets", verbose_name="شاخص")
    year = models.PositiveSmallIntegerField(verbose_name="سال")
    annual_target = models.DecimalField(
        max_digits=20, decimal_places=2, verbose_name="هدف سالانه"
    )

    # شکست اهداف ماهانه (اختیاری)
    jan_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="فروردین")
    feb_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="اردیبهشت")
    mar_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="خرداد")
    apr_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="تیر")
    may_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="مرداد")
    jun_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="شهریور")
    jul_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="مهر")
    aug_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="آبان")
    sep_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="آذر")
    oct_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="دی")
    nov_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="بهمن")
    dec_target = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="اسفند")

    class Meta:
        unique_together = ('indicator', 'year')
        verbose_name = "هدف شاخص"
        verbose_name_plural = "اهداف شاخص‌ها"
        ordering = ['indicator', 'year']

    def __str__(self):
        return f"{self.indicator.name} ({self.year})"


# -----------------------------
# مدل داده‌های شاخص‌ها
# -----------------------------
class IndicatorData(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name="data", verbose_name="شاخص")
    month = models.PositiveSmallIntegerField(verbose_name="ماه")
    year = models.PositiveSmallIntegerField(verbose_name="سال")
    value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="مقدار واقعی"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('indicator', 'month', 'year')
        verbose_name = "داده شاخص"
        verbose_name_plural = "داده‌های شاخص‌ها"
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.indicator.code} - {self.month}/{self.year}"


# -----------------------------
# مدل ماه فعال (فقط یک تعریف نهایی)
# -----------------------------
class ActiveMonth(models.Model):
    MONTH_CHOICES = [
        (1, 'فروردین'),
        (2, 'اردیبهشت'),
        (3, 'خرداد'),
        (4, 'تیر'),
        (5, 'مرداد'),
        (6, 'شهریور'),
        (7, 'مهر'),
        (8, 'آبان'),
        (9, 'آذر'),
        (10, 'دی'),
        (11, 'بهمن'),
        (12, 'اسفند'),
    ]

    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()
    is_active = models.BooleanField(default=False, verbose_name="فعال است؟")

    class Meta:
        unique_together = ('month', 'year')
        verbose_name = "ماه فعال"
        verbose_name_plural = "ماه‌های فعال"

    def __str__(self):
        return f"{dict(self.MONTH_CHOICES).get(self.month)} {self.year}"
