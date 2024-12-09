from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.db import connection
from django.utils.safestring import mark_safe

class SimpleForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    age = forms.IntegerField(label='Возраст', min_value=0)
    email = forms.EmailField(label='Электронная почта')
    birth_date = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))


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
        # print(key)
        column = f'''
            <p><label for=\"{key}\">{key}</label>
            <input type=\"text\" name=\"{key}\" maxlength=\"{length}\"></p>
        '''
        form += column
    # print(columns)
    return mark_safe(form)


TABELS = []

# Create your views here.

def index(req):
    return render(req, 'main/index.html')

# def testPage(request):
#     # return render(req, 'main/test.html')
#     form = SimpleForm()  # Создаём объект формы
#     if request.method == 'POST':
#         form = SimpleForm(request.POST)
#         if form.is_valid():
#             # Обрабатываем данные из формы
#             cleaned_data = form.cleaned_data
#             print(cleaned_data)  # Для примера, выводим данные в консоль
#             return render(request, 'main/test.html', {'form': form})  # Перенаправляем на страницу успеха
#
#     return render(request, 'main/test.html', {'form': form})


def testPage(request):
    table = 'gastarbiters'
    form = generateForm(table)
    if request.method == "POST":
        # print(request.POST)
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
        # print(', '.join(keys))
        with connection.cursor() as cursor:
            query = f'INSERT INTO {table} ({", ".join(keys)}) VALUES ({", ".join(values)})'
            print(query)
            cursor.execute(query)
        return render(request, 'main/test.html', {'form': mark_safe(form)})
    return render(request, 'main/test.html', {'form': mark_safe(form)})

def addPage(request):
    table = 'gastarbiters'
    form = generateForm(table)
    if request.method == "POST":
        # print(request.POST)
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
        # print(', '.join(keys))
        with connection.cursor() as cursor:
            query = f'INSERT INTO {table} ({", ".join(keys)}) VALUES ({", ".join(values)})'
            print(query)
            cursor.execute(query)
        return render(request, 'main/add.html', {'form': mark_safe(form)})
    return render(request, 'main/add.html', {'form': mark_safe(form)})