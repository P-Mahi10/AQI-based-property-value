import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# Load dataset
df = pd.read_csv("C:\\Users\\mahip\\Downloads\\archive (1)\\Bengaluru_House_Data.csv")

# Selecting the required features
df = df[['location', 'size', 'total_sqft', 'bath', 'balcony', 'price']]

# Drop missing values
df.dropna(inplace=True)

# Handling 'total_sqft' ranges like '1200 - 1500'
def convert_sqft(value):
    try:
        if '-' in value:
            low, high = value.split('-')
            return (float(low) + float(high)) / 2
        return float(value)
    except:
        return np.nan

df['total_sqft'] = df['total_sqft'].apply(convert_sqft)
df.dropna(inplace=True)

# Target Encoding for 'location'
location_price_map = df.groupby('location')['price'].mean().to_dict()
df['location_encoded'] = df['location'].map(location_price_map)

# Encoding 'size' (like '2 BHK', '3 BHK') to numeric
df['size'] = df['size'].apply(lambda x: int(x.split(' ')[0]))

# Final feature set (use 'location_encoded' instead of 'location')
X = df[['location_encoded', 'size', 'total_sqft', 'bath', 'balcony']]
y = df['price']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print(f"R2 Score: {r2_score(y_test, y_pred)}")
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred)}")

# Example Prediction (take the first row of test set)
example = X_test.iloc[0].values.reshape(1, -1)
predicted_price = model.predict(example)
print(f"Predicted Price for example: {predicted_price[0]}")
