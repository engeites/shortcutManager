import datetime


def get_current_time():
    now = datetime.datetime.now()

    cur_date = now.strftime("%Y-%m-%d")
    cur_time = now.strftime("%H:%M:%S")
    return {"current_time": cur_time,
            "current_date": cur_date}
