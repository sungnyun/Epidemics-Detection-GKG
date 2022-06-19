import numpy as np
from tqdm import tqdm
from copy import deepcopy
import math
from glob import glob
import time
import argparse
from pathlib import Path

# Training settings
parser = argparse.ArgumentParser()
parser.add_argument('--datapath', type=str, default='../../crawled',
                    help='Crawled dataset path')
parser.add_argument('--load_lookup_path', type=str, default='../LOOKUP-GKGTHEMES.txt',
                    help='Path for original GKG theme text file')
parser.add_argument('--save_lookup_path', type=str, default='../NEW-LOOKUP-GKGTHEMES.txt',
                    help='Path for summarized GKG supertheme text file')
parser.add_argument('--save_graph_path', type=str, default='./graph_reduced')

args = parser.parse_args()
Path(args.save_graph_path).mkdir(parents=True, exist_ok=True)
###########################################################################################
##                            Summarize lookup gkg themes
###########################################################################################
lookup_file = open(args.load_lookup_path, 'r')
lookup_gkg_themes = []
theme2id = {}
for i, line in enumerate(lookup_file.readlines()):
    lookup_theme = line.strip().split('\t')[0]
    lookup_gkg_themes.append(lookup_theme)
    theme2id[lookup_theme] = i
lookup_file.close()

theme_dict = {}
id2theme = {}

for i, theme in enumerate(lookup_gkg_themes):
    split_theme = theme.split('_')
    
    if len(split_theme)==1:
        theme_dict[split_theme[0]] = [theme]
        id2theme[theme2id[theme]] = theme
        
    elif split_theme[1].isdigit():
        if split_theme[2] in theme_dict:
            theme_dict[split_theme[2]].append(theme)
        else:
            theme_dict[split_theme[2]] = [theme]
        id2theme[theme2id[theme]] = split_theme[2]
        
    else:
        if split_theme[1].isalpha():
            if split_theme[1] in theme_dict:
                theme_dict[split_theme[1]].append(theme)
            else:
                theme_dict[split_theme[1]] = [theme]
            id2theme[theme2id[theme]] = split_theme[1]

        else:
            if split_theme[0] in theme_dict:
                theme_dict[split_theme[0]].append(theme)
            else:
                theme_dict[split_theme[0]] = [theme]
            id2theme[theme2id[theme]] = split_theme[0]

theme_count = {}
new_theme2id = {}
for i, key in enumerate(theme_dict.keys()):
    theme_count[key] = len(theme_dict[key])
    new_theme2id[key] = i

count = 0
for key in theme_count:
    if theme_count[key] > 100:
        print(key, theme_count[key])
        count += theme_count[key]

# print(count)
# print(len(lookup_gkg_themes))
# print(len(theme_dict))
# print(theme_dict['FNCACT'])

###########################################################################################
##                         Write summarized lookup gkg superthemes
###########################################################################################
new_lookup_file = open(args.save_lookup_path, 'w+')
i = 0
for k in theme_dict:
    new_lookup_file.write(f'{i},{k}\n')
    i += 1
new_lookup_file.close()

###########################################################################################
##                      Load crawled dataset and construct theme graph
###########################################################################################
# path = ['raw/202107{:02d}.gkg.csv'.format(day) for day in range(1,32)] +       ['raw/202108{:02d}.gkg.csv'.format(day) for day in range(1,32)] +       ['raw/202109{:02d}.gkg.csv'.format(day) for day in range(1,31)] +       ['raw/202110{:02d}.gkg.csv'.format(day) for day in range(1,32)] +       ['raw/202111{:02d}.gkg.csv'.format(day) for day in range(1,31)] +       ['raw/202112{:02d}.gkg.csv'.format(day) for day in range(1,32)] +       ['raw/202201{:02d}.gkg.csv'.format(day) for day in range(1,32)] +       ['raw/202202{:02d}.gkg.csv'.format(day) for day in range(1,29)]
path = []
for x in Path(args.datapath).iterdir():
    x = str(x.stem)
    path.append(x)
path = list(filter(lambda x: x.split(".")[-1] == 'csv', path))
themes_not_in_lookup = []

for e, t in enumerate(path):
    start = time.time()
    theme_graph = np.zeros([len(theme_dict), len(theme_dict)])
    try:
        file = open(f'{args.datapath}/{t}', 'r')
    except:
        continue
    for i, line in enumerate(file.readlines()):
        if i == 0:
            continue
            
        news_themes = line.strip().split('\t')[3].rstrip(';').split(';')
        themes_lst = []
        for theme in news_themes:
            if not theme:
                continue
            if theme not in lookup_gkg_themes:
                themes_not_in_lookup.append(theme)
                continue
            theme_ = id2theme[theme2id[theme]]
            if theme_ not in themes_lst:
                themes_lst.append(theme_)
            
        for theme1 in themes_lst:
            for theme2 in themes_lst:
                if theme1 != theme2:
                    theme_graph[new_theme2id[theme1], new_theme2id[theme2]] += 1
                        
    # way = t.split('/')[1]

    np.save(f'{args.save_graph_path}/theme_graph_{t}', theme_graph)
    max_ = np.sum(theme_graph, axis = 0)
    max__ = np.max(max_)
    end = time.time() - start
    print(end, t)
    
    graph = open(f'{args.save_graph_path}/{t}.txt', 'w')
    for i in range(len(theme_dict)):
        for j in range(len(theme_dict)):
            if j > i and int(theme_graph[i][j]) != 0:
                graph.write(f'{i},{j},{theme_graph[i][j]/max__}\n')
    graph.close()

