import os
import streamlit as st
from openai import OpenAI
from search import distributed_search, meta_search
from concurrent.futures import ThreadPoolExecutor

class AIAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.search_executor = ThreadPoolExecutor(max_workers=5)
        
    def generate_response(self, prompt, use_search=False):
        if use_search:
            search_results = meta_search(prompt)
            context = "\n".join(search_results[:3])
            prompt = f"Context: {context}\n\nQuestion: {prompt}\nAnswer:"
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    def decide_search_need(self, query):
        decision_prompt = f"""Should we perform a web search to answer this query? 
        Query: {query}
        Answer only Yes or No:"""
        
        decision = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": decision_prompt}],
            temperature=0.0
        )
        return "yes" in decision.choices[0].message.content.lower()

def main():
    st.title("🤖 AI Smart Agent with Meta Search")
    agent = AIAgent()
    
    user_input = st.text_input("Enter your question:")
    
    if st.button("Submit"):
        with st.spinner("Processing..."):
            need_search = agent.decide_search_need(user_input)
            if need_search:
                st.info("Performing meta search...")
                search_results = meta_search(user_input)
                with st.expander("View search results"):
                    for i, result in enumerate(search_results[:3], 1):
                        st.write(f"{i}. {result}")
            
            response = agent.generate_response(user_input, use_search=need_search)
            st.success(response)

if __name__ == "__main__":
    main()