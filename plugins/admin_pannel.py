from pyrogram import Client, filters
# from pyrogram.enums.chat_action
from plugins import query, admin


@Client.on_message(filters.private & filters.user(admin) & filters.regex('activate_'))
async def activate_user(client, message):
    user_to_activeate = message.text.split('_')[1]

    query.hset(user_to_activeate, 'active' , 'True' )

    await message.reply(user_to_activeate)

@Client.on_message(filters.private & filters.user(admin) & filters.command('help'))
async def help_message(client, message):
    chat_id = message.chat.id
    help_message = '''⚡️ **اپشن های موجود** ⚡️ 
       \n☔️ اضافه کردن پیام به ربات با کامند     /add_msg
        \n☔️ حذف کردن پیام از ربات با کامند       /del_msg
        \n☔️ نمایش جملات موجود با کامند       /show_msg
         \n☔️ نمایش وضعیت ربات     /info
         \n☔️ چک کردن وضعیت ربات با کامند      /status
         \n☔️ فوروارد کردن پیام       /forward
         \n☔️ جوین شدن داخل گروه مورد نظر     /join_chat
         \n☔️ ست کردن پیام بعد از جوین شدن ربات در گروه       /join_msg
         \n.
    '''
    await message.reply(text=help_message)

@Client.on_message(filters.private & filters.user(admin) & filters.command('add_msg'))
async def add_msg(client, message):
    chat_id = message.chat.id
    messages = '''⚡️ **اضافه کردن پیام** ⚡️
        \nلطفا جمله یا جملات خود را ارسال کنید و در انتها کامند زیر را ارسال کنید:
        \n/save
    '''
    await message.reply(text=messages)

    query.setbit('add:msg', 0, 1)


@Client.on_message(filters.private & filters.user(admin), group=1)
async def get_input(client, message):
    msg = message.text

    if query.getbit('add:msg', 0) == 1 and msg and not msg.startswith('/'):
        msg_counter = query.incr('New:Msg')
        query.sadd('Messages', f'{msg_counter}:{msg}')

    elif msg == '/save':
        chat_id = message.chat.id
        await message.reply(text='''⚡️ **اضافه کردن پیام** ⚡️
            \n✅ جمله های شما با موفقیت ذخیره شد
            \n.''')

        query.setbit('add:msg', 0, 0)

@Client.on_message(filters.private & filters.user(admin) & filters.command('show_msg'))
async def show_msg(client, message):
    chat_id = message.chat.id

    if query.exists('Messages'):
        messages = '⚡️ **نمایش جمله ها** ⚡️\n'
        data = sorted(query.smembers('Messages'), key=lambda x: x.split(':')[0])
        for item in data:
            item = item.split(':', 1)
            separator = '➖' * 12
            messages += f'`{item[0]}`:{item[1]}\n{separator}\n'
        await message.reply(text=messages)
    else:
        await message.reply(text='❌جمله ای یافت نشد❌')

# @Client.on_message(filters.private & filters.user(admin) & filters.command("del_msg"))
# async def del_msg(c, m):
#     chat_id = m.chat.id 

#     await c.send_chat_action(chat_id=chat_id, action="typing")

#     if r.exists("Messages"):

#         message = """⚡️ **حذف کردن جمه ها** ⚡️            
#             \nلطفا شماره جمله مورد نظر خود ارسال کنید. 🗑            
#             \nو یا برای حذف همه جمله ها  `*` را ارسال نمایید
#             \n.
#         """

#         await c.send_message(chat_id=chat_id, text=message)

#         r.setbit("del:msg", 0, 1)

#     else:
#         await c.send_message(chat_id=chat_id, text="❌جمله ای یافت نشد❌")

