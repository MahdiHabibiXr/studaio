from pyrogram import Client, filters
from plugins import query, admin, api_url

@Client.on_message(filters.private & filters.user(admin) & filters.regex('/sendmsgtoall_'))
async def sendMessageToAll(client, message):
    target = message.text.split('_')[1]
    msg = message.text.split('_')[2]

    if(target == 'all'):
        users = query.lrange('studaio_users', 0, -1)
        for user in users:

            try:
                name = query.hget(user, 'name') 
                await client.send_message(user, f'کاربر عزیز {name} \n'+ msg)
                print(f'sent message to {user} : {name}')

            except Exception as error :
                    print('[ERROR] : ' + error)

    else:
        try :
            name = query.hget(target, 'name')
            await client.send_message(target, f'کاربر عزیز {name} \n' + msg)
            print(f'sent message to {target} : {name}')
        except Exception as error :
            print('[ERROR] : ' + error)
