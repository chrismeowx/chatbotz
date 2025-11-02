import streamlit as st
import re
from langchain.chat_models import ChatOllama
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

st.set_page_config(layout="wide")
st.title("My Local Chatbot")

model_options = ["llama3.2", "deepseek-r1:1.5b"]
model = st.sidebar.selectbox("Choose a Model", model_options, index=0)

st.sidebar.write("Advanced Settings")
max_history = st.sidebar.number_input("Max History", min_value=1, max_value=10, value=2, step=1)
context_size = st.sidebar.number_input("Max Token", min_value=1024, max_value=2048, value=1024, step=1024)
top_p = st.sidebar.number_input("Top-P", min_value=0.8, max_value=0.95, value=0.8, step=0.01)
top_k = st.sidebar.number_input("Top-K", min_value=20, max_value=50, value=20, step=10)
temperature = st.sidebar.number_input("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)


def clear_memory():
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

if "prev_context_size" not in st.session_state or st.session_state.prev_context_size != context_size:
    clear_memory()
    st.session_state.prev_context_size = context_size

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_message=True)

llm = ChatOllama(model=model, streaming=True, temperature=temperature, top_p=top_p, top_k=top_k)

prompt_template = PromptTemplate(
    input_variable = ["history", "human_input"],
    template="{history}\nJangan tampilkan reasoning internal (<think>...</think>), cukup jawab final saja.\nUser: {human_input}\nAssistant:"
)

chain = LLMChain(llm=llm, prompt=prompt_template, memory=st.session_state.memory)

if "prev_model" not in st.session_state:
    st.session_state.prev_model = model

if st.session_state.prev_model != model:
    st.session_state.chat_history = []
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
    st.session_state.prev_model = model

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def trim_memory():
    while len(st.session_state.chat_history) > max_history * 2:
        st.session_state.chat_history.pop(0)
        if st.session_state.chat_history:
            st.session_state.chat_history.pop(0)

def clean(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

if prompt := st.chat_input("Say something"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    trim_memory()
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        for chunk in chain.stream({"human_input": prompt}):
            if isinstance(chunk, dict) and "text" in chunk:
                text_chunk = clean(chunk["text"])
                full_response += text_chunk
                response_container.markdown(full_response)
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
    trim_memory()

if st.sidebar.button("Summarize Conversation"):
    if st.session_state.chat_history:
        history_text = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history]
        )

        summarize_prompt = PromptTemplate(
            input_variables=["history"],
            template="Summarize the following conversation briefly:\n\n{history}\n\nSummary:"
        )

        summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)

        with st.spinner("Summarizing..."):
            summary = summarize_chain.run({"history": history_text})

        st.subheader("Summary")
        st.write(clean(summary))
    else:
        st.sidebar.warning("No conversation history to summarize.")
