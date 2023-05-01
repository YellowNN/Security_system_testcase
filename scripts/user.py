# Импорт функций для подключения к БД и использования каждой операции(вставки, удаления, обновления данных)
# Импорт datetime для добавления даты входа пользователей.
import operations_with_db as op
import datetime as dt

# Приветствие и реализация истории пользователей изменявших данные в базе
print('Добрый день! Как вас зовут?')
name = str(input())
filename = 'users_history.txt'
with open(filename, mode='a') as file:
    file.write(f'\nUsername: {name}; datetime: {dt.datetime.now()}\n')

# Интерфейс для использования реализованных возможностей пользователя
while True:
    print(f'Что вы хотите сделать {name}?\n'\
          '(Введите цифру)\n'\
          '0 - Закончить, 1 - Посмотреть данные\n'\
          '2 - Ввести данные о сигнале, 3 - Ввести данные о датчике\n'\
          '4 - Удалить данные о сигнале, 5 - Удалить данные о датчике\n'\
          '6 - Изменить данные о сигнале, 7 - Изменить данные о датчике\n'\
          '8 - Получить информацию о состоянии датчика в определённый день,\n'\
          '9 - Получить информацию о сигналах датчиков за определённый период')
    answer = str(input()).capitalize()
    if answer == '0':
        break
    elif answer == '2':
        op.insert_new_signal_info()
    elif answer == '3':
        op.insert_new_sensor_info()
    elif answer == '1':
        op.view()
    elif answer == '4':
        op.remove_signal_info()
    elif answer == '5':
        op.remove_sensor_info()
    elif answer == '6':
        op.update_signal_info()
    elif answer == '7':
        op.update_sensor_info()
    elif answer == '8':
        op.sensor_condition_report()
    elif answer == '9':
        op.signals_report()