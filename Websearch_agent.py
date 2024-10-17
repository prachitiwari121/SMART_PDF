import requests
import streamlit as st
from transformers import pipeline

# Initialize the search and question-answering models
search_pipeline = pipeline("search")
qa_pipeline = pipeline("question-answering")

def perform_web_search(query):
    """Perform a web search using a search API."""
    # Example search API (this should be replaced with a real API)
    search_url = "https://api.example.com/search"
    response = requests.get(search_url, params={"q": query})
    if response.ok:
        return response.json().get("results", [])
    else:
        return []

def extract_answer_from_context(context, question):
    """Use a QA pipeline to extract an answer from context."""
    return qa_pipeline(question=question, context=context)

# Streamlit application configuration
st.set_page_config(page_title="Web Search and QA", page_icon="🔍")
st.title("Web Search and Question Answering 🔍")

# User input for search
search_query = st.text_input("Enter your search query:")

if st.button("Search"):
    if search_query:
        # Perform web search
        search_results = perform_web_search(search_query)
        if search_results:
            st.success("Search completed successfully!")
            for result in search_results:
                st.write(f"**Title:** {result['title']}")
                st.write(f"**Link:** [Visit]({result['link']})")
                st.write(f"**Snippet:** {result['snippet']}\n")
        else:
            st.error("No results found.")
    else:
        st.warning("Please enter a search query.")

# User input for questions related to search results
user_question = st.text_input("Ask a question about the search results:")

if user_question and search_results:
    # Combine search snippets for context
    context = " ".join([result['snippet'] for result in search_results])
    answer = extract_answer_from_context(context, user_question)
    
    # Display the answer
    st.write("### Answer:")
    st.write(answer.get("answer", "I'm sorry, I couldn't find an answer to that."))
