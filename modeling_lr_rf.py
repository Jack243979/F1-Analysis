import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict

# 1. Load feature data
features = pd.read_csv("data/feature_dataset.csv")

# 2. Create binary target: has this driver ever won at Singapore?
features['ever_win'] = (features['sg_win_count'] > 0).astype(int)

# 3. Prepare X and y
X = features.drop(columns=['driver_name', 'team_name', 'ever_win'])
y = features['ever_win']

# 4. Train Logistic Regression with cross-validated probabilities
lr = LogisticRegression(max_iter=1000)
lr_probs = cross_val_predict(lr, X, y, cv=5, method='predict_proba')[:, 1]

# 5. Train Random Forest with cross-validated probabilities
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_probs = cross_val_predict(rf, X, y, cv=5, method='predict_proba')[:, 1]

# 6. Prepare output DataFrame
output = pd.DataFrame({
    'driver_name': features['driver_name'],
    'team_name':   features['team_name'],
    'lr_prob':     lr_probs,
    'rf_prob':     rf_probs
})

# 7. Save predictions
output.to_csv("data/predictions_lr_rf.csv", index=False)
print("✅ Saved Logistic Regression & RF predictions to data/predictions_lr_rf.csv")
print(output.head())
