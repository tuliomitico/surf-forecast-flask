from datetime import datetime,timedelta

class TimeUtil():
    @staticmethod
    def get_unix_time_for_a_future_day(days: int) -> int:
        return (datetime.now() + timedelta(days)).timestamp()