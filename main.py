from datetime import datetime, timedelta

def previous_monday(k=0):
    today = datetime.now()
    days_to_subtract = today.weekday() + 7 + k
    last_monday = today - timedelta(days=days_to_subtract)
    return last_monday.strftime("%Y-%m-%d")

def last_sunday():
    today = datetime.now()
    days_to_subtract = today.weekday() + 1
    last_sunday = today - timedelta(days=days_to_subtract)
    return last_sunday.strftime("%Y-%m-%d")
print()
print()
print()
print()
print()

print("SELECT count(*) FROM gpil_db.master_user WHERE status = 1")
print()


query_mirror_attendance = f'''
SELECT date(added_on) AS login_date, count(*) AS login_count
FROM gpil_db.master_user_attendance
WHERE added_on >= "{previous_monday()}" AND added_on <= "{last_sunday()}"
GROUP BY date(added_on)
'''
print()
print(query_mirror_attendance)
query_mt_orders = f'''
SELECT DATE(order_date) AS day_of_month, COUNT(*) AS mortal
FROM db_mtprod.orders
WHERE order_date BETWEEN '{previous_monday()}' AND '{last_sunday()}'
GROUP BY DATE(order_date);
'''
print()
print(query_mt_orders)
query_mt_attendance = f'''
SELECT DATE(checkin_date) AS day_of_month, COUNT(*) AS mortal
FROM db_mtprod.attendances
WHERE checkin_date BETWEEN '{previous_monday()}' AND '{last_sunday()}'
GROUP BY DATE(checkin_date);
'''
print()

print()
print(query_mt_attendance)
print()
print()

print("SELECT COUNT(*) FROM db_mtprod.users WHERE is_active = 1")
