import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Optional: XGBoost if available
try:
    from xgboost import XGBClassifier
    xgb_available = True
except ImportError:
    print("⚠️ XGBoost not installed, skipping that model.")
    xgb_available = False


data = load_breast_cancer()
X, y = data.data, data.target

# Step 3: Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Step 4: Scale features (important for neural nets and SVM)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 5: Define base learners (include neural net)
base_learners = [
    ('rf', RandomForestClassifier(n_estimators=200, random_state=42)),
    ('svm', SVC(probability=True, kernel='rbf', C=2, random_state=42)),
    ('mlp', MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42))
]

if xgb_available:
    base_learners.append(('xgb', XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)))

# Step 6: Define meta-learner
meta_learner = GradientBoostingClassifier(random_state=42)

# Step 7: Build stacking model
stack_model = StackingClassifier(
    estimators=base_learners,
    final_estimator=meta_learner,
    cv=5,
    stack_method='predict_proba'
)

# Step 8: Train
print("🚀 Training complex stacking model...")
stack_model.fit(X_train, y_train)

# Step 9: Predict
y_pred = stack_model.predict(X_test)

# Step 10: Evaluate
print("\n Accuracy:", accuracy_score(y_test, y_pred))
print("\n Classification Report:\n", classification_report(y_test, y_pred))
print("\n Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
