import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get('https://genshin-impact.fandom.com/wiki/Characters')
yc_website = response.text
soup = BeautifulSoup(yc_website, 'lxml')
playable = soup.select('.article-table tbody tr td')[:260]
playable = [name.getText().replace('\n', '').strip() for name in playable if name.getText().replace('\n', '').strip() != '']
playable1 = playable[:144]
playable1.append('')
playable = playable1 + playable[144:]
names = [playable[i] for i in range(0, len(playable), 5)]
raritys = []
rar = soup.find_all('img')
for i in range(len(rar)):
    try:
        rar[i]['title']
    except KeyError:
        pass
    else:
        raritys.append(rar[i]['title'].split(' ')[0])
raritys = raritys[30:-1]
elements = [playable[i] for i in range(1, len(playable), 5)]
weapons = [playable[i] for i in range(2, len(playable), 5)]
sexs = [playable[i] for i in range(3, len(playable), 5)]
nations = [playable[i] for i in range(4, len(playable), 5)]
data = {'Name': names, 'Rarity': raritys, 'Element': elements, 'Weapon': weapons, 'Sex': sexs, 'Nation': nations}
df = pd.DataFrame(data)
df.to_csv('./csv/genshin_playable_characters.csv', index=False)





