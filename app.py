import streamlit as st
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
genai.configure(api_key="AIzaSyDg507o-EmMj0D0A6weeV2VIl5BpKBYcd0")
qclient = QdrantClient(
    url="https://161a3fdc-cd95-4bca-ba74-f831daa45699.eu-west-1-0.aws.cloud.qdrant.io:6333",
    api_key= "6n6IfBtsHusmZIiHWvz5lZa0rW5SNa8DuZHY4B97KVcYO6yOddCPYg",
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


chat_session = model.start_chat()


# Set up the page configuration
st.set_page_config(
    page_title="Welcome to IIT Delhi",
    page_icon="💬",
    layout="centered",
)

# App title
st.title("Welcome to IIT Delhi 💬")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input form for user message
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Type your message here...")
    submit_button = st.form_submit_button("Send")

# Add user input to the chat
if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Placeholder response from the bot
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
