import pandas as pd
from fuzzywuzzy import process
from getNutrient import get_best_food_info, get_nutrition_info

df = pd.read_csv('food_data_with_clusters.csv')  # CSV 파일명과 경로를 실제에 맞게 수정

def find_food_info_csv(input_name, input_grams):
    """
    CSV 파일에서 사용자가 입력한 음식명과 섭취량(g)을 바탕으로
    가장 유사한 음식명을 찾고, 100g당 영양성분(칼로리, 단백질, 지방, 탄수화물)을
    입력 섭취량에 맞게 계산하여 반환.
    """
    best_match = process.extractOne(input_name, df['식품명'])
    if best_match is None:
        return None
    matched_name, match_score = best_match[:2]
    if match_score < 60:
        return None
    food_row = df[df['식품명'] == matched_name].iloc[0]
    cal_per_100g = food_row['칼로리']
    protein_per_100g = food_row['단백질']
    fat_per_100g = food_row['지방']
    carb_per_100g = food_row['탄수화물']
    
    factor = input_grams / 100.0
    result = {
        '음식명': matched_name,
        '섭취량(g)': input_grams,
        '칼로리': cal_per_100g * factor,
        '단백질': protein_per_100g * factor,
        '지방': fat_per_100g * factor,
        '탄수화물': carb_per_100g * factor,
        '유사도점수': match_score
    }
    return result

def main():
    input_name = input("음식명을 입력하세요: ")
    try:
        input_grams = float(input("섭취한 양(g)을 입력하세요: "))
    except ValueError:
        print("섭취량은 숫자로 입력해주세요.")
        return
    
    food_info = find_food_info_csv(input_name, input_grams)
    if food_info is not None:
        print("CSV에서 찾은 결과:")
        print("음식명:", food_info['음식명'])
        print("유사도 점수:", food_info['유사도점수'])
        print("섭취량(g):", food_info['섭취량(g)'])
        print("칼로리:", round(food_info['칼로리'], 2))
        print("단백질:", round(food_info['단백질'], 2))
        print("지방:", round(food_info['지방'], 2))
        print("탄수화물:", round(food_info['탄수화물'], 2))
    else:
        api_results = get_best_food_info(input_name)
        if api_results:
            selected_item = api_results[0]
            food_code = selected_item.get("food_Code")
            print("CSV에서 찾지 못하여 API 검색 결과:")
            print("음식명:", selected_item.get("food_FullName"))
            nutrition = get_nutrition_info(food_code)
            if nutrition is not None:
                print("영양성분 정보 (합산):")
                print("총 중량:", nutrition["total_Weight"])
                print("칼로리:", nutrition["total_Energy"])
                print("단백질:", nutrition["total_Protein"])
                print("지방:", nutrition["total_Fat"])
                print("탄수화물:", nutrition["total_Carbohydrate"])
            else:
                print("영양성분 정보를 가져오지 못했습니다.")
        else:
            print("데이터가 없습니다.")

if __name__ == "__main__":
    main()
