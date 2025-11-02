import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# --- Streamlit UI ---
st.title("Advanced Hugging Face Chatbot")

# Advanced settings
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.9)
top_k = st.sidebar.slider("Top K", 0, 100, 50)
max_history = st.sidebar.number_input("Max History", 1, 20, 5)
context_size = st.sidebar.number_input("Context Size", 1, 20, 5)

# Persona, examples, context, tone, format
persona = st.text_area("Persona", "You are a helpful assistant.")
examples = st.text_area("Examples", "User: Hi\nBot: Hello!")
context = st.text_area("Context", "This chatbot helps users with questions.")
tone = st.text_input("Tone", "Friendly")
output_format = st.text_input("Format", "Plain text")

# Chat input
user_input = st.text_input("You:")

# --- Setup Model ---
@st.cache_resource
def load_model():
    model_name = "tiiuae/falcon-7b-instruct"  # contoh model HF
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return pipeline("text-generation", model=model, tokenizer=tokenizer, 
                    return_full_text=False, temperature=temperature, top_p=top_p, top_k=top_k)

generator = load_model()

# --- Memory & Prompt ---
memory = ConversationBufferMemory(
    memory_key="chat_history",
    k=max_history,
    return_messages=True
)

prompt_template = """
Persona: {persona}
Tone: {tone}
Context: {context}
Examples: {examples}
Chat History: {chat_history}
User: {user_input}
Respond in format: {output_format}
Bot:
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["persona", "tone", "context", "examples", "chat_history", "user_input", "output_format"]
)

chain = LLMChain(llm=generator, prompt=prompt, memory=memory)

if user_input:
    chat_history = memory.buffer if hasattr(memory, "buffer") else ""
    response = chain.run(
        persona=persona,
        tone=tone,
        context=context,
        examples=examples,
        chat_history=chat_history,
        user_input=user_input,
        output_format=output_format
    )
    st.text_area("Bot:", value=response, height=200)
