# ui/main.py

import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"

# Initialize session state
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "new_msg_trigger" not in st.session_state:
    st.session_state.new_msg_trigger = False

def add_message(customer_id, role, text):
    st.session_state.chats.setdefault(customer_id, []).append((role, text))
def transcript_upload_ui():
    st.subheader("🎙️ Upload Audio for Transcription")

    audio_file = st.file_uploader("Upload an audio file (.mp3, .wav)", type=["mp3", "wav"])

    # Button to transcribe and store results in session state
    if audio_file and st.button("Transcribe & Identify Speakers"):
        try:
            files = {"file": (audio_file.name, audio_file, audio_file.type)}
            res = requests.post(f"{API_BASE_URL}/transcribe-audio", files=files)
            output = res.json()

            if "error" in output:
                st.error(output["error"])
                return

            # Store in session_state to persist
            st.session_state.raw_transcript = output.get("raw_transcript", "")
            st.session_state.aligned_transcript = output.get("transcript", [])

        except Exception as e:
            st.error(f"❌ Error: {e!s}")

    # Only show results if transcript is available
    if "raw_transcript" in st.session_state and "aligned_transcript" in st.session_state:
        st.markdown("### 📝 Full Transcript")
        st.code(st.session_state.raw_transcript)
        full_transcript = ""
        st.markdown("### Transcript")
        for segment in st.session_state.aligned_transcript:
            text = segment.get("text", "")
            full_transcript += f"{segment.get('speaker', 'Unknown')}: {text}\n"
            st.markdown(f"{text}")

        st.divider()
        st.subheader(" AI Insights")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Summarize Transcript"):
                try:
                    res = requests.post(f"{API_BASE_URL}/summarize", json={"query": full_transcript})
                    st.success(res.json().get("summary", ""))
                except Exception:
                    st.error("Failed to get summary.")

            if st.button("Get Intent"):
                try:
                    res = requests.post(f"{API_BASE_URL}/intent", json={"query": full_transcript})
                    st.info(res.json().get("intent", "Intent not found."))
                except Exception:
                    st.error("Failed to get intent.")

            if st.button("Get Sentiment"):
                try:
                    res = requests.post(f"{API_BASE_URL}/sentiment", json={"query": full_transcript})
                    st.info(f"Sentiment: {res.json().get('sentiment', 'Unknown')}")
                except Exception:
                    st.error("Failed to analyze sentiment.")

        with col2:
            if st.button("Suggest Solution"):
                try:
                    res = requests.post(f"{API_BASE_URL}/solution", json={"query": full_transcript})
                    st.success(res.json().get("solution", "No solution suggested."))
                except Exception:
                    st.error("Failed to get solution.")

            if st.button("Response Template"):
                try:
                    res = requests.post(f"{API_BASE_URL}/response-template", json={"query": full_transcript})
                    st.code(res.json().get("template", "No template found."))
                except Exception:
                    st.error("Failed to get template.")

            if st.button("Categorize"):
                try:
                    res = requests.post(f"{API_BASE_URL}/categorize", json={"query": full_transcript})
                    st.info(res.json().get("category", "Uncategorized"))
                except Exception:
                    st.error("Failed to categorize.")


def customer_ui():
    st.title("💬 Customer Chat")

    customer_id = st.text_input("Enter your name (Customer ID)", key="cust_id")
    if not customer_id:
        st.warning("Please enter your name to start chatting.")
        return

    st.subheader("Conversation")

    chat_history = st.session_state.chats.get(customer_id, [])

    # Display chat messages
    for role, msg in chat_history:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(msg)

    user_input = st.chat_input("Type your message")

    if user_input:
        add_message(customer_id, "user", user_input)
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            res = requests.post(f"{API_BASE_URL}/chat", json={"query": user_input})
            response = res.json().get("chat", "Let me help you with that.")

        except Exception:
            response = "sorry,what is the isssue you what to know about."

        add_message(customer_id, "assistant", response)
        with st.chat_message("assistant"):
            st.markdown(response)


def agent_ui():
    st.title("🧑‍💼 Agent Dashboard")
    st.sidebar.header("Available Customers")

    if not st.session_state.chats:
        st.warning("No active customers yet.")
        return

    selected_customer = st.sidebar.selectbox("Choose customer", list(st.session_state.chats.keys()))

    if not selected_customer:
        return

    st.subheader(f"💬 Conversation with: {selected_customer}")
    chat_history = st.session_state.chats[selected_customer]

    for role, msg in chat_history:
        if role == "user":
            st.markdown(f"👤 **Customer**: {msg}")
        else:
            st.markdown(f"🤖 **Assistant**: {msg}")

    st.divider()
    st.subheader("📎 AI Retrieved Context")

    last_msg = chat_history[-1][1] if chat_history else ""
    all_user_msgs = "\n".join([msg for role, msg in chat_history if role == "user"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Summarize Conversation"):
            try:
                res = requests.post(f"{API_BASE_URL}/summarize", json={"query": all_user_msgs})
                st.success(res.json().get("summary", "No summary found."))
            except Exception:
                st.error("Failed to fetch summary.")

        if st.button("Detect Intent"):
            try:
                res = requests.post(f"{API_BASE_URL}/intent", json={"query": last_msg})
                st.info(f"Intent: {res.json().get('intent', '')}")
            except Exception:
                st.error("Failed to detect intent.")

        if st.button("Suggest Solution"):
            try:
                res = requests.post(f"{API_BASE_URL}/solution", json={"query": last_msg})
                st.success(res.json().get("solution", "No suggestion found."))
            except Exception:
                st.error("Failed to fetch solution.")

        if st.button("Categorize Conversation"):
            try:
                res = requests.post(f"{API_BASE_URL}/categorize", json={"query": all_user_msgs})
                st.info(f"Category: {res.json().get('category', '')}")
            except Exception:
                st.error("Failed to categorize.")

    with col2:
        if st.button("Get Sentiment"):
            try:
                res = requests.post(f"{API_BASE_URL}/sentiment", json={"query": last_msg})
                st.info(f"Sentiment: {res.json().get('sentiment', '')}")
            except Exception:
                st.error("Error fetching sentiment.")

        if st.button("Response Template"):
            try:
                res = requests.post(f"{API_BASE_URL}/response-template", json={"query": last_msg})
                st.success(res.json().get("template", "No template found."))
            except Exception:
                st.error("Failed to get response template.")

        if st.button("Evaluate Micro-Skills"):
            try:
                res = requests.post(f"{API_BASE_URL}/micro-skills", json={"response": last_msg})
                st.success(res.json().get("skills_feedback", "No feedback."))
            except Exception:
                st.error("Failed to evaluate micro-skills.")

        if st.button("Evaluate Quality"):
            try:
                # You can add st.text_input for a policy guideline if needed
                res = requests.post(f"{API_BASE_URL}/quality", json={"response": last_msg, "policy": ""})
                st.info(f"Evaluation: {res.json().get('evaluation', 'No evaluation')}")
            except Exception:
                st.error("Failed to assess quality.")

def main():
    st.set_page_config(page_title="Customer Service Assistant", layout="wide")
    role = st.sidebar.selectbox("Choose Role", ["Customer", "Agent", "Transcription"])
    if role == "Customer":
        customer_ui()
    elif role == "Transcription":
        transcript_upload_ui()
    else:
        agent_ui()

    # Accessing current query params, if needed
    _ = st.query_params

if __name__ == "__main__":
    main()
