import pandas as pd

def format_price(value):
    """Format numeric price values using 'Cr' for Crores and 'L' for Lakhs."""
    try:
        value = float(value)  # Convert only if it's a number
    except ValueError:
        return value  # If already a string, return as is

    if value >= 1_00_00_000:  # 1 Crore and above
        return f"{value / 1_00_00_000:.2f} Cr"
    elif value >= 1_00_000:  # 1 Lakh and above
        return f"{value / 1_00_000:.2f} L"
    else:
        return f"{value:,.0f}"  # Regular format with commas

def csv_to_dict(file_path):
    """Convert CSV data to a list of dictionaries with proper formatting."""
    df = pd.read_csv(file_path)

    # Convert DataFrame to list of dictionaries
    data = df.to_dict(orient="records")

    # Format the price and adjusted price fields
    for p in data:
        if "price" in p:
            p["price"] = format_price(p["price"])
        if "adjusted price" in p:
            p["adjusted price"] = format_price(p["adjusted price"])

    return data

# Example usage
file_path = "properties_final.csv"  # Replace with actual path
data = csv_to_dict(file_path)
