from django.shortcuts import render
from sympy import sympify, sqrt
import math
import cmath
from django.conf.urls import handler404
from django.shortcuts import render

# Определение представления для 404 ошибки
def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)

# Настройка обработчика 404
handler404 = 'calc.urls.custom_page_not_found'



def home(request):
    if request.method == 'POST':
        if 'number' in request.POST:
            # Обработка формы с числом (дробные и целые числа)
            number = request.POST.get('number')
            precision = int(request.POST.get('precision', 2))  # Получаем точность

            try:
                # Преобразуем введенное значение в float
                number = float(number)

                # Извлекаем корень из числа
                if number > 0:
                    result = math.sqrt(number)
                    result = round(result, precision)  # Округляем до нужной точности
                    result = int(result) if result.is_integer() else result
                    number = int(number) if number.is_integer() else number
                    
                    return render(request, 'result.html', {'result': result, 'sign': '±','number': number})
                elif number==0:
                    return render(request, 'result.html', {'result': '0','number': '0', 'sign': ''})
                else:
                    result = cmath.sqrt(number)
                    result = complex(round(result.real, precision), round(result.imag, precision))
                    number = int(number) if number.is_integer() else round(number)
                    return render(request, 'result.html', {'result': result, 'sign': '±','number': number})
            
            except ValueError:
                # Обработка некорректных чисел
                return render(request, 'result.html', {'error': 'Некорректное число'})

        elif 'expression' in request.POST:
            # Обработка формы с выражением
            expression = request.POST.get('expression')

            try:
                # Преобразуем строку в математическое выражение с помощью sympy
                expr = sympify(expression)
                result = sqrt(expr)

                # Выводим результат
                return render(request, 'result.html', {'result': result})

            except Exception as e:
                # Если произошла ошибка в выражении
                return render(request, 'result.html', {'error': f'Некорректное выражение: {str(e)}'})

    # Если это GET-запрос, рендерим домашнюю страницу
    return render(request, 'home.html')

def result(request):#Страница с выводом результатов
    result = request.session.get('result', None)
    return render(request, 'result.html', {'result': result})
