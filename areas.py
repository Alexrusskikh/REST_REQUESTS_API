import requests
import json
import os
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
    дополняет наименование искомой вакансии '*' для  поиска по части строки
    :param profession:
    :return: f'{profession}*'
    """
    return f'{profession}'


vacancies_messege = """Введите искомую вакансию,
затем определите область поиска:"""

menu_messege = """\t\tМЕНЮ:
1.Создать поисковый запрос и сохранить данные в файл.
2. Создать отчет и записать в файл.
3. Открыть файл отчета
'q' - Выход из программы - 'q' """




def search_parametrs(profession, point, page=0):
    """
    Создает params для GET запроса
    :param profession: 'искомая вакансия*'
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
                    #print(f'Вы выбрали поиск: {name_locality}, {name_locality_id}')
                    return name_locality_id



def menu_search_parametrs():
    """
    Сождает параметры запроса GET
    Меню для вызова search_parametrs() с параметрами
    :return: params
    """
    print(separator('*', 35))
    print(vacancies_messege)
    print(separator('*', 35))

    profession = input('Введите искомую вакансию: ')
    profession = vacancies_search(profession)  # параметр profession

    #определение региона поиска

    country = input('В какой стране провести поиск?: ')
    all_locality = get_country_area_locality(country)#список всех id страны
    locality_area = input('Сузить поле поиска("да" - "нет")?: ')
    point = search_area(locality_area, all_locality, country)
    params = search_parametrs(profession, point)
    return params

def list_all_vacancies(profession, point, pages):
            list_vacancies = []  # все вакансии по  запросу
            for page in range(pages):
                params = search_parametrs(profession, point, page)

                result = requests.get(url_vacancies, params=params)
                data = result.json()
                list_page = data['items']
                list_vacancies.extend(list_page)
            return list_vacancies


def menu_parser():
    """
    Меню функци  парсера
    :return:
    """
    choice = ""
    while True:

        print(separator('*', 35))
        print(menu_messege)
        print(separator('*', 35))

        choice = input('Введите номер пункта меню: ')

        if choice == '1':
            params = menu_search_parametrs()
            keywords = params['text']
            profession = params['text']
            point = params['area']
            print('!!!!!  Поисковый запрос сформирован  !!!!!')
            print(input('!!!!!  Введите для продолжения Enter  !!!!!'))

            result = requests.get(url_vacancies, params=params)
            #первый запрос  нужен для определения количества  возвращаемых страниц

            print(separator('@@@@@@@@@@@@@', 2))
            print(f'\tStatus_code: {result.status_code}')
            print(separator('@@@@@@@@@@@@@', 2))
            print()
            data = result.json()
            pages = data['pages']
            found_vacancies = data['found']
            print(f'*** По запросу "{keywords}" найдено вакансий: {found_vacancies}  ***')

            all_vacancies_list = list_all_vacancies(profession, point, pages)

            with open('get_vacancies.json', 'w') as f:
                json.dump(all_vacancies_list, f)




        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == 'q' or choice == 'й':
            break
        else:
            print('Нераспознанная команда')
            print('Попробуйте вновь..')


if __name__ == "__main__":
    menu_parser()


