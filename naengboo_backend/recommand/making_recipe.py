import requests
from dotenv import load_dotenv
import os

load_dotenv()

def generate_recipe(ingredients, prefer):
    """
    gpt-3.5-turbo 모델을 사용하여 입력된 메인 재료 기반 레시피를 생성합니다.
    (생성된 레시피에는 제목, 재료 목록, 조리 순서 등이 포함됩니다.)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful chef. Please provide recipes based on the user's ingredients."
        },
        {
            "role": "user",
            "content": (                
                "다음 재료들만 이용한 레시피를 만들어줘.\n"
                "굳이 주어진 재료를 다 사용하지 않아도 괜찮아.\n"
                f"그리고 레시피의 유형은 {prefer}식단으로 해줘\n"
                f"재료: {', '.join(ingredients)}\n"
                "조미료(소금, 후추, 기름, 간장 등)는 기본적으로 있다고 가정해.\n"
                "출력할 때 제목 뒤에 '요리제목'(저단백식단)처럼 뒤에 레시피 유형써줘\n"
                "레시피는 제목, 재료 목록, 그리고 조리 순서를 포함해줘.\n"
                "대답은 한국어로만 해줘"
            )
        }
    ]
    
    data = {
        "model": "gpt-3.5-turbo",  # 사용 가능한 모델명 (예: gpt-3.5-turbo)
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7,
        "n": 1
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    else:
        print("Error:", response.text)
        return None

def main():
    # 사용자로부터 메인 재료 입력받기 (예: 연어, 고기, 밥)
    user_input = input("메인 재료를 콤마로 구분하여 입력하세요 (예: 연어, 고기, 밥): ")
    perfer_input = input("선호하는 식단을 입력하시오 (예: 고단백, 저탄수 등): ")
    ingredients = [item.strip() for item in user_input.split(",") if item.strip()]
    
    if not ingredients:
        print("적어도 하나의 메인 재료를 입력해 주세요.")
        return

    recipe = generate_recipe(ingredients, perfer_input)
    if recipe:
        print("\n=== GPT로 생성된 레시피 ===\n")
        print(recipe)
    else:
        print("레시피 생성에 실패했습니다.")

if __name__ == "__main__":
    main()
