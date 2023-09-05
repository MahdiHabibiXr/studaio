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
menout = 0
womenout = 0

o1 = 0
o2 = 0
o3 = 0
o4 = 0
o5 = 0
o6 = 0

for pic in all_outputs:
    stl = pic.split(':')[1]
    if( stl == '1') : o1 = o1 + 1
    elif( stl == '2') : o2 = o2 + 1
    elif( stl == '3') : o3 = o3 + 1
    elif( stl == '4') : o4 = o4 + 1
    elif( stl == '5') : o5 = o5 + 1
    elif( stl == '6') : o6 = o6 + 1

    gen = pic.split(':')[3]
    if(gen == 'man') : menout = menout + 1
    elif(gen == 'woman') : womenout = womenout + 1


print('All users data : \n')
print(f'counter : user : @username : name : active : credit : invite : gender')
for user in all_users:
    username = q.hget(user, 'username')

    name = q.hget(user, 'name')
    gender = q.hget(user, 'gender')
    if(gender == 'man') : men = men + 1
    elif(gender == 'woman') : women = women + 1

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
print(f'Credits by % : 0[{round(cr0/uc*100)}%] | 1[{round(cr1/uc*100)}%] | 2[{round(cr2/uc*100)}%] | 3[{round(cr3/uc*100)}%] | 4[{round(cr4/uc*100)}%] | 5[{round(cr5/uc*100)}%] | 6[{round(cr6/uc*100)}%] | 7[{round(cr7/uc*100)}%] | 8[{round(cr8/uc*100)}%] | 9[{round(cr9/uc*100)}%] |  10[{round(cr10/uc*100)}%] |  +10[{round(cr11/uc*100)}]')

print(f'Invites Done : 0[{inv0}] | 1[{inv1}] | 2[{inv2}] | 3[{inv3}] | 4[{inv4}] | 5[{inv5}] | +5[{inv6}]')
print(f'Invites by % : 0[{round(inv0/uc*100)}%] | 1[{round(inv1/uc*100)}%] | 2[{round(inv2/uc*100)}%] | 3[{round(inv3/uc*100)}%] | 4[{round(inv4/uc*100)}%] | 5[{round(inv5/uc*100)}%] | +5[{round(inv6/uc*100)}]')

print(f'Users by gender : man{men} [{round(men/uc*100)}%] |  woman{women} [{round(women/uc*100)}%]')

ic = len(all_outputs)
print(f'All images generated {ic}')
print(f'OutImages Styles : 1[{o1}] | 2[{o2}] | 3[{o3}] | 4[{o4}] | 5[{o5}] | 6[{o6}]')
print(f'OutImages by % : 1[{round(o1/ic*100)}%] | 2[{round(o2/ic*100)}%] | 3[{round(o3/ic*100)}%] | 4[{round(o4/ic*100)}%] | 5[{round(o5/ic*100)}%] | 6[{round(o6/ic*100)}]')
