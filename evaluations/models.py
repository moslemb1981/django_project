from django.db import models
from users.models import User

class Evaluation(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.username} - {self.score}"
