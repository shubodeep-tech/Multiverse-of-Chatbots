import streamlit as st
from groq import Groq

st.set_page_config(page_title="Multiverse Chatbot", page_icon="🤖")
st.title(" Multiverse Chatbot")


with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Groq API Key", type="password")

    personality = st.selectbox(
        "Choose a personality",
        ["Friendly Assistant", "Sarcastic Robot", "Pirate", "Shakespearean Poet"]
    )

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


client = None
if api_key:
    client = Groq(api_key=api_key)


personality_prompts = {
    "Friendly Assistant": "You are a warm, helpful, friendly assistant.",
    "Sarcastic Robot": "You are a sarcastic robot who answers with dry wit.",
    "Pirate": "You are a pirate who speaks in pirate slang.",
    "Shakespearean Poet": "You respond only in Shakespearean English, poetically.",
}


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_message := st.chat_input("Say something..."):

    if not api_key:
        st.error("Please enter your Groq API key in the sidebar first.")
        st.stop()

    # Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_message)

  
    st.session_state.messages.append({"role": "user", "content": user_message})

    api_messages = [{"role": "system", "content": personality_prompts[personality]}]
    for m in st.session_state.messages:
        api_messages.append({"role": m["role"], "content": m["content"]})

   
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                stream=True,
            )
            response_text = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
            )
        except Exception as e:
            st.error(f"Error calling Groq API: {e}")
            st.stop()

 
    st.session_state.messages.append({"role": "assistant", "content": response_text})