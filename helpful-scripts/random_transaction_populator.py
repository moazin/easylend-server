from django.contrib.auth.models import User

from transactions.models import Transaction

from random import choice, randint

for i in range(10000):
    amount = randint(1, 1000)
    from_user = choice(User.objects.all())
    to_user = choice(User.objects.all())
    if from_user != to_user:
        transaction = Transaction.objects.create(from_user=from_user, to_user=to_user, amount=amount)

