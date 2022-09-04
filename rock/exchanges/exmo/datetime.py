from datetime import datetime, timedelta


def datetime_from_ms(ms: int) -> datetime:
    epoch = datetime(1970, 1, 1)
    delta = timedelta(milliseconds=ms)
    return epoch + delta
