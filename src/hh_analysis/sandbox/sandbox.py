#%%
import requests

r = requests.get("https://api.hh.ru/areas")
print(r.request.headers)
print(r.request)

#%%
import requests
""" Пример запроса ключевых слов поиска"""
#https://api.hh.ru/suggests/vacancy_search_keyword?text=python
url = "https://api.hh.ru/suggests/vacancy_search_keyword"

params = {
    "text": "python"
}

#headers = {
#    "User-Agent": "hh-analysis/1.0 (your_email@example.com)"
#}

response = requests.get(url, params=params) #, headers=headers)

print(response.status_code)
print(response.json())

#%%

from hh_analysis.api.hh_client import get_vacancy_detail

data = get_vacancy_detail(131646127)

print(data["id"])
print(data["name"])
print(data.get("key_skills"))