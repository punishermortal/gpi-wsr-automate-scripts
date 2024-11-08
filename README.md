# gpi-wsr-automate-scripts

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
