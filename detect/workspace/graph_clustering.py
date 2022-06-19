import os
import sys
import time
import random
import numpy as np
from collections import defaultdict
import operator
import networkx as nx
import community as community_louvain
import argparse
from pathlib import Path
import pickle

# Training settings
parser = argparse.ArgumentParser()
parser.add_argument('--datapath', type=str, default='../../crawled',
                    help='Crawled dataset path')
parser.add_argument('--lookup_path', type=str, default='../NEW-LOOKUP-GKGTHEMES.txt',
                    help='Path for summarized GKG supertheme text file')
parser.add_argument('--graph_path', type=str, default='./graph_reduced')
parser.add_argument('--output_path', type=str, default='./output_reduced')
parser.add_argument('--target_theme', type=str, default='PANDEMICS',
                    help='a target theme to find a cluster')

args = parser.parse_args()
Path(args.graph_path).mkdir(parents=True, exist_ok=True)

seed = 42
random.seed(seed)
np.random.seed(seed)

args.target_theme = args.target_theme.upper()

table = dict()
f = open(args.lookup_path, 'r')
for line in f.readlines():
    index, new_theme = line.strip().split(',')
    table[int(index)] = new_theme
f.close()

# paths = ['./graph_reduced/r_201908{:02d}.gkg.csv.txt'.format(day) for day in range(1,32)] +['./graph_reduced/r_201909{:02d}.gkg.csv.txt'.format(day) for day in range(1,31)] +['./graph_reduced/r_201910{:02d}.gkg.csv.txt'.format(day) for day in range(1,32)] +['./graph_reduced/r_201911{:02d}.gkg.csv.txt'.format(day) for day in range(1,31)] +['./graph_reduced/r_201912{:02d}.gkg.csv.txt'.format(day) for day in range(1,32)] +['./graph_reduced/r_202001{:02d}.gkg.csv.txt'.format(day) for day in range(1,32)] +['./graph_reduced/r_202002{:02d}.gkg.csv.txt'.format(day) for day in range(1,30)] +['./graph_reduced/r_202003{:02d}.gkg.csv.txt'.format(day) for day in range(1,32)]
paths = []
for x in Path(args.graph_path).iterdir():
    # print(x)/
    x = str(x)
    paths.append(x)
# print(paths)
paths = sorted(list(filter(lambda x: x.split(".")[-1] == 'txt', paths)))
# print(paths)

Path(args.output_path).mkdir(parents=True, exist_ok=True)
result_dict = {'date':[], 
               'top 10 node degree in summation':[], 'top 30 node degree in summation':[], 'top 50 node degree in summation':[], 'top 100 node degree in summation':[],
               'top 10 node degree out summation':[], 'top 30 node degree out summation':[], 'top 50 node degree out summation':[], 'top 100 node degree out summation':[],
               'top 10 node degree total summation':[], 'top 30 node degree total summation':[], 'top 50 node degree total summation':[], 'top 100 node degree total summation':[],
               '{:s} in degree'.format(args.target_theme):[], '{:s} out degree'.format(args.target_theme):[], '{:s} total degree'.format(args.target_theme):[],
               '{:s} in order'.format(args.target_theme):[], '{:s} out order'.format(args.target_theme):[], '{:s} total order'.format(args.target_theme):[]}


for path in paths:
    start = time.time()
    # date = path.replace('.txt', '')
    date = path.split('/')[-1].split('.')[0]
    sys.stdout = open(os.path.join(args.output_path, 'output{:s}.txt'.format(date)), 'w')
    
    '''
    First Louvain Clustering
    '''
    G1 = nx.Graph()
    with open(path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.split(',')
            G1.add_edge(str(line[0]), str(line[1]), weight=float(line[2]))
        f.close()
    
    # Louvain clustering
    partition1 = community_louvain.best_partition(G1, random_state=seed)
    
    partition_set = defaultdict(list)
    for key, value in partition1.items():
        partition_set[value].append(key)
    
    partition_set_gkg = defaultdict(list)
    for i in partition_set:
        for k in partition_set[i]:
            partition_set_gkg[i].append(table[int(k)])
    
    print('{:s} First Clustering Properties: '.format(path), '\n')
    for i in partition_set_gkg:
        print('{:d} Cluster\'s number of nodes: '.format(i), len(partition_set_gkg[i]))
        
    for cnum in partition_set_gkg:
        if args.target_theme in partition_set_gkg[cnum]:
            int_list = partition_set[cnum]
            theme_list = partition_set_gkg[cnum]
            print('Cluster {:d} will be used \n'.format(cnum))
        
    theme_graph = np.load('{}/theme_graph_{:s}.gkg.csv.npy'.format(args.graph_path, date))
    max__ = np.max(np.sum(theme_graph, axis=0))
    
    degree_dict = dict()
    for e, j in enumerate(int_list):
        weight = 0
        for k in int_list:
            weight += theme_graph[int(j)][int(k)] / max__
        degree_dict[theme_list[e]] = weight
    
    sorted_degree_dict = sorted(degree_dict.items(), key=operator.itemgetter(1), reverse=True)
    alpha_list = [10, 30, 50, 100]
    for alpha in alpha_list:
        sum_ = np.sum(sorted(degree_dict.values())[::-1][:alpha])
        print('{:s} Big {:d} node in-degree summation: '.format(date.replace('.gkg.csv', ''), alpha), sum_, '\n')
        print(sorted_degree_dict[:alpha], '\n')
    
    del partition_set, partition_set_gkg
    
    '''
    Second Louvain Clustering
    '''
    int_partition_set = [int(i) for i in int_list]
    G2 = nx.Graph()
    with open(path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.split(',')
            if int(line[0]) in int_partition_set and int(line[1]) in int_partition_set:
                G2.add_edge(str(line[0]), str(line[1]), weight=float(line[2]))
        f.close()
    
    # Louvain clustering
    partition2 = community_louvain.best_partition(G2, random_state=seed)
    
    partition_set = defaultdict(list)
    for key, value in partition2.items():
        partition_set[value].append(key)
    
    partition_set_gkg = defaultdict(list)
    for i in partition_set:
        for k in partition_set[i]:
            partition_set_gkg[i].append(table[int(k)])
            
    print('\n\n################ Second Clustering ################')
    print('{:s} Second Clustering Properties: '.format(path), '\n')
    for i in partition_set_gkg:
        print('{:d} Cluster\'s number of nodes: '.format(i), len(partition_set_gkg[i]))
    
    for cnum in partition_set_gkg:
        if args.target_theme in partition_set_gkg[cnum]:
            int_list = partition_set[cnum]
            theme_list = partition_set_gkg[cnum]
            print('Cluster {:d} will be used \n'.format(cnum))
        
    theme_graph = np.load('./graph_reduced/theme_graph_{:s}.gkg.csv.npy'.format(date))
    max__ = np.max(np.sum(theme_graph, axis=0))

    in_degree_dict, out_degree_dict, tot_degree_dict = dict(), dict(), dict()
    for e, j in enumerate(int_list):
        in_weight, out_weight, tot_weight = 0, 0, 0
        for k in int_partition_set:
            tot_weight += theme_graph[int(j)][int(k)] / max__
            if str(k) in int_list:
                in_weight += theme_graph[int(j)][int(k)] / max__
            else:
                out_weight += theme_graph[int(j)][int(k)] / max__
        in_degree_dict[theme_list[e]] = in_weight
        out_degree_dict[theme_list[e]] = out_weight
        tot_degree_dict[theme_list[e]] = tot_weight
        
    sorted_in_degree_dict = sorted(in_degree_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_out_degree_dict = sorted(out_degree_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_tot_degree_dict = sorted(tot_degree_dict.items(), key=operator.itemgetter(1), reverse=True)
    
    alpha_list = [10, 30, 50, 100]
    for alpha in alpha_list:
        in_sum_ = np.sum(sorted(in_degree_dict.values())[::-1][:alpha])
        out_sum_ = np.sum(sorted(out_degree_dict.values())[::-1][:alpha])
        tot_sum_ = np.sum(sorted(tot_degree_dict.values())[::-1][:alpha])
        
        result_dict[f'top {alpha} node degree in summation'].append(in_sum_)
        result_dict[f'top {alpha} node degree out summation'].append(out_sum_)
        result_dict[f'top {alpha} node degree total summation'].append(tot_sum_)
        print('{:s} Small {:d} node degree summation = in_sum: {:.6f}, out_sum: {:.6f}, total_sum: {:.6f} '.format(
              date.replace('.gkg.csv', ''), alpha, in_sum_, out_sum_, tot_sum_
              ), '\n')
        print(sorted_in_degree_dict[:alpha], '\n')
    
    result_dict['date'].append(date.replace('.gkg.csv', ''))
    for order, theme_deg in enumerate(sorted_in_degree_dict):
        if theme_deg[0] == args.target_theme:
            result_dict['{:s} in degree'.format(args.target_theme)].append(theme_deg[1])
            result_dict['{:s} in order'.format(args.target_theme)].append(order + 1)
    for order, theme_deg in enumerate(sorted_out_degree_dict):
        if theme_deg[0] == args.target_theme:
            result_dict['{:s} out degree'.format(args.target_theme)].append(theme_deg[1])
            result_dict['{:s} out order'.format(args.target_theme)].append(order + 1)
    for order, theme_deg in enumerate(sorted_tot_degree_dict):
        if theme_deg[0] == args.target_theme:
            result_dict['{:s} total degree'.format(args.target_theme)].append(theme_deg[1])
            result_dict['{:s} total order'.format(args.target_theme)].append(order + 1)
    
    sys.stdout.flush()
    end = time.time() - start

with open('./result_dict_{:s}.pkl'.format(args.target_theme), 'wb') as pkl:
    pickle.dump(result_dict, pkl)
