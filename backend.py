from pyrogram import Client, filters
from plugins import query, admin
from sdapi import generate_image

import time


bot = Client('mahdi2',api_id=863373,api_hash='c9f8495ddd20615835d3fd073233a3f6' )
# bot = Client(
#     'mahdi'
#     # plugins=plugins
#     )

styles = [
    [
        'professional photo, closeup portrait photo of caucasian man, wearing black sweater, serious face, dramatic lighting, nature, gloomy, cloudy weather, bokeh. bright face',
        'professional photo, closeup portrait photo of caucasian woman, wearing black sweater, serious face, dramatic lighting, nature, gloomy, cloudy weather, bokeh. bright face'
    ],#1
    [
        'closeup face photo of man in black clothes, night city street, bokeh, bright face',
        'closeup face photo of woman in black clothes, night city street, bokeh, bright face'
    ],#2
    [
        'RAW photo, photo of man wearing closed buttoned up white shirt posing at studio, full face visible,low angle, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3',
        'RAW photo, photo of woman wearing closed buttoned up white shirt posing at studio, full face visible,low angle, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3'
    ],#3
    [
        '1 man, upper body, portrait, black_hair, wavy hair, blue eyes, black turtleneck sweater, depth of field, outdoors, perfect face,looking at viewer, face focus, torso',
        '1 woman, upper body, portrait, black_hair, wavy hair, blue eyes, black turtleneck sweater, depth of field, outdoors, perfect face,looking at viewer, face focus, torso'
    ],#4
    [
        'RAW photo,a headshot portrait photo of a man wearing a business suit,full face visible,upper body, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3',
        'RAW photo,a headshot portrait photo of a woman wearing a business suit,full face visible,upper body, 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3'
    ],#5
    [
        'high quality, face portrait photo of 30 y.o european man, wearing white shirt, serious face, detailed face, skin pores, cinematic shot, dramatic lighting',
        'high quality, face portrait photo of 30 y.o european woman,makeup, wearing white shirt, serious face, detailed face, skin pores, cinematic shot, dramatic lighting'
    ]#6
]


@bot.on_message(filters.private & filters.regex('run_auto'))
async def task_run(client,message):
    # await message.reply('AutoPilot ON')
    print('Going to run tasks : ')

    while(True):
        if(query.get('autopilot') == 'False') :
            print('BREAKING LOOP') 
            break

        task = query.rpop('tasks') #todo bring it to tghe last part of doin tasks

        if(task != None):

            task = task.split(':')
            style = task[2]
            user = task[1]
            photo = task[3]
            # if(len(task) == 4) :
            # photo = task[3] +':'+ task[4]

            gender = query.hget(user,'gender')

            if(gender == 'man'): prompt_index = 0
            else : prompt_index = 1

            print(f'doing task : USER[{user}], STYLE[{style}], PHOTO[{photo}], GENDER[{gender}]')
            prmpt = styles[int(style) - 1][prompt_index]

            try:
                r = generate_image(
                    styles[int(style) -1][prompt_index], #prompte
                    image_input = photo,
                    negative_prompt = 'no face, half face, invisible face, crop face, nsfw',
                    output_folder= f'outputdata/{user}/',
                    batch_size= int(query.get('batch')),
                    enable_roop= True,
                    enable_upscale= False,
                    step=25
                    )
                # await client.send_photo(user, r[0], caption = '0')
                # client.send_photo(user, r[1], caption = '1')
                # await message.reply(f'Dont the tasks, this is the photo : {r[0]}')

                for i in r :
                    # query.hset('images', 'user', user)
                    # query.hset('images', 'photo', i)
                    query.lpush('outputs',f'{user}:{style}:{photo}:{gender}:{i}')
                    print('Done Task, this is photo: ' + i)
                    await Client.send_photo(client ,chat_id=user , photo=i, caption='ساخته شده با @studaiobot')
                    # await client.send_photo(user, i)

                query.hset(user,'progress', 'False')

            except Exception as error:
                print(error)

            print('=-=-=-=-=-=-=-=-=')
            # print('sleep for 5 sec')
            # time.sleep(5)
            # await message.reply('done task ' + task)

# @bot.on_message(filters.private & filters.regex('run_auto_off'))
# async def task_run(client,message):
#     auto_pilot = True

# @bot.on_message(filters.private & filters.regex('run_auto_on'))
# async def task_run(client,message):
#     auto_pilot = False

# @bot.on_message(filters.private & filters.regex('run_auto_latest'))
# async def task_run(client,message):
#     tasks = query.lrange('tasks',0,-1)

#     for i in range(0,len(tasks)):
#         task = query.rpop('tasks')
#         if(task != None):
#             user = task.split(':')[1]
#             query.hset(user,'progress', 'False')
#             await message.reply(task)

# @bot.on_message(filters.private & filters.regex('run_by_'))
# async def task_run(client,message):
#     rng = int(message.text.split('_')[2])
#     for i in range(0,rng):
#         task = query.rpop('tasks')
#         if(task != None):
#             user = task.split(':')[1]
#             query.hset(user,'progress', 'False')
#             await message.reply(task)

# while(True):
#     tasks = query.lrange('tasks',0,-1)
#     task = query.rpop('tasks')
#     if(task != None):
#         user = task.split(':')[1]
#         query.hset(user,'progress', 'False')
#         # Client.send_message(user,'gonna run a task and sleep 5 sec')
#         time.sleep(5)
#         Client.send_message(Client, user,task)

bot.run()