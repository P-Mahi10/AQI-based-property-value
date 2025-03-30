import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib  # For saving/loading model

# Load Data
df = pd.read_csv('Bengaluru_House_Data.csv')

# Data Preprocessing
df = df.dropna(subset=['location', 'size', 'total_sqft', 'bath', 'balcony', 'price'])
df['total_sqft'] = df['total_sqft'].astype(str)

# Handle ranges in total_sqft
def convert_sqft(sqft):
    if '-' in sqft:
        tokens = sqft.split('-')
        return (float(tokens[0]) + float(tokens[1])) / 2
    try:
        return float(sqft)
    except:
        return np.nan

df['total_sqft'] = df['total_sqft'].apply(convert_sqft)
df.dropna(subset=['total_sqft'], inplace=True)

# Create price per sqft feature
df['price_per_sqft'] = df['price'] * 100000 / df['total_sqft']
df = df[df['price_per_sqft'] < df['price_per_sqft'].quantile(0.99)]  # Outlier removal

# ✅ Save location-based average price for encoding
location_price = df.groupby('location')['price'].mean()
location_price.to_csv('location_price.csv')  # 🔥 Save for Flask server usage

# Encode 'location' using the saved mapping
df['location_encoded'] = df['location'].map(location_price)

# Encode 'size'
le = LabelEncoder()
df['size_encoded'] = le.fit_transform(df['size'])

# 🔥 Save size encoding mapping for Flask
size_mapping = pd.DataFrame({'size': le.classes_, 'encoded': le.transform(le.classes_)})
size_mapping.to_csv('size_mapping.csv', index=False)

# Log transform price to handle skewness
df['log_price'] = np.log1p(df['price'])

# Final Feature Set
features = ['total_sqft', 'bath', 'balcony', 'location_encoded', 'size_encoded', 'price_per_sqft']
X = df[features]
y = df['log_price']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost Model with Hyperparameter Tuning
params = {
    'n_estimators': [200],
    'max_depth': [6],
    'learning_rate': [0.1],
    'subsample': [0.8]
}
xgb = XGBRegressor(random_state=42)
grid = GridSearchCV(xgb, param_grid=params, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
grid.fit(X_train, y_train)

# Best Model
best_model = grid.best_estimator_

# ✅ Save the trained model
joblib.dump(best_model, 'bengaluru_house_xgb_model.pkl')
print("✅ Model saved successfully as 'bengaluru_house_xgb_model.pkl'")

# Model Evaluation
y_pred_log = best_model.predict(X_test)
y_pred = np.expm1(y_pred_log)  # Convert back from log scale
y_test_actual = np.expm1(y_test)

mae = mean_absolute_error(y_test_actual, y_pred)
r2 = r2_score(y_test_actual, y_pred)

print(f"R2 Score: {r2}")
print(f"Mean Absolute Error (Lakhs): {mae:.2f}")

# Cross-Validation Score
cv_mae = -cross_val_score(best_model, X, y, cv=5, scoring='neg_mean_absolute_error')
print(f"Cross-Validated MAE (Lakhs): {np.mean(cv_mae):.2f}")

# ✅ Real-time Prediction Example
print("\n✅ Loading Model for Real-Time Prediction")
loaded_model = joblib.load('bengaluru_house_xgb_model.pkl')

# Predict example
example = np.array([[1200, 2, 1, location_price.mean(), 2, 8000]])  # Example values
example_pred_log = loaded_model.predict(example)
example_pred = np.expm1(example_pred_log)
print(f"Predicted Price for example (Lakhs): {example_pred[0]:.2f}")
