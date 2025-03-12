import os
import pandas as pd
import pickle
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

os.environ["LOKY_MAX_CPU_COUNT"] = "4"  # CPU 코어 개수 제한 (Windows 오류 방지)

# ✅ 프로젝트 최상위 폴더(`naengboo_backend/`) 기준으로 설정
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ 학습 데이터 (`datasets/food_data.xlsx`) 경로 수정
data_path = os.path.join(base_dir, "datasets", "food_data.xlsx")
df = pd.read_excel(data_path)  # ✅ `xlsx` 파일 읽기

# ✅ 영어 속성으로 변환 (한글 → 영어)
df.rename(columns={'탄수화물': 'carbohydrates', '단백질': 'protein', '지방': 'fat', '칼로리': 'calories'}, inplace=True)

# ✅ 클러스터링할 영양 성분 리스트
features = ['carbohydrates', 'protein', 'fat', 'calories']

models = {}   # K-Means 모델 저장
scalers = {}  # StandardScaler 저장
cluster_mappings = {}

for feature in features:
    # ✅ 데이터 표준화 (StandardScaler 사용)
    scaler = StandardScaler()
    df[feature] = scaler.fit_transform(df[[feature]])

    # ✅ K-Means 클러스터링 수행
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df[f'{feature}_cluster'] = kmeans.fit_predict(df[[feature]])

    # ✅ 클러스터 번호 정렬 (저 → 중 → 고)
    cluster_means = df.groupby(f'{feature}_cluster')[feature].mean()  # 클러스터별 평균 계산
    sorted_clusters = cluster_means.sort_values().index  # 평균값 기준으로 정렬
    new_cluster_mapping = {old: new for new, old in enumerate(sorted_clusters)}  # 0, 1, 2로 재배정

    # ✅ 클러스터 번호 변경 적용
    df[f'{feature}_cluster'] = df[f'{feature}_cluster'].map(new_cluster_mapping)

    # ✅ 모델 및 스케일러 저장
    models[feature] = kmeans
    scalers[feature] = scaler
    cluster_mappings[feature] = new_cluster_mapping

# ✅ 모델 저장 (`models/` 폴더에 저장)
models_path = os.path.join(base_dir, "models")
os.makedirs(models_path, exist_ok=True)  # 폴더가 없으면 생성

with open(os.path.join(models_path, "kmeans_models.pkl"), "wb") as f:
    pickle.dump(models, f)

with open(os.path.join(models_path, "scalers.pkl"), "wb") as f:
    pickle.dump(scalers, f)

with open(os.path.join(models_path, "cluster_mappings.pkl"), "wb") as f:
    pickle.dump(cluster_mappings, f)

# ✅ 클러스터링 결과 저장 (`datasets/food_data_with_clusters.csv`)
output_data_path = os.path.join(base_dir, "datasets", "food_data_with_clusters.csv")
df.to_csv(output_data_path, index=False, encoding='utf-8-sig')  # ✅ CSV로 저장

print(f"✅ 모델 학습 완료! 결과 저장: {output_data_path}")
