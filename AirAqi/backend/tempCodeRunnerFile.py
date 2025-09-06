def generate_devaluation_csv(output_file="devaluation_data.csv"):
    df_raw = pd.read_excel(file_path, sheet_name="Summary")  # Read raw data
    aqi_mapping = df_raw.groupby("Location")["AQI"].mean().to_dict()  # Create AQI lookup
    
    results = []
    for location in location_features["Location"].unique():
        devaluation_info = get_devaluation(location)
        if isinstance(devaluation_info, dict):
            devaluation_info["AQI"] = aqi_mapping.get(location, "N/A")  # Explicitly fetch AQI
            results.append(devaluation_info)

    df_results = pd.DataFrame(results)
    df_results.to_csv(output_file, index=False)
    print(f"Devaluation data saved to {output_file}")

generate_devaluation_csv()