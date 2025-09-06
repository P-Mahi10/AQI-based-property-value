import pandas as pd

# Load dataset
file_path = "C:\\Users\\Atharva\\AirAqi\\devaluation_data.csv"  # Update with actual path
df = pd.read_csv(file_path)

# Define thresholds for recommendations
THRESHOLDS = {
    "aqi_high": 150,
    "industry_high": 5,
    "traffic_high": 7000,
    "footfall_high": 8000,
    "population_high": 5000,
    "greenery_low": 100,
    "gov_land_sufficient": 50.0
}

# Expected AQI Reduction (Percentage) per Intervention
IMPACT_FACTORS = {
    "greenery": (10, 20),  # 10-20% AQI reduction
    "traffic": (15, 25),   # 15-25% AQI reduction
    "industry": (20, 30),  # 20-30% AQI reduction
    "transport_ev": (10, 15),  # 10-15% AQI reduction
    "awareness": (5, 10)   # 5-10% AQI reduction
}

# Function to generate recommendations
def generate_recommendations(row):
    recommendations = []
    estimated_aqi_reduction = 0

    # High AQI intervention
    if row["aqi"] > THRESHOLDS["aqi_high"]:
        recommendations.append(
            "⚠ The air quality in this area has reached hazardous levels, making it unsafe for prolonged exposure.\n"
            "Authorities should enforce stricter emission control policies and increase green cover.\n"
            "Individuals can contribute by reducing vehicle usage, opting for carpooling, and using air-purifying indoor plants.\n"
            "Avoid outdoor activities during peak pollution hours and consider wearing a mask when necessary.\n"
            "Support local green initiatives and encourage businesses to adopt eco-friendly practices."
        )
        estimated_aqi_reduction += sum(IMPACT_FACTORS["greenery"]) / 2  # Average impact

    # Industrial pollution control
    if row["industry_count"] > THRESHOLDS["industry_high"]:
        if row["free_gov_land_acres"] > THRESHOLDS["gov_land_sufficient"]:
            recommendations.append(
                "🏭 This area has a dense industrial presence, significantly impacting air quality and public health.\n"
                "The government should utilize available land to create green buffer zones, reducing pollution spread.\n"
                "Residents can push for stricter regulations and demand regular emission audits of nearby factories.\n"
                "Supporting local businesses that use sustainable production methods can also make a difference.\n"
                "If you live nearby, ensure your home is well-ventilated and consider installing air purifiers."
            )
        else:
            recommendations.append(
                "🏭 Industrial pollution is a serious issue here, but space constraints make afforestation challenging.\n"
                "Stronger emission controls and tax incentives for cleaner production methods are needed immediately.\n"
                "Individuals should advocate for policy changes and encourage industries to switch to renewable energy sources.\n"
                "Consider participating in awareness campaigns to bring attention to the pollution problem in this area.\n"
                "On a personal level, reducing reliance on products from polluting industries can drive demand for greener alternatives."
            )
        estimated_aqi_reduction += sum(IMPACT_FACTORS["industry"]) / 2

    # Traffic congestion management
    if row["traffic_volume"] > THRESHOLDS["traffic_high"]:
        recommendations.append(
            "🚗 The traffic congestion in this area is extremely high, leading to increased pollution levels.\n"
            "Authorities should introduce better traffic management strategies, expand public transport, and incentivize EV adoption.\n"
            "As a commuter, consider using public transport, cycling, or carpooling to help ease congestion.\n"
            "Local governments should also introduce pedestrian-friendly pathways and restrict unnecessary vehicle entry.\n"
            "Switching to electric or hybrid vehicles can drastically reduce carbon emissions over time."
        )
        estimated_aqi_reduction += sum(IMPACT_FACTORS["traffic"]) / 2

    # Footfall-based interventions
    if row["footfall"] > THRESHOLDS["footfall_high"]:
        if row["greenery_sqft"] < THRESHOLDS["greenery_low"]:
            recommendations.append(
                "🌳 This area experiences a high number of visitors daily but lacks the necessary greenery to combat pollution.\n"
                "The government should prioritize creating green spaces such as micro-parks and tree-lined pathways.\n"
                "Businesses can participate by adding indoor plants and green facades to their establishments.\n"
                "Individuals can volunteer in tree-planting programs and ensure their surroundings remain clean.\n"
                "A community-led effort to install vertical gardens can also be an effective step toward improving air quality."
            )
        else:
            recommendations.append(
                "🌫 With high footfall in this area, pollution exposure is a concern, even if some greenery exists.\n"
                "Installing localized air purification systems like mist-based air filters in public spaces can help.\n"
                "People should be mindful of peak pollution hours and wear masks if necessary.\n"
                "Encouraging local businesses and eateries to maintain clean surroundings and plant more greenery can be impactful.\n"
                "Residents should also engage in community discussions to push for more eco-friendly urban planning initiatives."
            )
        estimated_aqi_reduction += sum(IMPACT_FACTORS["greenery"]) / 2

    # Population density considerations
    if row["populationPerArea"] > THRESHOLDS["population_high"]:
        recommendations.append(
            "📉 Estimated AQI reduction if these measures are followed: *{}%*".format(round(estimated_aqi_reduction))
        )
    
    return recommendations

# Generate recommendations for all locations
df["recommendations"] = df.apply(generate_recommendations, axis=1)
df["recommendations"] = df["recommendations"].apply(lambda x: "\n\n".join(x))

# Save to CSV
df.to_csv("recommendations_output.csv", index=False)
print("Recommendations for all locations have been generated and saved to 'recommendations_output.csv'.")