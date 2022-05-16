from apscheduler.schedulers.blocking import BlockingScheduler
from db_queries.db_functions import *
from main import *
from img_comparing import *
from datetime import datetime

sched = BlockingScheduler({'apscheduler.timezone': 'Israel'})
# @sched.scheduled_job('interval', minutes=2)
# def timed_job():
#     print('This job will run every three minutes.')


@sched.scheduled_job('cron', hour='12', minute='05')
def schedule_for_today():
    print("===========")
    print("schedule works 12:10")
    print("===========")

    teachers = find_all('managers', {})
    clean_teachers = handle_cursor_obj(teachers)
    for teacher in clean_teachers:
        print("====in the teachers loop=====")
        class_name = teacher["class"]
        execute_date, db_date_format = handle_schedule_dates(teacher["schedule"])
        print("TEACHER SCHEDULE IS AT: ", teacher["schedule"])
        sched.add_job(create_attendance_report, trigger='date', run_date=execute_date,
                      args=[class_name, db_date_format])
    print("ADDED TASKS:")
    print(sched.get_jobs())


@sched.scheduled_job('interval', seconds=15)
def produce_by_click():
    db_format_date = get_db_date_format(date.today())
    fetch = find_all('manual', {"date": db_format_date, "status": "pending"})
    clean_tasks = handle_cursor_obj(fetch)
    for task in clean_tasks:
        print("====in TASKS loop=====")
        if task["status"] == 'pending':
            class_name = task["class_name"]
            update_one('tasks', {"_id": task["_id"]}, {"status": "done"})
            sched.add_job(create_attendance_report, args=[class_name, db_format_date])

# def produce_by_click(class_name, curr_date):
#     # execute now
#     print("TRYING TO ADD SCHEDULE TASK")
#     print("curr date:" ,curr_date)
#     execute_date = get_execute_date_format(datetime.now() + timedelta(seconds=30))
#     print("execute_date:", execute_date)
#     sched.add_job(create_attendance_report, trigger="date", run_date=execute_date,
#                   args=[class_name, curr_date])
#     print("ADDED TASKS:")
#     print(sched.get_jobs())


def trying(class_name, curr_date):
    print("im in trying function ")
    print(datetime.now())
    print(class_name, curr_date)

# will run everyday at 01:05 AM.
# sched.add_job(my_job, trigger='cron', hour='01', minute='05')

# @sched.scheduled_job('interval', minutes=2)

if __name__ == '__main__':
    sched.start()
    print('ok')
