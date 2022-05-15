from apscheduler.schedulers.blocking import BlockingScheduler
from db_queries.db_functions import *
from main import *


sched = BlockingScheduler({'apscheduler.timezone': 'GMT'})

@sched.scheduled_job('interval', minutes=2)
def timed_job():
    print('This job will run every three minutes.')


@sched.scheduled_job('cron', hour='16', minute='52')
def schedule_for_today():
    print("schedule works 17:07")
    teachers = find_all('managers',{})
    clean_teachers =handle_cursor_obj(teachers)
    for teacher in clean_teachers:
        print(teacher)
        # sched.add_job(my_job, trigger='date', hour='01', minute='05')


@sched.scheduled_job('cron', hour='13', minute='52')
def schedule_for_today2():
    print("schedule works 14:07")
    teachers = find_all('managers',{})
    clean_teachers =handle_cursor_obj(teachers)
    for teacher in clean_teachers:
        print(teacher)

# will run everyday at 01:05 AM.
# sched.add_job(my_job, trigger='cron', hour='01', minute='05')

# @sched.scheduled_job('interval', minutes=2)


sched.start()
