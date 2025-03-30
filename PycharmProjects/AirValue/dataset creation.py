import faker
import random
import csv

fake = faker.Faker()


def findPrice(high, low, av):
    base = random.gauss(av, (high - low) / 6)  # Normal distribution
    return max(min(base, high), low)


# Disease data
disease_list = [
    {"name": "Asthma", "weight": 0.15},
    {"name": "Chronic Obstructive Pulmonary Disease (COPD)", "weight": 0.1},
    {"name": "Lung Cancer", "weight": 0.05},
    {"name": "Ischemic Heart Disease", "weight": 0.1},
    {"name": "Stroke", "weight": 0.08},
    {"name": "Respiratory Infections (e.g., Bronchitis, Pneumonia)", "weight": 0.12},
    {"name": "Allergic Rhinitis", "weight": 0.1},
    {"name": "Chronic Bronchitis", "weight": 0.08},
    {"name": "Emphysema", "weight": 0.05},
    {"name": "Pulmonary Fibrosis", "weight": 0.04},
    {"name": "Hypertension (Air pollution aggravates it)", "weight": 0.06},
    {"name": "Diabetes (Emerging link in research)", "weight": 0.05},
    {"name": "Others", "weight": 0.02}
]

disease_treatment_costs = [
    {"disease": "Asthma", "average_cost": 3500, "lowest_cost": 3000, "highest_cost": 4000},
    {"disease": "Chronic Obstructive Pulmonary Disease (COPD)", "average_cost": 50000, "lowest_cost": 30000,
     "highest_cost": 70000},
    {"disease": "Lung Cancer", "average_cost": 500000, "lowest_cost": 300000, "highest_cost": 700000},
    {"disease": "Ischemic Heart Disease", "average_cost": 300000, "lowest_cost": 200000, "highest_cost": 500000},
    {"disease": "Stroke", "average_cost": 250000, "lowest_cost": 150000, "highest_cost": 400000},
    {"disease": "Respiratory Infections (e.g., Bronchitis, Pneumonia)", "average_cost": 80000, "lowest_cost": 50000,
     "highest_cost": 120000},
    {"disease": "Allergic Rhinitis", "average_cost": 10000, "lowest_cost": 5000, "highest_cost": 15000},
    {"disease": "Chronic Bronchitis", "average_cost": 60000, "lowest_cost": 40000, "highest_cost": 80000},
    {"disease": "Emphysema", "average_cost": 70000, "lowest_cost": 50000, "highest_cost": 90000},
    {"disease": "Pulmonary Fibrosis", "average_cost": 150000, "lowest_cost": 100000, "highest_cost": 200000},
    {"disease": "Hypertension (Air pollution aggravates it)", "average_cost": 20000, "lowest_cost": 15000,
     "highest_cost": 30000},
    {"disease": "Diabetes (Emerging link in research)", "average_cost": 25000, "lowest_cost": 20000,
     "highest_cost": 35000},
    {"disease": "Others", "average_cost": 50000, "lowest_cost": 20000, "highest_cost": 100000}
]

# Extract weights for disease sampling
diseases = [d["name"] for d in disease_list]
weights = [d["weight"] for d in disease_list]

# Location-based distribution
location_distribution = {
    "Indiranagar": 300,
    "Whitefield": 200,
    "HSR Layout": 500
}

dataset = []

for location, count in location_distribution.items():
    for _ in range(count):
        # Sample a disease
        sample_disease = random.choices(disease_list, weights=weights, k=1)[0]
        disease_name = sample_disease["name"]

        # Get cost info
        cost_info = next((item for item in disease_treatment_costs if item["disease"] == disease_name), None)

        if cost_info:
            cost = findPrice(cost_info["highest_cost"], cost_info["lowest_cost"], cost_info["average_cost"])
        else:
            cost = 0

        dataset.append([
            fake.name(),
            location,
            disease_name,
            round(cost, 2)
        ])

# Save to CSV
with open('location_based_medical_dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Location", "Disease", "Treatment Cost"])
    writer.writerows(dataset)

print("Dataset created successfully with location-based distribution!")

