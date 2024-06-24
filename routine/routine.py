"""
指定秒数や、特定の時間ごとに処理を行うためのモジュール
@routine.timer(),@routine.interval()でデコレータを指定することで、
指定した秒数や、特定の時間ごとに処理を行うことができる。
"""

import time
from datetime import datetime
import threading

class Routine():
    def __init__(self):
        self.timers = []
        self.intervals = []

    def timer(self, datetime_obj):
        def wrapper(func):
            self.timers.append({
                'func': func,
                'datetime_obj': datetime_obj,
                'last_executed': None
            })
            return func
        return wrapper

    def interval(self, sec):
        def wrapper(func):
            self.intervals.append({
                'func': func,
                'sec': sec,
                'last_executed': None
            })
            return func
        return wrapper

    def run_by_timer(self, func, datetime_obj):
        now = datetime.now()
        dt_secounds = (datetime_obj - now).total_seconds()
        time.sleep(dt_secounds)
        func()

    def run_by_interval(self, func, sec):
        while True:
            time.sleep(sec)
            func()

    def run(self):
        for timer in self.timers:
            threading.Thread(target=self.run_by_timer, args=(timer['func'], timer['datetime_obj'])).start()

        for interval in self.intervals:
            threading.Thread(target=self.run_by_interval, args=(interval['func'], interval['sec'])).start()


if __name__ == '__main__':
    routine = Routine()

    @routine.timer(datetime(2024, 5, 9, 22, 9, 30))
    def timer_func():
        print('timer_func')

    @routine.interval(3)
    def interval_func():
        print('interval_func')
    
    time.sleep(10)

    @routine.interval(5)
    def timer_func():
        print('timer_func2')

    routine.run()