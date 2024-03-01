import requests
import json
import os
import numpy as np
import pprint

DOMAIN = 'https://api.hh.ru/'  # domain HeadHanter.ru

url_vacancies = f'{DOMAIN}vacancies'  # поиск вакансий


def separator(symbol: str, multipl: int) -> str:
    """
    Сепаратор для оформления меню
    :param symbol: любой символ
    :param multipl: коэффициент размножения
    :return: строка из символов
    """
    return symbol * multipl


def get_country_area_locality(country):
    """ получает по имени страны список всех локалей и  их id в  виде  словаря
    и  сохраняет в файл json
    приповторном  поиске обращается к файлу с id локалей
    :param country:
    :return: country_all_locality
    """
    name_of_file = f'country_locality_id_{country}.json '

    country_all_locality = []
    if os.path.exists(name_of_file):

        with open(name_of_file, 'r') as dict_locality:
            country_all_locality = json.load(dict_locality)
    else:
        url_countries = f'{DOMAIN}areas/countries'
        response = requests.get(url_countries).json()
        # [{'id': '113', 'name': 'Россия', 'url': 'https://api.hh.ru/areas/113'}]
        for el in response:
            if el['name'] == country:  # el == dict
                country_url: str = el['url']  # url страны
                country_id: str = el['id']  # id страны

                country_dict = dict([(el['name'], el['id'])])
                country_all_locality.append(country_dict)

                response = requests.get(country_url).json()
                for region in response['areas']:
                    one_region_id = dict([(region['name'], region['id'])])
                    country_all_locality.append(one_region_id)
                    one_region_locality = region['areas']  # [{'areas': [], 'id': '3506',
                    # 'name': 'Белозерка', 'parent_id': '2209'}
                    for locality in one_region_locality:
                        one_locality_id = dict([(locality['name'], locality['id'])])
                        country_all_locality.append(one_locality_id)

        with open(name_of_file, 'w') as dict_locality:
            json.dump(country_all_locality, dict_locality)

    return country_all_locality


def vacancies_search(profession):
    """
    дополняет наименование искомой вакансии '*' для  поиска по части строки, отключил пока
    :param profession:
    :return: f'{profession}*'
    """
    return f'{profession}'


vacancies_message = """Введите искомую вакансию,
затем определите область поиска:"""

menu_message = """\t\tМЕНЮ:
1.Создать поисковый запрос и сохранить данные в файл.
2. Расчет средней зарплаты по вакансии \n\tи запись результата в файл.
3. Рейтинг  требуемых навыков по вакансии \n\tи запись результата в файл.
4.Открыть файл отчета
5.'q' - Выход из программы - 'q' """


def search_parametrs(profession, point, page=0):
    """
    Создает params для GET запроса
    :param profession: 'искомая вакансия'
    :param point: локация поиска
    :return: params для GET запроса
    """

    params = {
        'text': profession,
        'area': point,
        'locale': "RU",
        "vacancy_search_order": [{
            "id": "relevance",
            "name": "по соответствию"
        }],
        'page': page,
        'pages': 100,
        'per_page': 100}
    params['text'] = profession
    params['area'] = point
    params['page'] = page

    return params


def search_area(locality_area, all_locality, country):
    if locality_area == "да":
        locality = input('Введите локацию(регион или населенный пункт): ')

        # поиск в country_all_locality
        for one_locality in all_locality:
            for k, v in one_locality.items():
                name_locality = k
                name_locality_id = v
                if locality == name_locality:
                    print(f'Вы выбрали поиск: {name_locality}, {name_locality_id}')
                    return name_locality_id
    else:
        for one_locality in all_locality:
            for k, v in one_locality.items():
                name_locality = k
                name_locality_id = v
                if country == name_locality:
                    # print(f'Вы выбрали поиск: {name_locality}, {name_locality_id}')
                    return name_locality_id


def menu_search_parametrs():
    """
    Сождает параметры запроса GET
    Меню для вызова search_parametrs() с параметрами
    :return: params
    """
    print(separator('*', 35))
    print(vacancies_message)
    print(separator('*', 35))

    profession = input('Введите искомую вакансию: ')
    profession = vacancies_search(profession)  # параметр profession

    # определение региона поиска

    country = input('В какой стране провести поиск?: ')
    all_locality = get_country_area_locality(country)  # список всех id страны
    locality_area = input('Сузить поле поиска("да" - "нет")?: ')
    point = search_area(locality_area, all_locality, country)
    params = search_parametrs(profession, point)
    return params


def get_list_all_vacancies(profession, point, pages):
    """
    Получает вакансии со всех страниц и формирует лист с описанием вакансий
    :param profession: искомая вакансия
    :param point: локация поиска
    :param pages: количество страниц с сайта
    :return: list_vacancies, описание вакансий получены по индивидуальным url
    """
    list_vacancies = []  # все вакансии по запросу в [{},{}]

    for page in range(pages):
        params = search_parametrs(profession, point, page)

        result = requests.get(url_vacancies, params=params)
        result = result.json()
        for one_vacancy in result['items']:
            url_one_vacancy = one_vacancy['url']
            one_vacancy_expand = requests.get(url_one_vacancy).json()
            keys = one_vacancy_expand.keys()
            if ('id' in keys) and ('salary' in keys) and ('key_skills' in keys):
                del one_vacancy_expand['branded_description']
                del one_vacancy_expand['description']
                list_vacancies.append(one_vacancy_expand)

    return list_vacancies


def menu_parser():
    """
    Меню функци  парсера
    :return:
    """
    while True:

        print(separator('*', 35))
        print(menu_message)
        print(separator('*', 35))

        choice = input('Введите номер пункта меню: ')

        if choice == '1':
            params = menu_search_parametrs()  # создание параметров поиска

            keywords = params['text']
            profession = params['text']
            point = params['area']

            print('!!!!!  Поисковый запрос сформирован  !!!!!')
            print(input('!!!!!  Введите для продолжения Enter  !!!!!'))

            result = requests.get(url_vacancies, params=params)  # первый запрос нужен для определения
            # количества  возвращаемых страниц

            print(separator('@@@@@@@@@@@@@', 2))
            print(f'\tStatus_code: {result.status_code}')  # проверка ответа сайта
            print(separator('@@@@@@@@@@@@@', 2))
            print()

            data = result.json()
            pages = data['pages']
            found_vacancies = data['found']
            print(f'*** По запросу "{keywords}" найдено вакансий: {found_vacancies}  ***')
            print(f'*** Количество страниц данных: {pages}  ***')
            print('Процесс идет, ждите ответа....')
            # получение list с вакансиями, полученными по их url
            all_vacancies_list = get_list_all_vacancies(profession, point, pages)

            # Создать словарь с ключами 'ключ поиска" и "вакансии все и сохранить его в файл
            # dict_search  = {'keyword': str, 'vacancies_all': []}
            dict_search = dict(keyword=keywords, vacancies_all=all_vacancies_list)

            with open('get_vacancies.json', 'w') as f:  # перезапись данных
                json.dump(dict_search, f)
            print(f'*** Вакансии  по запросу "{keywords}" сохранены \nв файл "get_vacancies.json" '
                  f'для последующего анализа***')

            #найденные вакансии сохраним в файл для анализа

            if  os.path.exists('get_report.json'):
                with open('get_report.json', 'r') as f:
                    keywords = json.load(f)

                with open('get_report.json', 'w') as f:
                    json.dump(keywords, f)
            print(f'***   "get_vacancies.json" ***')

        elif choice == '2':
            # расчет средних зарплат

            if os.path.exists('get_vacancies.json'):

                with open('get_vacancies.json', 'r') as f:
                    dict_search = json.load(f)
                keyword = dict_search['keyword']  # значение
                list_vacancies_all = dict_search['vacancies_all']  # значение  в виде []

                list_salary_vacancies = []

                for vacancy in list_vacancies_all:
                    list_salary_vacancies.append(vacancy['salary'])

                print(f'\t\t*** Размер зарплат вакансии "{keyword}" ***')

                list_salary_from = []
                list_salary_to = []

                for salary_vacancy in list_salary_vacancies:

                    if salary_vacancy != None:
                        # print(f'{i}. {salary_vacancy}')
                        if salary_vacancy['from'] != None:
                            salary_from = int(salary_vacancy['from'])
                            list_salary_from.append(salary_from)

                        if salary_vacancy['to'] != None:
                            salary_to = int(salary_vacancy['to'])
                            list_salary_to.append(salary_to)

                salary_from_min = min(list_salary_from)
                salary_from_max = max(list_salary_from)
                mean_salary_from = int(np.mean(list_salary_from))

                salary_to_min = min(list_salary_to)
                salary_to_max = max(list_salary_from)
                mean_salary_to = int(np.mean(list_salary_to))

                dict_salary_from_to = dict(salary_from_min=salary_from_min, salary_from_max=salary_from_max,
                                           mean_salary_from=mean_salary_from, salary_to_min=salary_to_min,
                                           salary_to_max=salary_to_max, mean_salary_to=mean_salary_to)

                print(f'Зарплата минималная: \nминимальная {min(list_salary_from)}, '
                      f'\nмаксимальная:{max(list_salary_from)}, '
                      f'\nСредня минимальна зарплата :  {mean_salary_from} RUR ')
                print()
                print(f'Зарплата максимальная: \nминимальная {min(list_salary_to)}, '
                      f'\nмаксимальная:{max(list_salary_to)}, '
                      f'\nСредня максимальная зарплата :  {mean_salary_to} RUR ')
                print()
                answer = input('Сохранить данные в файл ? ("да" - "нет"): ')
                if answer == 'да':
                    with open('report_salary', 'w') as f:
                        json.dump(dict_salary_from_to, f)
                else:
                    print('Ладно, позже....')
            else:
                answer = input('Файл данных для анализа еще не создан, создать его ("да" - "нет?")')
                if answer == "да":
                    menu_parser()

        elif choice == '3':
            pass
            if os.path.exists('get_vacancies.json'):
                with open('get_vacancies.json', 'r') as f:
                    dict_search = json.load(f)
                keyword = dict_search['keyword']  # значение
                list_vacancies_all = dict_search['vacancies_all']  # значение  в виде []

                list_skills_vacancies = []  # создаем список всех скилов в виде [ [{},{},{}], [{},{},{}] ]

                for vacancy in list_vacancies_all:
                    list_skills_vacancies.append(vacancy['key_skills'])
                # удаляем пустые списки из каждого элемента list_skills_vacancies
                list_skills_vacancies = [skills for skills in list_skills_vacancies if skills != []]

                only_all_skills = []  # список повторяющихся скилов из всех вакансий

                for el_list in list_skills_vacancies:
                    for el in el_list:
                        only_all_skills.append(el['name'])

                count_list_all_skills = len(only_all_skills)  # это 100%
                set_only_all_skills = set(only_all_skills)  # скилы  без повторов
                count_set_all_skills = len(set_only_all_skills)  # общее количество скилов  без повторов

                dict_all_skill = []  # список словарей скилов с процентами
                sort_all_dict_skill = None
                for el in set_only_all_skills:  # берем один уникальный элемент
                    count_one_skill = only_all_skills.count(el)  # количество вхождений в общий список

                    #      percent_one_skill = (count_one_skill * 100) / count_list_all_skills  # процент от общего количества
                    #      percent_one_skill = round(percent_one_skill, 2)  # округлим до 2 знаков
                    dict_one_skill = dict([(el, count_one_skill)])
                    dict_all_skill.append(dict_one_skill)

                    def get_percent(element):
                        """
                        используется далее  в sorted
                        :param element:
                        :return:
                        """
                        for k, v in element.items():
                            return v

                    sort_all_dict_skill = sorted(dict_all_skill, key=get_percent, reverse=True)
                print(f'Рейтинг навыков  по  запросу {keyword} (первые 50): ')
                pprint.pprint(sort_all_dict_skill[0:50])
                answer = input('Сохранить данные в файл ? ("да" - "нет"): ')
                if answer == 'да':
                    with open('report_skill_rating', 'w') as f:
                        json.dump(sort_all_dict_skill, f)
                else:
                    print('Ладно, позже....')

            else:
                answer = input('Файл данных для анализа еще не создан, создать его ("да" - "нет?")')
                if answer == "да":
                    menu_parser()
        elif (choice == 'q') or (choice == 'й'):
             break
        else:
            print('Нераспознанная команда')
            print('Попробуйте вновь..')


if __name__ == "__main__":
    menu_parser()
