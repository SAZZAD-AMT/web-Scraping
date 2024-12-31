import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
# Set up the WebDriver
driver = webdriver.Chrome()  # Ensure 'chromedriver' is in PATH

# Open the URL
url = "https://www.bgmea.com.bd/page/member-list?page=1"
driver.get(url)

# Scrape company names
company_details = []
while True:
    # Find all company names
    rows = driver.find_elements(By.XPATH, "/html/body/div/div[4]/div[4]/table/tbody/tr")
    for row in rows:
        company_name = row.find_element(By.XPATH, "./td[1]").text.strip()  # First <td> in each row
        company_url = row.find_element(By.XPATH, "./td[5]/a").get_attribute("href")  # Extract URL from the <a> tag
        
        # Navigate to the company detail page
        driver.get(company_url)

        # Extract details from the company detail page using XPaths
        try:
            position = driver.find_element(By.XPATH, "//*[@id='company_info']/div/div/table/tbody/tr[3]/td/table/tbody/tr/td[1]").text.strip()
        except:
            position = "Not Available"
        
        try:
            name = driver.find_element(By.XPATH, "//*[@id='company_info']/div/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]").text.strip()
        except:
            name = "Not Available"
        
        try:
            mobile_no = driver.find_element(By.XPATH, "//*[@id='company_info']/div/div/table/tbody/tr[3]/td/table/tbody/tr/td[3]").text.strip()
        except:
            mobile_no = "Not Available"
        
        try:
            # Navigate to mailing address and factory address section (click on the second link)
            mailing_address_link = driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div/div[1]/div/ul/li[2]/a")
            mailing_address_link.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='address_info']/table/tbody/tr[3]/td")))  # Wait until the element is loaded

            mailing_address = driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div/div[1]/div/div/div[2]/table/tbody/tr[5]/td").text.strip()
            factory_address = driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div/div[1]/div/div/div[2]/table/tbody/tr[8]/td").text.strip()
        except NoSuchElementException:
            mailing_address = "Not Available"
            factory_address = "Not Available"

        # Save all details
        company_details.append({
            "company_name": company_name,
            "position": position,
            "name": name,
            "mobile_no": mobile_no,
            "mailing_address": mailing_address,
            "factory_address": factory_address
        })
        # Write results to CSV file
        with open('company_details.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["company_name", "position", "name", "mobile_no", "mailing_address", "factory_address"])
            writer.writeheader()  # Write the header
            for company in company_details:
                writer.writerow(company) 
                print(company)
        # Go back to the main list page
        driver.back()
        time.sleep(1)
    
    # Check for the next button and click if available
    try:
        next_button = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[5]/nav/ul/li[9]")  # Adjusted XPath for "Next" button
        next_button.click()
        time.sleep(1)
    except:
        break  # Exit if there's no "Next" button

# Close the driver
driver.quit()

print("Data has been written to 'company_details.csv'.")
