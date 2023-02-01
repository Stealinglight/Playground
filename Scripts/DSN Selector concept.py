## DSN Selector concept

import requests





proxies = [
    {'http': 'http://10.10.1.10:3128/'},
    {'http': 'http://10.10.2.10:3128/'},
    {'http': 'http://10.10.3.10:3128/'},
]

def choose_proxy():
    for i, proxy in enumerate(proxies):
        print(f'{i}: {proxy}')

    choice = int(input('Choose a proxy (0-2): '))
    selected_proxy = proxies[choice]
    return selected_proxy

selected_proxy = choose_proxy()
print(f'Selected proxy: {selected_proxy}')
