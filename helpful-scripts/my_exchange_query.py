from django.contrib.auth.models import User
from time import time

users = User.objects.raw("select auth_user.id, auth_user.username, ((select sum(amount) from transactions_transaction WHERE from_user_id=%s AND to_user_id=auth_user.id GROUP BY to_user_id)-(select sum(amount) from transactions_transaction WHERE from_user_id=auth_user.id AND to_user_id=%s GROUP BY to_user_id)) AS exchange from auth_user", [1, 1])

# This is also possible
# select auth_user.username, lpc.person, sum(lpc.exchange) from ((select to_user_id as person, sum(amount) as exchange from transactions_transaction where from_user_id=1 group by to_user_id) union all (select from_user_id as person, (-1*sum(amount)) as exchange from transactions_transaction where to_user_id=1 group by from_user_id)) as lpc INNER JOIN auth_user ON (auth_user.id = lpc.person) group by person, auth_user.username;
