import datetime

SUBGROUP_1 = 62254
SUBGROUP_2 = 62253
SUBGROUP_BOTH = 0

class subject:
    """
    Obviously subject class.
    """
    def __init__(self, discipline, subgroup, auditorium, date, begin_lesson, end_lesson):
        self.discipline = discipline
        self.subgroup = subgroup
        self.auditorium = auditorium
        self.date = date
        self.begin_lesson = begin_lesson
        self.end_lesson = end_lesson

class WrongFormatError(BaseException):
    pass


class WrongDateFormatError(BaseException):
    pass


class WrongDisciplineError(BaseException):
    pass


def valid_date(date_text):
    """
    Checks if date fits proper format
    """
    try:
        datetime.datetime.strptime(date_text, '%d.%m.%y')
        return True
    except ValueError:
        return False

def write_task(tasks, data):
    tasks[data[0]] = tasks.get(data[0], {})
    tasks[data[0]][data[1]] = tasks.get(data[1], [])
    tasks[data[0]][data[1]].append(data[2])