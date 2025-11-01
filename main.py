# import streamlit as st
# import re
# from langchain_community.chat_models import ChatOllama
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

# def clear_memory():
#     st.session_state.memory = ConversationBufferMemory(return_messages=True)

# st.set_page_config(layout="wide")
# st.title("Local Chatbot")

# model_options = ["llama3.2", "deepseek-r1:1.5b"]
# with st.sidebar.expander("Model Options"):
#     model_choose = st.selectbox("Choose one of the model" ,model_options, index=0)


# with st.sidebar.expander("Advanced Settings"):
#     max_history = st.number_input("Max History", min_value=1, max_value=10, value=2, step=1)
#     context_size = st.number_input("Max Token", min_value=1024, max_value=2048, value=1024, step=1024)
#     top_p = st.number_input("Top-P", min_value=0.8, max_value=0.95, value=0.8, step=0.01)
#     top_k = st.number_input("Top-K", min_value=20, max_value=50, value=20, step=10)
#     temperature = st.number_input("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

#     if "prev_context_size" not in st.session_state or st.session_state.prev_context_size != context_size:
#         clear_memory()
#         st.session_state.prev_context_size = context_size

# with st.sidebar.expander("Chatbot Persona"):
#     label_persona = "Enter the persona of the chatbot:"
#     persona = st.text_area(label_persona, placeholder="Super charismatic, genius, millionare AI", height=None, max_chars=120, label_visibility="visible")

# with st.sidebar.expander("Context"):
#     label_context = "Give a context to our chatbot!"
#     context = st.text_area(label_context, placeholder="You are a top wolf street investor that made 300k dollars a year, who's a genius in predicting stocks.", height=None, max_chars=120, label_visibility="visible")

# with st.sidebar.expander("Tone"):
#     label_tone = "How do you want your chatbot talk?"
#     tone_options = ["Professional", "Friendly and Casual", "Straightforward", "Sarcastic"]
#     tone = st.selectbox(label_tone, tone_options)

# with st.sidebar.expander("Format"):
#     label_format = "Choose the format of your answer!"
#     format_options = ["Bullet Points", "Markdown", "Table"]
#     formats = st.selectbox(label_format, format_options)

# with st.sidebar.expander("Examples"):
#     label_example = "Give example of how do you want your answer will be:"
#     example = st.text_area(label_example, placeholder="Markdown adalah sebuah format penulisan teks yang digunakan untuk mempermudah pembuatan tampilan teks yang terstruktur, seperti membuat judul, teks tebal, miring, daftar, atau bahkan menampilkan kode. Bahasa ini sering digunakan di berbagai platform seperti GitHub, Notion, Discord, Reddit. Dengan Markdown, kamu bisa membuat teks terlihat rapi tanpa perlu menulis kode HTML yang panjang.")


# def submitz():
#     st.session_state["chatbot_customization"] = {
#         "model" : model_choose, 
#         "max_history": max_history,
#         "context_size": context_size,
#         "top_p" : top_p,
#         "top_k" : top_k,
#         "temperature": temperature,
#         "persona" : persona,
#         "context" : context,
#         "tone" : tone,
#         "format" : formats,
#         "examples" : example
#     }

# submit = st.sidebar.button(label="Customize Chatbot", help="Customize all the available choices before you click the submit button.", on_click=submitz, type="secondary")

# def customization(key, default):
#     return st.session_state.get(key, default)


# model = customization("model_choose", "llama3.2")
# top_p = customization("top_p", 0.8)
# top_k = customization("top_k", 20)
# temperature = customization("temperature", 0.5)
# max_history = customization("max_history", 2)
# persona = customization("persona", "Super Smart")
# tone = customization("tone", "Professional")
# formats = customization("format", "Bullet Points")
# context = customization("context", "Very Smart")
# examples = customization("examples", "JAWAB LIKE THIS")

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "memory" not in st.session_state:
#     st.session_state.memory = ConversationBufferMemory(return_message=True)

# def clean(text):
#     return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# def trim_memory():
#    entries = st.session_state.chat_history
#    max_entries = max_history * 2
#    while len(entries) > max_entries:
#         entries.pop(0)

# llm = ChatOllama(model=model, streaming=True, temperature=temperature, top_p=top_p, top_k=top_k)

# prompt_text = '''

# ======================
#     Chatbot Instructions
#     ======================

#     Persona:
#     {persona}

#     Context:
#     {context}

#     Tone of Answer:
#     {tone}

#     Answer Format:
#     {formats}

#     Example of Answer Style:
#     {examples}

#     Conversation History:
#     {history}

#     ======================
#     User Question:
#     {human_input}

#     ======================
#     Guidelines:
#     - Jangan tampilkan reasoning internal (<think>...</think>), hanya jawaban final.
#     - Jawaban harus mengikuti persona, konteks, tone, format, dan contoh yang diberikan.
#     - Jika format adalah "Bullet Points", gunakan daftar poin.
#     - Jika format adalah "Markdown", gunakan markdown syntax.
#     - Jika format adalah "Table", tampilkan dalam bentuk tabel yang rapi.
#     - Jawaban harus jelas, ringkas, dan mudah dipahami.

#     Assistant:
#     """
# '''

# if "prev_model" not in st.session_state:
#     st.session_state.prev_model = model

# if st.session_state.prev_model != model:
#     st.session_state.chat_history = []
#     st.session_state.memory = ConversationBufferMemory(return_messages=True)
#     st.session_state.prev_model = model

# for msg in st.session_state.chat_history:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# prompt_template = PromptTemplate(
#     input_variables=[
#         "history",
#         "human_input"
#     ],
#     template=prompt_text
    
# )

# chain = LLMChain(llm=llm, prompt=prompt_template, memory=st.session_state.memory)

# for msg in st.session_state.chat_history:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])


# if prompt := st.chat_input("Say something"):
#     st.session_state.chat_history.append({"role": "user", "content": prompt})
#     trim_memory()

#     history_text = "\n".join(
#         [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_history]
#     )

#     with st.chat_message("assistant"):
#         response_container = st.empty()
#         full_response = ""
#         try:
#             for chunk in chain.stream({
#                 "persona": persona,
#                 "context": context,
#                 "tone": tone,
#                 "formats": formats,
#                 "examples": examples,
#                 "history": history_text,
#                 "human_input": prompt
#             }):
#                 if isinstance(chunk, dict) and "text" in chunk:
#                     text_chunk = clean(chunk["text"])
#                 else:
#                     text_chunk = clean(str(chunk))
#                 full_response += text_chunk
#                 response_container.markdown(full_response)
#         except ValueError as e:
#             st.error(f"Input validation error: {e}")
#             full_response = f"(Error: {e})"

#     st.session_state.chat_history.append({"role": "assistant", "content": full_response})
#     trim_history()

# if st.sidebar.button("Summarize Conversation"):
#     if st.session_state.chat_history:
#         history_text = "\n".join(
#             [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history]
#         )

#         summarize_prompt = PromptTemplate(
#             input_variables=["history"],
#             template="Summarize the following conversation briefly:\n\n{history}\n\nSummary:"
#         )

#         summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)

#         with st.spinner("Summarizing..."):
#             summary = summarize_chain.run({"history": history_text})

#         st.subheader("Summary")
#         st.write(clean(summary))
#     else:
#         st.sidebar.warning("No conversation history to summarize.")

import streamlit as st
import re
from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(layout="wide")
st.title("Local Chatbot (Simplified Prompt Inputs)")

# ----------------------------
# Sidebar Controls
# ----------------------------
model_options = ["llama3.2", "deepseek-r1:1.5b"]
model = st.sidebar.selectbox("Choose model", model_options, index=0)

max_history = st.sidebar.number_input("Max History", min_value=1, max_value=10, value=3, step=1)
temperature = st.sidebar.number_input("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
top_p = st.sidebar.number_input("Top-P", min_value=0.0, max_value=1.0, value=0.8, step=0.01)
top_k = st.sidebar.number_input("Top-K", min_value=1, max_value=200, value=20, step=1)

persona = st.sidebar.text_input("Persona", value="Super charismatic, genius AI")
context = st.sidebar.text_area("Context", value="You are a top investor with deep CS knowledge.", height=80)
tone = st.sidebar.selectbox("Tone", ["Professional", "Friendly", "Straightforward"], index=0)
formats = st.sidebar.selectbox("Format", ["Bullet Points", "Markdown", "Table"], index=0)
examples = st.sidebar.text_area("Example Style (optional)", value="", height=80)

# ----------------------------
# Session State Initialization
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# ----------------------------
# Utility Functions
# ----------------------------
def clean(text):
    """Remove internal reasoning markers like <think>...</think>."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def trim_history():
    """Keep only limited chat history."""
    entries = st.session_state.chat_history
    max_entries = max_history * 2  # user + assistant pairs
    while len(entries) > max_entries:
        entries.pop(0)

# ----------------------------
# LLM Initialization
# ----------------------------
llm = ChatOllama(
    model=model,
    streaming=True,
    temperature=temperature,
    top_p=top_p,
    top_k=top_k
)

# ----------------------------
# Prompt Template
# ----------------------------
prompt_template_text = """
======================
Chatbot Instructions
======================

Persona:
{persona}

Context:
{context}

Tone of Answer:
{tone}

Answer Format:
{formats}

Example of Answer Style:
{examples}

Conversation History:
{history}

======================
User Question:
{human_input}

======================
Guidelines:
- Do not show internal reasoning (<think>...</think>).
- The answer must follow persona, context, tone, and format.
- If format = "Bullet Points", use list format.
- If format = "Markdown", use Markdown syntax.
- If format = "Table", use a neat table format.
- Answer clearly, concisely, and in easy-to-understand language.

Assistant:
"""

prompt_template = PromptTemplate(
    input_variables=[
        "persona", "context", "tone", "formats", "examples",
        "history", "human_input"
    ],
    template=prompt_template_text
)

# ----------------------------
# Chain Setup
# ----------------------------
chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    memory=st.session_state.memory
)

# ----------------------------
# Display Chat History
# ----------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# Handle User Input
# ----------------------------
if prompt := st.chat_input("Say something"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    trim_history()

    history_text = "\n".join(
        [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_history]
    )

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        try:
            for chunk in chain.stream({
                "persona": persona,
                "context": context,
                "tone": tone,
                "formats": formats,
                "examples": examples,
                "history": history_text,
                "human_input": prompt
            }):
                if isinstance(chunk, dict) and "text" in chunk:
                    text_chunk = clean(chunk["text"])
                else:
                    text_chunk = clean(str(chunk))
                full_response += text_chunk
                response_container.markdown(full_response)
        except ValueError as e:
            st.error(f"Input validation error: {e}")
            full_response = f"(Error: {e})"

    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
    trim_history()

# ----------------------------
# Summarize Conversation
# ----------------------------
if st.sidebar.button("Summarize Conversation"):
    if st.session_state.chat_history:
        history_text = "\n".join(
            [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_history]
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
