from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv
import time
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('--headless')
service = Service(executable="chromedriver.exe")
driver = webdriver.Chrome(service=service,options=options)

csv_file_path = "test.csv"
place_holder = "Belirtilmemiş"
start_time = datetime.now()
columns = [
                "ad_Id",
                "ad_date",
                "ad_loc1",
                "ad_loc2",
                "brand",
                "series",
                "model",
                "year",
                "mileage",
                "transmission",
                "fuel_type",
                "body_type",
                "color",
                "engine_capacity",
                "engine_power",
                "drive_type",
                "vehicle_condition",
                "fuel_consumption",
                "fuel_tank",
                "paint/replacement",
                "trade_in",
                "seller_type",
                "seller_name",
                "ad_price",
                "ad_url"
            ]

key_to_column = {
    "İlan No": "ad_Id",
    "İlan Tarihi": "ad_date",
    "Marka": "brand",
    "Seri": "series",
    "Model": "model",
    "Yıl": "year",
    "Kilometre": "mileage",
    "Vites Tipi": "transmission",
    "Yakıt Tipi": "fuel_type",
    "Kasa Tipi": "body_type",
    "Renk": "color",
    "Motor Hacmi": "engine_capacity",
    "Motor Gücü": "engine_power",
    "Çekiş": "drive_type",
    "Araç Durumu": "vehicle_condition",
    "Ortalama Yakıt Tüketimi": "fuel_consumption",
    "Yakıt Deposu": "fuel_tank",
    "Boya-değişen": "paint/replacement",
    "Takasa Uygun": "trade_in",
    "Kimden": "seller_type"
}

driver.get("https://www.arabam.com/ikinci-el/otomobil")

brand_list_parent = driver.find_element(By.CSS_SELECTOR, ".category-list-wrapper")
brand_list = brand_list_parent.find_elements(By.CSS_SELECTOR, ".inner-list")

#markaları tek tek geziyoruz
for index in range(len(brand_list)):
    try:
        brand_list_parent = driver.find_element(By.CSS_SELECTOR, ".category-list-wrapper")
        brand_list = brand_list_parent.find_elements(By.CSS_SELECTOR, ".inner-list")
        brand_url = brand_list[index].find_element(By.TAG_NAME,"a").get_attribute("href")+"?take=50"
        driver.get(brand_url)
        brand_count = driver.find_element(By.XPATH, '//*[@id="facet-desktop"]/div[2]/span/form/div[1]/div/div/div[1]/div/ul/li/ul/li/a/span[2]')
        brand_count_int = int(brand_count.text.replace(".",""))
        print(brand_count_int)
        #eğer markanın 2500den fazla ilanı varsa modelleri tek tek gezip ilanları kaydetmemiz lazım
        #yani aslında inception bir işlem oluyor aynı şeyleri bir daha yapıyoruz
        if brand_count_int > 2500:
            model_parent = driver.find_element(By.CSS_SELECTOR, ".category-list-wrapper")
            model_list = model_parent.find_elements(By.CSS_SELECTOR, ".inner-list")
            for index in range(len(model_list)):
                model_parent = driver.find_element(By.CSS_SELECTOR, ".category-list-wrapper")
                model_list = model_parent.find_elements(By.CSS_SELECTOR, ".inner-list")
                model_url = model_list[index].find_element(By.TAG_NAME,"a").get_attribute("href")+"?take=50"
                driver.get(model_url)
                try:
                    # Locate the pagination container
                    pagination = driver.find_element(By.CSS_SELECTOR, "ul.pagination")

                    # Find all <li> elements in the pagination
                    page_items = pagination.find_elements(By.CSS_SELECTOR, "li")

                    # Loop through the items to find the last page number
                    last_page_number = 1  # Default to 1 if no pages found
                    for item in page_items:
                        try:
                            # Extract the page number from the <a> element if it exists
                            page_link = item.find_element(By.TAG_NAME, "a")
                            page_number = int(page_link.text.strip())
                            last_page_number = max(last_page_number, page_number)
                        except Exception:
                            # Skip items without <a> tags or non-numeric content
                            continue
                except Exception as e:
                    print(f"Error extracting last page number: {e}")
                for index_page in range(last_page_number):
                    print("index page: ", index_page)
                    current_url = model_url + f"&page={index_page + 1}"
                    driver.get(current_url)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "tr[class='listing-list-item should-hover bg-white']"))
                    )
                    car_list = driver.find_elements(By.CSS_SELECTOR, "tr[class='listing-list-item should-hover bg-white']")
                    for index_ad in range(len(car_list)):
                        car_url = car_list[index_ad].find_element(By.TAG_NAME, 'a').get_attribute('href')
                        driver.execute_script("window.open(arguments[0]);", car_url)
                        driver.switch_to.window(driver.window_handles[-1])

                        ad_data = {column: None for column in columns}
                        try:
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located(
                                    (By.CSS_SELECTOR, "tr[class='listing-list-item should-hover bg-white']"))
                            )
                        except TimeoutException:
                            print("No listings found on the current page.")
                            continue  # Skip to the next iteration
                        property_items = driver.find_elements(By.CSS_SELECTOR, ".property-item")
                        for item in property_items:
                            try:
                                key = item.find_element(By.CSS_SELECTOR, ".property-key").text.strip()
                                value_element = item.find_element(By.CSS_SELECTOR, ".property-value")
                                value = value_element.text.strip()
                                column_name = key_to_column.get(key)  # Use the mapping
                                if column_name:
                                    ad_data[column_name] = value

                            except Exception as e:
                                print(f"Error processing property item: {e}")
                            try:
                                ad_loc = driver.find_element(By.CSS_SELECTOR, '.product-location').text
                                loc1, loc2 = ad_loc.split(",")
                                ad_data["ad_loc1"] = loc1
                                ad_data["ad_loc2"] = loc2

                            except Exception as e:
                                continue
                            ad_data["seller_name"] = driver.find_element(By.CSS_SELECTOR, ".advert-owner-name").text.strip()
                            # ad_data["ad_price"] = driver.find_element(By.CSS_SELECTOR,'.product-price').text.strip()
                            ad_data["ad_price"] = driver.find_element(By.XPATH,
                                                                      '//*[@data-testid="desktop-information-price"]').text.strip()
                            ad_data["ad_url"] = car_url
                        print(ad_data)
                        processed_data = [ad_data[column] if ad_data[column] is not None else place_holder for column in
                                          columns]
                        with open(csv_file_path, mode="a", newline="", encoding="utf-8-sig") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(processed_data)
                        print("row added")
                        current_time = datetime.now()
                        print(current_time - start_time)
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                driver.get(brand_url)

        else:
            try:
                # Locate the pagination container
                pagination = driver.find_element(By.CSS_SELECTOR, "ul.pagination")

                # Find all <li> elements in the pagination
                page_items = pagination.find_elements(By.CSS_SELECTOR, "li")

                # Loop through the items to find the last page number
                last_page_number = 1  # Default to 1 if no pages found
                for item in page_items:
                    try:
                        # Extract the page number from the <a> element if it exists
                        page_link = item.find_element(By.TAG_NAME, "a")
                        page_number = int(page_link.text.strip())
                        last_page_number = max(last_page_number, page_number)
                    except Exception:
                        # Skip items without <a> tags or non-numeric content
                        continue
            except Exception as e:
                print(f"Error extracting last page number: {e}")
            for index_page in range(last_page_number):
                print("index page: ", index_page)
                current_url = brand_url + f"&page={index_page+1}"
                driver.get(current_url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "tr[class='listing-list-item should-hover bg-white']"))
                )
                car_list = driver.find_elements(By.CSS_SELECTOR, "tr[class='listing-list-item should-hover bg-white']")
                for index_ad in range(len(car_list)):
                    car_url = car_list[index_ad].find_element(By.TAG_NAME, 'a').get_attribute('href')
                    driver.execute_script("window.open(arguments[0]);", car_url)
                    driver.switch_to.window(driver.window_handles[-1])

                    ad_data = {column: None for column in columns}
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, "tr[class='listing-list-item should-hover bg-white']"))
                        )
                    except TimeoutException:
                        print("No listings found on the current page.")
                        continue  # Skip to the next iteration
                    property_items = driver.find_elements(By.CSS_SELECTOR, ".property-item")
                    for item in property_items:
                        try:
                            key = item.find_element(By.CSS_SELECTOR, ".property-key").text.strip()
                            value_element = item.find_element(By.CSS_SELECTOR, ".property-value")
                            value = value_element.text.strip()
                            column_name = key_to_column.get(key)  # Use the mapping
                            if column_name:
                                ad_data[column_name] = value

                        except Exception as e:
                            print(f"Error processing property item: {e}")
                        try:
                            ad_loc = driver.find_element(By.CSS_SELECTOR,'.product-location').text
                            loc1,loc2 = ad_loc.split(",")
                            ad_data["ad_loc1"] = loc1
                            ad_data["ad_loc2"] = loc2

                        except Exception as e:
                            continue
                        ad_data["seller_name"] = driver.find_element(By.CSS_SELECTOR,".advert-owner-name").text.strip()
                        #ad_data["ad_price"] = driver.find_element(By.CSS_SELECTOR,'.product-price').text.strip()
                        ad_data["ad_price"] = driver.find_element(By.XPATH,'//*[@data-testid="desktop-information-price"]').text.strip()
                        ad_data["ad_url"] = car_url
                    print(ad_data)
                    processed_data = [ad_data[column] if ad_data[column] is not None else place_holder for column in columns]
                    with open(csv_file_path, mode="a", newline="", encoding="utf-8-sig") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(processed_data)
                    print("row added")
                    current_time = datetime.now()
                    print(current_time - start_time)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
        driver.get("https://www.arabam.com/ikinci-el/otomobil")
        time.sleep(1)
    except TimeoutException:
        continue