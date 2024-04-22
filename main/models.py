from django.db import models
from accounts.models import User


class ChatBot(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="GeminiUser", null=True
    )
    text_input = models.CharField(max_length=500)
    gemini_output = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.text_input
    

class Sales(models.Model):

    STATUS = {
        'sales': 'sales',
        'on loan': 'on loan',
        'on order': 'on order',
    }

    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    date = models.DateField()
    status = models.CharField(choices=STATUS, max_length=50)

    def __str__(self) -> str:
        return f"The sales for the month of {self.date} is {self.amount}"
