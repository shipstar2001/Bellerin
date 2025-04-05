import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    roc_auc_score
)
import matplotlib.pyplot as plt

# ------------------------------
# 1) CSV 파일 병합 함수
# ------------------------------
def load_and_merge_csv(file_list):
    df_list = [pd.read_csv(f) for f in file_list]
    merged_df = pd.concat(df_list, axis=0, ignore_index=True)
    return merged_df

# ------------------------------
# 2) Confusion Matrix 시각화 함수
# ------------------------------
def plot_confusion_matrix(cm, target_names, title='Confusion Matrix', cmap=plt.cm.Blues):
    """
    혼동행렬 시각화를 위한 함수
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)

    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j, i, format(cm[i, j], 'd'),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black"
            )
    
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# ------------------------------
# 3) Training 데이터 (Control 그룹과 Alzheimer 그룹 각각 2개의 파일 사용)
# ------------------------------
# Training용: Control 그룹에 2개의 파일, Alzheimer 그룹에 2개의 파일 사용
control_files = [
    "Control3/merged/Control3_merged.csv",
    "Control4/merged/Control4_merged.csv"
]
ad_files = [
    "STZ3/merged/STZ3_merged.csv",
    "STZ4/merged/STZ4_merged.csv"
]

# 새로운 데이터 (Test용 - 모델이 본 적 없는 데이터)
new_control_files = ["Control2/merged/Control2_merged.csv"]
new_ad_files = ["STZ2/merged/STZ2_merged.csv"]

# ---- (3-1) 데이터 로드/전처리 ----
control_df = load_and_merge_csv(control_files)
ad_df = load_and_merge_csv(ad_files)

# 그룹별 평균 계산
control_df = control_df.groupby(['Index', 'm/z'])['intensity'].mean().reset_index()
ad_df = ad_df.groupby(['Index', 'm/z'])['intensity'].mean().reset_index()

# Pivot (Wide format)
control_pivot = control_df.pivot(index='Index', columns='m/z', values='intensity')
ad_pivot = ad_df.pivot(index='Index', columns='m/z', values='intensity')

# 라벨 생성
control_labels = pd.Series(0, index=control_pivot.index)  # Control=0
ad_labels = pd.Series(1, index=ad_pivot.index)            # AD=1

# ---- (3-2) 데이터 합치기 ----
X_df = pd.concat([control_pivot, ad_pivot], axis=0).fillna(0)
y_series = pd.concat([control_labels, ad_labels], axis=0)

# 넘파이 변환
X = X_df.values
y = y_series.values

# ---- (3-3) Train/Test Split ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, stratify=y, random_state=42
)

# ------------------------------
# 4) 데이터 스케일링
# ------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ------------------------------
# 5) Random Forest 모델 학습 (과적합 방지를 위해 파라미터 수정)
# ------------------------------
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    min_samples_split=25,
    min_samples_leaf=15,
    max_features='log2',
    class_weight="balanced",
    random_state=42
)
rf.fit(X_train_scaled, y_train)

# 모델 저장
joblib.dump(rf, 'random_forest_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# ------------------------------
# 6) 모델 평가 (Train-Test Split 기반)
# ------------------------------
print("\n=== Random Forest Performance (Train-Test Split) ===")
y_pred_rf = rf.predict(X_test_scaled)
print(classification_report(y_test, y_pred_rf, target_names=["Control", "Alzheimer"]))

# Confusion Matrix 시각화
cm_test = confusion_matrix(y_test, y_pred_rf)
plt.figure()
plot_confusion_matrix(cm_test, target_names=["Control", "Alzheimer"], 
                      title="Confusion Matrix - Random Forest (Test Split)")
plt.show()

# ROC Curve 시각화
y_pred_proba_rf = rf.predict_proba(X_test_scaled)[:, 1]
fpr_rf, tpr_rf, _ = roc_curve(y_test, y_pred_proba_rf)
roc_auc_rf = roc_auc_score(y_test, y_pred_proba_rf)

plt.figure()
plt.plot(fpr_rf, tpr_rf, label='Random Forest (area = {:.4f})'.format(roc_auc_rf), color='blue')
plt.plot([0,1], [0,1], linestyle='--', color='gray', label='Random Guess')
plt.title("ROC Curve - Random Forest (Test Split)")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend(loc='lower right')
plt.show()

# ------------------------------
# 7) 완전히 새로운 데이터 평가 (Control4 & STZ4)
# ------------------------------
def evaluate_new_data(control_files, ad_files, model, scaler, model_name="Model"):
    # 1) 데이터 로드
    control_df = load_and_merge_csv(control_files)
    ad_df = load_and_merge_csv(ad_files)

    # 2) 그룹화 후 평균, pivot
    control_df = control_df.groupby(['Index', 'm/z'])['intensity'].mean().reset_index()
    ad_df = ad_df.groupby(['Index', 'm/z'])['intensity'].mean().reset_index()

    control_pivot = control_df.pivot(index='Index', columns='m/z', values='intensity')
    ad_pivot = ad_df.pivot(index='Index', columns='m/z', values='intensity')

    # 3) 라벨링 & 합치기
    control_labels = pd.Series(0, index=control_pivot.index)
    ad_labels = pd.Series(1, index=ad_pivot.index)
    
    X_df_new = pd.concat([control_pivot, ad_pivot], axis=0).fillna(0)
    y_series_new = pd.concat([control_labels, ad_labels], axis=0)

    # 4) 스케일링 & 예측
    X_new = X_df_new.values
    X_new_scaled = scaler.transform(X_new)
    y_pred_new = model.predict(X_new_scaled)

    # 5) 결과 출력
    print(f"\n=== {model_name} Performance (New Data) ===")
    print(classification_report(y_series_new.values, y_pred_new, target_names=["Control", "Alzheimer"]))
    
    # 6) Confusion Matrix 시각화
    cm_new = confusion_matrix(y_series_new.values, y_pred_new)
    plt.figure()
    plot_confusion_matrix(cm_new, target_names=["Control", "Alzheimer"],
                          title=f"Confusion Matrix - {model_name} (New Data)")
    plt.show()

    # 7) ROC Curve 시각화
    y_pred_new_proba = model.predict_proba(X_new_scaled)[:, 1]
    fpr_new, tpr_new, _ = roc_curve(y_series_new.values, y_pred_new_proba)
    roc_auc_new = roc_auc_score(y_series_new.values, y_pred_new_proba)

    plt.figure()
    plt.plot(fpr_new, tpr_new, label=f'{model_name} (area = {roc_auc_new:.4f})', color='red')
    plt.plot([0,1], [0,1], linestyle='--', color='gray', label='Random Guess')
    plt.title(f"ROC Curve - {model_name} (New Data)")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc='lower right')
    plt.show()

# ------------------------------
# 8) 새로운 데이터(Control4, STZ4) 평가
# ------------------------------
evaluate_new_data(new_control_files, new_ad_files, rf, scaler, model_name="Random Forest")