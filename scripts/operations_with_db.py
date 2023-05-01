import psycopg2

# Установка подключения с БД
def make_connection():
    conn = psycopg2.connect(dbname='SecuritySystem', user='postgres', password='12345')
    return conn

# Создание курсора в установленном подключении
def make_cursor(conn):
    cur = conn.cursor()
    return cur

# Сохранение изменений и закрытие курсора и подключения к БД
def commit_and_closing(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# Просмотр данных
def view():
    conn = make_connection()
    cur = make_cursor(conn)
    print(f'Какую информацию вы хотите посмотреть?\n'\
          '(Введите цифру)\n'\
          '(1 - Сигналы/2 - Датчики/3 - Типы сигналов)')
    answer = str(input()).capitalize()
    if answer == '1':
        cur.execute('''SELECT * FROM signal_info''')
    elif answer == '2':
        cur.execute('''SELECT * FROM sensor_info''')
    elif answer == '3':
        cur.execute('''SELECT * FROM sensor_conditions''')
    for i in cur.fetchall():
        print(i)
    commit_and_closing(conn, cur)

# Вставка данных о сигнале
def insert_new_signal_info():
    conn = make_connection()
    cur = make_cursor(conn)
    print('Пожалуйста, введите данные для ввода в базу:'\
          'дата сигнала, номер датчика (от которого пришел сигнал), тип сигнала\n'
          '(пример: 2022-06-16 19:37:23,0123456789,1)')
    date_time, serial_number, signal_type = map(str, input().split(','))
    cur.execute('''INSERT INTO signal_info (date_time, sensor_parent, signal_type)
                VALUES (%s, %s, %s)''', (date_time, serial_number, signal_type))
    commit_and_closing(conn, cur)

# Вставка данных о датчике
def insert_new_sensor_info():
    conn = make_connection()
    cur = make_cursor(conn)
    print('Пожалуйста, введите данные для ввода в базу:'\
          'номер датчика, место установки, уровень заряда, состояние датчика\n'
          '(пример: 0123456789,пр-т Ленина дом 10,0.55,активен)')
    serial_number, address, power_level, condition = map(str, input().split(','))
    cur.execute('''INSERT INTO sensor_info (serial_number, install_location, power_level, sensor_condition)
                VALUES (%s, %s, %s, %s)''', (serial_number, address, power_level, condition))
    commit_and_closing(conn, cur)

# Обновление данных о сигнале
def update_signal_info():
    conn = make_connection()
    cur = make_cursor(conn)
    print('Пожалуйста, введите ID сигнала, данные о котором нужно изменить:\n' \
          '(пример: 1)')
    signal_id = int(input())
    cur.execute('''SELECT * FROM signal_info WHERE signal_id = %s''', [signal_id])
    print(f'Текущие данные о выбранном сигнале: {cur.fetchall()}\n' \
          'Введите новые данные' \
          '(пример: 2022-06-16 19:37:23,0123456789,1)')
    datetime, serial_number, signal_type = map(str, input().split(','))
    cur.execute('''UPDATE signal_info
                SET date_time = %s, sensor_parent = %s, signal_type = %s
                WHERE signal_id = %s''', (datetime, serial_number, signal_type, signal_id))
    commit_and_closing(conn, cur)

# Обновление данных о датчике
def update_sensor_info():
    conn = make_connection()
    cur = make_cursor(conn)
    print('Пожалуйста, введите ID датчика, данные о котором нужно изменить:\n' \
          '(пример: 1)')
    sensor_id = int(input())
    cur.execute('''SELECT * FROM sensor_info WHERE sensor_id = %s''', [sensor_id])
    print(f'Текущие данные о выбранном датчике: {cur.fetchall()}\n' \
          'Введите новые данные' \
          '(пример: 0123456789,пр-т Ленина дом 10,0.55б,активен)')
    serial_number, address, power_level, condition = map(str, input().split(','))
    cur.execute('''UPDATE sensor_info
                SET serial_number = %s, install_location = %s, power_level = %s, sensor_condition = %s
                WHERE sensor_id = %s''', (serial_number, address, power_level, condition, sensor_id))
    commit_and_closing(conn, cur)

# Удаление данных о сигнале
def remove_signal_info():
    conn = make_connection()
    cur = make_cursor(conn)
    print('Пожалуйста, ведите ID сигнала, который хотите удалить' \
          '(пример: 1)')
    signal_id = int(input())
    cur.execute('''DELETE FROM signal_info 
                WHERE signal_id = %s''', [signal_id])
    commit_and_closing(conn, cur)

# Удаление данных о датчике
def remove_sensor_info():
    conn = make_connection()
    cur = make_cursor(conn)
    print('Пожалуйста, ведите ID датчика, который хотите удалить' \
          '(пример: 1)')
    sensor_id = int(input())
    cur.execute('''DELETE FROM sensor_info 
                WHERE sensor_id = %s''', [sensor_id])
    commit_and_closing(conn, cur)

# Отчет о состоянии датчика в указанную дату
def sensor_condition_report():
    conn = make_connection()
    cur = make_cursor(conn)
    print('Введите серийный номер интересующего датчика и дату' \
          '(пример: 0123456789,2022-06-16)')
    serial_number, datetime = map(str, input().split(','))
    cur.execute('''
                SELECT sensor_id, serial_number, install_location, sensor_conditions.sensor_condition FROM signal_info
                JOIN sensor_info ON signal_info.sensor_parent = sensor_info.serial_number
                JOIN sensor_conditions ON signal_info.signal_type = sensor_conditions.condition_id
                WHERE sensor_parent = %s 
                        AND date_time < %s 
                        AND date_time = (SELECT MAX(date_time) FROM signal_info 
                                         WHERE sensor_parent = %s
                                         AND date_time < %s)
                        ''', (serial_number, datetime + ' 23:59:59', serial_number, datetime + ' 23:59:59'))
    print(cur.fetchall())
    commit_and_closing(conn, cur)

# Отчет о сигналах в запрошенном временном интервале
def signals_report():
    conn = make_connection()
    cur = make_cursor(conn)
    print('Введите период времени (начало и конец)' \
          '(пример: 2022-06-16 19:37:23,2022-06-18 10:14:55)')
    start_time, end_time = map(str, input().split(','))
    cur.execute('''
                SELECT * FROM signal_info
                WHERE date_time BETWEEN %s AND %s
                ''', (start_time, end_time))
    for i in cur.fetchall():
        print(i)
    commit_and_closing(conn, cur)
