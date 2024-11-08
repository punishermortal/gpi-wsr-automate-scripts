# gpi-wsr-automate-scripts and redme of primary data push is below after 63 line

# Active User Report Generator

This Python script generates a report for active users and attendance data, and sends it via email as a PDF attachment. It fetches data from two MySQL databases (MT and Mirror) and creates a detailed report including:

- Active User Count
- User Attendance Data
- MT Order Data
- MT Attendance Data

The report is generated as a PDF and emailed to the recipient specified.

## Features

- Connects to two MySQL databases (MT and Mirror)
- Fetches user attendance, active user count, MT orders, and MT attendance data
- Generates a PDF report with the fetched data
- Sends the report via email as a PDF attachment

## Prerequisites

Ensure the following are installed:

- Python 3.x
- MySQL Connector for Python: `mysql-connector-python`
- ReportLab for PDF generation: `reportlab`
- smtplib for sending emails (built-in Python module)

## Installation

1. Clone this repository or copy the script to your local machine.
2. Install the required dependencies:

   ```bash
   pip install mysql-connector-python reportlab


# Database connection details
host_mt = 'your_mt_database_host'
database_mt = 'your_mt_database_name'
user_mt = 'your_mt_database_user'
password_mt = 'your_mt_database_password'

host_mirror = 'your_mirror_database_host'
database_mirror = 'your_mirror_database_name'
user_mirror = 'your_mirror_database_user'
password_mirror = 'your_mirror_database_password'



# Email Configuration
msg['From'] = 'your_email@gmail.com'
msg['To'] = 'recipient_email@example.com'

# SMTP Configuration
server.login('your_email@gmail.com', 'your_email_password_or_app_password')

# Run the script:

python report_generator.py



# PRIMARY DATA PUSH

# XLS to JSON Processor with API Integration

This project is a Python-based tool designed to automate the conversion of `.xls` files to JSON format, followed by posting the JSON data to an API and saving the API's response into a CSV file. It is particularly useful for processing batches of `.xls` files from a folder and interacting with REST APIs.

## Features

- Convert `.xls` files to JSON format.
- Post JSON data to a specified API endpoint.
- Save API responses as CSV files for further analysis.
- Logging system to track the progress of the data processing and handle errors.

## Requirements

- Python 3.x
- The following Python libraries are required:
  - `pandas`: for handling Excel and CSV file operations.
  - `requests`: for making HTTP API requests.
  - `openpyxl`: for reading Excel files.
  - `logging`: for logging progress and errors.

## Installation

1. Clone the repository or download the script files to your local system:

   ```bash
   git clone https://github.com/punishermortal/gpi-wsr-automate-scripts.git
   cd primarydata

# Update the Script

folder_path: str = '/path/to/your/xls/files'
api_url: str = 'https://api.example.com/v1/endpoint'
token: str = 'your-api-token'

#  Running the Script
python data_processor.py
