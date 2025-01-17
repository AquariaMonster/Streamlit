import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("taskmanager-448113-3daa3be90edb.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("TaskManager").sheet1

# Function to add a task
def add_task(task):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([task, "Pending", current_time])

# Function to mark a task as completed
def complete_task(task_index):
    sheet.update_cell(task_index + 2, 2, "Completed")  # +2 because headers are in row 1

# Function to get all tasks
def get_tasks():
    return sheet.get_all_records()

# Streamlit app
st.title("Task Manager")

# Add a new task
st.header("Add a New Task")
new_task = st.text_input("Enter a new task:")
if st.button("Add Task"):
    if new_task:
        add_task(new_task)
        st.success("Task added successfully!")
    else:
        st.error("Please enter a task.")

# View all tasks
st.header("All Tasks")
tasks = get_tasks()
if tasks:
    df = pd.DataFrame(tasks)
    st.dataframe(df)

    # Mark tasks as completed
    st.header("Mark Tasks as Completed")
    task_index = st.selectbox("Select a task to mark as completed:", range(len(tasks)))
    if st.button("Mark as Completed"):
        complete_task(task_index)
        st.success("Task marked as completed!")
else:
    st.info("No tasks found.")