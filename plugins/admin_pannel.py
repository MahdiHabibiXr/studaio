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
    staudaio_users = query.lrange('studaio_users',0,-1)
    count = len(users)
    actives = 0
    for user in users:
        try :
            if(query.hget(user,"active") == 'True'):
                actives = actives + 1
        except :
            pass
    await message.reply(f'all stduaio users table {len(staudaio_users)}')
    await message.reply('all records count : ' + str(count) + '\nall active users : ' + str(actives))

@Client.on_message(filters.private & filters.user(admin) & filters.command('off_run'))
async def off_run(client, message):
    query.set('autopilot','False')
    await message.reply('AutoPilot Off')

@Client.on_message(filters.private & filters.user(admin) & filters.command('on_run'))
async def on_run(client, message):
    query.set('autopilot','True')
    await message.reply('AutoPilot On')

@Client.on_message(filters.private & filters.user(admin) & filters.regex('/addcredit_'))
async def add_credit(client, message):
    user = message.text.split('_')[1]
    amount = message.text.split('_')[2]

    query.hset(user, 'credit', int(amount))
    await message.reply(f'added {amount} to {user}')

@Client.on_message(filters.private & filters.user(admin) & filters.regex('/batchsize_'))
async def changeBatchSize(client, message):
    amount = message.text.split('_')[1]
    query.set('batch', int(amount))
    await message.reply(f'batch size now {amount}')

@Client.on_message(filters.private & filters.user(admin) & filters.command('invcodes_report'))
async def invitescodeReport(client, message):
    invcodes = query.hgetall('inv_codes')
    msg = ''
    for code in invcodes:
        addition = f'{code} : {invcodes[code]}\n'
        msg = msg + addition
    await message.reply(msg)

@Client.on_message(filters.private & filters.user(admin) & filters.regex('/get_images'))
async def getOutputs(client,message):
    images = query.lrange('outputs', 0 , -1)
    count = len(images)


    await message.reply()