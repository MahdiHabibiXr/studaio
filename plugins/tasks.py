from celery import Celery
import time
from pyrogram import Client
# app = Celery('tasks', broker = 'redis://localhost:6379/0')
app = Celery('tasks', broker = 'amqp://localhost:5672')


@app.task
def task1(id):
    print('starting task1')
    # Client.send_message(id,'task 1 received')
    # time.sleep(10)
    print('done task 1')

@app.task
def task2(id):
    print('starting task2')
    # time.sleep(10)
    print('done task 2')