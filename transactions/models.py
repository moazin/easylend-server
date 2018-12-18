from django.contrib.auth.models import User
from django.db import models

class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    verified =  models.BooleanField(default=False)
