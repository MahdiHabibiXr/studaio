from sdapi import generate_image
from PIL import Image
from pyrogram import Client, filters
from plugins import query, admin, name, botname, bannerfid
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
@bot.on_message(filters.command('test') & filters.private)
async def test_bot(client, message):
    await message.reply('im upppp')

@bot.on_message((filters.regex('/start') | filters.regex('/Start') ) & filters.private)
async def start_bot(client, message):
    chat_id = message.chat.id

    #Add new user to db
    if(query.hgetall(chat_id) == {}):
        query.lpush('studaio_users', chat_id)
        query.hset(chat_id,'name', message.from_user.first_name)
        query.hset(chat_id,'username',message.from_user.username)
        query.hset(chat_id,'active', 'True')
        query.hset(chat_id,'progress', 'False')
        query.hset(chat_id,'invite', 0)
        query.hset(chat_id,'credit', 5)


        #TODO : referal things here
        if(message.text != '/start' and message.text != '/Start'):
            ref = message.text.split(' ')[1]
            query.hset(chat_id,'ref',ref)

            ref_invs = query.hget(ref,'invite')
            query.hset(ref, 'invite', (int(ref_invs) + 1))

            ref_cr = query.hget(ref, 'credit')
            query.hset(ref, 'credit', (int(ref_cr) + 1))
            await client.send_message(ref, '😎👌یک کاربر جدید با لینک شما وارد ربات شد و به اعتبار حسابتون اضافه شد')

        msg = f'''سلام **{query.hget(chat_id,'name')}**، خوش اومدی👋
این ربات یه نسخه دمو از **{name}** هست که بهت کمک می‌کنه که بی‌نهایت عکس از خودت بسازی
👈نحوه کار این ربات اینجوریه که اول یه عکس از خودت میفرستی و بعد با دستوراتی که وجود داره، به کمک هوش مصنوعی عکس‌هایی با صورت خودت ساخته میشه

اعتبار هدیه 5 تایی ساخت عکس رایگان برای حساب شما اعمال شد🫶

برای شروع روی /set_image کلیک کن
        '''
        await message.reply(msg)

    #old user    
    else:
        #check if user is Activated
        if(query.hget(chat_id, 'active') == 'True'):
            msg = f'''سلام **@{query.hget(chat_id, "username")}** 👋
خوش برگشتی به ربات. برای ادامه از لیست زیر یه دستور رو کلیک کن😇

🔸 تنظیم عکس ورودی جدید : /set_image
🔸 ساخت عکس جدید از خودت : /imagine_help
🔸دعوت از دوستان و افزایش اعتبار : /invite
🔸بررسی اعتبار شما : /credit
'''
            
            await message.reply(msg)

        else :
            #not active user
            msg = f'''سلام **{query.hget(chat_id,'name')}**، خوش برگشتی 👋

این ربات یه نسخه دمو از **{name}** هست که بهت کمک می‌کنه که بی‌نهایت عکس از خودت بسازی
👈نحوه کار این ربات اینجوریه که اول یه عکس از خودت میفرستی و بعد با دستوراتی که وجود داره، به کمک هوش مصنوعی عکس‌هایی با صورت خودت ساخته میشه

‼️ متاسفانه ربات برای شما فعال نیست! 
برای اطلاعات بیشتر با ادمین در ارتباط باشید : @habibidev
            '''
            await message.reply(msg)

@bot.on_message(filters.private & filters.command('menu'))
async def mainMenu(client, message):
    msg = f'''
برای ادامه از لیست زیر یه دستور رو کلیک کن😇

🔸 تنظیم عکس ورودی جدید : /set_image
🔸 ساخت عکس جدید از خودت : /imagine_help
🔸دعوت از دوستان و افزایش اعتبار : /invite
🔸بررسی اعتبار شما : /credit
'''
    await message.reply(msg)

@bot.on_message(filters.private & filters.command('invite'))
async def createInviteLink(client, message):
    chat_id = message.chat.id
    link = f'https://t.me/{botname}?start={chat_id}'

    if(query.hget(chat_id,'invite') == None):
        query.hset(chat_id, 'invite', 0)

    msg = f'''
😎این ربات هوش مصنوعی ازت عکاسی میکنه!
کافیه رباتو استارت کنی و یه عکس معمولی از خودتو براش بفرستی، بعدش با استایل‌های مختلفی که داره، عکسهای حرفه‌ای که انگار با دوربین عکاسی گرفتنو تحویل بگیری. بزن رو لینک و از قابلیتهاش استفاده کن 👇👇

🔥{link}
'''

    await client.send_photo(chat_id, bannerfid, caption = msg)
    mg = '''
👆با ارسال بنر اختصاصیت به دوستات، میتونی اعتبار تولید عکس جدید بگیری.
با هر  نفری که از طریق بنر تو وارد این برنامه بشن، به اعتبارت اضافه میشه و میتونی عکسهای بیشتری بسازی🔥

اگه میخوای بدونی تا حالا چند نفر رو با موفقیت دعوت کردی، /credit رو کلیک کن
↩️برگشت به منوی اصلی : /menu
'''
    await message.reply(mg)


@bot.on_message(filters.private & filters.command('credit'))
async def creditsReport(client, message):
    chat_id = message.chat.id
    cr = query.hget(chat_id, 'credit')
    inv = query.hget(chat_id, 'invite')

    msg = f'''
کاربر @{query.hget(chat_id,'username')} عزیز

👤 تعداد افرادی که به ربات دعوت کردی : {inv}
💰اعتبار حسابت (چند بار دیگه میتونی عکس جدید بسازی) : {cr}

🔗 دریافت لینک اختصاصی دعوت از دوستان : /invite
↩️برگشت به منوی اصلی : /menu
'''
    await message.reply(msg)

#no need to be here anymore!
@bot.on_message(filters.private & filters.regex('/activate'))
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

        msg = 'قابلیت های ربات با موفقیت برای شما فعال شد😍 \nبرای شروع تولید عکس با صورت خودت، روی این دستور کلیک کن : /set_image '
    else:
        #inv_code is false
        if(query.hget(chat_id, 'active') == 'False'):
            msg = '😔متاسفانه این کد دعوت معتبر نیست'
        else:
            msg = '😁قابلیت های ربات برای شما فعاله دیگه، با دستور /set_image میتونی عکس جدید بسازی'

    await message.reply(msg)

@bot.on_message(filters.private & filters.command('imagine_help'))
async def helpImagine(client, message):
    msg = '''
🔰راهنمای ساخت عکس جدید :


برای ساختن عکس جدید از خودت، فقط کافیه که از بین استلاهایی که توی این چنل هست(@studaio_styles) یکی رو انتخاب کنی 

📌بعدش به کمک دستور /imagine_styleNumber استایل مورد نظرت رو به ربات بگی و درخواستت رو ثبت کنی، مثلا 
/imagine_1 

✅بعد از اینکه دستورت رو ثبت کردی، درخواستت توی صف قرار میگیره و بعد از اینکه عکسات ساخته بشه، همینجا برات ارسال میشه
'''
    await message.reply(msg)


@bot.on_message(filters.private & filters.command('set_image'))
async def newImage(client, message):
    chat_id = message.chat.id

    #check if user is active!!!!
    if(query.hget(chat_id, 'active') == 'True'):
        #is user submitted he/she's own photo?
        if(query.hget(chat_id, 'photo') != None):
            #submitted photo before
#             msg = '''
# ☺️خب حالا وقت ساختنه
# برای ساختن عکست، لازمه که یه دستور (prompt) به ربات بدی تا هوش مصنوعی‌ما، بتونه با صورتت اون عکس رو بسازه.

# 🔻برای ارسال دستورت به ربات، از /imagine استفاده کن و با یک فاصله، توضیحاتت رو بنویس.

# 📝برای نوشتن یه prompt مناسب می‌تونی از این قالب استفاده کنی :
# /imagine a [man/woman] wearing a [cloth] at [place] ...
# ✅Example : /imagine a man wearing a black suit at business pitch desk meeting

# 📌چند تا نکته برای نوشتن یه prompt خوب :
# 1. سعی کن تا جایی که میتونی به ربات توضیح بدی که دوست داری چه عکسی ازت بسازه، از تعیین جنسیت تا نوع لباسی که قراره تنت باشه و جایی که میخوای باشی، حتی مدل مو و سن و سال و ...
# 2. حتما دستوری که میفرستی باید به زبان انگلیسی باشه
# 3. اگه یک سبک خاصی عکاسی مد نظرته، میتونی میتونی در قالب a ... photo of a به اول دستورت اضافه کنی، مثلا : a candid photo of a woman

# 👈برای ایده گرفتن و دیدن استایل‌های مختلفی که میتونی دستورشون رو به ربات بدی، به این کانال مراجعه کن : @studAIo_prompts
# ''' 
#             await message.reply(msg) 
            await client.send_photo(chat_id,query.hget(chat_id,'photo'),'شما قبلا این عکس رو بعنوان ورودی ثبت کردی، اگه میخوای عکستو تغییر بدی، عکس جدیدت رو بفرست\n🔻منوی اصلی : /menu')

#             msg = '''
# برای ساختن عکس جدید از خودت، فقط کافیه که از بین استلاهایی که توی این چنل هست(@studaio_styles) یکی رو انتخاب کنی 

# 📌بعدش فقط کافیه به کمک دستور /imagine_styleNumber استایل مورد نظرت رو به ربات بگی و درخواستت رو ثبت کنی، مثلا 
# /imagine_1 

# ✅بعد از اینکه دستورت رو ثبت کردی، درخواستت توی صف قرار میگیره و بعد از اینکه عکسات ساخته بشه، همینجا برات ارسال میشه
# '''
#             await message.reply(msg)

        else:
            #have not submitted 
            msg = '''🔻برای شروع یک عکس از خودتون ارسال کنید.

    نکاتی که باید در نظر  بگیرید :
    1️⃣ عکسی که ارسال می‌کنید، لازمه که حتما شامل صورتتون باشه، این عکس برای ایجاد عکسهای جدید بعنوان رفرنس از طرف هوش مصنوعی استفاده میشه
    2️⃣ ترجیحا صورتتون توی عکس با یک نور مناسب باشه و از زاویه رو به رو باشه به طوری که همه بخش های صورتتون مشخص باشه
    3️⃣ بهتره که توی عکس حالت صورتتون عادی باشه و خیلی شامل احساسات نباشه و اگه عینک دارید، عینکتون رو برداشته باشید
    '''
            await message.reply(msg)

    else:
        #user in not active yet!!
        msg = f'''سلام **{query.hget(chat_id,'name')}**، خوش برگشتی 👋

این ربات یه نسخه دمو از **{name}** هست که بهت کمک می‌کنه که بی‌نهایت عکس از خودت بسازی
👈نحوه کار این ربات اینجوریه که اول یه عکس از خودت میفرستی و بعد با دستوراتی که وجود داره، به کمک هوش مصنوعی عکس‌هایی با صورت خودت ساخته میشه

قابلیت های ربات برای شما فعال نیست! لطفا با ادمین در ارتباط باشید : @habibidev
            '''
        await message.reply(msg)


@bot.on_message(filters.private & filters.photo)
async def savePhoto(client, message):
    chat_id = message.chat.id

    if(message.from_user.is_bot == False) : 

        # if(message.from_user._ == 'User') : print('yes userrrr')
        #Is it active user?
        if(query.hget(chat_id, 'active') == 'True'):
            if(query.hget(chat_id, 'photo') == None) :
                file = await client.download_media(message.photo.file_id, file_name = f'input_images/{chat_id}/')
                query.hset(chat_id, 'photo', file)
                await client.send_photo(chat_id, query.hget(chat_id,'photo'), caption='✅عکس ورودیت با موفقیت ثبت شد')
            else:
                file = await client.download_media(message.photo.file_id, file_name = f'input_images/{chat_id}/')
                query.hset(chat_id, 'photo', file)
                await client.send_photo(chat_id, query.hget(chat_id,'photo'), caption='✅عکس ورودیت به این عکس تغییر کرد')

    #         msg = '''
    # ☺️خب حالا وقت ساختنه
    # برای ساختن عکست، لازمه که یه دستور (prompt) به ربات بدی تا هوش مصنوعی‌ما، بتونه با صورتت اون عکس رو بسازه.

    # 🔻برای ارسال دستورت به ربات، از /imagine استفاده کن و با یک فاصله، توضیحاتت رو بنویس.

    # 📝برای نوشتن یه prompt مناسب می‌تونی از این قالب استفاده کنی :
    # /imagine a [man/woman] wearing a [cloth] at [place] ...
    # ✅Example : /imagine a man wearing a black suit at business pitch desk meeting

    # 📌چند تا نکته برای نوشتن یه prompt خوب :
    # 1. سعی کن تا جایی که میتونی به ربات توضیح بدی که دوست داری چه عکسی ازت بسازه، از تعیین جنسیت تا نوع لباسی که قراره تنت باشه و جایی که میخوای باشی، حتی مدل مو و سن و سال و ...
    # 2. حتما دستوری که میفرستی باید به زبان انگلیسی باشه
    # 3. اگه یک سبک خاصی عکاسی مد نظرته، میتونی میتونی در قالب a ... photo of a به اول دستورت اضافه کنی، مثلا : a candid photo of a woman

    # 👈برای ایده گرفتن و دیدن استایل‌های مختلفی که میتونی دستورشون رو به ربات بدی، به این کانال مراجعه کن : @studAIo_prompts
    # ''' 
    #         await message.reply(msg)
            keyboard = ikb([[('🧔‍♂️ مرد', 'setgender_man'), ('🙎‍♀️ زن' , 'setgender_woman') ]])
            await message.reply('لطفا جنسیتتون رو تعیین کنید :', reply_markup = keyboard)

        else:
            #not active user
            msg = f'''سلام **{query.hget(chat_id,'name')}**، خوش برگشتی 👋

این ربات یه نسخه دمو از **{name}** هست که بهت کمک می‌کنه که بی‌نهایت عکس از خودت بسازی
👈نحوه کار این ربات اینجوریه که اول یه عکس از خودت میفرستی و بعد با دستوراتی که وجود داره، به کمک هوش مصنوعی عکس‌هایی با صورت خودت ساخته میشه

قابلیت های ربات برای شما فعال نیست! لطفا با ادمین در ارتباط باشید : @habibidev
                '''
            await message.reply(msg)


@bot.on_callback_query()
async def set_gender(client, cquery):
    chat_id = cquery.message.chat.id

    if('setgender_' in cquery.data):
        gender = cquery.data.split('_')[1]
        query.hset(chat_id, 'gender', gender)
        await cquery.answer('جنسیت عکس ورودیت با موفقیت ثبت شد')
        await client.delete_messages(chat_id,message_ids=cquery.message.id)

        msg = '''
😎خب حالا وقت ساختنه
برای ساختن عکس جدید از خودت، فقط کافیه که از بین استلاهایی که توی این چنل هست(@studaio_styles) یکی رو انتخاب کنی 

📌بعدش فقط کافیه به کمک دستور /imagine_styleNumber استایل مورد نظرت رو به ربات بگی و درخواستت رو ثبت کنی، مثلا 
/imagine_1 

✅بعد از اینکه دستورت رو ثبت کردی، درخواستت توی صف قرار میگیره و بعد از اینکه عکسات ساخته بشه، همینجا برات ارسال میشه
'''
        await cquery.message.reply(msg)


@bot.on_message(filters.private & filters.regex('/imagine_'))
async def imagine(client, message):
    chat_id = message.chat.id
    style = message.text.replace('/imagine', '')
    style = style.replace('_','')
    valid_styles = ['1','2','3','4','5','6']

    if(style not in valid_styles):
        await message.reply('استایل ورودی معتبر نیست! برای راهنمایی در مورد نحوه تولید عکس جدید : /imagine_help')
        return
    
    credits = int(query.hget(chat_id, 'credit'))
    progress_stat = query.hget(chat_id,'progress')

    #ACTIVE USER?!
    if(query.hget(chat_id,'active') == 'True' and query.hget(chat_id,'photo') != None):
        #active user
        #ENOUGH CREDITS?
        if(credits > 0):
            #enough credits
            #Already in progress?
            if(progress_stat == 'False'):
                #no
                #time to GENERATE images
                

                query.hset(chat_id,'progress', 'True')                           #set progress True


                photo = query.hget(chat_id, 'photo')
                query.lpush('tasks', f'imagine:{chat_id}:{style}:{photo}')       #add new task to task queue
                query.hset(chat_id, 'credit', str(credits-1))                    #decrease credits 

                await client.send_photo(
                    admin,
                    photo,
                    caption = f'New Task\nImagine:{chat_id}:{style}:@{query.hget(chat_id,"username")}\n'
                )

                await message.reply('✅درخواست شما ثبت شد، عکسهای شما بعد از اینکه پردازش شدن همینجا براتون ارسال میشن\nبرگشت به منوی اصلی : /menu')
            else:
                #already have one on progress
                await message.reply('شما در حال حاضر یک درخواست در حال انجام دارید، لطفا تا انجام درخواست قبلی منتظر باشید')
        else:
            #not enought credits
            await message.reply('اعتبار تولید عکس شما به پایان رسیده! برای افزایش اعتبار /credit کلیک کنید')

    else:
        #not active user
        msg = f'''دوست خوبم **{query.hget(chat_id,'name')}**،
شما هنوز عکس ورودیت رو تعیین نکردی، لطفا از طریق /set_image یه عکس برای ربات ارسال کن

منوی اصلی : /menu
            '''
        await message.reply(msg)







    # #check if input is valid
    # if(len(prompt) < 5):
    #     await message.reply('دستور ورودی شما کوتاه تر از حد مجاز است! لطفا دوباره تلاش کنید')

    # else:
    #     #it is at least 5 chrs
    #     if('man'in prompt or 'woman' in prompt):
    #         #OKKKK
    #         file = query.hget(chat_id, 'photo')
    #         # input = 'images/ahmad.jpg'
    #         prmpt = f'RAW photo,{prompt}, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3'
    #         await message.reply('عکس شما در حال پردازش است، لطف منتظر باشید ...')
    #         try:
    #             r = generate_image(
    #                 prmpt,
    #                 image_input = file,
    #                 output_folder= 'outputdata/',
    #                 batch_size= 4,
    #                 enable_roop= True,
    #                 enable_upscale= False,
    #                 step=25
    #                 )

    #             for i in r :
    #                 await client.send_photo(chat_id, i)
    #         except Exception as error:
    #             await client.send_message(admin, error)
            
    #     else:
    #         #should use man or woman in this
    #         await message.reply('دستور شما باید حاوی جنسیت باشد')


# @bot.on_message(filters.private & filters.command('task'))
# async def add_task(client, message):
#     id = message.chat.id
#     task1.delay('791927771')
#     await message.reply('task 1 started')
#     task2.delay('791927771')
#     await message.reply('task 2 started')



bot.run()








