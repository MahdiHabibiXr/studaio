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
cr7 = 0
cr8 = 0
cr9 = 0
cr10 = 0
cr11 = 0

inv0 = 0
inv1 = 0
inv2 = 0
inv3 = 0
inv4 = 0
inv5 = 0
inv6 = 0

men = 0
women = 0

print('All users data : \n')
print(f'counter : user : @username : name : active : credit : invite : gender')
for user in all_users:
    username = q.hget(user, 'username')

    name = q.hget(user, 'name')
    gender = int(q.hget(user, 'gender'))
    if(gender == 'man') : men = men + 1
    elif(gender == 'woman') : wpmen = women + 1

    if(q.hget(user, 'active') == 'False' or q.hget(user, 'active') == None):
        q.hset(user, 'active', 'True')
    active = q.hget(user, 'active')

    if(q.hget(user, 'credit') == None):
        q.hset(user, 'credit', 0)
    credit = int(q.hget(user, 'credit'))

    if(credit == 0) : cr0 = cr0 + 1
    elif(credit == 1) : cr1 = cr1 + 1
    elif(credit == 2) : cr2 = cr2 + 1
    elif(credit == 3) : cr3 = cr3 + 1
    elif(credit == 4) : cr4 = cr4 + 1
    elif(credit == 5) : cr5 = cr5 + 1
    elif(credit == 6) : cr6 = cr6 + 1
    elif(credit == 7) : cr7 = cr7 + 1
    elif(credit == 8) : cr8 = cr8 + 1
    elif(credit == 9) : cr9 = cr9 + 1
    elif(credit == 10) : cr10 = cr10 + 1
    elif(credit > 10) : cr11 = cr11 + 1

    if(q.hget(user,'invite') == None):
        q.hset(user, 'invite', 0)
    invite = int(q.hget(user, 'invite'))

    if(invite == 0) : inv0 = inv0 + 1
    elif(invite == 1) : inv1 = inv1 + 1
    elif(invite == 2) : inv2 = inv2 + 1
    elif(invite == 3) : inv3 = inv3 + 1
    elif(invite == 4) : inv4 = inv4 + 1
    elif(invite == 5) : inv5 = inv5 + 1
    elif(invite > 5) : inv6 = inv6 + 1



    print(f'{counter} : {user} : @{username} : {name} : {active} : {credit} : {invite} : {gender}')
    counter = counter + 1

uc = len(all_users)
print(f'\nUsers count : {uc}')
print(f'Credits Used : 0[{cr0}] | 1[{cr1}] | 2[{cr2}] | 3[{cr3}] | 4[{cr4}] | 5[{cr5}] | 6[{cr6}] | 7[{cr7}] | 8[{cr8}] | 9[{cr9}] |  10[{cr10}] |  +10[{cr11}]')
print(f'Credits by % : 0[{cr0/uc*100}] | 1[{cr1/uc*100}] | 2[{cr2/uc*100}] | 3[{cr3/uc*100}] | 4[{cr4/uc*100}] | 5[{cr5/uc*100}] | 6[{cr6/uc*100}] | 7[{cr7/uc*100}] | 8[{cr8/uc*100}] | 9[{cr9/uc*100}] |  10[{cr10/uc*100}] |  +10[{cr11/uc*100}]')

print(f'Invites Done : 0[{inv0}] | 1[{inv1}] | 2[{inv2}] | 3[{inv3}] | 4[{inv4}] | 5[{inv5}] | +5[{inv6}]')
print(f'Invites by % : 0[{inv0/uc*100}] | 1[{inv1/uc*100}] | 2[{inv2/uc*100}] | 3[{inv3/uc*100}] | 4[{inv4/uc*100}] | 5[{inv5/uc*100}] | +5[{inv6/uc*100}]')

print(f'All images generated {len(all_outputs)}')
