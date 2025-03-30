from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from datetime import datetime, timedelta

# Setup Selenium Chrome Driver
driver = webdriver.Chrome()

# Open your AQI website
driver.get('https://airquality.cpcb.gov.in/AQI_India/')  # Change to actual URL

time.sleep(3)  # Let the page load

# ✅ Step 1: Fetch all station names from the dropdown
station_dropdown = Select(driver.find_element(By.ID, 'station-dropdown'))  # Change ID accordingly
stations = [option.text for option in station_dropdown.options]
print(f"Stations found: {stations}")

# ✅ Step 2: Prepare date range (Example: past 7 days - change as needed)
data = []
start_date = datetime.today() - timedelta(days=7)

for station in stations:
    station_dropdown.select_by_visible_text(station)
    time.sleep(1)  # Small wait after changing station

    # Loop through past 7 days (change range for 1 year if needed)
    for i in range(8):  # 0 to 7 = 8 days
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')  # Adjust format based on website

        # ✅ Step 3: Set the date
        date_input = driver.find_element(By.ID, 'date-input')  # Change ID accordingly
        date_input.clear()
        date_input.send_keys(date_str)

        # ✅ Step 4: Submit / load AQI data
        driver.find_element(By.ID, 'submit-btn').click()  # Change ID accordingly
        time.sleep(2)  # Wait for data to load

        # ✅ Step 5: Scrape AQI Value
        try:
            aqi_value = driver.find_element(By.CLASS_NAME, 'aqi-value').text  # Change class
            print(f"{station} | {date_str} | AQI: {aqi_value}")
            data.append([station, date_str, aqi_value])
        except Exception as e:
            print(f"Data not found for {station} on {date_str}")
            data.append([station, date_str, 'N/A'])

# ✅ Step 6: Save to CSV
df = pd.DataFrame(data, columns=["Station", "Date", "AQI"])
df.to_csv('aqi_data.csv', index=False)
print("✅ AQI Data saved to 'aqi_data.csv'")

# ✅ Done
driver.quit()
