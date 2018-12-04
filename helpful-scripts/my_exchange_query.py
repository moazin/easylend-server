from django.contrib.auth.models import User
from time import time

users = User.objects.raw("select auth_user.id, auth_user.username, ((select sum(amount) from transactions_transaction WHERE from_user_id=%s AND to_user_id=auth_user.id GROUP BY to_user_id)-(select sum(amount) from transactions_transaction WHERE from_user_id=auth_user.id AND to_user_id=%s GROUP BY to_user_id)) AS exchange from auth_user", [1, 1])
