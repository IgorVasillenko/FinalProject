from apscheduler.schedulers.blocking import BlockingScheduler
from db_queries.db_functions import *
from main import *
from img_comparing import *
from datetime import datetime

sched = BlockingScheduler({'apscheduler.timezone': 'Israel'})


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
                      args=[class_name, db_date_format], id=class_name)
    print("ADDED TASKS:")
    print(sched.get_jobs())


# @sched.scheduled_job('interval', minutes=1)
# def produce_by_click():
#     db_format_date = get_db_date_format(date.today())
#     fetch = find_all('manual', {"date": db_format_date, "status": "pending"})
#     clean_tasks = handle_cursor_obj(fetch)
#     for task in clean_tasks:
#         print("====in TASKS loop=====")
#         class_name = task["class_name"]
#         print(update_one('manual', {"date": db_format_date, "class_name": task["class_name"]}, {"status": "done"}))
#         print('updated status to done')
#         sched.add_job(create_attendance_report, args=[class_name, db_format_date])



if __name__ == '__main__':
    sched.start()
    print('ok')
