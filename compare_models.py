import pandas as pd
from sklearn.metrics import roc_auc_score, accuracy_score, log_loss

# 1. Load predictions
lr_rf    = pd.read_csv("data/predictions_lr_rf.csv")
xgb_svm  = pd.read_csv("data/predictions_xgb_svm.csv")

# 2. Merge them
preds = lr_rf.merge(xgb_svm, on=["driver_name", "team_name"])

# 3. Load true labels from features
features = pd.read_csv("data/feature_dataset.csv")
features['ever_win'] = (features['sg_win_count'] > 0).astype(int)
true = features.set_index("driver_name")["ever_win"]

# 4. Evaluate each model
results = []
for col in ["lr_prob", "rf_prob", "xgb_prob", "svm_prob"]:
    y_true = true.loc[preds["driver_name"]]
    y_pred = preds[col]
    results.append({
        "model":    col,
        "roc_auc":  roc_auc_score(y_true, y_pred),
        "accuracy": accuracy_score(y_true, (y_pred > 0.5).astype(int)),
        "log_loss": log_loss(y_true, y_pred)
    })

# 5. (Optional) Ensemble average of all four
preds["ensemble_prob"] = preds[["lr_prob", "rf_prob", "xgb_prob", "svm_prob"]].mean(axis=1)
y_pred_ens = preds["ensemble_prob"]
results.append({
    "model":    "ensemble",
    "roc_auc":  roc_auc_score(y_true, y_pred_ens),
    "accuracy": accuracy_score(y_true, (y_pred_ens > 0.5).astype(int)),
    "log_loss": log_loss(y_true, y_pred_ens)
})

# 6. Save & display
metrics_df = pd.DataFrame(results)
metrics_df.to_csv("data/model_comparison_metrics.csv", index=False)
preds.to_csv("data/combined_predictions.csv", index=False)

print(metrics_df)
