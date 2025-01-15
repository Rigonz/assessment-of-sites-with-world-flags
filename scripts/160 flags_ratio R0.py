"""
Created on: see version log.
@author: RiGonz
coding: utf-8

The script computes the size and aspect ratio of flags downloaded in #100, and
presents the results in charts.

Sources:
- CF: https://github.com/hampusborgos/country-flags?tab=readme-ov-file
- EB: https://kids.britannica.com/students/article/flags-of-the-world/274335
- FB: https://www.cia.gov/the-world-factbook/references/flags-of-the-world/
- WK: https://en.m.wikipedia.org/wiki/List_of_national_flags_of_sovereign_states
- WO: https://www.worldometers.info/geography/flags-of-the-world/ + https://www.worldometers.info/geography/flags-of-dependent-territories/

Version log:
R0 20250106
- first trials

TODO:
-

"""

# %% Import libraries.
from os import chdir, listdir
from bs4 import BeautifulSoup as bs
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt


# %% Local functions.

# %% Common auxiliaries.
CWD = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/'
chdir(CWD)
del CWD

# %% Support variables.

# %% Get data.
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
ctr_d = {}
for ctr in ctr_l:
    with open(RootDir + ctr, 'r') as f:
        data = f.read()
    svg = bs(data, "lxml")
    aux_l = svg.find('svg')['viewbox'].split(' ')
    ctr_d[ctr.split('.')[0]] = (float(aux_l[2]), float(aux_l[3]))
ctr_df['CF'] = ctr_d
aux_s = set(ctr_d.keys()).difference(ctr_df.index)
ctr_df.loc['XKX'] = ['Kosovo', ctr_d['XKX']]
ctr_df.loc['EUR'] = ['European Union', ctr_d['EUR']]
del RootDir, ctr_l, ctr_d, ctr, f, data, svg, aux_l, aux_s

# EB:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/'
ctr_l = listdir(RootDir)
ctr_d = {}
for ctr in ctr_l:
    img = Image.open(RootDir + ctr)
    ctr_d[ctr.split('.')[0]] = img.size
ctr_df['EB'] = ctr_d
del RootDir, ctr_l, ctr_d, ctr, img

# CIA-FB:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/FB/JPG/'
ctr_l = listdir(RootDir)
ctr_d = {}
for ctr in ctr_l:
    img = Image.open(RootDir + ctr)
    ctr_d[ctr.split('.')[0]] = img.size
ctr_df['FB'] = ctr_d
del RootDir, ctr_l, ctr_d, ctr, img

# WK:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WK/SVG/'
ctr_l = listdir(RootDir)
ctr_d = {}
for ctr in ctr_l:
    with open(RootDir + ctr, 'r') as f:
        data = f.read()
    svg = bs(data, "lxml")
    aux = svg.find('svg')
    try:
        aux_l = [aux['width'], aux['height']]
        ctr_d[ctr.split('.')[0]] = ((float(aux_l[0]),
                                     float(aux_l[1])))
    except:
        try:  # ',' not in aux['viewbox']
            aux_l = aux['viewbox'].split(' ')
            ctr_d[ctr.split('.')[0]] = (float(aux_l[2]), float(aux_l[3]))
        except:
            aux_l = aux['viewbox'].split(' ')[1].split(',')
            ctr_d[ctr.split('.')[0]] = (float(aux_l[0]), float(aux_l[1]))
ctr_df['WK'] = ctr_d
del RootDir, ctr_l, ctr_d, ctr, f, data, svg, aux_l

# WO:
RootDir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WO/GIF/'
ctr_l = listdir(RootDir)
ctr_d = {}
for ctr in ctr_l:
    img = Image.open(RootDir + ctr)
    ctr_d[ctr.split('.')[0]] = img.size
ctr_df['WO'] = ctr_d
del RootDir, ctr_l, ctr_d, ctr, img

# %% Widths.
# Data:
w_df = pd.DataFrame(data=None, index=ctr_df.index, columns=ctr_df.columns)
w_df['NAME'] = ctr_df['NAME']
for idx in w_df.index:
    for col in w_df.columns:
        if col == 'NAME':
            continue
        if ctr_df.loc[idx, col] == 9999:
            continue
        w_df.loc[idx, col] = ctr_df.loc[idx, col][0]
del idx, col

# Plot:
fig, ax = plt.subplots(dpi=300)
col_l = ['CF', 'EB', 'FB', 'WK', 'WO']
dif_l = [w_df[col].dropna(inplace=False) for col in col_l]
ax.set_ylabel('Width, pixels')
bplot = ax.boxplot(dif_l,
                   patch_artist=True,  # fill with color
                   tick_labels=col_l,  # will be used to label x-ticks
                   sym='+')
plt.setp(bplot['fliers'], markersize=2)
plt.ylim(0, 2000)
plt.grid()
plt.show()
del fig, ax, col_l, dif_l, bplot

del w_df

# %% Compute aspect ratio.
ctr_df.fillna(value=9999, inplace=True)
rat_df = pd.DataFrame(data=None, index=ctr_df.index, columns=ctr_df.columns)
rat_df['NAME'] = ctr_df['NAME']
for idx in rat_df.index:
    for col in rat_df.columns:
        if col == 'NAME':
            continue
        if ctr_df.loc[idx, col] == 9999:
            continue
        rat_df.loc[idx, col] = ctr_df.loc[idx, col][0] / ctr_df.loc[idx, col][1]
del idx, col

# Relative differences:
dif_df = pd.DataFrame(data=None, index=ctr_df.index, columns=ctr_df.columns)
dif_df['NAME'] = ctr_df['NAME']
for col in rat_df.columns:
    if col == 'NAME':
        continue
    dif_df[col] = (rat_df[col] - rat_df['CF']) / rat_df['CF']
del col

# %% Plots.
# Boxplot:
fig, ax = plt.subplots(dpi=300)
col_l = ['EB', 'FB', 'WK', 'WO']
dif_l = [dif_df[col].dropna(inplace=False) for col in col_l]
ax.set_ylabel('Relative Difference')
bplot = ax.boxplot(dif_l,
                   patch_artist=True,  # fill with color
                   tick_labels=col_l,  # will be used to label x-ticks
                   sym='+')
plt.setp(bplot['fliers'], markersize=2)
# plt.ylim(-.1, .1)
plt.grid()
plt.show()
del fig, ax, bplot

# Histogram:
n_bins = 20
plt.figure(dpi=300)
for k, dif in enumerate(dif_l):
    plt.hist(dif, n_bins,
             density=True, cumulative=True, histtype='step',
             label=col_l[k], alpha=0.8)
plt.legend()
plt.grid()
plt.xlabel('Relative Difference of Aspect Ratio (ref: Country-Flag)')
plt.ylabel('Cumulated Relative Frequency')
plt.show()
del n_bins, k, dif

del col_l, dif_l

# %% Script done.
print('\a')
print('\nScript completed. Thanks!')
