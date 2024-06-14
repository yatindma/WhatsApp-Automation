import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
import re
import time

# Define a function to validate phone numbers
def is_valid(phone):
    pattern = re.compile("(0/91)?[1-9][0-9]{9}")
    return pattern.match(phone)

# Initialize the webdriver
service = FirefoxService('/Users/yatin/Desktop/mummy-lic/geckodriver')
driver = webdriver.Firefox(service=service)

# Open WhatsApp Web and wait for the user to log in
driver.get("https://web.whatsapp.com")
print("Please scan the QR code to log in to WhatsApp Web. You have 40 seconds.")
time.sleep(120)  # Wait for 40 seconds to allow the user to log in

# Read the Excel file without headers
df = pd.read_excel('/Users/yatin/Desktop/mummy-lic/BLY_MTY_06.xlsx', header=None)

# Split the dataframe into blocks of 10 rows each
block_size = 10
start_row = 312
blocks = [df.iloc[i:i + block_size].copy() for i in range(start_row, df.shape[0], block_size)]


# Create the output directory if it doesn't exist
output_dir = '/Users/yatin/Desktop/mummy-lic/output_blocks'
os.makedirs(output_dir, exist_ok=True)

# Define the XPATH for the send button and confirmation check
send_button_xpath = '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
message_sent_xpath = '//span[@data-testid="msg-time"]'

# Function to send message and confirm
def send_whatsapp_message(driver, phone_number, message, send_button_xpath, message_sent_xpath):
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}&app_absent=0"
    driver.get(url)
    wait = WebDriverWait(driver, 5)
    try:
        # Wait for the send button to be clickable and click it 5 times
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
        for _ in range(5):
            try:
                send_button.click()
            except Exception:
                # Retry finding and clicking the send button if it becomes stale
                send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
                time.sleep(1)
                send_button.click()
        wait.until(EC.presence_of_element_located((By.XPATH, message_sent_xpath)))
        return 'sent'
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")
        return 'failed'

# Process each block and save the results
for block_index, block in enumerate(blocks):
    statuses = []
    for index, row in block.iterrows():
        phone_number = str(row[2])
        message = row[3]
        if is_valid(phone_number):
            status = send_whatsapp_message(driver, phone_number, message, send_button_xpath, message_sent_xpath)
            statuses.append(status)
        else:
            statuses.append('invalid number')
            print(f"Invalid phone number: {phone_number}")

        # Ensure a small delay between each message to avoid triggering any anti-automation mechanisms
        time.sleep(2)

    # Add statuses to the block dataframe
    block['status'] = statuses

    # Save the block dataframe to a new CSV file with semicolon delimiter
    block_output_path = os.path.join(output_dir, f'block_{block_index + 31}.csv')
    block.to_csv(block_output_path, index=False, sep=';')

# Close the webdriver
driver.quit()
