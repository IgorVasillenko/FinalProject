from apscheduler.schedulers.blocking import BlockingScheduler
from db_queries.db_functions import *
from main import *
from img_comparing import *



sched = BlockingScheduler({'apscheduler.timezone': 'Israel'})
#
# @sched.scheduled_job('interval', minutes=2)
# def timed_job():
#     print('This job will run every three minutes.')


@sched.scheduled_job('cron', hour='20', minute='02')
def schedule_for_today():
    print("===========")
    print("schedule works 20:02")
    print("===========")

    teachers = find_all('managers', {})
    clean_teachers = handle_cursor_obj(teachers)
    for teacher in clean_teachers:
        print("====in the teachers loop=====")
        class_name = teacher["class"]

        execute_date_format, db_date_format = handle_schedule_dates(teacher["schedule"])
        print("TEACHER SCHEDULE IS AT: ", teacher["schedule"])
        sched.add_job(create_attendance_report, trigger='date', run_date=execute_date_format,
                      args=[class_name, db_date_format])
    print("ADDED TASKS:")
    print(sched.get_jobs())


def produce_by_click(class_name, curr_date):
    # execute now
    print("TRYING TO ADD SCHEDULE TASK")
    sched.add_job(create_attendance_report, id="report of today",  args=[class_name, curr_date])
    print("ADDED TASKS:")
    for job in sched.get_jobs():
        print(job)




# will run everyday at 01:05 AM.
# sched.add_job(my_job, trigger='cron', hour='01', minute='05')

# @sched.scheduled_job('interval', minutes=2)

if __name__ == '__main__':
    sched.start()
