import json
import time

from selenium import webdriver
import pandas as pd

data_foot_prints_result = {}
def analyze_footprints_satellites():
    # 以位置为键，卫星数组为值的集合
    satellites = {}
    # 用于统计footprints中的数据，主要用于调用方法中的数据处理
    active_satellites = {}
    # 统计footprints中存在波片的卫星数目
    sat_total_number = 0
    # 读取文件
    with open("footprints_satellites_v2.json", 'rb') as a:
        satellites_spots = json.load(a)
        for key, value in satellites_spots.items():
            sat_total_number += len(value)
            # 用于记录卫星的数组
            sat = []
            # 每个经度(位置)下对应的卫星集合
            data_foot_prints = {}
            # 如果该位置下有卫星
            if len(value) != 0:
                for key_2, value_2 in value.items():
                    sat.append(key_2)
                    # 记录该卫星所包含的波片数量
                    data_foot_prints[key_2] = len(value_2)
            active_satellites[key] = sat
            satellites[key] = data_foot_prints
            # 初始化集合中的数组
            if data_foot_prints_result.get(key) == None:
                data_foot_prints_result[key] = []
            data_foot_prints_result[key] = value
        # 根据位置进行内部元素排序
        satellites = {str(key_sort): satellites[str(key_sort)] for key_sort in sorted(list(map(int, satellites.keys())))}
        with open('footprints_analysis_result.json', 'w+', encoding='utf-8') as f:
            json.dump(satellites, f, indent=2)
        print('卫星数量为 ：' + str(sat_total_number))
    return satellites, active_satellites

def check(invalid_array):
    browser = webdriver.Chrome()
    for pos in invalid_array:
        browser.get("https://satbeams.com/footprints?position=" + str(pos))
        time.sleep(10)



if __name__ == '__main__':
    # 用于记录存在波片数目为0的位置
    invalid_position_array = []
    # 波片数为0的卫星数量
    zero_number = 0
    satellites, active_satellite = analyze_footprints_satellites()
    data_analysis_result = {}
    with open("active_satellites.json", 'rb') as f:
        active_satellites = json.load(f)
        for key, value in active_satellites.items():
            pd_value = pd.Series(value)
            result = {}
            sat_list = active_satellite[key]
            # 该纬度下无卫星的情况
            if len(sat_list) == 0:
                invalid_position_array.append(int(key))
                for i in value:
                    zero_number += 1
                    result[i] = 0
                satellites[key] = result
            # 该纬度下有卫星的情况
            else:
                for i in sat_list:
                    index = pd_value == i
                    # 如果active的卫星不包含footprints中的卫星
                    if pd_value[index].size == 0:
                        # 统计spot为0的卫星数
                        zero_number += 1
                        (satellites[key])[i] = 0
                        invalid_position_array.append(int(key))
                    # 删除active卫星列表中已经比较过的卫星
                    pd_value.drop(pd_value[pd_value == i].index, inplace=True)
                # active卫星比footprints中卫星多的情况
                if len(pd_value) != 0:
                    invalid_position_array.append(int(key))
                    for v in pd_value:
                        zero_number += 1
                        # 在字典中更新footprints不包含的卫星，并设置波片数目为0
                        (satellites[key])[v] = 0
    with open('active_satellites_analysis_result.json', 'w+', encoding='utf-8') as f:
        json.dump(satellites, f, indent=2, ensure_ascii=False)
    print('spot数目为0的卫星数量为 ：' + str(zero_number))
    # 将含有spot = 0的位置进行统计，并自动点击网页查看
    # invalid_position_array = list(set(invalid_position_array))
    # invalid_position_array.sort()
    # print(invalid_position_array)
    # check(invalid_array)








