import streamlit as st
import google.generativeai as genai
import time
import json

st.title("CICR AI Powered ChatBOT")

userImage = 'images/userImage.jpg'
assistantImage = 'images/cicrRobo.jpg'

with open('cicrData.json','r') as file:
    cicrData = json.load(file)  # Load JSON into a Python dictionary

if "messages" not in st.session_state and "cicrData" not in st.session_state:
    st.session_state.messages = [{"role" : "assistant","parts":[{"text":"Hey I am here to help you with CICR related queries !!",'avatar':assistantImage}]}]
    st.session_state.cicrData = cicrData

genai.configure(api_key="AIzaSyDJZN6sy41nOxU2qp9aqZ9qYNKQoqGM8zU")
model = genai.GenerativeModel("gemini-2.0-flash-lite")
chat = model.start_chat(history=st.session_state.cicrData)

def aiResponse(prompt):
    response = chat.send_message(prompt,stream=True)
    response.resolve() # Ensure the response is fully generated

    for word in response.text.split():
        yield word + " "
        time.sleep(0.2)

for message in st.session_state.messages: #st.session_state.messages is a [{},{},{},....]
    with st.chat_message(message["role"],avatar = message["parts"][0]['avatar']):
        st.markdown(message["parts"][0]['text'])



if prompt := st.chat_input("Hey ! Chat with me"): # := assigns chat_input to prompt and checks if the prompt is not None in a single line
    with st.chat_message("user",avatar=userImage):
        st.markdown(prompt)

    status_bar = st.status("Thinking", state="running")

    with st.chat_message("assistant",avatar = assistantImage):
        response = st.write_stream(aiResponse(prompt))

    
    status_bar.update(label = "Response Generated",state="complete") 

    st.session_state.messages.append({"role" : "user","parts":[{"text":prompt,'avatar':userImage}]})
    st.session_state.messages.append({"role" : "assistant","parts":[{"text":response,'avatar':assistantImage}]})
    st.session_state.cicrData.append({"role" : "user","parts":[{"text":prompt}]})
    st.session_state.cicrData.append({"role" : "assistant","parts":[{"text":response}]})
