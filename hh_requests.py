import pprint
import numpy as np
import requests
from areas import separator, seach_parametrs
from areas import url_vacancies
from areas import menu_seach_parametrs, menu_parser







# list_name_vacancies = []
# for vacancy in list_vacancies:
#     list_name_vacancies.append(vacancy['name'])
# set_name_vacancies = set(list_name_vacancies)
# print(f'*** Перечень наименований вакансий ***')
# print(f'Всего наименований вакансий: {len(set_name_vacancies)}')
# i = 1
# for name_vacancy in set_name_vacancies:
#     print(f'{i}. {name_vacancy}')
#     i += 1


# расчет средних зарплат

# list_salary_vacancies = []
#
# for vacancy in list_vacancies:
#     list_salary_vacancies.append(vacancy['salary'])
#
# print(f'*** Перечень зарплат вакансий ***')
#
# list_salary_from = []
# list_salary_to = []
# for salary_vacancy in list_salary_vacancies:
#
#     if salary_vacancy != None:
#         #print(f'{i}. {salary_vacancy}')
#         if salary_vacancy['from'] != None:
#             salary_from = int(salary_vacancy['from'])
#             list_salary_from.append(salary_from)
#             #print(f'Максимальна зарплата: {salary_from}')
#
#         if salary_vacancy['to'] != None:
#             salary_to = int(salary_vacancy['to'])
#             list_salary_to.append(salary_to)
#             #print(f'Минимальна зарплата: {salary_to}')
#         else:
#             salary_to = 0
#             #print(f'Минимальна зарплата не указана')
#         #i += 1
# mean_salary_from = int(np.mean(list_salary_from))
# mean_salary_to = int(np.mean(list_salary_to))
# print(f'*** Средня минимальна зарплата "{keywords}":  {mean_salary_from} RUR ***')
# print(f'*** Средняя максимальна зарплата "{keywords}": {mean_salary_to} RUR ***')


list_skills_vacancies = []  # все скилы с повторами, куча
# по url вакансии получаем все скилы с повторами одним списком
for vacancy in list_vacancies:
    url_one_vacancy = vacancy['url']
    one_vacancy = requests.get(url_one_vacancy).json()
    skills_one_vacancy = one_vacancy.get('key_skills', 'Ключ отсутствует')
    if skills_one_vacancy != [] and skills_one_vacancy != 'Ключ отсутствует':
        for name_skill_one_vacancy in skills_one_vacancy:
            list_skills_vacancies.append(name_skill_one_vacancy['name'])

set_skills_vacancies = set(list_skills_vacancies)  # скилы  без повторов
count_all_skills = len(set_skills_vacancies)  # общее количество скилов  без повторов

dict_all_skill = []  # список словарей скилов с процентами

for el in set_skills_vacancies:  # берем один уникальный элемент
    count_one_skill = list_skills_vacancies.count(el)  # количество  уникальных  элементов в list_skills_vacancies

    percent_one_skill = (count_one_skill * 100) / count_all_skills  # процент от общего количества
    percent_one_skill = round(percent_one_skill, 2)  # округлим до 2 знаков
    dict_one_skill = dict([(el, percent_one_skill)])
    dict_all_skill.append(dict_one_skill)



def get_percent(element):
    for k, v in element.items():
        return v

sort_all_dict_skill = sorted(dict_all_skill, key=get_percent, reverse=True)
print(sort_all_dict_skill)
