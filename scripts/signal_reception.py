# Импорт функций для подключения к БД и использования каждой операции(вставки, удаления, обновления данных)
# Импорт datetime для добавления даты полученного сигнала.
import datetime as dt
import operations_with_db as op

# Вставка данных о сигнале в БД
def new_signal(date_time, serial_number, signal_type):
    conn = op.make_connection()
    cur = op.make_cursor(conn)
    cur.execute('''INSERT INTO signal_info (date_time, sensor_parent, signal_type)
                VALUES (%s, %s, %s)''', (date_time, serial_number, signal_type))
    op.commit_and_closing(conn, cur)

# Обновление сведений о датчике на основе данных сигнала
def sensor_update(serial_number, power_level, sensor_condition):
    conn = op.make_connection()
    cur = op.make_cursor(conn)
    cur.execute('''UPDATE sensor_info
                SET power_level = %s, sensor_condition = %s
                WHERE serial_number = %s''', (power_level, sensor_condition, serial_number))
    op.commit_and_closing(conn, cur)

# Функция приёма сигнала от датчика
# За границу 'низкого заряда' был взят порог в 15% от максимального заряда
def reception():
    while True:
        signal = input()
        serial_number, signal_type, power_level = map(str, signal.split('|'))
        date_time = dt.datetime.now()
        power_level = float(power_level)*0.01
        signal_type = int(signal_type)
        if signal_type == 1:
            sensor_condition = 'тревога'
        else:
            if power_level > 0.15:
                sensor_condition = 'активен'
                signal_type = 2
            elif 0.15 >= power_level > 0:
                sensor_condition = 'низкий заряд'
                signal_type = 3
            else:
                sensor_condition = 'неактивен'
                signal_type = 4

        new_signal(date_time, serial_number, signal_type)
        sensor_update(serial_number, power_level, sensor_condition)

reception()
