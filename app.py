import os
import pandas as pd
import re
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from tempfile import NamedTemporaryFile

# Function to validate phone numbers
def is_valid(phone):
    pattern = re.compile("(0/91)?[1-9][0-9]{9}")
    return pattern.match(phone)

# Function to send message and confirm
def send_whatsapp_message(driver, phone_number, message, send_button_xpath, message_sent_xpath):
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}&app_absent=0"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    try:
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
        for _ in range(5):
            try:
                send_button.click()
            except Exception:
                send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
                time.sleep(2)
                send_button.click()
        wait.until(EC.presence_of_element_located((By.XPATH, message_sent_xpath)))
        return 'sent'
    except Exception as e:
        st.error(f"Failed to send message to {phone_number}: {e}")
        return 'failed'

# Streamlit UI
st.set_page_config(page_title="WhatsApp Bulk Message Sender", layout="wide")
st.markdown(
    """
    <style>
    .blurred {
        filter: blur(5px);
    }
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .next-button, .submit-button {
        display: block;
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        font-size: 18px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .next-button:hover, .submit-button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Store user information and path in session state
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "output_dir" not in st.session_state:
    st.session_state["output_dir"] = ""

st.sidebar.header("User Information")
user_name = st.sidebar.text_input("Enter your name", value=st.session_state["user_name"])
submit_user_name = st.sidebar.button("Submit")

if submit_user_name and user_name:
    st.session_state["user_name"] = user_name

if st.session_state["user_name"]:
    st.markdown(f"### Hello, {st.session_state['user_name']}!")
    st.markdown("### Step 1: Upload File")
    uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=['xlsx', 'csv'])

    if uploaded_file:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, header=None)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, header=None)

        st.write("File uploaded successfully!")
        st.write("Here is a preview of the data:")
        st.write(df.head())

        st.markdown("### Step 2: Specify Columns")
        phone_col = st.text_input("Enter the column number or name for phone numbers")
        message_col = st.text_input("Enter the column number or name for messages")
        next_button = st.button("Next", key="next")

        if next_button and phone_col and message_col:
            if phone_col.isdigit():
                phone_col = int(phone_col)
            if message_col.isdigit():
                message_col = int(message_col)

            if phone_col in df.columns and message_col in df.columns:
                st.success("Columns found in the file!")
                st.session_state["phone_col"] = phone_col
                st.session_state["message_col"] = message_col

                st.markdown("### Step 3: Select Output Directory")
                st.write("Example paths for Windows users: `C:\\Users\\username\\Documents\\output_directory`")
                output_dir = st.text_input("Enter the directory path to save the results",
                                           value=st.session_state["output_dir"], key="output_dir_input")
                set_output_dir = st.button("Set Output Directory")

                if set_output_dir and output_dir:
                    st.session_state["output_dir"] = output_dir
                    os.makedirs(output_dir, exist_ok=True)
                    st.write(f"Selected directory: {output_dir}")

                if st.session_state["output_dir"]:
                    st.markdown("### Step 4: Upload GeckoDriver")
                    gecko_file = st.file_uploader("Choose GeckoDriver file")
                    if gecko_file:
                        with NamedTemporaryFile(delete=False) as tmp_file:
                            tmp_file.write(gecko_file.read())
                            gecko_path = tmp_file.name
                            os.chmod(gecko_path, 0o755)  # Fix permissions

                        service = FirefoxService(gecko_path)
                        driver = webdriver.Firefox(service=service)

                        st.markdown("### Step 5: Log in to WhatsApp Web")
                        driver.get("https://web.whatsapp.com")
                        st.info("You have 80 seconds to log in.")
                        time.sleep(80)

                        send_button_xpath = '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
                        message_sent_xpath = '//span[@data-testid="msg-time"]'

                        block_size = 10
                        blocks = [df.iloc[i:i + block_size].copy() for i in range(0, df.shape[0], block_size)]

                        for block_index, block in enumerate(blocks):
                            statuses = []
                            for index, row in block.iterrows():
                                phone_number = str(row[st.session_state["phone_col"]])
                                message = row[st.session_state["message_col"]]
                                if is_valid(phone_number):
                                    status = send_whatsapp_message(driver, phone_number, message, send_button_xpath, message_sent_xpath)
                                    statuses.append(status)
                                else:
                                    statuses.append('invalid number')
                                    st.warning(f"Invalid phone number: {phone_number}")
                                time.sleep(2)
                            block['status'] = statuses
                            block_output_path = os.path.join(st.session_state["output_dir"], f'block_{block_index + 1}.csv')
                            block.to_csv(block_output_path, index=False, sep=';')
                            st.success(f"Block {block_index + 1} saved successfully!")
                        driver.quit()
                        st.success("All messages sent and results saved!")
            else:
                st.error("Column not found in the file. Please check the column names or numbers.")
