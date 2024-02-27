import requests
import pprint

# Авторизация
import requests
import pprint

url = ''

token = 'MY_TOKEN'
# 1. auth

# result = requests.get(url, auth=('DanteOnline', token))

# 2. headers

# headers = {
#     'Authorization': f'token {token}'
# }
#
# result = requests.get(url, headers=headers)

# 3. session

session = requests.Session()
session.auth = ('DanteOnline', token)

# Поиск репозиториев
# url = 'https://api.github.com/search/repositories?q=tetris+language:assembly&sort=stars&order=desc'
#
# result = session.get(url)
#
# pprint.pprint(result.json())

# Поиск кода
# url = 'https://api.github.com/search/code?q=addClass+in:file+language:js+repo:jquery/jquery'
#
# result = session.get(url)
#
# pprint.pprint(result.json())


url = 'https://api.github.com/search/code?q=eval+in:file+language:python+user:DanteOnline'

result = session.get(url).json()

items = result['items']

for item in items:
    if not item['path'].startswith('venv'):
        pprint.pprint(item)