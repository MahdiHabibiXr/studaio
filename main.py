from sdapi import generate_image
from PIL import Image
from pyrogram import Client, filters
from plugins import query, admin, name
from plugins.tasks import task1,task2
from pyromod.helpers import ikb, kb, array_chunk
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from celery import Celery
plugins = dict(
    root = "plugins"
)

bot = Client('mahdi',api_id=863373,api_hash='c9f8495ddd20615835d3fd073233a3f6',plugins=plugins )
# bot = Client(
#     'mahdi',
#     plugins=plugins
#     )


#/START
@bot.on_message(filters.command('start') & filters.private)
async def test(client, message):
    chat_id = message.chat.id

    #Add new user to db
    if(not query.exists(chat_id)):
        #check if user does not exists
        data = {
            'name' : message.from_user.first_name,
            'username' : message.from_user.username,
            'active' : 'False',
        }
        #query to db [key: chat_id , data{name,username,active}]
        query.hset(chat_id, mapping = data)
        msg = f'''سلام **{query.hget(chat_id,'name')}**، خوش اومدی👋
این ربات یه نسخه دمو از **{name}** هست که بهت کمک می‌کنه که بی‌نهایت عکس از خودت بسازی
👈نحوه کار این ربات اینجوریه که اول یه عکس از خودت میفرستی و بعد با دستوراتی که وجود داره، به کمک هوش مصنوعی عکس‌هایی با صورت خودت ساخته میشه

از اونجایی که منابع ما برای این دمو محدوده، حتما باید کد دعوت داشته باشی
میتونی با دستور `/singup_invcode` و جایگذاری کد دعوتت با به قابلیت های این ربات دسترسی پیدا کنی

✅مثلا : `/signup_248569`
        '''
        await message.reply(msg)

    #old user    
    else:
        #check if user is Activated
        if(query.hget(chat_id, 'active') == 'True'):
            msg = f'''سلام **@{query.hget(chat_id, "username")}** 👋
خوش برگشتی به ربات. شما به قابلیت‌های ربات دسترسی داری😇

برای ساخت عکس جدید از خودت، دستور /new_image رو کلیک کن '''
            
            await message.reply(msg)

        else :
            #not active user
            msg = f'''سلام **{query.hget(chat_id,'name')}**، خوش برگشتی 👋

این ربات یه نسخه دمو از **{name}** هست که بهت کمک می‌کنه که بی‌نهایت عکس از خودت بسازی
👈نحوه کار این ربات اینجوریه که اول یه عکس از خودت میفرستی و بعد با دستوراتی که وجود داره، به کمک هوش مصنوعی عکس‌هایی با صورت خودت ساخته میشه

از اونجایی که منابع ما برای این دمو محدوده، حتما باید کد دعوت داشته باشی
میتونی با دستور `/singup_invcode` و جایگذاری کد دعوتت با به قابلیت های این ربات دسترسی پیدا کنی

✅مثلا : `/signup_248569`
            '''
            await message.reply(msg)


@bot.on_message(filters.private & filters.regex('/signup_'))
async def signUp(client, message):
    input_code = message.text.split('_')[1]
    chat_id = message.chat.id

    #check if invite is valid
    
    if(query.hget('inv_codes', input_code) == 'True'):
        #inv_code is true
        if(query.hget(chat_id, 'active') == 'False'):
            #just if not activated before
            query.hset(chat_id, 'active', 'True')
            query.hset(chat_id, 'credit', 5)
            query.hset('inv_codes', input_code, 'False')

        msg = 'قابلیت های ربات با موفقیت برای شما فعال شد😍 \nبرای شروع تولید عکس با صورت خودت، روی این دستور کلیک کن : /new_image '
    else:
        #inv_code is false
        if(query.hget(chat_id, 'active') == 'False'):
            msg = '😔متاسفانه این کد دعوت معتبر نیست'
        else:
            msg = '😁قابلیت های ربات برای شما فعاله دیگه، با دستور /new_image میتونی عکس جدید بسازی'

    await message.reply(msg)

@bot.on_message(filters.private & filters.command('new_image'))
async def newImage(client, message):
    chat_id = message.chat.id

    #is user submitted he/she's own photo?
    if(query.hget(chat_id, 'photo') != None):
        #submitted photo before
        msg = '''
☺️خب حالا وقت ساختنه
برای ساختن عکست، لازمه که یه دستور (prompt) به ربات بدی تا هوش مصنوعی‌ما، بتونه با صورتت اون عکس رو بسازه.

🔻برای ارسال دستورت به ربات، از /imagine استفاده کن و با یک فاصله، توضیحاتت رو بنویس.

📝برای نوشتن یه prompt مناسب می‌تونی از این قالب استفاده کنی :
/imagine a [man/woman] wearing a [cloth] at [place] ...
✅Example : /imagine a man wearing a black suit at business pitch desk meeting

📌چند تا نکته برای نوشتن یه prompt خوب :
1. سعی کن تا جایی که میتونی به ربات توضیح بدی که دوست داری چه عکسی ازت بسازه، از تعیین جنسیت تا نوع لباسی که قراره تنت باشه و جایی که میخوای باشی، حتی مدل مو و سن و سال و ...
2. حتما دستوری که میفرستی باید به زبان انگلیسی باشه
3. اگه یک سبک خاصی عکاسی مد نظرته، میتونی میتونی در قالب a ... photo of a به اول دستورت اضافه کنی، مثلا : a candid photo of a woman

👈برای ایده گرفتن و دیدن استایل‌های مختلفی که میتونی دستورشون رو به ربات بدی، به این کانال مراجعه کن : @studAIo_prompts
''' 
        await message.reply(msg)

    else:
        #have not submitted 
        msg = '''🔻برای شروع یک عکس از خودتون ارسال کنید.

نکاتی که باید در نظر  بگیرید :
1️⃣ عکسی که ارسال می‌کنید، لازمه که حتما شامل صورتتون باشه، این عکس برای ایجاد عکسهای جدید بعنوان رفرنس از طرف هوش مصنوعی استفاده میشه
2️⃣ ترجیحا صورتتون توی عکس با یک نور مناسب باشه و از زاویه رو به رو باشه به طوری که همه بخش های صورتتون مشخص باشه
3️⃣ بهتره که توی عکس حالت صورتتون عادی باشه و خیلی شامل احساسات نباشه و اگه عینک دارید، عینکتون رو برداشته باشید
'''
        await message.reply(msg)

@bot.on_message(filters.private & filters.photo)
async def savePhoto(client, message):
    chat_id = message.chat.id
    #Is it active user?
    if(query.hget(chat_id, 'active') == 'True'):
        if(query.hget(chat_id, 'photo') != None) :
            file = await client.download_media(message.photo.file_id, file_name = f'input_images/{chat_id}/')
            query.hset(chat_id, 'photo', file)
            await client.send_photo(chat_id, file, caption='✅عکس ورودیت با موفقیت ثبت شد')

        # msg = '😌حالا وقتشه که عکستو بسازی، لطفا از بین استایلهایی که برات ارسال میشه، یکی رو انتخاب کن و با کلیک کردن روی دستور هر عکس، به ربات بگو که میخوای عکست تو چه سبکی ساخته بشه :'
        # await message.reply(msg)

        msg = '''
☺️خب حالا وقت ساختنه
برای ساختن عکست، لازمه که یه دستور (prompt) به ربات بدی تا هوش مصنوعی‌ما، بتونه با صورتت اون عکس رو بسازه.

🔻برای ارسال دستورت به ربات، از /imagine استفاده کن و با یک فاصله، توضیحاتت رو بنویس.

📝برای نوشتن یه prompt مناسب می‌تونی از این قالب استفاده کنی :
/imagine a [man/woman] wearing a [cloth] at [place] ...
✅Example : /imagine a man wearing a black suit at business pitch desk meeting

📌چند تا نکته برای نوشتن یه prompt خوب :
1. سعی کن تا جایی که میتونی به ربات توضیح بدی که دوست داری چه عکسی ازت بسازه، از تعیین جنسیت تا نوع لباسی که قراره تنت باشه و جایی که میخوای باشی، حتی مدل مو و سن و سال و ...
2. حتما دستوری که میفرستی باید به زبان انگلیسی باشه
3. اگه یک سبک خاصی عکاسی مد نظرته، میتونی میتونی در قالب a ... photo of a به اول دستورت اضافه کنی، مثلا : a candid photo of a woman

👈برای ایده گرفتن و دیدن استایل‌های مختلفی که میتونی دستورشون رو به ربات بدی، به این کانال مراجعه کن : @studAIo_prompts
''' 
        await message.reply(msg)


@bot.on_message(filters.private & filters.command('imagine'))
async def imagine(client, message):
    chat_id = message.chat.id
    prompt = message.text.replace('/imagine', '')

    #check if input is valid
    if(len(prompt) < 5):
        await message.reply('دستور ورودی شما کوتاه تر از حد مجاز است! لطفا دوباره تلاش کنید')

    else:
        #it is at least 5 chrs
        if('man'in prompt or 'woman' in prompt):
            #OKKKK
            file = query.hget(chat_id, 'photo')
            # input = 'images/ahmad.jpg'
            prmpt = f'RAW photo,{prompt}, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3'
            await message.reply('عکس شما در حال پردازش است، لطف منتظر باشید ...')
            try:
                r = generate_image(
                    prmpt,
                    image_input = file,
                    output_folder= 'outputdata/',
                    batch_size= 4,
                    enable_roop= True,
                    enable_upscale= False,
                    step=25
                    )

                for i in r :
                    await client.send_photo(chat_id, i)
            except:
                await client.send_message(admin, 'error in connection')
            
        else:
            #should use man or woman in this
            await message.reply('دستور شما باید حاوی جنسیت باشد')


@bot.on_message(filters.private & filters.command('task'))
async def add_task(client, message):
    id = message.chat.id
    task1.delay('791927771')
    await message.reply('task 1 started')
    task2.delay('791927771')
    await message.reply('task 2 started')



bot.run()

# @bot.on_message(filters.private & filters.photo)
# async def savePhoto(client, message):
#     chat_id = message.chat.id
#     #Is it active user?
#     if(query.hget(chat_id, 'active') == 'True'):
#         file = await client.download_media(message.photo.file_id, file_name = f'input_images/{chat_id}/')
#         query.hset(chat_id, 'photo', file)
#         await client.send_photo(chat_id, file, caption='✅عکس ورودیت با موفقیت ثبت شد')
        
#         msg = '''
# 🔻لطفا جنسیتت رو مشخص کن :
# '''
#         keyboard = ikb([
#             [
#                 ('مرد', 'gender_male'),
#                 ('زن', 'gender_female')
#             ]
#         ])
#         await client.send_message(chat_id, msg, reply_markup = keyboard)

# @bot.on_callback_query()
# async def get_callback(client, callback_query):
#     chat_id = callback_query.message.chat.id
#     query_data = callback_query.data

#     if('gender_' in query_data):
#         gender = query_data.split('_')[1]
#         query.hset(f'img:{chat_id}' , 'gender' , gender)

#         msg = 'رده سنی ات رو مشخص کن :'
#         keyboard = ikb([
#             [
#                 ('زیر 20', 'age_1'),
#                 ('20 تا 40', 'age_2'),
#                 ('بالای 60', 'age_3')
#             ]
#         ])

#         await client.send_message(chat_id, reply_markup = keyboard)

#     elif('age_' in query_data):
#         age_input = query_data.split('_')
#         if(age_input == '1') : age = 15
#         elif(age_input == '2') : age = 25
#         elif(age_input == '3') : age = 65

#         query.hset(f'img:{chat_id}' , 'age' , age)

#         msg = 'مدل مویی که میخوای توی عکس داشته باشی رو انتخاب کن:'
#         keyboard = ikb([
#             [
#                 ('بلند', 'hair_long'),
#                 ('کوتاه', 'hair_short'),
#                 ('کچل', 'hair_bald'),
#                 ('فرفری', 'hair_curly')
#             ]
#         ])

#         await client.send_message(chat_id, reply_markup = keyboard)












