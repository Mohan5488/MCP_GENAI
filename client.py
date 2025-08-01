import streamlit as st
import os
import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=api_key,
    model="llama3-8b-8192",
    temperature=0.3
)

async def setup_agent():
    client = MultiServerMCPClient({
        'email': {
            'command': 'python',
            'args': ['email_sender_mcp_server.py'],
            'transport': 'stdio'
        },
        'math': {
            'command': 'python',
            'args': ['mathserver.py'],
            'transport': 'stdio'
        },
        'funfacts': {
            'command': 'python',
            'args': ['FunFacts.py'],
            'transport': 'stdio'
        },
        'whatsapp': {
            'command': 'python',
            'args': ['whatsapp_msg.py'],
            'transport': 'stdio'
        }
    })

    tools = await client.get_tools()
    return create_react_agent(llm, tools=tools)

async def handle_email_request(agent, recipient, message_request):
    system_prompt = (
        "You are an email assistant. "
        "When a user asks you to send an email containing content, "
        "you must first generate that content (for example, a 500-word paragraph about MCP trends), "
        "then immediately call the 'send_email' tool with the recipient email, "
        "a clear subject line, and the generated body. "
        "Do not ask the user for permission or confirmation."
        "Just do it."
    )

    email_prompt = f"Send an email to {recipient}. {message_request}"

    response = await agent.ainvoke({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": email_prompt}
        ]
    })
    return response['messages'][-1].content

async def handle_whatsapp_request(agent, message_request):
    whatsapp_prompt = (
        "You are a helpful assistant specialized in drafting WhatsApp messages. "
        "Given a user's request, draft a clear and polite WhatsApp message they can copy and send."
    )

    response = await agent.ainvoke({
        "messages": [
            {"role": "system", "content": whatsapp_prompt},
            {"role": "user", "content": message_request}
        ]
    })
    return response['messages'][-1].content

def run_streamlit():
    st.set_page_config(page_title="MCP Email/WhatsApp Assistant", layout="centered")
    st.title("📩 Email and WhatsApp Generator using LangGraph")

    with st.form("assistant_form"):
        input_type = st.selectbox("Choose Action", ["Send Email", "Draft WhatsApp Message"])
        recipient = st.text_input("Recipient (Email or Phone Number)")
        message = st.text_area("Message Instruction (What should the message say?)", height=200)
        submitted = st.form_submit_button("Generate")

    if submitted and message:
        with st.spinner("Generating response..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            agent = loop.run_until_complete(setup_agent())
            if input_type == "Send Email":
                output = loop.run_until_complete(handle_email_request(agent, recipient, message))
            else:
                output = loop.run_until_complete(handle_whatsapp_request(agent, message))

            st.subheader("📨 Generated Output")
            st.code(output, language="markdown")

if __name__ == "__main__":
    run_streamlit()
