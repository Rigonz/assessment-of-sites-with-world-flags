"""
Created on: see version log.
@author: RiGonz
coding: utf-8

The script shows the flags downloaded in #100, grouped by country.

Sources:
- CF: https://github.com/hampusborgos/country-flags?tab=readme-ov-file
- EB: https://kids.britannica.com/students/article/flags-of-the-world/274335
- FB: https://www.cia.gov/the-world-factbook/references/flags-of-the-world/
- WK: https://en.m.wikipedia.org/wiki/List_of_national_flags_of_sovereign_states
- WO: https://www.worldometers.info/geography/flags-of-the-world/ + https://www.worldometers.info/geography/flags-of-dependent-territories/

Couldn't manage to show SVG files, so I (off-script, online) converted them to
PNG (100% quality, width=1000 px) with https://pixelied.com/convert/svg-converter/svg-to-png

Version log:
R0 20250107
- first trials

TODO:
-

"""

# %% Import libraries.
from os import chdir, listdir
import pandas as pd
import matplotlib.pyplot as plt


# %% Local functions.

# %% Common auxiliaries.
CWD = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/'
chdir(CWD)
del CWD

# %% Support variables.

# %% Identify flags.
# List of countries (FIPS codes, https://github.com/datasets/country-codes):
RootDir = 'E:/2 EN/00 CIVIL/Normas Generales/International/Country Names/'
FileName = RootDir + 'CC1_country-codes.csv'
ctr_df = pd.read_csv(FileName, usecols=['CLDR display name', 'ISO3166-1-Alpha-3'])
ctr_df.columns = ['ISO3', 'NAME']
ctr_df.dropna(inplace=True)
ctr_df.set_index('ISO3', inplace=True)
del RootDir, FileName

# CF:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/CF/SVG/'
ctr_l = listdir(RootDir)
ctr_d = {x.split('.')[0]: 1 for x in ctr_l}
ctr_df['CF'] = ctr_d
aux_s = set(ctr_d.keys()).difference(ctr_df.index)
# Inspect aux_s!
ctr_df.loc['XKX'] = ['Kosovo', 1]
ctr_df.loc['EUR'] = ['European Union', 1]
del RootDir, ctr_l, ctr_d, aux_s

# EB:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/'
ctr_l = listdir(RootDir)
ctr_d = {x.split('.')[0]: 1 for x in ctr_l}
ctr_df['EB'] = ctr_d
aux_s = set(ctr_d.keys()).difference(ctr_df.index)
# Inspect aux_s!
del RootDir, ctr_l, ctr_d, aux_s

# CIA-FB:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/FB/JPG/'
ctr_l = listdir(RootDir)
ctr_d = {x.split('.')[0]: 1 for x in ctr_l}
ctr_df['FB'] = ctr_d
aux_s = set(ctr_d.keys()).difference(ctr_df.index)
# Inspect aux_s!
del RootDir, ctr_l, ctr_d, aux_s

# WK:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WK/SVG/'
ctr_l = listdir(RootDir)
ctr_d = {x.split('.')[0]: 1 for x in ctr_l}
ctr_df['WK'] = ctr_d
aux_s = set(ctr_d.keys()).difference(ctr_df.index)
# Inspect aux_s!
del RootDir, ctr_l, ctr_d, aux_s

# WO:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WO/GIF/'
ctr_l = listdir(RootDir)
ctr_d = {x.split('.')[0]: 1 for x in ctr_l}
ctr_df['WO'] = ctr_d
aux_s = set(ctr_d.keys()).difference(ctr_df.index)
# Inspect aux_s!
del RootDir, ctr_l, ctr_d, aux_s

ctr_df.sort_index(inplace=True)
ctr_df.fillna(value=0, inplace=True)

# %% Plot by country.
root_l = ['E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/CF/PNG/',
          'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/',
          'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/FB/JPG/',
          'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WK/PNG/',
          'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WO/GIF/',
          ]
save_dir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/120PNG/'

for iso3 in ctr_df.index:
    nam = ctr_df.loc[iso3, 'NAME']
    src_l = ctr_df.loc[iso3].to_list()[1:]
    plt.figure(figsize=(9, 6))
    plt.title(f'{iso3}/{nam}', loc='right', size='xx-large',)  # c='red')
    plt.xticks([])
    plt.yticks([])
    # CF:
    if src_l[0] == 1:
        plt.subplot(231, autoscale_on=True)
        RootDir = root_l[0]
        FileName = RootDir + iso3 + '.png'
        img = plt.imread(FileName)
        plt.imshow(img)
        plt.plot([])
        plt.xticks([])
        plt.yticks([])
        plt.title('CF', loc='center')
    # EB:
    if src_l[1] == 1:
        plt.subplot(232, autoscale_on=True)
        RootDir = root_l[1]
        FileName = RootDir + iso3 + '.jpg'
        img = plt.imread(FileName)
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.title('EB', loc='center')
    # FB:
    if src_l[2] == 1:
        plt.subplot(233, autoscale_on=True)
        RootDir = root_l[2]
        FileName = RootDir + iso3 + '.jpg'
        img = plt.imread(FileName)
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.title('FB', loc='center')
    # WK:
    if src_l[3] == 1:
        plt.subplot(234, autoscale_on=True)
        RootDir = root_l[3]
        FileName = RootDir + iso3 + '.png'
        img = plt.imread(FileName)
        plt.imshow(img)
        plt.plot([])
        plt.xticks([])
        plt.yticks([])
        plt.title('WK', loc='center')
    # WO:
    if src_l[4] == 1:
        plt.subplot(236, autoscale_on=True)
        RootDir = root_l[4]
        FileName = RootDir + iso3 + '.gif'
        img = plt.imread(FileName)
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.title('WO', loc='center')
    # ALL:
    plt.savefig(save_dir + iso3 + '.png', dpi=300)
    plt.show()

    # _ = input('Enter to continue: ')
    print(f'{iso3} done!')

del root_l, save_dir, iso3, nam, src_l, RootDir, FileName, img

# %% Script done.
print('\a')
print('\nScript completed. Thanks!')
