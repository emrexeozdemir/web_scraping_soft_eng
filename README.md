# Web Scraper for arabam.com

This Python script is designed to scrape car listings from [arabam.com](https://www.arabam.com), extracting detailed information about each vehicle and saving it into a CSV file. The script uses Selenium to interact with the website and navigate through multiple levels of data, handling pagination and nested categories as needed.

---

## Features
- Scrapes detailed information about car listings, including:
  - Brand, series, and model
  - Year, mileage, and engine details
  - Transmission and fuel type
  - Seller information and price
  - Location and additional attributes
- Handles:
  - Categories with more than 2500 listings by iterating over specific models.
  - Pagination within listing pages.
- Saves all extracted data into a CSV file.
- Operates in headless mode for better performance.

---

## Prerequisites

### 1. Python Libraries
Ensure you have the following Python libraries installed:
- `selenium`
- `datetime`
- `csv`

You can install Selenium via pip:
```bash
pip install selenium
```

### 2. ChromeDriver
- Download the appropriate version of [ChromeDriver](https://chromedriver.chromium.org/) for your version of Google Chrome.
- Place the `chromedriver` executable in the same directory as the script or specify its location in the script.

---

## Setup and Configuration

### Headless Chrome Options
The script runs Chrome in headless mode by default. To enable this, the following option is set:
```python
options.add_argument('--headless')
```
You can disable headless mode for debugging by removing or commenting out this line.

### File Paths
- The script saves data to a file named `test.csv` by default. You can change this in the variable `csv_file_path`.

### Column Mapping
The script maps specific property keys on the website to predefined column names using the `key_to_column` dictionary. Update this mapping if arabam.com changes its structure.

---

## How to Run

1. Clone or download the repository containing the script.
2. Ensure all prerequisites are set up.
3. Run the script:
   ```bash
   python your_script_name.py
   ```

---

## Data Structure
The script extracts and saves data with the following columns:
- `ad_Id`: Advertisement ID
- `ad_date`: Advertisement date
- `ad_loc1`, `ad_loc2`: Location details
- `brand`, `series`, `model`: Vehicle brand, series, and model
- `year`: Manufacturing year
- `mileage`: Vehicle mileage
- `transmission`: Transmission type
- `fuel_type`: Type of fuel
- `body_type`: Body style
- `color`: Vehicle color
- `engine_capacity`: Engine capacity
- `engine_power`: Engine power
- `drive_type`: Drive type (e.g., front-wheel drive)
- `vehicle_condition`: Vehicle condition
- `fuel_consumption`: Fuel consumption rate
- `fuel_tank`: Fuel tank capacity
- `paint/replacement`: Paint/replacement status
- `trade_in`: Trade-in option
- `seller_type`: Type of seller
- `seller_name`: Name of the seller
- `ad_price`: Listing price
- `ad_url`: URL of the advertisement

---

## Error Handling and Debugging
- The script retries operations for dynamically loaded elements using WebDriverWait.
- Errors during processing individual listings are logged, and the script skips to the next item.
- Timeout exceptions for missing elements are handled gracefully.

---

## Limitations
- The script is tailored for arabam.com and may not work correctly if the website structure changes.
- Large datasets can take significant time to scrape, depending on the number of listings and pagination depth.

---

## Disclaimer
This script is for educational and personal use only. Ensure compliance with the terms of service of arabam.com before using this script.

---

## Contribution
Feel free to fork the repository and submit pull requests to improve the script or add new features.
