import sqlite3

def create_db():
    try:
        connection = sqlite3.connect('main_dictionary_db.db')
        cursor = connection.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS DictData (
                Name  TEXT PRIMARY KEY,
                ItemsCount INTEGER)''')
        connection.commit()
        cursor.close()
        connection.close()
    except:
        print('error')
def get_column_names(number:int):
    str = '"Name", "ItemsCount"'
    for i in range(number):
        str += f',"N{i}"'
    return str
def add_dict(dictName:str, values:list):
    try:
        while (get_db_columns_count() < 2 + len(values)): # to get enough column number
            add_new_column()
        connection = sqlite3.connect('main_dictionary_db.db')
        cursor = connection.cursor()
        columns = get_column_names(len(values))

        values.insert(0, str(len(values)))
        values.insert(0, '"' + dictName+'"')
        for i in range(2, len(values)):
            values[i] = '"' + values[i] + '"'
        params = ','.join(values)
        params = params[0:len(params)]
        print(f'INSERT INTO DictData ({columns}) VALUES ({params})')
        cursor.execute(f'INSERT INTO DictData ({columns}) VALUES ({params});')
        connection.commit()
        cursor.close()
        connection.close()
    except:
        print('error')

def get_db_columns_count():
    try:
        connection = sqlite3.connect('main_dictionary_db.db')
        cursor = connection.cursor()
        cursor.execute('PRAGMA table_info(DictData)')
        tmp = cursor.fetchall()
        cursor.close()
        connection.close()
        print(tmp)
        return len(tmp)
    except:
        print('error')
        return 0
def add_new_column():
    try:
        connection = sqlite3.connect('main_dictionary_db.db')
        cursor = connection.cursor()
        currentLen = get_db_columns_count()
        cursor.execute(f'ALTER TABLE DictData ADD N{currentLen-2} TEXT;')
        cursor.close()
        connection.close()
    except:
        print('error')

def get_total_dictionary():
    try:
        connection = sqlite3.connect('main_dictionary_db.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM DictData")
        totalDict = dict()
        tmp = cursor.fetchall()
        for lst in tmp:
            totalDict[lst[0]] = list(lst)[2:len(lst)]

        cursor.close()
        connection.close()
        return totalDict
    except:
        print('error')
        return dict()
def edit_dict(dictName:str, values:list):
    try:
        while (get_db_columns_count() < 2 + len(values)): # to get enough column number
            add_new_column()
        connection = sqlite3.connect('main_dictionary_db.db')
        cursor = connection.cursor()
        columns = get_column_names(len(values))

        values.insert(0, str(len(values)))
        values.insert(0, '"' + dictName+'"')
        for i in range(2, len(values)):
            values[i] = '"' + values[i] + '"'
        params = ','.join(values)
        cursor.execute(f"REPLACE INTO DictData ({columns}) VALUES ({params});")
        connection.commit()
        cursor.close()
        connection.close()
    except:
        print('error')

def remove_dict(dictName:str):
    try:
        connection = sqlite3.connect('main_dictionary_db.db')
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM DictData WHERE Name='{dictName}'")
        connection.commit()
        cursor.close()
        connection.close()
    except:
        print('error')
add_dict("Округ", ["Центральный", "Северо-Западный", "Приволжский", "Южный","Северо-Кавкасзкий", "Уральский", "Сибирский", "Дальневосточный" ])
add_dict("Звание", ["Рядовой", "Ефрейтор", "Мл. сержант", "Сержант", "Ст. сержант", "Старшина"])