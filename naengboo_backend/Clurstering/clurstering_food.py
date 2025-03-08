import pandas as pd
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1️⃣ 엑셀 데이터 불러오기
df = pd.read_excel("food_data.xlsx")

# 2️⃣ 클러스터링을 수행할 영양 성분 리스트
features = ['탄수화물', '단백질', '지방', '당류', '칼로리']

# 3️⃣ 각 영양소별 개별적인 K-Means 클러스터링 수행 및 저장
models = {}
scalers = {}

# 클러스터링 결과를 저장할 데이터프레임 복사
df_clustered = df.copy()

# 클러스터 평균값을 저장할 딕셔너리
cluster_means_dict = {}

for feature in features:
    print(f"📌 {feature} 클러스터링 모델 학습 중...")

    # 결측값 제거
    df_feature = df.dropna(subset=[feature])

    # 데이터 표준화
    scaler = StandardScaler()
    scaled_feature = scaler.fit_transform(df_feature[[feature]])

    # K-Means 클러스터링 수행
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_feature[f'{feature}_cluster'] = kmeans.fit_predict(scaled_feature)

    # 클러스터 번호 정렬 (저 -> 중 -> 고)
    cluster_means = df_feature.groupby(f'{feature}_cluster')[feature].mean()
    sorted_clusters = cluster_means.sort_values().index  # 평균값 기준으로 정렬
    new_cluster_mapping = {old: new for new, old in enumerate(sorted_clusters)}  # 0, 1, 2로 재배정

    # 클러스터 번호 변경 적용
    df_feature[f'{feature}_cluster'] = df_feature[f'{feature}_cluster'].map(new_cluster_mapping)

    # ✅ 중복 제거: 동일한 feature 값이 있으면 첫 번째 값만 유지 (Index를 유니크하게 만듦)
    df_feature_unique = df_feature.groupby(feature).first()

    # ✅ 기존 데이터(`df_clustered`)에 클러스터 값을 매핑
    df_clustered.loc[df_clustered[feature].notna(), f'{feature}_cluster'] = df_clustered[feature].map(df_feature_unique[f'{feature}_cluster'])

    # 모델 및 스케일러 저장
    models[feature] = kmeans
    scalers[feature] = scaler

    # 정렬된 클러스터별 평균값 저장
    cluster_means_dict[feature] = cluster_means.rename(index=new_cluster_mapping).sort_index()

# 4️⃣ 모든 모델 및 스케일러 저장
with open("kmeans_models.pkl", "wb") as f:
    pickle.dump(models, f)

with open("scalers.pkl", "wb") as f:
    pickle.dump(scalers, f)

# 5️⃣ 클러스터링 결과를 엑셀 파일로 저장
df_clustered.to_excel("food_data_with_clusters.xlsx", index=False)

# 6️⃣ 클러스터별 평균값을 새로운 엑셀 파일로 저장
df_cluster_means = pd.DataFrame(cluster_means_dict)
df_cluster_means.to_excel("cluster_means.xlsx", index=True)

print("✅ 중복 없는 클러스터링 결과 저장 완료!")
