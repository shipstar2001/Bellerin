import pandas as pd
import numpy as np
from scipy.signal import find_peaks, savgol_filter
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from pybaselines import Baseline
import itertools
import sys

def load_msi_data(csv_file):
    """ CSV 파일에서 DESI MSI 데이터를 로드하는 함수 """
    df = pd.read_csv(csv_file)
    return df

def baseline_correction(df, mz_columns, lam, p):
    """ ALS Baseline Correction 수행 (진행상황 표시) """
    baseline_corrector = Baseline().asls
    corrected_df = df.copy()
    
    total_mz = len(mz_columns)
    
    for i, mz in enumerate(mz_columns):
        intensities = df[mz].values
        baseline_output = baseline_corrector(intensities, lam=lam, p=p)
        baseline = baseline_output[0]
        corrected_df[mz] = np.maximum(intensities - baseline, 0)  # Baseline 제거 후 0 이하 값은 0으로 설정
        corrected_df = corrected_df.fillna(0)  # NaN을 0으로 대체
        
        # 진행 상황 표시 (진행률 % 출력)
        progress = (i + 1) / total_mz * 100
        sys.stdout.write(f"\rBaseline Correction 진행 중: {progress:.2f}% 완료")
        sys.stdout.flush()

    print("\n✅ Baseline Correction 완료!")
    return corrected_df

def smoothing(df, mz_columns, window_length, polyorder):
    """ Savitzky-Golay Smoothing 수행 """
    smoothed_df = df.copy()
    
    for mz in mz_columns:
        smoothed_df[mz] = savgol_filter(df[mz], window_length=window_length, polyorder=polyorder)
        smoothed_df = smoothed_df.fillna(0)  # NaN을 0으로 대체
    
    print("Smoothing 완료")
    return smoothed_df

def compute_metrics(original_df, processed_df, mz_columns):
    """ SNR, PPR, CV Ratio 계산 """
    original = original_df[mz_columns].values
    processed = processed_df[mz_columns].values

    # Signal-to-Noise Ratio (SNR)
    signal_power = np.mean(original ** 2)
    noise_power = np.mean((original - processed) ** 2)
    snr = 10 * np.log10(signal_power / noise_power)

    # Peak Preservation Rate (PPR)
    peak_threshold = 0.05 * np.max(original)
    peak_count_before = np.sum((np.diff(np.sign(np.diff(original, axis=0)), axis=0) < 0) & (original[:, 1:-1] > peak_threshold))
    peak_count_after = np.sum((np.diff(np.sign(np.diff(processed, axis=0)), axis=0) < 0) & (processed[:, 1:-1] > peak_threshold))
    ppr = (peak_count_after / peak_count_before) * 100 if peak_count_before > 0 else 0

    # Coefficient of Variation (CV)
    cv_before = np.std(original) / np.mean(original) * 100
    cv_after = np.std(processed) / np.mean(processed) * 100
    cv_ratio = cv_after / cv_before if cv_before > 0 else 0

    # 최적화 점수 계산 (SNR과 PPR이 높을수록, CV Ratio가 1과 가까울수록 좋음)
    optimization_score = snr + ppr - abs(1 - cv_ratio) * 100
    return snr, ppr, cv_ratio, optimization_score

def normalize_spectra(df, mz_columns, method="minmax"):
    """ Normalization 수행 (Min-Max 또는 Z-score) """
    normalized_df = df.copy()
    
    if method == "minmax":
        scaler = MinMaxScaler()
    elif method == "zscore":
        scaler = StandardScaler()
    else:
        raise ValueError("지원되지 않는 정규화 방법입니다. 'minmax' 또는 'zscore'를 사용하세요.")

    normalized_df[mz_columns] = scaler.fit_transform(df[mz_columns])
    return normalized_df

# 실행 예제
csv_file = "csv_dataset/STZ2.csv"
df = load_msi_data(csv_file)

# Pixel_X, Pixel_Y를 제외한 m/z 컬럼 선택
mz_columns = [col for col in df.columns if col not in ['Pixel_X', 'Pixel_Y']]

# 탐색할 파라미터 값 조합
lam_values = [1e4, 1e5, 1e6]  # ALS lambda
p_values = [0.001, 0.01, 0.1]  # ALS p 값
window_lengths = [5, 7, 9]  # Savitzky-Golay 윈도 크기 (홀수)
polyorders = [2, 3]  # 다항식 차수

# 최적의 조합 찾기
best_score = float("-inf")
best_params = None
best_processed_df = None

for lam, p, window_length, polyorder in itertools.product(lam_values, p_values, window_lengths, polyorders):
    if window_length >= len(df):
        continue
    
    # Baseline Correction & Smoothing 수행
    df_baseline_corrected = baseline_correction(df, mz_columns, lam, p)
    df_smoothed = smoothing(df_baseline_corrected, mz_columns, window_length, polyorder)

    # 평가 지표 계산
    snr, ppr, cv_ratio, score = compute_metrics(df, df_smoothed, mz_columns)

    print(f"lam: {lam}, p: {p}, window_length: {window_length}, polyorder: {polyorder}, SNR: {snr:.2f}, PPR: {ppr:.2f}, CV Ratio: {cv_ratio:.2f}, Score: {score:.2f}")

    # 최적의 조합 갱신
    if score > best_score:
        best_score = score
        best_params = (lam, p, window_length, polyorder)
        best_processed_df = df_smoothed

# 선택된 최적의 조합으로 Normalization 수행
df_normalized = normalize_spectra(best_processed_df, mz_columns, method="minmax")

# 결과 저장
df_normalized.to_csv("preprocessed_dataset/STZ2.csv", index=False)
print(f"✅ 최적의 조합: lam={best_params[0]}, p={best_params[1]}, window_length={best_params[2]}, polyorder={best_params[3]}")
print("✅ Peak Picking, Baseline Correction, Smoothing 및 Normalization 완료!")
