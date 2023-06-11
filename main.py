import requests
import bs4
from fake_headers import Headers
import json

vacancy_table = []

def finder(vacancy_list_tag):
    for vacancy in vacancy_list_tag:
        vacancy_title_tag = vacancy.find('a', class_='serp-item__title')
        vacancy_title = vacancy_title_tag.text
        link = vacancy.find('a')['href']
        salary = vacancy.find('span', {'data-qa':"vacancy-serp__vacancy-compensation"})
        if salary != None:
            salary = salary.text.replace('\u202f', ' ')
        company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', ' ')
        city = vacancy.find('div', {'data-qa':'vacancy-serp__vacancy-address'}).text
        vacancy_table.append(
            {
            'Вакансия:' : vacancy_title,
            'Компания:' : company,
            'Зарплата:' : salary,
            'Ссылка:': link,
            'Город:': city
        }
        )
    return vacancy_table

def saver_to_json(file):
    with open('vacancy.json', 'w', encoding='utf-8') as v:
        json.dump(file, v, ensure_ascii=False, indent=4, sort_keys=True)

def main():
    max_pages = 5
    url = 'https://hh.ru/search/vacancy?text=python+django+flask&area=1&area=2&page='
    for p in range(max_pages):
        cur_url = url + str(p + 1)
        headers = Headers(browser='chrome', os='win')
        headers_data = headers.generate()
        search_page = requests.get(cur_url, headers=headers_data).text
        search_page_soup = bs4.BeautifulSoup(search_page, features='lxml')
        vacancy_list_tag = search_page_soup.find_all('div', class_='vacancy-serp-item__layout')
        vacancy_file = finder(vacancy_list_tag)
    saver_to_json(vacancy_file)

if __name__ == '__main__':
    main()



