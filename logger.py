from plugins import query as q

all_users = q.lrange('studaio_users', 0, -1)
all_outputs = q.lrange('outputs', 0, -1)

counter =0
cr0 = 0
cr1 = 0
cr2 = 0
cr3 = 0
cr4 = 0
cr5 = 0
cr6 = 0
print('All users data : \n')

for user in all_users:
    username = q.hget(user, 'username')

    name = q.hget(user, 'name')

    if(q.hget(user, 'active') == 'False' or q.hget(user, 'active') == None):
        q.hset(user, 'active', 'True')
    active = q.hget(user, 'active')

    if(q.hget(user, 'credit') == None):
        q.hset(user, 'credit', 0)
    credit = int(q.hget(user, 'credit'))

    if(credit == 0) : cr0 = cr0 + 1
    elif(credit == '1') : cr1 = cr1 + 1
    elif(credit == 2) : cr2 = cr2 + 1
    elif(credit == 3) : cr3 = cr3 + 1
    elif(credit == 4) : cr4 = cr4 + 1
    elif(credit == 5) : cr5 = cr5 + 1
    elif(credit > 5) : cr6 = cr6 + 1

    if(q.hget(user,'invite') == None):
        q.hset(user, 'invite', 0)
    invite = q.hget(user, 'invite')

    print(f'{counter} : {user} : @{username} : {name} : {active} : {credit} : {invite}')
    counter = counter + 1

print(f'\nUsers count : {len(all_users)}')
print(f'Credits Used : 0[{cr0}] | 1[{cr1}] | 2[{cr2}] | 3[{cr3}] | 4[{cr4}] | 5[{cr5}] | +5[{cr6}]')
print(f'All images generated {len(all_outputs)}')
