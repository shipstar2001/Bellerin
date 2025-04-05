import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier
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
# Training & Test Data (기존 데이터: Control2,3 & STZ2,3)
# ------------------------------
# training 데이터셋에 두 개씩 넣음
control_files = ["Control2/merged/Control2_merged.csv", "Control3/merged/Control3_merged.csv"]
ad_files = ["STZ2/merged/STZ2_merged.csv", "STZ3/merged/STZ3_merged.csv"]

# 데이터 불러오기
control_df = load_and_merge_csv(control_files)
ad_df = load_and_merge_csv(ad_files)

# 그룹별 평균값 계산
control_df = control_df.groupby(['Index', 'm/z'])['intensity'].mean().reset_index()
ad_df = ad_df.groupby(['Index', 'm/z'])['intensity'].mean().reset_index()

# Pivot 변환
test_control_pivot = control_df.pivot(index='Index', columns='m/z', values='intensity')
test_ad_pivot = ad_df.pivot(index='Index', columns='m/z', values='intensity')

# 라벨 생성
control_labels = pd.Series(0, index=test_control_pivot.index)
ad_labels = pd.Series(1, index=test_ad_pivot.index)

# 데이터 합치기 및 결측치 처리
X_df = pd.concat([test_control_pivot, test_ad_pivot], axis=0).fillna(0)
y_series = pd.concat([control_labels, ad_labels], axis=0)

# 넘파이 배열로 변환
X = X_df.values
y = y_series.values

# Train/Test 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, stratify=y, random_state=42
)

# ------------------------------
# 3) 데이터 스케일링
# ------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ------------------------------
# 4) XGBoost 모델 학습
# ------------------------------
# 클래스 불균형이 있을 경우를 대비해서 scale_pos_weight 계산 (음성:양성 비율)
neg_count = np.sum(y_train == 0)
pos_count = np.sum(y_train == 1)
scale_pos_weight = neg_count / pos_count if pos_count != 0 else 1

xgb_model = XGBClassifier(
    n_estimators=300,
    max_depth=10,
    learning_rate=0.05,
    min_child_weight=6,
    scale_pos_weight=scale_pos_weight,
    use_label_encoder=False,
    random_state=42,
    eval_metric='logloss'
)
xgb_model.fit(X_train_scaled, y_train)

# 모델과 스케일러 저장
joblib.dump(xgb_model, 'xgboost_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# ------------------------------
# 5) Test 데이터 평가 (Control2,3 & STZ2,3)
# ------------------------------
y_pred_test = xgb_model.predict(X_test_scaled)
print("=== Classification Report (Test set) ===")
print(classification_report(y_test, y_pred_test, target_names=["Control", "Alzheimer"]))

cm_test = confusion_matrix(y_test, y_pred_test)
print("=== Confusion Matrix (Test set) ===")
print(cm_test)
plt.figure()
plot_confusion_matrix(cm_test, target_names=["Control", "Alzheimer"], title="Confusion Matrix (Test Set)")
plt.show()

y_pred_test_proba = xgb_model.predict_proba(X_test_scaled)[:, 1]
fpr_test, tpr_test, _ = roc_curve(y_test, y_pred_test_proba)
roc_auc_test = roc_auc_score(y_test, y_pred_test_proba)
print("ROC AUC (Test set): {:.4f}".format(roc_auc_test))
plt.figure()
plt.plot(fpr_test, tpr_test, color='red', label='ROC curve (area = %0.4f)' % roc_auc_test)
plt.plot([0, 1], [0, 1], color='navy', linestyle='--', label='Random guess')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve (Test Set)')
plt.legend(loc="lower right")
plt.show()

# ------------------------------
# 6) New 데이터 평가 (새로운 데이터: Control4 & STZ4)
# ------------------------------
new_control_files = ["Control4/merged/Control4_merged.csv"]
new_ad_files = ["STZ4/merged/STZ4_merged.csv"]

new_control_df = load_and_merge_csv(new_control_files)
new_ad_df = load_and_merge_csv(new_ad_files)

new_control_df = new_control_df.groupby(['Index', 'm/z'])['intensity'].mean().reset_index()
new_ad_df = new_ad_df.groupby(['Index', 'm/z'])['intensity'].mean().reset_index()

new_control_pivot = new_control_df.pivot(index='Index', columns='m/z', values='intensity')
new_ad_pivot = new_ad_df.pivot(index='Index', columns='m/z', values='intensity')

new_control_labels = pd.Series(0, index=new_control_pivot.index)
new_ad_labels = pd.Series(1, index=new_ad_pivot.index)

X_new_df = pd.concat([new_control_pivot, new_ad_pivot], axis=0).fillna(0)
y_new = pd.concat([new_control_labels, new_ad_labels], axis=0)

X_new = X_new_df.values
X_new_scaled = scaler.transform(X_new)

y_pred_new = xgb_model.predict(X_new_scaled)
print("\n=== Classification Report (New Data) ===")
print(classification_report(y_new, y_pred_new, target_names=["Control", "Alzheimer"]))

cm_new = confusion_matrix(y_new, y_pred_new)
print("=== Confusion Matrix (New Data) ===")
print(cm_new)
plt.figure()
plot_confusion_matrix(cm_new, target_names=["Control", "Alzheimer"], title="Confusion Matrix (New Data)")
plt.show()

y_pred_new_proba = xgb_model.predict_proba(X_new_scaled)[:, 1]
fpr_new, tpr_new, _ = roc_curve(y_new, y_pred_new_proba)
roc_auc_new = roc_auc_score(y_new, y_pred_new_proba)
print("ROC AUC (New Data): {:.4f}".format(roc_auc_new))
plt.figure()
plt.plot(fpr_new, tpr_new, color='blue', label='ROC curve (area = %0.4f)' % roc_auc_new)
plt.plot([0, 1], [0, 1], color='navy', linestyle='--', label='Random guess')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve (New Data)')
plt.legend(loc="lower right")
plt.show()

