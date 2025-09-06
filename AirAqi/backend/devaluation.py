import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error

# Load the dataset
file_path = "C:\\Users\\Atharva\\AirAqi\\backend\\location_based_medical_summary_single.xlsx"
df = pd.read_excel(file_path, sheet_name="Summary")

# Compute total frequency per location (proxy for relative population)
df["Total_Frequency"] = df.groupby("Location")["Frequency"].transform("sum")
df["Relative_Population"] = df["Total_Frequency"] / df["Total_Frequency"].max()

# Normalize treatment cost impact to avoid excessive weight
df["Normalized_Cost"] = np.log1p(df["Avg_Treatment_Cost"])  # Log transformation

# Compute Disease Burden Score (frequency * normalized cost)
df["Disease_Burden"] = df["Frequency"] * df["Normalized_Cost"]

# Aggregate features at the Location level
location_features = df.groupby("Location").agg({
    "AQI": "mean",  # AQI per location
    "Disease_Burden": "sum",  # Total disease burden
    "Relative_Population": "mean"  # Population estimate
}).reset_index()

# Adjust Devaluation per Sq. Ft. with per capita adjustment
epsilon = 1e-5  # Small value to prevent division by zero
location_features["Devaluation_per_sqft"] = (
    0.7 * location_features["AQI"] + 0.03* (location_features["Disease_Burden"] / (location_features["Relative_Population"] + epsilon))
)

# Dictionary for market prices per square foot (dummy values with variation)
market_prices = {
    location: np.random.randint(8000, 12000) for location in location_features["Location"].unique()
}

# Compute Disease Burden Factor (log-transformed for scaling stability)
location_features["Disease_Burden_Factor"] = np.log1p(location_features["Disease_Burden"]) / np.log1p(location_features["Disease_Burden"].max())

# Prepare data for training
X = location_features[["AQI", "Disease_Burden", "Relative_Population"]]
y = location_features["Devaluation_per_sqft"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train XGBoost model
model = XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1)
model.fit(X_train_scaled, y_train)

# Evaluate model
predictions = model.predict(X_test_scaled)
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae}")

# Function to get devaluation per square foot for a given location
def get_devaluation(location):
    if location not in location_features["Location"].values:
        return f"Location {location} not found."
    
    loc_data = location_features[location_features["Location"] == location]
    loc_X = scaler.transform(loc_data[["AQI", "Disease_Burden", "Relative_Population"]])
    predicted_devaluation = model.predict(loc_X)[0]
    
    disease_burden_factor = loc_data["Disease_Burden_Factor"].values[0]
    location_aqi = loc_data["AQI"].values[0]
    if location_aqi in range(0,51):
        scaling_factor = 0 * np.sqrt(disease_burden_factor)
    elif location_aqi in range(51,101):
        scaling_factor = 0.351 * np.sqrt(disease_burden_factor)
    elif location_aqi in range(101,151):
        scaling_factor = 0.712 * np.sqrt(disease_burden_factor)
    elif location_aqi in range(151,201):
        scaling_factor = 0.913 * np.sqrt(disease_burden_factor)
    elif location_aqi > 200:
        scaling_factor = 1*np.sqrt(disease_burden_factor)
    
    

    
    scaled_devaluation = predicted_devaluation * scaling_factor
    
    return {
        "Location": location,
        "Predicted Devaluation": predicted_devaluation,
        "Scaled Devaluation": scaled_devaluation
    }



# Function to calculate health risk based on scaled devaluation
def calculate_health_risk():
    devaluation_values = [
        get_devaluation(loc)["Scaled Devaluation"]
        for loc in location_features["Location"].unique()
    ]
    
    if not devaluation_values:  # Safety check
        return {}
    
    # Normalize devaluation values to a scale of 0-10
    min_dev, max_dev = min(devaluation_values), max(devaluation_values)
    
    health_risk_mapping = {}
    
    for location in location_features["Location"].unique():
        scaled_devaluation = get_devaluation(location)["Scaled Devaluation"]
        
        # Apply normalization formula
        health_risk = 0 if max_dev == min_dev else ((scaled_devaluation - min_dev) / (max_dev - min_dev)) * 10
        health_risk_mapping[location] = round(health_risk, 2)  # Round to 2 decimals
    
    return health_risk_mapping

# Function to generate CSV with devaluation and health risk
def generate_devaluation_csv(output_file="devaluation_data.csv"):
    df_raw = pd.read_excel(file_path, sheet_name="Summary")  # Read raw data
    aqi_mapping = df_raw.groupby("Location")["AQI"].mean().to_dict()  # Create AQI lookup
    health_risk_data = calculate_health_risk()  # Get Health Risk Ratings

    results = []
    for location in location_features["Location"].unique():
        devaluation_info = get_devaluation(location)
        if isinstance(devaluation_info, dict):
            row = {
                "Location": location,
                "AQI": aqi_mapping.get(location, "N/A"),  # Explicitly fetch AQI
                "Scaled Devaluation": devaluation_info["Scaled Devaluation"],
                "Health Risk": health_risk_data.get(location, "N/A")  # Explicitly add health risk rounded to 2 decimals
            }
            results.append(row)

    df_results = pd.DataFrame(results)
    df_results.to_csv(output_file, index=False)
    print(f"Devaluation data saved to {output_file}")

# Generate CSV
generate_devaluation_csv()
