from supabase import create_client, Client

# Replace these with your Supabase project details
SUPABASE_URL = "https://kddfapqhvjvjsllwppfd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkZGZhcHFodmp2anNsbHdwcGZkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MzAwNDcyNiwiZXhwIjoyMDU4NTgwNzI2fQ.xg1UXZHOkWLaRGYerEtUSq-oWXw8wAKpwPgNqXXXjEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch all rows from the 'properties' table
response = supabase.table('properties').select('*').execute()

# Print the data
if response.data:
    for row in response.data:
        print(f"Property: {row['property_name']}")
        print(f"About: {row['about']}")
        print(f"Location: {row['location']}")
        print(f"Size: {row['size']} | Sqft: {row['total_sqft']} | Bath: {row['bath']} | Balcony: {row['balcony']}")
        print(f"Price per Sqft: {row['price_per_sqft']} | Price (Lakhs): {row['predicted_price_lakhs']}")
        print(f"Contact: {row['contact']}\n{'-'*50}\n")
else:
    print("No data found.")
