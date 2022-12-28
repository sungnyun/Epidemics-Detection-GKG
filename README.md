# Epidemics Detection with GKG Dataset



This repository contains the official implementation of the following paper:
> **Real-time and Explainable Detection of Epidemics with Global News Data** by
> Sungnyun Kim*, Jaewoo Shin*, Seongha Eom, Jihwan Oh, and Se-Young Yun, [ICML Workshop on Healthcare AI and COVID-19](https://healthcare-ai-covid19.github.io/), 2022.
> 
> **Paper**: https://proceedings.mlr.press/v184/kim22a
>
> **Abstract:** *Monitoring and detecting epidemics are essential for protecting humanity from extreme harm. However, it must be done in real time for accurate epidemic detection to use limited resources efficiently and save time preventing the spread. Nevertheless, previous studies have focused on predicting the number of confirmed cases after the disease has already spread or when the relevant data are provided. Moreover, it is difficult to give the reason for predictions made using existing methods. In this study, we investigated how to detect and alert infectious diseases that might develop into pandemics soon, even before the information about a specific disease is aggregated. We propose an explainable method to detect an epidemic. This method uses only global news data, which are easily accessible in real time. Hence, we convert the news data to a graph form and cluster the news themes to curate and extract relevant information. The experiments on previous epidemics, including COVID-19, show that our approach allows the explainable real-time prediction of an epidemic disease and guides decision-making for prevention.*

<p align="center">
  <img src=https://user-images.githubusercontent.com/46050900/209757585-89f26258-01ed-4f4f-b1da-31812136b09e.png width="450">    
</p>

# Getting Started

This repo works in `Python>=3.6`.    
Install Python packages by `pip install -r requirements.txt`.

### 1. Go to workspace directory and run bash file
This will download raw dataset and unzip all.    
Be aware that you have to input by month.
```sh
cd detect/workspace
bash crawl.sh
Enter a start date: 20210701
You entered 20210701
Enter a end date: 20210731
You entered 20210731
20210701
--2022-05-31 17:21:09--  http://data.gdeltproject.org/gkg/20210701.gkg.csv.zip
...
```

### 2. Extract superthemes
```sh
python graph_generation.py --datapath='../../crawled' --load_lookup_path='../LOOKUP-GKGTHEMES.txt' --save_lookup_path='../NEW-LOOKUP-GKGTHEMES.txt' --save_graph_path='./graph_reduced'
```
Check output files in `./graph_reduced` directory.

### 3. Implement Louvain clustering
```sh
python graph_clustering.py --datapath='../../crawled' --lookup_path='../NEW-LOOKUP-GKGTHEMES.txt' --graph_path='./graph_reduced'
```
Check output files in `./output_reduced` directory.

## Citing This Work
```
@inproceedings{kim2022real,
  title={Real-time and Explainable Detection of Epidemics with Global News Data},
  author={Kim, Sungnyun and Shin, Jaewoo and Eom, Seongha and Oh, Jihwan and Yun, Se-Young},
  booktitle={Workshop on Healthcare AI and COVID-19},
  pages={73--90},
  year={2022},
  organization={PMLR}
}
```

## Contact
**Sungnyun Kim**: ksn4397@kaist.ac.kr
