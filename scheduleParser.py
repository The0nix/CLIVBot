import datetime
import requests, json
from my_lib import *
import datetime
from consts import SCHEDULE_LINK

def parse_schedule(st, fin):
    """
    Parser schedule from st to fin from RUZ
    """
    link = SCHEDULE_LINK
    st = st.strftime('%Y.%m.%d')
    fin = fin.strftime('%Y.%m.%d')
    params = {'fromdate': st, 'todate': fin, 'receivertype': 3,'groupoid': 4418}
    timetable = requests.get(link, params=params)
    try:
        content = timetable.json()
    except json.decoder.JSONDecodeError:
        print('json.decoder.JSONDecodeError. May be wrong dates?')
        return []
    result = []
    for item in content:
        result.append(subject(item['discipline'],
                              item['subGroupOid'],
                              item['auditorium'],
                              datetime.datetime.strptime(item['date'], '%Y.%m.%d'),
                              datetime.datetime.strptime(item['beginLesson'], '%H:%M'),
                              datetime.datetime.strptime(item['endLesson'], '%H:%M')))
    return result