from apscheduler.schedulers.blocking import BlockingScheduler
from db_queries.db_functions import *
from main import *
from img_comparing import *



sched = BlockingScheduler({'apscheduler.timezone': 'Israel'})
#
# @sched.scheduled_job('interval', minutes=2)
# def timed_job():
#     print('This job will run every three minutes.')


@sched.scheduled_job('cron', hour='18', minute='47')
def schedule_for_today():
    print("===========")
    print("schedule works 18:47")
    print("===========")

    teachers = find_all('managers', {})
    clean_teachers = handle_cursor_obj(teachers)

    schedule_datetime = get_datetime_for_scheduler(teachers["schedule"])
    db_curr_date_format = schedule_datetime.strftime("%d/%m/%Y")

    for teacher in clean_teachers:
        print("in the teachers loop")
        class_name = teacher["class"]
        sched.add_job(create_attendance_report, trigger='date', run_date=schedule_datetime,
                      args=[class_name, db_curr_date_format])
    print("ADDED TASKS:")
    print(sched.get_jobs())


# will run everyday at 01:05 AM.
# sched.add_job(my_job, trigger='cron', hour='01', minute='05')

# @sched.scheduled_job('interval', minutes=2)


sched.start()
