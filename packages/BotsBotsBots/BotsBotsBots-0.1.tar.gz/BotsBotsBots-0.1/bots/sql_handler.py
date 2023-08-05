import sqlite3


def connect(database_name='test.db'):
    connection = sqlite3.connect(database_name)
    print('Database opened successfully!')
    return connection


def create_table(connection, table_name, fields, types, primary_key=None, nullable=None):
    contents = []
    if primary_key is None:
        primary_key = len(fields) * [False]
    if nullable is None:
        nullable = len(fields) * [True]
    assert len(fields) == len(types) == len(primary_key) == len(nullable)
    for field, pk, field_type, n in zip(fields, primary_key, types, nullable):
        e = f'{field} {field_type}'
        if pk:
            e += ' PRIMARY KEY'
        if not n:
            e += ' NOT NULL'
        contents.append(e)
    contents = '(' + ', '.join(contents) + ')'
    command = f'CREATE TABLE {table_name} {contents};'
    connection.execute(command)
    print("Table created successfully")


def get_string_array(connection, table):
    is_string = []
    cursor = connection.execute(f"PRAGMA table_info({table})")
    for row in cursor:
        t = row[2]
        if 'TEXT' in t or 'CHAR' in t:
            is_string.append(True)
        else:
            is_string.append(False)
    return is_string


def insert(connection, table, fields, values):
    if len(fields) != len(values):
        print('www')


    assert len(fields) == len(values)
    f = ', '.join(fields)
    is_string = get_string_array(connection, table)
    corrected_values = []
    for value, s in zip(values, is_string):
        if s:
            corrected_values.append(f"\'{value}\'")
        else:
            corrected_values.append(str(value))
    values = corrected_values
    v = ', '.join(values)
    command = f"INSERT INTO {table} ({f}) VALUES ({v})"
    connection.execute(command)
    connection.commit()


def insert_multiple(connection, table, all_fields, all_values):
    for fields, values in zip(all_fields, all_values):
        insert(connection, table, fields, values)


def select(connection, table, fields, condition=None):
    c = ' '
    if condition is not None:
        c += f'WHERE {condition}'
    command = 'SELECT ' + ', '.join(fields) + f' from {table}' + c
    cursor = connection.execute(command)
    result = []
    for row in cursor:
        line = []
        for e in row:
            line.append(e)
        result.append(line)
    return result


def update(connection, table, fields, values, condition=None):
    command = f'UPDATE {table} set ' + ', '.join([f'{field} = {value}' for field, value in zip(fields, values)])
    if condition is not None:
        command += f' WHERE {condition}'
    connection.execute(command)
    connection.commit()


def delete(connection, table, condition):
    command = f'DELETE from {table} where {condition}'
    connection.execute(command)
    connection.commit()


def close_connection(connection):
    connection.close()


# https://www.tutorialspoint.com/sqlite/sqlite_python.htm
if __name__ == '__main__':
    conn = connect(database_name='test.db')

    # create_table(
    #     connection=conn,
    #     table_name='COMPANY',
    #     fields=['ID', 'NAME', 'AGE', 'ADDRESS', 'SALARY'],
    #     primary_key=[True, False, False, False, False],
    #     types=['INT', 'TEXT', 'INT', 'CHAR(50)', 'REAL'],
    #     nullable=[False, False, False, True, True]
    # )

    # fields = ['ID', 'NAME', 'AGE', 'ADDRESS', 'SALARY']
    # insert_multiple(
    #     connection=conn,
    #     table='COMPANY',
    #     all_fields=[fields, fields, fields, fields],
    #     all_values=[
    #         [1, 'Paul', 32, 'California', 20000.00],
    #         [2, 'Allen', 25, 'Texas', 15000.00],
    #         [3, 'Teddy', 23, 'Norway', 20000.00],
    #         [4, 'Mark', 25, 'Rich-Mond', 65000.00]
    #     ]
    # )

    # s = select(
    #     connection=conn,
    #     table='COMPANY',
    #     fields=['ID', 'NAME', 'ADDRESS', 'SALARY']
    # )
    # print(s)

    # update(
    #     connection=conn,
    #     table='COMPANY',
    #     fields=['SALARY'],
    #     values=[25000.00],
    #     condition='ID = 1'
    # )

    # conn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID = 1")
    # conn.commit()

    # delete(
    #     connection=conn,
    #     table='COMPANY',
    #     condition='ID = 2'
    # )

    close_connection(conn)
