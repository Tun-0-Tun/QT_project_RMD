def getTableRows():
    return [
            "ID",
            "личный номер (при наличии)",
            "в/зв по запасу (при наличии)",
            "Пол",
            "Фамилия",
            "Имя",
            "Отчество",
            "Число, год рождения",
            "Контакты (тел. адррес эл. почты)",
            "Статус",
            "Отдельная квота",
            "Выпускник СВУ, ПКУ, КК Минобороны",
            "Округ",
            "Субъект",
            "Выбор ВК",
            "Наименование вуза",
            "Дата регистрации заявления",
            "Признак отбора",
            "Дата направления учебного центра",
            "Исходящий номер документа",
            "Примечание",
            "Резервная_1",
            "Резервная_2",
            "Резервная_3",
            "Резервная_4",
            "Резервная_5"
        ]
def getShortTableRows():
    return [
        "ID",
        "личный номер (при наличии)",
        "в/зв по запасу (при наличии)",
        "Пол",
        "Фамилия",
        "Имя",
        "Отчество",
        "Число, год рождения",
        "Контакты (тел. адррес эл. почты)",
        "Статус",
        "Отдельная квота",
        "Выпускник СВУ, ПКУ, КК Минобороны",
        "Округ",
        "Субъект",
        "Выбор ВК",
        "Наименование вуза",
        "Дата регистрации заявления",
        "Признак отбора",
        "Дата направления учебного центра",
        "Исходящий номер документа",
        "Примечание"
    ]
def getSelectableRows():
        return [
            "в/зв по запасу (при наличии)",
            "Пол",
            "Статус",
            "Отдельная квота",
            "Выпускник СВУ, ПКУ, КК Минобороны",
            "Округ",
            "Субъект",
            "Выбор ВК",
            "Наименование вуза"
        ]

def getColumnValues():
    dictionary = dict()
    dictionary['Sex'] = ['M', 'Ж']
    dictionary['Rang'] = ['рядовой', 'ейфрейтор', 'мл. сержант', 'сержант', 'ст. сержант', 'старшина']
    dictionary['Status'] = ['зачислен', 'отчислен']
    return dictionary
def getRussianColumnNames() :
    dictionary = dict()
    dictionary['Пол'] = 'Sex'
    dictionary['в/зв по запасу (при наличии)'] = 'Rang'
    dictionary['Статус'] = 'Status'
    return dictionary

def getDBColumnsList():
    return ['ID', 'PersonalNumber', 'Rang', 'Sex' , 'Surname', 'Name', 'FatherName', 'Birthday', 'Contacts', 'Status', 'SeparateQuota', 'Graduated',
            'District', 'Subject', 'VK', 'University', 'RegistrationDate', 'SelectionCriteria', 'ReferalDate', 'DocumentNumber', 'Note', "ADD1", "ADD2","ADD3", "ADD4","ADD5"]
