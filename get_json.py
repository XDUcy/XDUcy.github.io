import numpy as np
import pandas as pd
import json

MODULE_PATH = r'./data/modules/'
JSON_PATH = r'./data/jsons/'
# 配置 parties.txt, parties.csv 路径
module = r"Native" # module名对应

parties_file = MODULE_PATH + module + '/' + "parties.txt"
trans_file = MODULE_PATH + module + '/' + "parties.csv"
json_out = JSON_PATH + module + "_data_and_layout.json"

# 保留parties.txt中的城镇、城堡、村庄，并提取id和坐标列
parties_df = pd.read_csv(parties_file, sep=' ', skiprows=2, header=None)
parties_df = parties_df.iloc[:, [4, 5, 15, 16]].dropna()
parties_df.columns = ['party_id', 'party_name', 'locx', 'locy']
place = parties_df[parties_df['party_id'].str.match(r'p_(town|castle|village)_\d+')]
# txt中每一项的id对应在游戏中显示的名字存在csv中，将其匹配
trans_df = pd.read_csv(trans_file, names=['party_id', 'name_shown'], skiprows=1, sep='|')
trans_df = trans_df[trans_df['party_id'].str.match(r'p_(town|castle|village)_\d+')]
place_with_name = pd.merge(parties_df, trans_df, on=['party_id'])
place_with_name['name_shown'] = place_with_name['name_shown'].str.strip()
place_with_name['name_shown'] = place_with_name['name_shown'].str.replace(' ', '')
# print(place_with_name)
# p_town_1    Sargoth  -17.6   79.7       萨哥斯...

# 根据不同的 party_id 创建不同的 trace
town_trace = place_with_name[place_with_name['party_id'].str.startswith('p_town_')]
castle_trace = place_with_name[place_with_name['party_id'].str.startswith('p_castle_')]
village_trace = place_with_name[place_with_name['party_id'].str.startswith('p_village_')]

# 创建每个 trace 的数据
town_data = {
    "x": town_trace['locx'].tolist(),
    "y": town_trace['locy'].tolist(),
    "text": town_trace['name_shown'].tolist(),
    "mode": "markers+text",
    "marker": {"symbol": "square", "size": 15},
    "textposition": "bottomcenter",
    "opacity":0.5

}

castle_data = {
    "x": castle_trace['locx'].tolist(),
    "y": castle_trace['locy'].tolist(),
    "text": castle_trace['name_shown'].tolist(),
    "mode": "markers+text",
    "marker": {"symbol": "castle", "size": 7},
    "textposition": "bottomcenter",
    "opacity":0.5
}

village_data = {
    "x": village_trace['locx'].tolist(),
    "y": village_trace['locy'].tolist(),
    "text": village_trace['name_shown'].tolist(),
    "mode": "markers+text",
    "marker": {"symbol": "circle", "size": 3},
    "textposition": "bottomcenter",
    "opacity":0.5
}

# 合并所有的 trace 数据
all_traces = [town_data, castle_data, village_data]

layout = {
    "title": "地点分布散点图",
    "xaxis": {"title": "X轴标签"},
    "yaxis": {"title": "Y轴标签"},
    "showlegend": False,
    "autosize": True
}

# 写出供网页读取的json到data/jsons下，以module命名
json_data = {"data": all_traces, "layout": layout}
with open(json_out, 'w', encoding = 'utf-8') as json_file:
    json.dump(json_data, json_file, indent=2, ensure_ascii=False)