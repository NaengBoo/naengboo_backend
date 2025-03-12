import os
import numpy as np
import pandas as pd
import pickle

# ✅ 프로젝트 최상위 폴더(`naengboo_backend/`) 기준으로 설정
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ 모델 불러오기 (`models/` 폴더에서 가져오기)
def load_models():
    models_path = os.path.join(base_dir, "models")

    with open(os.path.join(models_path, "kmeans_models.pkl"), "rb") as f:
        kmeans_models = pickle.load(f)

    with open(os.path.join(models_path, "scalers.pkl"), "rb") as f:
        scalers = pickle.load(f)

    with open(os.path.join(models_path, "cluster_mappings.pkl"), "rb") as f:
        cluster_mappings = pickle.load(f)  # ✅ 클러스터 정렬 정보 불러오기

    return kmeans_models, scalers, cluster_mappings

# ✅ 새로운 데이터를 예측하는 함수
def predict_cluster(new_data):
    """각 영양소별로 개별 클러스터 예측 (정렬된 클러스터 적용)"""
    kmeans_models, scalers, cluster_mappings = load_models()
    features = ['carbohydrates', 'protein', 'fat', 'calories']

    cluster_results = {}

    for i, feature in enumerate(features):
        scaler = scalers[feature]
        kmeans = kmeans_models[feature]

        # ✅ Pandas DataFrame으로 변환하여 feature name 유지
        new_data_df = pd.DataFrame([[new_data[i]]], columns=[feature])

        # 데이터 표준화 후 예측
        new_data_scaled = scaler.transform(new_data_df)  # ✅ feature name 유지됨
        predicted_cluster = kmeans.predict(new_data_df)

        # ✅ 클러스터 정렬을 적용하여 변경
        cluster_results[f'{feature}_cluster'] = cluster_mappings[feature][predicted_cluster[0]]

    return cluster_results

# ✅ CSV 파일 읽고 클러스터링 결과 추가 후 저장
def process_csv():
    """CSV 파일에서 데이터를 읽어 클러스터링 후 저장"""
    datasets_path = os.path.join(base_dir, "datasets")
    input_csv = os.path.join(datasets_path, "recipes.csv")
    output_csv = os.path.join(datasets_path, "recipes_with_clusters.csv")

    df = pd.read_csv(input_csv)

    # ✅ 클러스터링할 feature 리스트
    features = ['carbohydrates', 'protein', 'fat', 'calories']

    # ✅ 클러스터링 결과 저장용 컬럼 추가
    for feature in features:
        df[f'{feature}_cluster'] = np.nan

    # ✅ 각 행에 대해 클러스터 예측 수행
    for index, row in df.iterrows():
        try:
            nutrition_data = [row[feature] for feature in features]  # 각 행의 영양 데이터 가져오기
            cluster_results = predict_cluster(nutrition_data)  # 클러스터 예측

        # ✅ 예측된 클러스터링 결과를 DataFrame에 추가
            for feature in features:
                df.at[index, f'{feature}_cluster'] = cluster_results[f'{feature}_cluster']
        except Exception as e:
            print(f"⚠️ 오류 발생: {e} (파일: {input_csv}, index: {index}, 데이터: {row})")

    # ✅ 결과를 새로운 CSV 파일로 저장
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"✅ 클러스터링 결과가 추가된 파일이 저장되었습니다: {output_csv}")

# ✅ 실행 예제
if __name__ == "__main__":
    process_csv()
