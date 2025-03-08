import csv
from making_recipe import generate_recipe

def search_recipes(user_ingredients):
    exact_matches = []
    partial_matches = []
    try:
        with open(r"C:\Users\a0103\OneDrive\Desktop\new\naeng_boo\naengboo_backend\recommand\recommand\recipes.csv", "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_ing_str = row.get("ingredients", "")
                csv_ingredients = [ing.strip() for ing in csv_ing_str.split(",") if ing.strip()]
                
                user_ing_lower = [item.lower() for item in user_ingredients]
                csv_ing_lower = [ing.lower() for ing in csv_ingredients]
                
                missing = [csv_ingredients[idx] for idx, ing in enumerate(csv_ing_lower) if ing not in user_ing_lower]
                
                if not missing:
                    exact_matches.append({
                        "title": row.get("title", ""),
                        "ingredients": csv_ingredients
                    })
                else:
                    if 0 < len(missing) <= 2:
                        partial_matches.append({
                            "title": row.get("title", ""),
                            "ingredients": csv_ingredients,
                            "missing": missing
                        })
    except Exception as e:
        print("CSV 파일을 읽는 중 오류 발생:", e)
    return exact_matches, partial_matches

def main():
    user_input = input("메인 재료를 콤마로 구분하여 입력하세요 (예: 연어, 고기, 밥): ")
    user_ingredients = [item.strip() for item in user_input.split(",") if item.strip()]
    prefer = input("테마를 입력하시오 : ")
    
    if not user_ingredients:
        print("적어도 하나의 메인 재료를 입력해 주세요.")
        return

    exact_matches, partial_matches = search_recipes(user_ingredients)
    
    print("\n=== CSV에서 가진 재료로 만들 수 있는 레시피 (정확히 일치) ===")
    if exact_matches:
        for match in exact_matches:
            print(f"- {match['title']} (재료: {', '.join(match['ingredients'])})")
    else:
        print("CSV에서 가진 재료로만 만들 수 있는 레시피를 찾지 못했습니다.")
    
    print("\n=== CSV에서 가진 재료 중 1~2개 재료가 부족한 레시피 ===")
    if partial_matches:
        for match in partial_matches:
            print(f"- {match['title']} (재료: {', '.join(match['ingredients'])})")
            print(f"  부족한 재료: {', '.join(match['missing'])}")
    else:
        print("CSV에서 부족한 재료가 1~2개인 레시피를 찾지 못했습니다.")
    
    print("\n=== GPT로 생성된 레시피 추천 ===")
    recipe = generate_recipe(user_ingredients,prefer)
    if recipe:
        print(recipe)
    else:
        print("레시피 생성에 실패했습니다.")

if __name__ == "__main__":
    main()
