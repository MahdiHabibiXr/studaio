from plugins import query as q

all_users = q.lrange('studaio_users', 0, -1)
amount = int(input('How much ?'))
for user in all_users:
    credit = q.hget(user, "credit")
    print(f'Adding credit to {user}, {credit} ==>', end='')
    q.hset(user, 'credit', int(credit) + amount)
    print(f'[{q.hget(user, "credit")}]')