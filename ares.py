import requests
import pprint

DOMAIN = 'https://api.hh.ru/'  # domain HeadHanter

url_vacancies = f'{DOMAIN}vacancies'  # поиск вакансий


def country_url_id(country: str) -> tuple:
    """
    Поиск id страны
    :param country:
    :return: country_url, country_url
    """
    url_countries = f'{DOMAIN}areas/countries'
    response = requests.get(url_countries).json()  # => class 'list',
    # [{'id': '113', 'name': 'Россия', 'url': 'https://api.hh.ru/areas/113'}]
    for el in response:
        if el['name'] == country:  # el == dict
            country_url: str = el['url']  # url страны
            country_id: str = el['id']  # id страны
            return country_id, country_url


def country_region(country_url: str, area: str) -> tuple:
    """
    Поиск id региона  страны
    :param area:
    :param country_url:
    :return: 'id' и 'url' региона страны
    """
    response = requests.get(country_url).json()  # => class 'dict'

    for region in response['areas']:
        if region['name'] == area:
            region_id = region['id']
            region_url: str = f'{DOMAIN}areas/{region_id}'
            return region_id, region_url


def region_locality(region_url: str, locality_name: str) -> str:
    """
    Поиск id населенного пункта
    :param region_url:
    :return:url населенного пункта
    """
    response = requests.get(region_url).json()
    locality_dict = response['areas']  # => class 'list'\
    # [{'areas': [], 'id': '8997', 'name': 'Сарана', 'parent_id': '1261'}]

    for el in locality_dict:
        if el['name'] == locality_name:
            locality_id = el['id']
            # locality_url: str = f'{DOMAIN}areas/{locality_id}'
            return locality_id


def separator(symbol: str, multipl: int) -> str:
    """
    Сепаратор для оформления меню
    :param symbol: любой символ
    :param multipl: коэффициент размножения
    :return: строка из символов
    """
    return symbol * multipl


def vacancies_seach(profession):
    """
    дополняет наименование искомой вакансии '*' для  поиска по части строки
    :param profession:
    :return: f'{profession}*'
    """
    return f'{profession}'


vacancies_messege = """Введите искомую вакансию,
затем определите область поиска:"""

menu_messege = """\t\tМЕНЮ поля поиска:
1. Поиск по стране:
2. Поиск по региону страны:
3. Поиск по населенному  пункту:
4. Выход из программы: 'q' """


def menu_seach_area() -> str:
    """
    Меню для определения поля поиска, его сужения
    :return: "point" значение ключа "area"
    """
    # choice = ""
    while True:

        print(separator('*', 35))
        print(menu_messege)
        print(separator('*', 35))

        choice = input('Введите номер пункта меню: ')

        if choice == '1':
            country = input('Введите название страны: ')
            country_id, country_url = country_url_id(country)
            point = country_id
            return point
        elif choice == '2':
            country = input('Введите название страны: ')
            country_id, country_url = country_url_id(country)
            #создается файл со всеми регионами и
            area = input('Введите название региона: ')
            region_id, region_url = country_region(country_url, area)
            point = region_id
            return point
        elif choice == '3':
            country = input('Введите название страны: ')
            country_id, country_url = country_url_id(country)
            area = input('Введите название региона: ')
            region_id, region_url = country_region(country_url, area)
            locality_name = input('Введите название населенного пункта: ')
            point = region_locality(region_url, locality_name)
            return point
        elif choice == 'q' or choice == 'й':
            break
        else:
            print('Нераспознанная команда')
            print('Попробуйте вновь..')


def seach_parametrs(profession, point, page=0):
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


def menu_seach_parametrs():
    """
    Меню для вызова seach_parametrs() с параметрами
    :return: params
    """
    print(separator('*', 35))
    print(vacancies_messege)
    print(separator('*', 35))

    profession = input('Введите искомую вакансию: ')
    profession = vacancies_seach(profession)  # параметр profession

    point = menu_seach_area()  # параметр point

    params = seach_parametrs(profession, point)
    return params, profession, point


if __name__ == "__main__":
