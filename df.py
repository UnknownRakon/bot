# Функции для DialogFLow
import json
import apiai
import config_reader as config_reader


# Функция конструктор (выбирает из функций ниже)
def make_response(response_from_ai, action, parameters):
    def cons_response(data_obtain):
        if data_obtain == 'response_ai':
            return response_from_ai
        elif data_obtain == 'action':
            return action
        elif data_obtain == 'parameters':
            return parameters
        else:
            return None
    return cons_response


# Достаём ответ от DF
def response_ai(response):
    return response('response_ai')


# Достаём action из DF
def action(response):
    return response('action')


# Для времени(параметры даты и времени)
def parameters(response):
    return response('parameters')


# Сборка данных для запроса
def collect_request(message):
    config = config_reader.config()

    request = apiai.ApiAI(f'{config_reader.token(config)}').text_request()
    request.session_id = f'{config_reader.session_id(config)}'
    request.lang = f'{config_reader.lang(config)}'
    request.query = message

    return request


# Главная функция (Получает все данные)
def request_to_dialogflow(request):
    full_json_response = json.loads(request.getresponse().read().decode('utf-8'))
    response_ai = full_json_response['result']['fulfillment']['speech']
    action = full_json_response['result']['action']
    try:
        parameters = full_json_response['result']['parameters']
    except KeyError:
        parameters = None

    return make_response(response_ai, action, parameters)
