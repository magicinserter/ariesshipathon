import streamlit as st
from datetime import datetime
import streamlit as st
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
genai.configure(api_key=st.secrets["googleapi"])
qclient = QdrantClient(
    url="https://161a3fdc-cd95-4bca-ba74-f831daa45699.eu-west-1-0.aws.cloud.qdrant.io:6333",
    api_key= st.secrets["qdrantapi"],
)
encoder = SentenceTransformer('all-MiniLM-L6-v2')
# Create the model
generation_config = {
  "temperature": 0.1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
def search(user_input):
    hits = qclient.query_points(
    collection_name="fests",
    query=encoder.encode(user_input).tolist(),
    limit=1,
    ).points
    for hit in hits:
      return hit.payload["name"]
model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)
# import PIL.Image
# img = PIL.Image.open('/content/Screenshot 2025-01-12 at 12.41.16 PM.png')
# response = model.generate_content(["Tell me the event name, date, time and contact info from the image and show it", img], stream=True)
# response.resolve()
# print(response.text)
# Set the page configuration
st.set_page_config(
    page_title="Event Manager",
    page_icon="📅",
    layout="centered",
)

# Heading
st.title("Welcome to Event Manager 📅")

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
chat_session = model.start_chat() 
if st.button("Submit"):

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
if "messages" not in st.session_state:
    st.session_state.messages =     []

# Input form for user message
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Type your message here...")
    submit_button = st.form_submit_button("Send")

# Add user input to the chat
if submit_button and user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})
    
    response1 = chat_session.send_message(search(user_input)) 
    response = chat_session.send_message(user_input).candidates[0].content.parts[0].text 
    st.session_state.messages.append({"role": "bot", "content": response})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"*You:* {msg['content']}")
    else:
        st.markdown(f"*Bot:* {msg['content']}")

# Optional: Add a clear button
if st.button("Clear Chat"):
    st.session_state.messages = []
