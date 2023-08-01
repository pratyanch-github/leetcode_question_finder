import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setting up the driver
chrome_driver_path = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# CSS selectors to extract required data from each problem page
header_selector = ".mr-2.text-label-1"
body_selector = ".px-5.pt-4"
index = 1
questions_data_folder = "qData"

def append_text_to_file(filename, text):
    with open(filename, "a") as file:
        file.write(text + '\n')

def create_file_and_write_text(file_path, text):
    folder_path = os.path.dirname(file_path)
    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, "w", encoding="utf-8", errors="ignore") as new_file:
        new_file.write(text)

def get_problem_data(link, index):
    try:
        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, body_selector)))
        time.sleep(1)
        header = driver.find_element(By.CSS_SELECTOR, header_selector)
        body = driver.find_element(By.CSS_SELECTOR, body_selector)
        print(header.text)
        if header.text:
            append_text_to_file(os.path.join(questions_data_folder, "index.txt"), header.text)
            append_text_to_file(os.path.join(questions_data_folder, "Qlink.txt"), link)
            create_file_and_write_text(os.path.join(questions_data_folder, str(index), str(index) + ".txt"), body.text)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

# Extracting all links that we scraped and cleaned
links = []
with open("lc_problems.txt", "r") as file:
    for line in file:
        links.append(line.strip())

# Extracting data from each link and storing them in files in a new folder named questions_data.
for link in links:
    is_found = get_problem_data(link, index)
    if is_found:
        index += 1

print("Total number of questions scraped:", index - 1)
driver.quit()
