# Epidemics Detection with GKG Dataset
This repo contains the implementation of the paper,    
**Real-time and Explainable Detection of Epidemics with Global News Data**    
presented at [ICML Workshop on Healthcare AI and COVID-19](https://healthcare-ai-covid19.github.io/), 2022.

## Getting Started

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
