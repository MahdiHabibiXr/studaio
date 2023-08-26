from pyrogram import Client, filters
# from pyrogram.enums.chat_action
from plugins import query, admin, api_url


@Client.on_message(filters.private & filters.user(admin) & filters.regex('activate_'))
async def activate_user(client, message):
    user_to_activeate = message.text.split('_')[1]

    query.hset(user_to_activeate, 'active' , 'True' )

    await message.reply(user_to_activeate)

@Client.on_message(filters.private & filters.user(admin) & filters.command('add_code'))
async def add_code(client, message):
    codes = message.text.split(' ')[1]

    for code in codes.split(','):
        query.hset('inv_codes', code, 'True')
        await message.reply(code + ' added to database')

@Client.on_message(filters.private & filters.user(admin) & filters.command('set_url'))
async def set_url(client, message):
    url_msg = message.text.split(' ')[1]
    query.set('url', url_msg)
    await message.reply('API url changed to : ' + url_msg)

@Client.on_message(filters.private & filters.user(admin) & filters.command('users'))
async def set_active(client, message):
    users = query.keys()
    count = len(users)
    actives = 0
    for user in users:
        try :
            if(query.hget(user,"active") == 'True'):
                actives = actives + 1
        except :
            pass
    await message.reply('all users count : ' + str(count) + '\nall active users : ' + str(actives))

@Client.on_message(filters.private & filters.user(admin) & filters.command('off_run'))
async def off_run(client, message):
    query.set('autopilot','False')
    message.reply('AutoPilot Off')

@Client.on_message(filters.private & filters.user(admin) & filters.command('on_run'))
async def on_run(client, message):
    query.set('autopilot','True')
    message.reply('AutoPilot On')

