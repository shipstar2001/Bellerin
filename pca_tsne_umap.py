import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.sparse import diags, csc_matrix
from scipy.sparse.linalg import spsolve
from tqdm import tqdm  # 진행 상황 표시
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 사용자 입력: Control2(정상) 및 STZ2(알츠하이머) 폴더 경로 입력
control_folder = input("정상 mouse brain 데이터 폴더 경로 입력: ")
stz_folder = input("알츠하이머 mouse brain 데이터 폴더 경로 입력: ")

def load_data(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    if not files:
        print(f"폴더 {folder} 내 CSV 파일이 없습니다. 프로그램 종료.")
        exit()
    
    data_list = []
    labels = []
    for file in tqdm(files, desc=f"Loading {folder}"):
        file_path = os.path.join(folder, file)
        df = pd.read_csv(file_path)
        df_sorted = df.sort_values(by='m/z')
        intensity_vec = df_sorted['intensity'].values
        data_list.append(intensity_vec)
        labels.append(folder)  # 폴더명(군집)을 라벨로 저장
    
    return np.array(data_list), labels

# 정상 및 알츠하이머 데이터 로드
control_data, control_labels = load_data(control_folder)
stz_data, stz_labels = load_data(stz_folder)

# 데이터 병합 및 라벨 생성
pca_data = np.vstack([control_data, stz_data])
labels = np.array(control_labels + stz_labels)

# PCA 분석 수행
scaler = StandardScaler()
pca_data_scaled = scaler.fit_transform(pca_data)  # 정규화

pca = PCA(n_components=2)
pca_result = pca.fit_transform(pca_data_scaled)

# PCA 결과 시각화
plt.figure(figsize=(8, 6))
plt.scatter(pca_result[:len(control_data), 0], pca_result[:len(control_data), 1], color='blue', label='Control')
plt.scatter(pca_result[len(control_data):, 0], pca_result[len(control_data):, 1], color='red', label='STZ', alpha=0.7)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Analysis of Normal and Alzheimer's Mouse Brain Spectra")
plt.legend()
plt.grid(True)
plt.show()

print("PCA 분석 완료! ✅")

# 3. 각 축(주성분)별 분산과 설명 분산 비율
explained_variances = pca.explained_variance_
explained_variance_ratios = pca.explained_variance_ratio_

# 4. 출력
for i in range(len(explained_variances)):
    print(f"PC{i+1} 분산: {explained_variances[i]:.4f}, "
          f"설명 분산 비율: {explained_variance_ratios[i]*100:.2f}%")






import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.sparse import diags, csc_matrix
from scipy.sparse.linalg import spsolve
from tqdm import tqdm  # 진행 상황 표시
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

# 사용자 입력: Control2(정상) 및 STZ2(알츠하이머) 폴더 경로 입력
control_folder = input("정상 mouse brain 데이터 폴더 경로 입력: ")
stz_folder = input("알츠하이머 mouse brain 데이터 폴더 경로 입력: ")

# t-SNE 파라미터 조합 설정
perplexity_values = [5,7,9]
learning_rates = [50, 100, 200]

def load_data(folder):
    files = [f for f in os.listdir(folder) if f.endswith('merged.csv')]
    if not files:
        print(f"폴더 {folder} 내 CSV 파일이 없습니다. 프로그램 종료.")
        exit()
    
    data_list = []
    labels = []
    for file in tqdm(files, desc=f"Loading {folder}"):
        file_path = os.path.join(folder, file)
        df = pd.read_csv(file_path)
        df_sorted = df.sort_values(by='m/z')
        intensity_vec = df_sorted['Smoothed Intensity'].values
        data_list.append(intensity_vec)
        labels.append(folder)  # 폴더명(군집)을 라벨로 저장
    
    return np.array(data_list), labels

# 정상 및 알츠하이머 데이터 로드
control_data, control_labels = load_data(control_folder)
stz_data, stz_labels = load_data(stz_folder)

# 데이터 병합 및 라벨 생성
tsne_data = np.vstack([control_data, stz_data])
labels = np.array(control_labels + stz_labels)

# t-SNE 분석 수행
scaler = StandardScaler()
tsne_data_scaled = scaler.fit_transform(tsne_data)  # 정규화

# 여러 t-SNE 파라미터 조합 실행
fig, axes = plt.subplots(len(perplexity_values), len(learning_rates), figsize=(15, 12))

for i, perplexity in enumerate(perplexity_values):
    for j, learning_rate in enumerate(learning_rates):
        tsne = TSNE(n_components=2, perplexity=perplexity, learning_rate=learning_rate, random_state=42)
        tsne_result = tsne.fit_transform(tsne_data_scaled)
        
        ax = axes[i, j]
        ax.scatter(tsne_result[:len(control_data), 0], tsne_result[:len(control_data), 1], color='blue', label='Control')
        ax.scatter(tsne_result[len(control_data):, 0], tsne_result[len(control_data):, 1], color='red', label='STZ', alpha=0.7)
        ax.set_xlabel("TSNE Component 1")
        ax.set_ylabel("TSNE Component 2")
        ax.set_title(f"t-SNE (Perplexity={perplexity}, Learning Rate={learning_rate})")
        ax.legend()
        ax.grid(True)

plt.tight_layout()
plt.show()

print("t-SNE 분석 완료! ✅")





import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.sparse import diags, csc_matrix
from scipy.sparse.linalg import spsolve
from tqdm import tqdm  # 진행 상황 표시
from sklearn.preprocessing import StandardScaler
import umap

# 사용자 입력: Control2(정상) 및 STZ2(알츠하이머) 폴더 경로 입력
control_folder = input("정상 mouse brain 데이터 폴더 경로 입력: ")
stz_folder = input("알츠하이머 mouse brain 데이터 폴더 경로 입력: ")

# 여러 UMAP 파라미터 조합 설정
n_neighbors_values = [5, 15, 30]
min_dist_values = [0.1, 0.5, 0.9]

def load_data(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    if not files:
        print(f"폴더 {folder} 내 CSV 파일이 없습니다. 프로그램 종료.")
        exit()
    
    data_list = []
    labels = []
    for file in tqdm(files, desc=f"Loading {folder}"):
        file_path = os.path.join(folder, file)
        df = pd.read_csv(file_path)
        df_sorted = df.sort_values(by='m/z')
        intensity_vec = df_sorted['Smoothed Intensity'].values
        data_list.append(intensity_vec)
        labels.append(folder)  # 폴더명(군집)을 라벨로 저장
    
    return np.array(data_list), labels

# 정상 및 알츠하이머 데이터 로드
control_data, control_labels = load_data(control_folder)
stz_data, stz_labels = load_data(stz_folder)

# 데이터 병합 및 라벨 생성
tsne_data = np.vstack([control_data, stz_data])
labels = np.array(control_labels + stz_labels)

# 데이터 정규화
scaler = StandardScaler()
tsne_data_scaled = scaler.fit_transform(tsne_data)  # 정규화

# 여러 UMAP 파라미터 조합 실행
fig, axes = plt.subplots(len(n_neighbors_values), len(min_dist_values), figsize=(15, 12))

for i, n_neighbors in enumerate(n_neighbors_values):
    for j, min_dist in enumerate(min_dist_values):
        umap_reducer = umap.UMAP(n_components=2, n_neighbors=n_neighbors, min_dist=min_dist, random_state=42)
        umap_result = umap_reducer.fit_transform(tsne_data_scaled)
        
        ax = axes[i, j]
        ax.scatter(umap_result[:len(control_data), 0], umap_result[:len(control_data), 1], color='blue', label='Control')
        ax.scatter(umap_result[len(control_data):, 0], umap_result[len(control_data):, 1], color='red', label='STZ', alpha=0.7)
        ax.set_xlabel("UMAP Component 1")
        ax.set_ylabel("UMAP Component 2")
        ax.set_title(f"UMAP (n_neighbors={n_neighbors}, min_dist={min_dist})")
        ax.legend()
        ax.grid(True)

plt.tight_layout()
plt.show()

print("UMAP 분석 완료! ✅")