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
names = [playable[i] for i in range(0, len(playable), 5) if playable[i] != 'Traveler']
for name in names:
    response1 = requests.get(f'https://genshin-impact.fandom.com/wiki/{name}')
    yc_website1 = response1.text
    soup1 = BeautifulSoup(yc_website1, 'lxml')
    const = soup1.select('.tdc1 tbody tr td')
    const = [i.getText().replace('\n', '') for i in const if i.getText().replace('\n', '') != '']
    levels = [const[i] for i in range(0, len(const), 3)]
    const_names = [const[i] for i in range(1, len(const), 3)]
    const_effects = [const[i] for i in range(2, len(const), 3)]
    mat = soup1.select('.wikitable tbody tr td div div a')
    mat = [i.getText() for i in mat if i.getText() != '']
    mat1 = soup1.select('.card_font')
    mat1 = [i.getText() for i in mat1][:30]
    materials2 = []
    for i in range(len(mat)):
        material = f'{mat1[i]} {mat[i]}'
        materials2.append(material)
    materials1 = materials2[:8]
    materials1.append('')
    materials = materials1 + materials2[8:]
    talent_mat = materials[:7]
    ascension_mat = materials[7:]
    moras = ['20,000', '40,000', '60,000', '80,000', '100,000', '120,000']
    levels1 = ['20/40', '40/50', '50/60', '60/70', '70/80', '80/90']
    phases = ['1', '2', '3', '4', '5', '6']
    char_asc_mats1 = [ascension_mat[i] for i in range(0, len(ascension_mat), 4)]
    char_asc_mats2 = [ascension_mat[i] for i in range(1, len(ascension_mat), 4)]
    loc_specs = [ascension_mat[i] for i in range(2, len(ascension_mat), 4)]
    comm_mats = [ascension_mat[i] for i in range(3, len(ascension_mat), 4)]
    talents_levelup = [talent_mat[i] for i in range(3)]
    common_ascensions = [talent_mat[i] for i in range(6) if i >= 3]
    weekly_boss = []
    for i in range(7):
        if i == 6:
            weekly_boss.append(talent_mat[i])
            weekly_boss.append('')
            weekly_boss.append('')
    tal = soup1.select('.wikitable tbody tr td')
    tal = [i.getText().replace('\n', '') for i in tal if i.getText().replace('\n', '') != '']
    tal = tal[:18]
    name_talents = [tal[i] for i in range(0, len(tal), 3)]
    type_names = [tal[i] for i in range(1, len(tal), 3)]
    descriptions = [tal[i] for i in range(2, len(tal), 3)]
    data = {'Talent Name': name_talents, 'Type Name': type_names, 'Description': descriptions}
    df = pd.DataFrame(data)
    df.to_csv(f'./csv/characters/{name}_talents.csv', index=False)
    data = {'Talent Level-Up Materials': talents_levelup, 'Common Ascension Materials': common_ascensions,
            'Weekly Boss Materials': weekly_boss}
    df = pd.DataFrame(data)
    df.to_csv(f'./csv/characters/{name}_materials.csv', index=False)
    data = {'Level': levels, 'Name': const_names, 'Effect': const_effects}
    df = pd.DataFrame(data)
    df.to_csv(f'./csv/characters/{name}_constellation.csv', index=False)
    data = {'Ascension Phase': phases, 'Level': levels1, 'Mora': moras, 'Character Ascension Materials 1': char_asc_mats1,
            'Character Ascension Materials 2': char_asc_mats2, 'Local Specialities': loc_specs, 'Common Materials': comm_mats}
    df = pd.DataFrame(data)
    df.to_csv(f'./csv/characters/{name}_ascensions.csv', index=False)

