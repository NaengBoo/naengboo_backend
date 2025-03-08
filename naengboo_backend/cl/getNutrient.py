import requests
import xml.etree.ElementTree as ET
import difflib

def get_food_info(food_name):
    """
    식단관리(메뉴젠) 오픈API를 이용하여 음식 목록을 검색하는 함수.
    """
    serviceKey = "CgUFB4ty1nZ3tHzsF9EV2c85nc01oLHjituo+vull9cGoVjH37DuihiX/niTfkS/tmxmM9W9uGlAciE0VG+V9A=="
    url = "http://apis.data.go.kr/1390802/AgriFood/MzenFoodCode/getKoreanFoodList"
    params = {
        "serviceKey": serviceKey,
        "Page_No": "1",
        "Page_Size": "30",
        "food_Name": food_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        items = root.find('.//items')
        if items is None:
            return []
        food_info_list = []
        for item in items.findall('item'):
            code_elem = item.find('food_Code')
            name_elem = item.find('food_Name')
            if code_elem is not None and name_elem is not None:
                food_info_list.append({
                    "food_Code": code_elem.text,
                    "food_FullName": name_elem.text
                })
        return food_info_list
    else:
        print("API 요청 실패, 상태코드:", response.status_code)
        return None

def get_best_food_info(food_name):
    """
    API 검색 결과 중 음식명이 정확히 일치하는 항목이 있으면 반환하고,
    없으면 문자열 유사도 계산을 통해 가장 유사한 항목을 선택하여 리스트로 반환.
    """
    food_info_list = get_food_info(food_name)
    if food_info_list is None:
        return None
    if not food_info_list:
        print("API 검색 결과가 없습니다.")
        return []
    
    for item in food_info_list:
        if item["food_FullName"] == food_name:
            return [item]
    
    best_item = None
    best_ratio = 0
    for item in food_info_list:
        ratio = difflib.SequenceMatcher(None, food_name, item["food_FullName"]).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_item = item
    return [best_item] if best_item else []

def get_nutrition_info(food_code):
    """
    식단관리(메뉴젠) 오픈API를 이용하여 음식코드에 해당하는 영양성분(칼로리, 탄수화물, 단백질, 지방, 중량) 정보를 합산하여 반환.
    """
    serviceKey = "CgUFB4ty1nZ3tHzsF9EV2c85nc01oLHjituo+vull9cGoVjH37DuihiX/niTfkS/tmxmM9W9uGlAciE0VG+V9A=="
    url = "http://apis.data.go.kr/1390802/AgriFood/MzenFoodNutri/getKoreanFoodIdntList"
    params = {
        "serviceKey": serviceKey,
        "food_Code": food_code
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        items = root.find('.//items')
        if items is None:
            print("영양성분 정보가 없습니다.")
            return None
        item_elem = items.find('item')
        if item_elem is None:
            print("영양성분 데이터가 없습니다.")
            return None
        idnt_lists = item_elem.findall('idnt_List')
        if not idnt_lists:
            print("영양성분 목록이 비어있습니다.")
            return None

        total_weight = 0.0
        total_energy = 0.0
        total_protein = 0.0
        total_fat = 0.0
        total_carbs = 0.0
        
        for idnt in idnt_lists:
            try:
                weight = float(idnt.findtext('food_Weight', default="0"))
            except ValueError:
                weight = 0.0
            try:
                energy = float(idnt.findtext('energy_Qy', default="0"))
            except ValueError:
                energy = 0.0
            try:
                protein = float(idnt.findtext('prot_Qy', default="0"))
            except ValueError:
                protein = 0.0
            try:
                fat = float(idnt.findtext('ntrfs_Qy', default="0"))
            except ValueError:
                fat = 0.0
            try:
                carbs = float(idnt.findtext('carbohydrate_Qy', default="0"))
            except ValueError:
                carbs = 0.0
            
            total_weight += weight
            total_energy += energy
            total_protein += protein
            total_fat += fat
            total_carbs += carbs
        
        return {
            "total_Weight": total_weight,
            "total_Energy": total_energy,
            "total_Protein": total_protein,
            "total_Fat": total_fat,
            "total_Carbohydrate": total_carbs
        }
    else:
        print("영양성분 API 요청 실패, 상태코드:", response.status_code)
        return None
