"""
Created on: see version log.
@author: RiGonz
coding: utf-8

The script obtains the urls for the flags of the world from the following sites:
- CF: https://github.com/hampusborgos/country-flags?tab=readme-ov-file
- EB: https://kids.britannica.com/students/article/flags-of-the-world/274335
- FB: https://www.cia.gov/the-world-factbook/references/flags-of-the-world/
- WK: https://en.m.wikipedia.org/wiki/List_of_national_flags_of_sovereign_states
- WO: https://www.worldometers.info/geography/flags-of-the-world/ + https://www.worldometers.info/geography/flags-of-dependent-territories/
and downloads the flags as image files.

Not used:
- https://flagpedia.net/index
- http://www.flags.net/

Version log:
R0 20250104
- first trials

TODO:
-

"""

# %% Import libraries.
from os import chdir, listdir, rename, remove
import requests
from random import choice
from bs4 import BeautifulSoup as bs
from time import sleep
import pycountry
import pandas as pd


# %% Local functions.
def f_show_progress(count, count_all, N=20):
    '''
    Shows the progress of an iteration.
    Returns: nothing; issues a printout with the progress.
    Uses: -
    '''
    N = min(N, count_all)
    if count % int(count_all / N) == 0:
        print('Progress {:4.1f}%'.format(count/count_all*100))
    return


# %% Common auxiliaries.
CWD = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/'
chdir(CWD)
del CWD

# %% Support variables.
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    ]

# %% Get data: CF.
url0 = 'https://github.com/CFusborgos/country-flags/archive/refs/heads/main.zip'
head = {'User-Agent': choice(user_agents)}
r = requests.get(url0, allow_redirects=True, headers=head)
if r.status_code != requests.codes.ok:
    print(f'Error opening page {url0}.')
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/CF/'
FileName = RootDir + 'CF.zip'
try:
    with open(FileName, 'wb') as f:
        f.write(r.content)
except:
    print('Error downloading file.')
del url0, head, r, RootDir, FileName, f

# Manually unzip and remove files of no interest.

# Capitalize, rename to ISO-3:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/CF/SVG/'
file_l = listdir(RootDir)
file_l = [x.split('.')[0].upper() for x in file_l]
for ctr in pycountry.countries:
    iso2 = ctr.alpha_2
    iso3 = ctr.alpha_3
    if iso2 in file_l:
        rename(RootDir + iso2 + '.svg', RootDir + iso3 + '.svg')
del RootDir, file_l, ctr, iso2, iso3

# Manually fix issues:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/CF/SVG/'
ctr_d = {'eu': 'EUR',
         'xk': 'XKX'}
for ctr in ctr_d.keys():
    rename(RootDir + ctr + '.svg', RootDir + ctr_d[ctr] + '.svg')
ctr_l = ['gb-eng', 'gb-nir', 'gb-sct', 'gb-wls']
for ctr in ctr_l:
    remove(RootDir + ctr + '.svg')
del RootDir, ctr_d, ctr_l, ctr

# %% Get data: EB.
# Get list of urls:
flag_l = []
url0 = 'https://kids.EBannica.com/students/article/flags-of-the-world/274335'
head = {'User-Agent': choice(user_agents)}
r = requests.get(url0, allow_redirects=True, headers=head)
if r.status_code != requests.codes.ok:
    print(f'Error opening page {url0}.')
soup = bs(r.text, 'lxml')
url_l = soup.find_all(class_="d-flex justify-content-center")
url0 = "https://kids.EBannica.com/"
for url in url_l:
    aux = url.find('a', href=True)
    flag_l.append((aux.find("img")['data-title'],
                   url0 + aux['href']))
del url0, r, soup, url_l, aux

# Open url and download flag:
err_l = []
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/'
for i, flag in enumerate(flag_l):
    r = requests.get(flag[1], allow_redirects=True, headers=head)
    if r.status_code != requests.codes.ok:
        print(f'Error opening page {flag}.')
        err_l.append(flag)
        continue
    soup = bs(r.text, 'lxml')
    try:
        url = soup.find(alt=flag[0])['src']
        r = requests.get(url, allow_redirects=True, headers=head)
        if r.status_code != requests.codes.ok:
            print(f'Error opening page {flag}.')
            err_l.append(flag)
            continue
        FileName = RootDir + flag[0] + '.jpg'
        with open(FileName, 'wb') as f:
            f.write(r.content)
    except:
        print(f'Error downloading page {flag}.')
        err_l.append(flag)
    sleep(1)
    f_show_progress(i, len(flag_l))
del head, RootDir, i, flag, r, soup, url, FileName, f

# Retry with errors:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/'
head = {'User-Agent': choice(user_agents)}
for i, flag in enumerate(err_l):
    r = requests.get(flag[1], allow_redirects=True, headers=head)
    if r.status_code != requests.codes.ok:
        print(f'Error opening page {flag}.')
        continue
    soup = bs(r.text, 'lxml')
    try:
        url = soup.find(alt=flag[0]+"\n")['src']
        r = requests.get(url, allow_redirects=True, headers=head)
        if r.status_code != requests.codes.ok:
            print(f'Error opening page {flag}.')
            continue
        FileName = RootDir + flag[0] + '.jpg'
        with open(FileName, 'wb') as f:
            f.write(r.content)
    except:
        print(f'Error downloading page {flag}.')
    sleep(2)
    f_show_progress(i, len(flag_l))
del head, RootDir, i, flag, r, soup, url, FileName, f
del flag_l

# Manually fix missing countries:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/'
head = {'User-Agent': choice(user_agents)}
err_l = [
    ('The Bahamas', 'https://cdn.EBannica.com/06/5106-004-B8EE9FD3.jpg'),
    ('United States', 'https://cdn.EBannica.com/33/4833-004-828A9A84.jpg'),
    ('Brazil', 'https://cdn.EBannica.com/47/6847-004-7D668BB0.jpg')]
for flag in err_l:
    r = requests.get(flag[1], allow_redirects=True, headers=head)
    if r.status_code != requests.codes.ok:
        print(f'Error opening page {flag}.')
        continue
    soup = bs(r.text, 'lxml')
    try:
        url = flag[1]
        FileName = RootDir + flag[0] + '.jpg'
        with open(FileName, 'wb') as f:
            f.write(r.content)
    except:
        print(f'Error downloading page {flag}.')
    sleep(1)
del RootDir, head, flag, r, soup, url, FileName, f
del err_l

# Manually fix wrong names:
err_d = {"Chad's flag": 'Chad',
         'flag of Costa Rica': 'Costa Rica',
         'Flag of India': 'India',
         'flag of Iraq': 'Iraq',
         'flag of Micronesia': 'Micronesia',
         'TMP': 'TLS',
         }
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/'
for key in err_d.keys():
    rename(RootDir + key + '.jpg', RootDir + err_d[key] + '.jpg')
del err_d, RootDir, key

# Change names to ISO3:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/'
file_l = listdir(RootDir)
file_l = [x.split('.')[0] for x in file_l]
for file in file_l:
    try:
        iso3 = pycountry.countries.search_fuzzy(file)[0].alpha_3
        if iso3 is not None:
            rename(RootDir + file + '.jpg', RootDir + iso3 + '.jpg')
    except:
        print(f'Error renaming {file}.')
del RootDir, file_l, file, iso3

# Manually fix some names:
err_d = {'Congo (Brazzaville)': 'COG',
         'Congo, Kinshasa': 'COD',
         'East Timor': 'TMP',
         'NGA': 'NER',
         'Nigeria': 'NGA',
         'SRB': 'XKX',
         'Serbia': 'SRB',
         'Turkey': 'TUR'}
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/'
for key in err_d.keys():
    rename(RootDir + key + '.jpg', RootDir + err_d[key] + '.jpg')
del err_d, RootDir, key

# %% Get data: CIA-FB.
# FIPS codes (https://github.com/datasets/country-codes):
RootDir = 'E:/2 EN/00 CIVIL/Normas Generales/International/Country Names/'
FileName = RootDir + 'CC1_country-codes.csv'
ctr_df = pd.read_csv(FileName, usecols=['CLDR display name', 'FIPS', 'ISO3166-1-Alpha-2', 'ISO3166-1-Alpha-3'])
ctr_df.columns = ['ISO3', 'FIPS', 'ISO2', 'NAME']
ctr_df.dropna(inplace=True)
ctr_df.drop(ctr_df[ctr_df['FIPS'].apply(lambda x: len(x) != 2)].index, inplace=True)
ctr_d = ctr_df.set_index('FIPS')['ISO3'].to_dict()
del RootDir, FileName
del ctr_df

RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/FB/JPG/'
head = {'User-Agent': choice(user_agents)}
url0 = 'https://www.cia.gov/the-world-factbook/about/archives/2024/static/flags/NNN-flag.jpg'
for i, ctr in enumerate(ctr_d.keys()):
    url = url0.replace('NNN', ctr)
    r = requests.get(url, allow_redirects=True, headers=head)
    if r.status_code != requests.codes.ok:
        print(f'Error opening country {ctr}.')
        continue
    FileName = RootDir + ctr_d[ctr] + '.jpg'
    try:
        with open(FileName, 'wb') as f:
            f.write(r.content)
    except:
        print(f'Error downloading country {ctr}.')
    sleep(1)
    f_show_progress(i, len(ctr_d))
del ctr_d, RootDir, head, url0, i, ctr, url, r, FileName, f

# %% Get data: WK.
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WK/SVG/'
head = {'User-Agent': choice(user_agents)}
url0 = 'https://en.m.WKpedia.org/WK/List_of_national_flags_of_sovereign_states'
r = requests.get(url0, allow_redirects=True, headers=head)
if r.status_code != requests.codes.ok:
    print('Error opening url0.')
soup = bs(r.text, 'lxml')
url_l = soup.find_all(class_="mw-default-size mw-halign-center")
url_l = ['https:' + url.find(class_="mw-file-element")['src'].replace('/thumb', '').split('/220px')[0] for url in url_l]
for i, url in enumerate(url_l):
    r = requests.get(url, allow_redirects=True, headers=head)
    if r.status_code != requests.codes.ok:
        print(f'Error opening {url}.')
        continue
    FileName = RootDir + url.split('Flag_of_')[-1]
    try:
        with open(FileName, 'wb') as f:
            f.write(r.content)
    except:
        print(f'Error downloading {url}.')
    sleep(1)
    f_show_progress(i, len(url_l))
del RootDir, head, url0, r, soup, url_l, i, url, FileName, f

# Manually fix some names:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WK/SVG/'
del_l = ['Austria_%28state%29.svg',
         'Costa_Rica.svg',
         'Paraguay_%28reverse%29.svg',
         'Peru.svg',
         'Venezuela_%28state%29.svg',
         'the_Taliban.svg']
for key in del_l:
    remove(RootDir + key)

ren_d = {'Afghanistan_%282013%E2%80%932021%29': 'Afghanistan',
         'Australia_%28converted%29': 'Australia',
         'Costa_Rica_%28state%29.svg': 'Costa Rica.svg',
         'Dominica_%28variant_6%29': 'Dominica',
         'Peru_%28state%29.svg': 'Peru.svg',
         'Syria_%282024%E2%80%93present%29': 'Syria',
         'Togo_%283-2%29': 'Togo',
         'Transnistria_%28state%29': 'Transnistria',
         'Vatican_City_%282023%E2%80%93present%29': 'Vatican',
         'C%C3%B4te_d%27Ivoire': "Côte d'Ivoire",
         'S%C3%A3o_Tom%C3%A9_and_Pr%C3%ADncipe': 'Sao Tome and Principe',
         'the_People%27s_Republic_of_China': 'China',
         'the_Republic_of_China': 'Taiwan',
         'Cape_Verde': 'Cabo Verde',
         'East_Timor': 'Timor-Leste',
         'the_Sahrawi_Arab_Democratic_Republic': 'Sahara',
         'Nigeria': 'NGA',
         'Niger': 'NER',
         'Kosovo': 'XKX',
         'the_Central_African_Republic': 'Central_African_Republic',
         'the_Czech_Republic': 'Czech_Republic',
         'the_Democratic_Republic_of_the_Congo': 'COD',
         'the_Dominican_Republic': 'Dominican_Republic',
         'the_Federated_States_of_Micronesia': 'Federated_States_of_Micronesia',
         'the_Republic_of_the_Congo': 'Republic_of_the_Congo',
         'the_Solomon_Islands': 'Solomon_Islands',
         'the_United_Arab_Emirates': 'United_Arab_Emirates',
         'the_United_Kingdom': 'United_Kingdom',
         'the_United_States': 'United_States',
         'Turkey': 'TUR',
         'the_Republic_of_Abkhazia': 'Abkhazia',
         'South_Ossetia': 'South Ossetia',
         'the_Turkish_Republic_of_Northern_Cyprus': 'Northern Cyprus',
         }
for key in ren_d.keys():
    rename(RootDir + key + '.svg', RootDir + ren_d[key] + '.svg')
del RootDir, del_l, key, ren_d

# Change names to ISO3:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WK/SVG/'
file_l = listdir(RootDir)
file_d = {x.split('.')[0]: x.split('.')[0].replace('_', ' ') for x in file_l}
for key in file_d.keys():
    try:
        iso3 = pycountry.countries.search_fuzzy(file_d[key])[0].alpha_3
        if iso3 is not None:
            rename(RootDir + key + '.svg', RootDir + iso3 + '.svg')
        else:
            print(f'Not found ISO3 for {key}.')
    except:
        print(f'Error renaming {key}.')
del RootDir, file_l, file_d, key, iso3

# %% Get data: WO.
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WO/GIF/'
head = {'User-Agent': choice(user_agents)}
url0 = 'https://www.worldometers.info/geography/flags-of-the-world/'
r = requests.get(url0, allow_redirects=True, headers=head)
if r.status_code != requests.codes.ok:
    print('Error opening url0.')
soup = bs(r.text, 'lxml')
url_l = soup.find_all(class_="col-md-4")
url0 = 'https://www.worldometers.info'
for i, url in enumerate(url_l[0:-1]):
    url = url.find('a')['href']
    try:
        r = requests.get(url0 + url, allow_redirects=True, headers=head)
        if r.status_code != requests.codes.ok:
            print(f'Error opening {url}.')
            continue
        FileName = RootDir + url.split('/')[-1].replace('-flag', '')
        with open(FileName, 'wb') as f:
            f.write(r.content)
    except:
        print(f'Error downloading {url}.')
    sleep(1)
    f_show_progress(i, len(url_l))
del RootDir, head, url0, r, soup, url_l, i, url, FileName, f

RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WO/GIF/'
head = {'User-Agent': choice(user_agents)}
url0 = 'https://www.worldometers.info/geography/flags-of-dependent-territories/'
r = requests.get(url0, allow_redirects=True, headers=head)
if r.status_code != requests.codes.ok:
    print('Error opening url0.')
soup = bs(r.text, 'lxml')
url_l = soup.find_all(class_="col-md-4")
url0 = 'https://www.worldometers.info'
for i, url in enumerate(url_l[0:-1]):
    url = url.find('a')['href']
    try:
        r = requests.get(url0 + url, allow_redirects=True, headers=head)
        if r.status_code != requests.codes.ok:
            print(f'Error opening {url}.')
            continue
        FileName = RootDir + url.split('/')[-1].replace('-flag', '')
        with open(FileName, 'wb') as f:
            f.write(r.content)
    except:
        print(f'Error downloading {url}.')
    sleep(1)
    f_show_progress(i, len(url_l))
del RootDir, head, url0, r, soup, url_l, i, url, FileName, f

# Capitalize, rename to ISO-3:
# FIPS codes (https://github.com/datasets/country-codes):
RootDir = 'E:/2 EN/00 CIVIL/Normas Generales/International/Country Names/'
FileName = RootDir + 'CC1_country-codes.csv'
ctr_df = pd.read_csv(FileName, usecols=['CLDR display name', 'FIPS', 'ISO3166-1-Alpha-2', 'ISO3166-1-Alpha-3'])
ctr_df.columns = ['ISO3', 'FIPS', 'ISO2', 'NAME']
ctr_df.dropna(inplace=True)
ctr_df.drop(ctr_df[ctr_df['FIPS'].apply(lambda x: len(x) != 2)].index, inplace=True)
ctr_d = ctr_df.set_index('FIPS')['ISO3'].to_dict()
del RootDir, FileName
del ctr_df

RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WO/GIF/'
file_l = listdir(RootDir)
file_l = [x.split('.')[0].upper() for x in file_l]
for ctr in file_l:
    if ctr not in ctr_d.keys():
        print(f'Error with code {ctr}.')
        continue
    iso3 = ctr_d[ctr]
    rename(RootDir + ctr + '.gif', RootDir + iso3 + '.gif')
del RootDir, file_l, ctr, iso3

# Manually fix pending names:
err_d = {'cc': 'CUW',
         # 'congo': 'COD',
         'palestine': 'PSE',
         'ri': 'SRB',
         'sk': 'SXM',
         'wa': 'NAM'}
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WO/GIF/'
for key in err_d.keys():
    rename(RootDir + key + '.gif', RootDir + err_d[key] + '.gif')
del err_d, RootDir, key

# %% Script done.
print('\a')
print('\nScript completed. Thanks!')
