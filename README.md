
# WhatsApp Bulk Message Sender 📲💬

Welcome to the WhatsApp Bulk Message Sender! This tool allows you to send personalized messages to multiple contacts via WhatsApp Web. It uses Selenium for web automation and pandas for handling Excel/CSV files. The application is designed to automate the process of sending messages in bulk efficiently and effectively.

## Developer Information
**Developer:** Yatin Arora

## Features
- **Bulk Messaging:** Send messages to multiple contacts from an Excel or CSV file.
- **Validation:** Validates phone numbers to ensure they are in the correct format.
- **Block Processing:** Processes contacts in blocks of 10 to avoid triggering anti-automation mechanisms.
- **Streamlit UI:** User-friendly interface for uploading files, specifying columns, and setting output directories.

## Installation and Setup

### Prerequisites
- Python 3.x
- Firefox browser
- GeckoDriver for Selenium

### Python Libraries
Install the required libraries using pip:
```sh
pip install pandas selenium streamlit
```

### GeckoDriver
Download the GeckoDriver from [Mozilla GeckoDriver](https://github.com/mozilla/geckodriver/releases) and place it in a known directory.

## Usage

### Running the Script
1. **Initialize the WebDriver:**
   Update the path to your GeckoDriver in the script:
   ```python
   service = FirefoxService('/path/to/geckodriver')
   driver = webdriver.Firefox(service=service)
   ```

2. **Run the Script:**
   ```sh
   python whatsapp_bulk_sender.py
   ```

### Using the Streamlit Application
1. **Run the Streamlit App:**
   ```sh
   streamlit run whatsapp_bulk_sender_app.py
   ```

2. **Upload Your File:**
   - Upload an Excel or CSV file containing phone numbers and messages.

3. **Specify Columns:**
   - Enter the column numbers or names for phone numbers and messages.

4. **Set Output Directory:**
   - Provide the directory path where the results will be saved.

5. **Upload GeckoDriver:**
   - Upload your GeckoDriver file.

6. **Log in to WhatsApp Web:**
   - Log in to WhatsApp Web within the provided time.

7. **Send Messages:**
   - The application will send messages and save the status of each contact.

## Example File Format

Your Excel/CSV file should be formatted as follows:
| Column 1 | Column 2 | Phone Number | Message         |
|----------|----------|--------------|-----------------|
| Data     | Data     | 919876543210 | Hello, John Doe |
| Data     | Data     | 911234567890 | Hi, Jane Smith  |

## Output
The results are saved as CSV files in the specified output directory. Each block of 10 contacts is saved as a separate file.

## Notes
- Ensure that your phone numbers are in the correct format.
- Make sure to scan the QR code and log in to WhatsApp Web within the provided time.

## Contributing
Feel free to contribute to the project by submitting issues or pull requests. Let's make this tool even better together!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
Thanks to the developers of pandas, selenium, and streamlit for providing these amazing tools. Special thanks to the contributors of open-source projects.

![WhatsApp Logo](https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg)
