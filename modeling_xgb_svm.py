import pandas as pd
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_predict

# 1. Load feature data
features = pd.read_csv("data/feature_dataset.csv")

# 2. Create binary target: has this driver ever won at Singapore?
features['ever_win'] = (features['sg_win_count'] > 0).astype(int)

# 3. Prepare X and y
X = features.drop(columns=['driver_name', 'team_name', 'ever_win'])
y = features['ever_win']

# 4. Train XGBoost with cross-validated probabilities
#    Removed `use_label_encoder` (no longer needed)
xgb = XGBClassifier(eval_metric="logloss", random_state=42)
xgb_probs = cross_val_predict(xgb, X, y, cv=5, method='predict_proba')[:, 1]

# 5. Train SVM with probability=True
svm = SVC(kernel='rbf', probability=True, random_state=42)
svm_probs = cross_val_predict(svm, X, y, cv=5, method='predict_proba')[:, 1]

# 6. Prepare output DataFrame
output = pd.DataFrame({
    'driver_name': features['driver_name'],
    'team_name':   features['team_name'],
    'xgb_prob':    xgb_probs,
    'svm_prob':    svm_probs
})

# 7. Save predictions
output.to_csv("data/predictions_xgb_svm.csv", index=False)
print("✅ Saved XGBoost & SVM predictions to data/predictions_xgb_svm.csv")
print(output.head())
