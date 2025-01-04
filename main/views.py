from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.db import connection
from django.utils.safestring import mark_safe

dictTables = {
    'apartments' : 'Жильё',
    'gastarbiters' : 'Гастарбайтеры',
    'Gas_Tools' : 'Гастарбайтеры-инструменты',
    'owners' : 'Хозяева квартир',
    'tools' : 'Инструменты',
    'workplaces' : 'Калым'
}

dictLabels = {
    'f_name' : 'Фамилия',
    'i_name' : 'Имя',
    'o_name' : 'Отчество',
    'pasport_ser' : 'Серия паспорта',
    'pasport_num' : 'Номер серии',
    'salary' : 'Зарплата',
    'id_workplace' : 'id рабочего места',
    'id_apartment' : 'id квартиры проживания'
}


class SimpleForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    age = forms.IntegerField(label='Возраст', min_value=0)
    email = forms.EmailField(label='Электронная почта')
    birth_date = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))


def GETTable(request):
    table_name = request.GET.get('table')
    print(f'table: {table_name}')
    return table_name


def generateTableList():
    tableList = ''
    for table in dictTables:
        if dictTables[table] != '':
            title = dictTables[table]
        else:
            title = table
        string = f'<li><a href="?table={table}"><button>{title}</button></a></li>'
        tableList += string
    return tableList


def generateForm(table_name):
    form = ""
    with connection.cursor() as cursor:
        query = f"""
        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        """
        cursor.execute(query)
        columns = cursor.fetchall()

    for key, type, length in columns:
        if key == 'id':
            continue
        if key in dictLabels:
            title = dictLabels[key]
        else:
            title = key
        column = f'''
            <p><label for=\"{key}\">{title}</label>
            <input type=\"text\" name=\"{key}\" maxlength=\"{length}\"></p>
        '''
        form += column
    return mark_safe(form)


# Create your views here.

def index(req):
    return render(req, 'main/index.html')

def testPage(request):
    table = ''
    form = generateForm(table)
    if request.method == "POST":
        keys = []
        values = []
        for key, value in request.POST.items():
            if key == 'csrfmiddlewaretoken':
                continue

            if value == '':
                values.append('NULL')
            else:
                values.append(f"\'{value}\'")

            keys.append(key)
        with connection.cursor() as cursor:
            query = f'INSERT INTO {table} ({", ".join(keys)}) VALUES ({", ".join(values)})'
            print(query)
            cursor.execute(query)
        return render(request, 'main/test.html', {'form': mark_safe(form)})
    return render(request, 'main/test.html', {'form': mark_safe(form)})


def viewPage(request):
    return render(request, 'main/view.html')


def changePage(request):
    return render(request, 'main/change.html')


def addPage(request):
    table = ''

    if request.method == "GET":
        table = GETTable(request)

    form = generateForm(table)
    tableList = generateTableList()
    renderPage = render(request, 'main/add.html', {'form': mark_safe(form), 'tablelistGen': mark_safe(tableList)})


    if request.method == "POST":
        keys = []
        values = []
        for key, value in request.POST.items():
            if table == '': # exit
                return renderPage
            if key == 'csrfmiddlewaretoken':
                continue

            if value == '':
                values.append('NULL')
            else:
                values.append(f"\'{value}\'")

            keys.append(key)
        with connection.cursor() as cursor:
            query = f'INSERT INTO {table} ({", ".join(keys)}) VALUES ({", ".join(values)})'
            print(query)
            cursor.execute(query)
        return renderPage
    return renderPage


def deletePage(request):
    return render(request, 'main/delete.html')