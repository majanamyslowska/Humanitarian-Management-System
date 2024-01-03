# import tkinter
# from datetime import datetime, timedelta
# from tkinter import *
# from tkinter import ttk
# import sqlite3
# from connectdb import *

# def toggle_booking(self,date):
#     user_id = self.session['username']
#     if can_user_book(user_id, date):
#         print(f"Booking toggled for user {user_id} on {date.strftime('%Y-%m-%d')}")
#     else:
#         print("Booking not allowed due to availability restrictions.")

# def get_user_id(self, username):
#     with setup_conn() as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT userID FROM users WHERE username = ?", (username,))
#         user_id = cursor.fetchone()[0]
#     return user_id


# def can_user_book(user_id, date):
#     availability = get_user_bookings(user_id)
#     if availability == "full-time":
#         return True
#     elif availability == "part-time":
#         booking_count = count_weekly_bookings(user_id, date)
#         return booking_count < 3
#     else:
#         return False


# def get_user_bookings(user_id):
#     with setup_conn() as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT availability FROM users WHERE userID = ?", (user_id,))
#         availability = cursor.fetchone()[0]
#     return availability


# def count_weekly_bookings(user_id, date):
#     start_of_week = date - timedelta(days=date.weekday())
#     end_of_week = start_of_week + timedelta(days=6)
#     query = """
#     SELECT COUNT(*) FROM bookings
#     WHERE userID = ?
#     AND bookingDate BETWEEN ? AND ?
#     """
#     with setup_conn() as conn:
#         cursor = conn.cursor()
#         cursor.execute(query, (user_id, start_of_week, end_of_week))
#         count = cursor.fetchone()[0]

#     return count
