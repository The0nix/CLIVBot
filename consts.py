BOT_TOKEN = '234891684:AAFBx9W0Ona57eE7_hDSPSowQMib5L4vzJ4'
HELP_MESSAGE = 'You can use this bot to check CLIV\'s schedule and hometasks.'
START_MESSAGE_PRIVATE = "Choose what you want to do:"
CHECK_SCHEDULE_TEXT = 'Check schedule'
CHECK_TASKS_TEXT = 'Check hometask'
ADD_TASK_TEXT = 'Add hometask'
CANCEL_FAIL_TEXT = 'Nothing to cancel'
ADD_TASK_MESSAGE = 'Provide the task in the following format:\n <discipline_name>; <date>; <task>\n'
WRONG_FORMAT_TEXT = 'Wrong format.\nTry again or type "/cancel" to cancel current action.'
WRONG_DATE_FORMAT_TEXT = 'Wrong date format.\nTry again or type "/cancel" to cancel current action.'
WRONG_DISCIPLINE_TEXT = 'Unknown discipline name.\nTry again or type "/cancel" to cancel current action.'
SUCCESSFUL_ADDING_TEXT = 'Added successfully.'
DISCIPLINES = ('Английский', 'АиСД', 'Дискретная математика', 'Теорвер и матстат', 'Матанализ')
SCHEDULE_LINK = 'http://ruz.hse.ru/RUZService.svc/personlessons'
NO_TASKS_MESSAGE = 'No tasks! Hooray!'
COMMANDS = '/start - Starts the bot\n' \
           '/menu - Shows the menu\n' \
           '/cancel - Cancels current action\n' \
           '/commands - Shows commands\n' \
           '/schedule - Followed by dd.mm.yy shows schedule for date\n' \
           '/tasks - Followed by dd.mm.yy shows tasks since date\n' \
           '/history - Shows all tasks (not only upcoming)\n' \
           '/help - Shows help'
DISCIPLINE_ALIASES = {'английский' : DISCIPLINES[0],
                      'англ': DISCIPLINES[0],
                      'английский язык': DISCIPLINES[0],
                      'анг. яз.' : DISCIPLINES[0],
                      'аиcд' : DISCIPLINES[1],
                      'алгоритмы' : DISCIPLINES[1],
                      'алго' : DISCIPLINES[1],
                      'алгоритмы и структуры данных' : DISCIPLINES[1],
                      'дискретная математика' : DISCIPLINES[2],
                      'дискра' : DISCIPLINES[2],
                      'дискретка' : DISCIPLINES[2],
                      'теорвер и матстат' : DISCIPLINES[3],
                      'теория вероятностей и математическая статистика' : DISCIPLINES[3],
                      'теорвер' : DISCIPLINES[3],
                      'тервер' : DISCIPLINES[3],
                      'матстат' : DISCIPLINES[3],
                      'матанализ' : DISCIPLINES[4],
                      'матан' : DISCIPLINES[4],
                      'математический анализ' : DISCIPLINES[4]}