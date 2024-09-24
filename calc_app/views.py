from django.shortcuts import render
#from sympy import sympify, sqrt
import math
import cmath
from django.conf.urls import handler404, handler403, handler500
from django.shortcuts import render

def custom_500(request):
    return render(request, '404.html', status=500)

def custom_403(request, exception):
    return render(request, '404.html', status=403)

def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)

handler404 = 'calc.urls.custom_page_not_found'
handler500 = 'calc.urls.custom_500'
handler403 = 'calc.urls.custom_403'



def home(request):
    if request.method == 'POST':
        if 'number' in request.POST:
            # Обработка формы с числом (дробные и целые числа)
            number = request.POST.get('number')
            precision = int(request.POST.get('precision', 2))  # Получаем точность

            try:
                # Преобразуем введенное значение в float
                if ('.' in number):
                    number = float(number)
                else:
                    number = int(number)

                # Извлекаем корень из числа
                if number > 0:
                    result = math.sqrt(number)
                    result = round(result, precision)  # Округляем до нужной точности
                    
                     # Обрабатываем числа, близкие к нулю, для корректного отображения
                    if result < 10**-precision:  # Если результат близок к нулю
                        result = format(result, f".{precision}f")  # Форматируем с нужной точностью
                    else:
                        result = int(result) if result.is_integer() else result

                     
                    return render(request, 'result.html', {'result': result, 'sign': '±', 'number': number})
                    
                    result = int(result) if result.is_integer() else result
                    number = int(number) if number.is_integer() else number
                    
                    return render(request, 'result.html', {'result': result, 'sign': '±','number': number})
                elif number==0:
                    return render(request, 'result.html', {'result': '0','number': '0', 'sign': ''})
                elif number < 0:
                    result = cmath.sqrt(number)
                    result = complex(round(result.real, precision), round(result.imag, precision))
                    number = int(number) if number.is_integer() else round(number)
                    return render(request, 'result.html', {'result': result, 'sign': '±','number': number})
            
            except ValueError:
                # Обработка некорректных чисел
                return render(request, 'result.html', {'error': 'Некорректное число'})

    # Если это GET-запрос, рендерим домашнюю страницу
    return render(request, 'home.html')

def result(request):#Страница с выводом результатов
    result = request.session.get('result', None)
    return render(request, 'result.html', {'result': result})
