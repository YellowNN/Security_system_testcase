import psycopg2

# Установка подключения с БД и подготовка к созданию необходимых таблиц
conn = psycopg2.connect(dbname = 'SecuritySystem', user = 'postgres', password = '12345')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS sensor_info')
cur.execute('DROP TABLE IF EXISTS signal_info')
cur.execute('DROP TABLE IF EXISTS sensor_conditions')
conn.commit()

# Создание необходим таблиц и заполнение таблицы типов состояния датчиков
cur.execute('''CREATE TABLE sensor_info
            (sensor_id serial PRIMARY KEY NOT NULL,
            serial_number varchar(10) NOT NULL,
            install_location text NOT NULL,
            power_level real,
            sensor_condition text, 
            CHECK (length(serial_number) = 10),
            CHECK (power_level >= 0 AND power_level <= 1));''')
cur.execute('''CREATE TABLE signal_info
            (signal_id serial PRIMARY KEY NOT NULL,
            date_time timestamptz NOT NULL,
            sensor_parent varchar(10) NOT NULL,
            signal_type int NOT NULL,
            CHECK (length(sensor_parent) = 10));''')
cur.execute('''CREATE TABLE sensor_conditions
            (condition_id serial PRIMARY KEY NOT NULL,
            sensor_condition text);''')
query = '''INSERT INTO sensor_conditions (sensor_condition) VALUES (%s);'''
conditions = (('тревога',),('активен',),('низкий заряд',),('неактивен',))
cur.executemany(query, conditions)

conn.commit()
cur.close()
conn.close()

