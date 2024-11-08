import mysql.connector
from mysql.connector import Error
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

class DataReport:
    def __init__(self, host_mt, database_mt, user_mt, password_mt, host_mirror, database_mirror, user_mirror, password_mirror, recipient_email):
        self.host_mt = host_mt
        self.database_mt = database_mt
        self.user_mt = user_mt
        self.password_mt = password_mt
        self.host_mirror = host_mirror
        self.database_mirror = database_mirror
        self.user_mirror = user_mirror
        self.password_mirror = password_mirror
        self.recipient_email = recipient_email
        self.pdf_filename = "active_user_count.pdf"

    def previous_monday(self, k=0):
        # return "2024-07-05"
        today = datetime.now()
        days_to_subtract = today.weekday() + 7 + k
        last_monday = today - timedelta(days=days_to_subtract)
        return last_monday.strftime("%Y-%m-%d")

    def last_sunday(self):
        # return "2024-07-10"
        today = datetime.now()
        days_to_subtract = today.weekday() + 1
        last_sunday = today - timedelta(days=days_to_subtract)
        return last_sunday.strftime("%Y-%m-%d")

    def fetch_active_user_count(self):
        try:
            connection = mysql.connector.connect(
                host=self.host_mirror,
                database=self.database_mirror,
                user=self.user_mirror,
                password=self.password_mirror
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT count(*) FROM abc.master_user WHERE status = 1")
                result = cursor.fetchone()
                return result[0]
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_attendance_data(self):
        try:
            connection = mysql.connector.connect(
                host=self.host_mirror,
                port=3306,
                database=self.database_mirror,
                user=self.user_mirror,
                password=self.password_mirror
            )
            if connection.is_connected():
                cursor = connection.cursor()
                query = f'''
                    SELECT date(added_on) AS login_date, count(*) AS login_count
                    FROM abc.master_user_attendance
                    WHERE added_on >= "{self.previous_monday()}" AND added_on <= "{self.last_sunday()}"
                    GROUP BY date(added_on)
                '''
                cursor.execute(query)
                return cursor.fetchall()
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_mt_order_data(self):
        try:
            connection = mysql.connector.connect(
                host=self.host_mt,
                database=self.database_mt,
                port=3306,
                user=self.user_mt,
                password=self.password_mt
            )
            if connection.is_connected():
                cursor = connection.cursor()
                query = f'''
                    SELECT DATE(order_date) AS day_of_month, COUNT(*) AS mortal
                    FROM wsr_mt.orders
                    WHERE order_date BETWEEN '{self.previous_monday()}' AND '{self.last_sunday()}'
                    GROUP BY DATE(order_date);
                '''
                cursor.execute(query)
                return cursor.fetchall()
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_mt_attendance_data(self):
        try:
            connection = mysql.connector.connect(
                host=self.host_mt,
                database=self.database_mt,
                user=self.user_mt,
                password=self.password_mt
            )
            if connection.is_connected():
                cursor = connection.cursor()
                query = f'''
                    SELECT DATE(checkin_date) AS day_of_month, COUNT(*) AS mortal
                    FROM wsr_mt.attendances
                    WHERE checkin_date BETWEEN '{self.previous_monday()}' AND '{self.last_sunday()}'
                    GROUP BY DATE(checkin_date);
                '''
                cursor.execute(query)
                return cursor.fetchall()
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_mt_active_user_count(self):
        try:
            connection = mysql.connector.connect(
                host=self.host_mt,
                database=self.database_mt,
                user=self.user_mt,
                password=self.password_mt
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM wsr_mt.users WHERE is_active = 1")
                result = cursor.fetchone()
                return result[0]
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def create_pdf(self, user_count, attendance_data, mt_order_data, mt_attendance_data, mt_active_user_count):
        c = canvas.Canvas(self.pdf_filename, pagesize=letter)

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 750, f"Active User Count: {user_count}")

        y_position = 730
        c.drawString(100, y_position, "Attendance Data:")
        y_position -= 20

        c.setFont("Helvetica", 12)
        for login_date, login_count in attendance_data:
            c.drawString(100, y_position, f"Date: {login_date}, Login Count: {login_count}")
            y_position -= 20

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, "MT Order Data:")
        y_position -= 20

        c.setFont("Helvetica", 12)
        for order_date, order_count in mt_order_data:
            c.drawString(100, y_position, f"Date: {order_date}, Order Count: {order_count}")
            y_position -= 20

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, "MT Attendance Data:")
        y_position -= 20

        c.setFont("Helvetica", 12)
        for attendance_date, attendance_count in mt_attendance_data:
            c.drawString(100, y_position, f"Date: {attendance_date}, Attendance Count: {attendance_count}")
            y_position -= 20

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, f"MT Active User Count: {mt_active_user_count}")
        y_position -= 20

        c.save()
        print(f"PDF saved as {self.pdf_filename}")

    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = 'your_email@gmail.com'
        msg['To'] = self.recipient_email
        msg['Subject'] = 'Active User Report'

        body = 'Please find attached the active user report.'
        msg.attach(MIMEText(body, 'plain'))

        with open(self.pdf_filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {self.pdf_filename}')

        msg.attach(part)

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('mortalp369@gmail.com', ' Use an app password if 2FA is enabled') 
                server.send_message(msg)
                print(f"Email sent to {self.recipient_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def generate_report(self):
        active_user_count = self.fetch_active_user_count()
        attendance_data = self.fetch_attendance_data()
        mt_order_data = self.fetch_mt_order_data()
        mt_attendance_data = self.fetch_mt_attendance_data()
        mt_active_user_count = self.fetch_mt_active_user_count()

        if (
            active_user_count is not None 
            and attendance_data is not None 
            and mt_order_data is not None 
            and mt_attendance_data is not None 
            and mt_active_user_count is not None
        ):
            self.create_pdf(active_user_count, attendance_data, mt_order_data, mt_attendance_data, mt_active_user_count)
            self.send_email()


def main():
    # Database connection details
    host_mt = 'localhost'
    database_mt = 'wsr_mt'
    user_mt = 'bh aiji'
    password_mt = 'mortal@1'

    host_mirror = 'localhost'
    database_mirror = 'abc'
    user_mirror = 'bhaiji'
    password_mirror = 'mortal@1'


    recipient_email = 'dhirajs@triazinesoft.com'

    report = DataReport(host_mt, database_mt, user_mt, password_mt, host_mirror, database_mirror, user_mirror, password_mirror, recipient_email)
    report.generate_report()

if __name__ == "__main__":
    main()
