import pandas as pd

df = pd.read_excel("food_DB.xlsx")

# 식품명을 기준으로 영양소 평균값 계산하여 그룹화
df_grouped = df.drop(columns=['식품코드', '식품대분류명', '대표식품코드', '대표식품명', '식품중분류코드', '식품중분류명', '영양성분함량기준량','식품중량']).groupby('식품명', as_index=False).mean()


# 새로운 엑셀 파일로 저장
df_grouped.to_excel("food_data_aggregated.xlsx", index=False)
