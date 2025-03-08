import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

# 환경 변수에서 API 키 설정 (환경 변수에 OPENAI_API_KEY가 등록되어 있어야 합니다)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# 요청 데이터 모델 정의
class FoodInput(BaseModel):
    food_name: str

def classify_food(food_name: str) -> str:
    """
    GPT API를 호출하여 음식 분류를 수행하는 함수.
    미리 정의된 카테고리 기준에 따라 프롬프트를 구성합니다.
    이제 최신 API 인터페이스인 ChatCompletion을 사용합니다.
    """
    prompt = f"""
아래의 기준에 따라 음식 분류를 해주세요.

[카테고리 기준]
- 요리 종류: 한식, 중식, 양식, 일식 등
- 식사 형태: 밥류, 면류, 빵류 등
- 조리법: 볶음, 비빔, 조림, 구이 등
- 재료: 육류, 해산물, 비건

예시:
음식: 비빔밥
분류 결과:
요리 종류: 한식
식사 형태: 밥류
조리법: 비빔
재료: 육류, 채소

이제 음식 분류:
음식: {food_name}
분류 결과:
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "당신은 음식 분류 전문가입니다. 아래 기준에 따라 음식의 카테고리를 분류해주세요."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        classification = response.choices[0].message.content.strip()
        return classification
    except Exception as e:
        print("OpenAI API 호출 중 오류 발생:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify_food")
async def api_classify_food(food: FoodInput):
    """
    POST /classify_food
    요청 본문에 food_name을 담아 보내면, GPT API를 통해 분류 결과를 반환합니다.
    """
    result = classify_food(food.food_name)
    return {"classification": result}

@app.get("/")
async def read_root():
    return "This is root path from MyAPI"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)


