from plugins import query as q

all_users = q.lrange('studaio_users', 0, -1)
counter = 0

for user in all_users:
    username = q.hget(user, 'username')
    name = q.hget(user, 'name')
    if(q.hget(user, 'active') == 'False'):
        q.hset(user, 'active', 'True')
    active = q.hget(user, 'active')
    credit = q.hget(user, 'credit')
    if(q.hget(user,'invite') == None):
        q.hset(user, 'invite', 0)
    invite = q.hget(user, 'invite')

    print(f'{counter} : {user} : @{username} : {name} : {active} : {credit} : {invite}')
    