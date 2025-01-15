"""
Created on: see version log.
@author: RiGonz
coding: utf-8

The script analyzes the distribution of colors of the flags downloaded in #100,
and grahically presents the results.

Sources:
- CF: https://github.com/hampusborgos/country-flags?tab=readme-ov-file
- EB: https://kids.britannica.com/students/article/flags-of-the-world/274335
- FB: https://www.cia.gov/the-world-factbook/references/flags-of-the-world/
- WK: https://en.m.wikipedia.org/wiki/List_of_national_flags_of_sovereign_states
- WO: https://www.worldometers.info/geography/flags-of-the-world/ + https://www.worldometers.info/geography/flags-of-dependent-territories/

Version log:
R0 20250109
- first trials

TODO:
-

"""

# %% Import libraries.
from os import chdir, listdir
from PIL import Image
import pandas as pd
from collections import Counter

import matplotlib.pyplot as plt
from numpy.linalg import norm
from numpy import array


# %% Local functions.

# %% Common auxiliaries.
CWD = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/'
chdir(CWD)
del CWD

# %% Support variables.
src_d = {
    'CF': 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/CF/PNG/',
    'EB': 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/EB/JPG/',
    'FB': 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/FB/JPG/',
    'WK': 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WK/PNG/',
    'WO': 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/WO/GIF/'
    }

src_l = list(src_d.keys())

# %% Get list of flags.
# List of countries (FIPS codes, https://github.com/datasets/country-codes):
RootDir = 'E:/2 EN/00 CIVIL/Normas Generales/International/Country Names/'
FileName = RootDir + 'CC1_country-codes.csv'
ctr_df = pd.read_csv(FileName, usecols=['CLDR display name', 'ISO3166-1-Alpha-3'])
ctr_df.columns = ['ISO3', 'NAME']
ctr_df.dropna(inplace=True)
ctr_df.set_index('ISO3', inplace=True)
del RootDir, FileName

for src in src_d.keys():
    RootDir = src_d[src]
    ctr_l = listdir(RootDir)
    ctr_d = {x.split('.')[0]: 1 for x in ctr_l}
    ctr_df[src] = ctr_d
    if src == 'CF':
        ctr_df.loc['XKX'] = ['Kosovo', 1]
        ctr_df.loc['EUR'] = ['European Union', 1]

ctr_df.sort_index(inplace=True)
ctr_df.fillna(value=0, inplace=True)

del src, RootDir, ctr_l, ctr_d

# %% Extract color distribution. Plot sources together.
col_l = ['red', 'green', 'blue', 'k']
save_dir = 'E:/0 DOWN/00 PY RG/HTML/FLAGS/IO DATA/180PNG/'
err_d = {}

for iso3 in ctr_df.index:
    # Retrieve data:
    img_l = []
    for j, val in enumerate([int(x) for x in ctr_df.loc[iso3].to_list()[1:]]):
        if val == 0:
            img_l.append(None)
        else:
            RootDir = src_d[src_l[j]]
            ext = RootDir.split('/')[-2].lower()
            img = Image.open(RootDir + iso3 + '.' + ext)
            img = img.convert('RGBA')
            aux_l = [(x[0], x[1], x[2]) for x in list(img.getdata())]  # remove alpha
            img_l.append(Counter(aux_l))
    del j, val, RootDir, ext, img, aux_l

    # Plot:
    fig = plt.figure(dpi=300)
    fig.set_figheight(4)
    fig.set_figwidth(9)

    # 1st plot, all sources together:
    ax1 = plt.subplot2grid(shape=(1, 9), loc=(0, 0), colspan=5, projection='3d')
    for img_c in img_l:
        if img_c is None:
            continue
        img_df = pd.DataFrame.from_dict(img_c, orient='index', columns=['FR'])
        img_df.reset_index(drop=False, inplace=True)
        img_df['FR'] = img_df['FR'] / img_df['FR'].sum()
        img_df['R'] = img_df['index'].apply(lambda x: x[0])
        img_df['G'] = img_df['index'].apply(lambda x: x[1])
        img_df['B'] = img_df['index'].apply(lambda x: x[2])
        img_df['RGB'] = img_df['index'].apply(lambda x: (x[0]/255, x[1]/255, x[2]/255))
        img_df.drop(columns=['index'], inplace=True)
        ax1.scatter(img_df['R'], img_df['G'], img_df['B'],
                    s=img_df['FR']*1000,
                    c=img_df['RGB'],
                    alpha=0.8)
    ax1.set_xlabel('R', color='red')
    ax1.set_ylabel('G', color='green')
    ax1.set_zlabel('B', color='blue')
    ax1.set_xticks(range(0, 255, 50))
    ax1.set_yticks(range(0, 255, 50))
    ax1.set_zticks(range(0, 255, 50))
    ax1.set_xticklabels(range(0, 255, 50), color='red', size=8)
    ax1.set_yticklabels(range(0, 255, 50), color='green', size=8)
    ax1.set_zticklabels(range(0, 255, 50), color='blue', size=8)
    ax1.set_xlim(0, 255)
    ax1.set_ylim(0, 255)
    ax1.set_zlim(0, 255)
    ax1.set_title('FREQ', loc='right', fontsize=8)
    del img_c, img_df

    # 2nd plot, compute error/difference.
    # Use HAMP as ref:
    img_df = pd.DataFrame.from_dict(img_l[0], orient='index', columns=['FR'])
    img_df.reset_index(drop=False, inplace=True)
    img_df['FR'] = img_df['FR'] / img_df['FR'].sum()
    img_df['R'] = img_df['index'].apply(lambda x: x[0])
    img_df['G'] = img_df['index'].apply(lambda x: x[1])
    img_df['B'] = img_df['index'].apply(lambda x: x[2])
    img_df.drop(columns=['index'], inplace=True)
    aux_l = []
    for col in ['R', 'G', 'B']:
        aux_l.append([img_df[img_df[col] <= x]['FR'].sum() for x in range(0, 255+1)])
    cfd0_a = array(aux_l)
    err_l = [[0., 0., 0., 0.]]  # Differential error in channels RGB + total
    # Other sources:
    for img_c in img_l[1:]:
        if img_c is None:
            err_l.append(None)
            continue
        img_df = pd.DataFrame.from_dict(img_c, orient='index', columns=['FR'])
        img_df.reset_index(drop=False, inplace=True)
        img_df['FR'] = img_df['FR'] / img_df['FR'].sum()
        img_df['R'] = img_df['index'].apply(lambda x: x[0])
        img_df['G'] = img_df['index'].apply(lambda x: x[1])
        img_df['B'] = img_df['index'].apply(lambda x: x[2])
        img_df.drop(columns=['index'], inplace=True)
        aux_l = []
        for col in ['R', 'G', 'B']:
            aux_l.append([img_df[img_df[col] <= x]['FR'].sum() for x in range(0, 255+1)])
        cfd_a = array(aux_l)
        aux_l = []
        for i in range(len(cfd_a)):
            aux_l.append(norm(cfd0_a[i] - cfd_a[i]) / 256)  # 256 is max.error
        aux_l.append(sum(aux_l))
        err_l.append(aux_l)
        del cfd_a
    # 2nd plot:
    ax2 = plt.subplot2grid(shape=(1, 9), loc=(0, 6), colspan=3)
    for i, err in enumerate(err_l):
        if err is None:
            ax2.scatter(src_l[i], 0, s=0)
        else:
            for j, val in enumerate(err):
                ax2.scatter(src_l[i], val, s=14, c=col_l[j])
    ax2.set_title('ERR', loc='right', fontsize=8)
    ax2.tick_params(axis='both', labelsize=8)
    ax2.grid()
    del img_df, aux_l, col, cfd0_a, img_c, i, err, j, val

    fig.suptitle(f'{iso3}', x=0.88)
    # fig.tight_layout()
    plt.savefig(save_dir + iso3 + '.png', dpi=300)
    plt.show()

    err_d[iso3] = err_l
    del img_l, fig, ax1, ax2, err_l

    # _ = input('Enter to continue: ')
    print(f'{iso3} done!')

del iso3, col_l, save_dir

# %% Analysis of errors.
# Total:
k = 3
y_l = []
for i in range(5):
    y_l.append([(-1 if x[i] is None else x[i][k]) for x in err_d.values()])
del k, i

plt.figure(dpi=200)
for i in [1, 3, 4]:
    plt.scatter(y_l[2], y_l[i], s=4, label=src_l[i])
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.xlabel('ERR_FB')
plt.ylabel('ERR')
plt.legend(fontsize=8)
plt.grid()
plt.show()
del i

# Total cumulated:
plt.figure(dpi=200)
for i in [1, 2, 3, 4]:
    aux_l = y_l[i].copy()
    aux_l = sorted([y for y in aux_l if y >= 0])
    plt.plot(aux_l, range(len(aux_l)), linewidth=1, label=src_l[i])
plt.xlabel('Total Error')
plt.ylabel('Cumulated Count')
plt.legend(fontsize=8)
plt.grid()
plt.show()
del i, aux_l

# %% Script done.
print('\a')
print('\nScript completed. Thanks!')
