
# AQI-based-property-value

This project investigates how **Air Quality Index (AQI)** impacts property values and health risks.  
It introduces a methodology to compute **property devaluation per square foot** using AQI, disease burden, and relative population, and applies **XGBoost regression** to improve prediction accuracy.  
Additionally, it provides a framework to calculate **health risk scores** on a 0–10 scale based on devaluation results.

---

## Overview

- Analyzes property devaluation due to air quality.  
- Uses AQI, health burden, and population frequency as key features.  
- Employs both **formula-based computation** and **XGBoost regression**.  
- Provides standardized **health risk scores** alongside devaluation values.  
- Evaluates model accuracy using **Mean Absolute Error (MAE)**.  

---

## Dataset processing

The model requires three main inputs:  

1. **Air Quality Index (AQI)**  
   - Mean AQI is computed for each location.  

2. **Relative Population**  
   - Estimated using frequency counts:  
```

Relative Population = Total Frequency at Location / max(Total Frequency)

```

3. **Disease Burden Score**  
- Combines disease frequency with average treatment costs:  
```

Disease Burden = Frequency × log(1 + Avg Treatment Cost)

```

4. **Aggregated features**  
For each location, the dataset includes:  
- Mean AQI  
- Sum of Disease Burden  
- Mean Relative Population  

---

## Devaluation calculation

### Base formula
The **property devaluation per square foot** is estimated as:  

```

Devaluation = (0.7 × AQI + 0.03 × Disease Burden) / (Relative Population + ϵ)

```

where ϵ = 10⁻⁵ is added to prevent division by zero.  

### Scaling factor
A scaling factor adjusts values for realism, depending on AQI levels and the Disease Burden Factor (DBF):  

```

Scaling Factor =
0 × √DBF,         if 0 ≤ AQI ≤ 50
0.351 × √DBF,     if 51 ≤ AQI ≤ 100
0.712 × √DBF,     if 101 ≤ AQI ≤ 150
0.913 × √DBF,     if 151 ≤ AQI ≤ 200
1 × √DBF,         if AQI > 200

```

with  
```

DBF = log(1 + Disease Burden) / log(1 + max(Disease Burden))

```

### Final devaluation
The scaled devaluation is given by:  

```

Scaled Devaluation = Predicted Devaluation × Scaling Factor

```

---

## Predictive modeling with XGBoost

To refine predictions, an **XGBoost regression model** is trained.  

- **Features**:  
  - AQI  
  - Disease Burden  
  - Relative Population  

- **Target**:  
  - Devaluation per square foot  

- **Process**:  
  - Dataset split into training and testing sets (80/20).  
  - Features standardized with `StandardScaler`.  
  - Model trained with squared error loss.  

- **Evaluation metric**:  
```

MAE = (1/n) Σ |ŷᵢ – yᵢ|

```

### Model performance
The model achieved:  

```

Mean Absolute Error (MAE) = 7.02

```

This indicates strong accuracy in estimating property devaluation due to AQI.  

---

## Health risk calculation

Devaluation values are normalized to a **0–10 scale** to indicate health risks:  

```

Health Risk =
(Scaled Devaluation – min(Scaled Devaluation)) × 10
\---------------------------------------------------
max(Scaled Devaluation) – min(Scaled Devaluation)

````

This provides an interpretable risk score where **0 = lowest risk** and **10 = highest risk**.  

---

## Sample results

| Location         | AQI | Scaled Devaluation (per sqft) | Health Risk |
|------------------|-----|-------------------------------|-------------|
| Banashankari     | 210 | 293.43                        | 9.80        |
| Electronic City  | 243 | 299.49                        | 10.00       |
| HSR Layout       | 176 | 258.75                        | 8.64        |
| Indiranagar      | 182 | 254.77                        | 8.51        |
| Jayanagar        | 126 | 166.31                        | 5.55        |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/P-Mahi10/AQI-based-property-value.git
cd AQI-based-property-value
````

Install dependencies (as listed in `requirements.txt`):

```bash
pip install -r requirements.txt
```

---

## Usage

1. **Prepare the data**

   * Gather AQI, population, and medical cost datasets.
   * Compute relative population and disease burden scores.

2. **Compute devaluation**

   * Apply the base formula and scaling factor.

3. **Train the XGBoost model**

   * Use AQI, disease burden, and relative population as input features.

4. **Evaluate results**

   * Measure accuracy using MAE.

5. **Calculate health risk**

   * Normalize scaled devaluation values into 0–10 risk scores.

---

## Results and insights

* AQI has a direct, quantifiable effect on **property devaluation**.
* Locations with higher AQI levels show significantly greater **loss in value per square foot**.
* **Health burden** magnifies this effect, as higher treatment costs increase overall devaluation.
* The XGBoost regression model achieves **MAE = 7.02**, confirming reliable predictions.
* Health risk scores provide a clear, interpretable scale for decision-making.

---

## Conclusion

This methodology provides a systematic way to:

* Measure property devaluation caused by air pollution.
* Incorporate health and population data for more accurate results.
* Train and validate machine learning models to refine predictions.
* Quantify health risks in a standardized, actionable format.

The approach demonstrates how environmental data and health metrics can be combined to better understand real estate market impacts.

