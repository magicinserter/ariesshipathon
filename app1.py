import streamlit as st
from datetime import datetime

# Set the page configuration
st.set_page_config(
    page_title="Event Suggestor",
    page_icon="📅",
    layout="centered",
)

# Heading
st.title("Welcome to Event Suggestor 📅")

# Instruction for selecting interests
st.write("### Select your areas of interest")
slots_per_row_interest = 6
events = ["Debate", "Literature", "Drama", "Music", "Indian Culture", "Hindi Samiti",
          "Robotics", "Coding", "Racing", "Hyper-Loop", "Dev (UI/UX)", "Economic"]

# Initialize session state for interests
if "interests" not in st.session_state:
    st.session_state.interests = []

rows = [events[i:i + slots_per_row_interest] for i in range(0, len(events), slots_per_row_interest)]

# Create toggle buttons (checkboxes) for interests
for row in rows:
    cols = st.columns(len(row))  # Create a column for each slot in the row
    for col, slot in zip(cols, row):
        with col:
            # Create a checkbox for each interest
            if st.checkbox(slot, key=f"interest_{slot}"):
                # Append to the interests list if not already present
                if slot not in st.session_state.interests:
                    st.session_state.interests.append(slot)
            else:
                # Remove from the interests list if unchecked
                if slot in st.session_state.interests:
                    st.session_state.interests.remove(slot)

# Initialize session state for storing free time selections
if "free_time" not in st.session_state:
    st.session_state.free_time = []

# Hour-wise slots from 9:00 to 22:00
time_slots = [f"{hour}:00 - {hour+1}:00" for hour in range(9, 22)]

# Display toggle buttons (checkboxes) for free time slots
st.write("### Select slots when you are busy:")
slots_per_row = 6
rows = [time_slots[i:i + slots_per_row] for i in range(0, len(time_slots), slots_per_row)]

for row in rows:
    cols = st.columns(len(row))  # Create a column for each slot in the row
    for col, slot in zip(cols, row):
        with col:
            # Create a checkbox for each time slot
            if st.checkbox(slot, key=f"free_time_{slot}"):
                # Append to the free_time list if not already present
                if slot not in st.session_state.free_time:
                    st.session_state.free_time.append(slot)
            else:
                # Remove from the free_time list if unchecked
                if slot in st.session_state.free_time:
                    st.session_state.free_time.remove(slot)

# Show events button
if st.button("Show events"):

        current_date = datetime.now().date()

        st.session_state.busy_list = []
        year, month, date = current_date.year, current_date.month, current_date.day  # Added date
    
        for time in st.session_state.free_time:
            start_hour = int(time.split(":")[0])  # Extracting the start hour from the busy slot string
        
        # Create start time and end time lists with the specified format (including date)
            start_time = [year, month, date, start_hour, 0]  # Added the date
            end_time = [year, month, date, start_hour + 1, 0]  # End time is 1 hour later, added the date
        
            st.session_state.busy_list.append({
                "start": start_time,
                "end": end_time
            })
        
        st.session_state.event_list = {"role":"user", "parts":"I like "}
        for likes in st.session_state.interests:
            st.session_state.event_list["parts"]+=(likes+", ")
        
        st.write(st.session_state.busy_list)
        st.write(st.session_state.event_list)   
