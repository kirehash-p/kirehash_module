import datetime

t_delta = 9 # 日本時間とUTCの時差
str_to_day = {
    "一昨日": -2,
    "昨日": -1,
    "今日": 0,
    "明日": 1,
    "明後日": 2,
    "明々後日": 3,
}
datetime_strp_formats = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
    "%m-%d",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
    "%Y/%m/%d",
    "%m/%d",
    "%Y年%m月%d日 %H時%M分%S秒",
    "%Y年%m月%d日 %H時%M分",
    "%Y年%m月%d日",
    "%H:%M:%S",
    "%H:%M",
    "%H時%M分%S秒",
    "%H時%M分",
]

def set_t_delta(delta):
    global t_delta
    t_delta = delta

# サーバーがアメリカとかにあっても大丈夫なようutcからずらした日本時間の時刻を返す。
def now():
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=t_delta)

def now_str():
    return now().strftime("%Y-%m-%d %H:%M:%S")

def now_minute_str():
    return now().strftime("%H:%M")

def now_day_str():
    return now().strftime("%Y-%m-%d")

def now_minute_str():
    return now().strftime("%H:%M")

def try_strptime(time_str):
    for fmt in datetime_strp_formats:
        try:
            return datetime.datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    return None

# YYYY-MM-DD形式の文字列が今日より前かどうかを判別し、bool値で返す。
def if_date_before_today(date_string):
    try:
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    except:
        return True # YYYY-MM-DD形式でないものもTrueとして処理する。
    return date < now().date()

# 今日から換算してn日後の日付をYYYY-MM-DD形式で返す。
def future_date(n):
    return (now().date() + datetime.timedelta(days=n)).strftime("%Y-%m-%d")

def datetime_to_utc(dt):
    return dt - datetime.timedelta(hours=t_delta)

def interpret_day(day_str: str) -> str:
    """
    日付を解釈する。
    :param day_str: 日付を表す文字列
    :return: YYYY-MM-DD形式の日付 | 空文字"""
    res_day = ""
    try:
        res_day = datetime.datetime.strptime(day_str, '%Y-%m-%d').strftime("%Y-%m-%d")
    except:
        if day_str in str_to_day:
            res_day = future_date(str_to_day[day_str])
    return res_day

def get_diff_minute(dest_time: str):
    now_time = now()
    target_time = datetime.datetime.strptime(dest_time, '%H:%M').replace(year=now_time.year, month=now_time.month, day=now_time.day, tzinfo=datetime.timezone.utc)
    if target_time < now_time:
        target_time += datetime.timedelta(days=1)
    td = target_time - now_time
    td_secounds = td.total_seconds()
    return td_secounds
