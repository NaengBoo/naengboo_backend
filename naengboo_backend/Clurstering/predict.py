import numpy as np
import pandas as pd  # 추가
import pickle

# ✅ 저장된 모델 불러오기
def load_models():
    """저장된 K-Means 모델과 스케일러 불러오기"""
    with open("kmeans_models.pkl", "rb") as f:
        kmeans_models = pickle.load(f)

    with open("scalers.pkl", "rb") as f:
        scalers = pickle.load(f)

    return kmeans_models, scalers

# ✅ 새로운 데이터를 예측하는 함수
def predict_cluster(new_data):
    """각 영양소별로 개별 클러스터 예측"""
    kmeans_models, scalers = load_models()  # 저장된 모델 불러오기
    features = ['탄수화물', '단백질', '지방', '당류', '칼로리']

    cluster_results = {}

    for i, feature in enumerate(features):
        scaler = scalers[feature]
        kmeans = kmeans_models[feature]

        # ✅ Pandas DataFrame으로 변환하여 feature name 유지
        new_data_df = pd.DataFrame([[new_data[i]]], columns=[feature])

        # 데이터 표준화 후 예측
        new_data_scaled = scaler.transform(new_data_df)  # DataFrame 사용
        predicted_cluster = kmeans.predict(new_data_scaled)

        cluster_results[feature] = predicted_cluster[0]

    return cluster_results

# ✅ 실행 예제
if __name__ == "__main__":
    test_data = [30, 10, 5, 3, 250]  # 예제 음식 데이터 (탄수화물, 단백질, 지방, 당류, 칼로리)
    cluster_assignments = predict_cluster(test_data)
    
    for feature, cluster in cluster_assignments.items():
        print(f"🔹 {feature} 클러스터: {cluster}")
