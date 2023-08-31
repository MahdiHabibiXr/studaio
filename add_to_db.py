from plugins import query as q
import os

with open('backup.txt', 'r', encoding="utf8") as f:
    users = f.readlines()
with open('outputs.txt', 'r', encoding="utf8") as f:
    outputs = f.readlines()
# users = open('backup.txt', 'r')
print('=========================================================')
errors = []
# keys = q.keys('*')
# q.delete(*keys)
print(type(users))
users.reverse()
outputs.reverse()
for u in users:
    try : 

        u = u.split('|')
        id = u[0]
        q.lpush('studaio_users', id)
        name = u[1].split(':')[1]
        if(name != 'None') : q.hset(id, 'name', name)
        username = u[2].split(':')[1]
        if(username != 'None') : q.hset(id, 'username', username)
        credit = u[3].split(':')[1]
        if(credit != 'None') : q.hset(id, 'credit', credit)
        invite = u[4].split(':')[1]
        if(invite != 'None') : q.hset(id, 'name', name)
        gender = u[5].split(':')[1]
        if(gender != 'None') : q.hset(id, 'gender', gender)
        photo = u[6].split(':')[1]
        if(photo != 'None') : q.hset(id, 'photo', photo)
        q.hset(id, 'progress', 'False')
        q.hset(id, 'active', 'True')

        print(f'id:{id} gender:{gender} credit:{credit} name:{name} username:{username} invite:{invite} photo:{photo}')
    except Exception as error:
        print('-------------------')
        print(f'====>error on {u} => {error}')
        print('--------------------')
        errors.append(id)

for o in outputs:
    q.lpush('outputs', o.replace('\n',''))