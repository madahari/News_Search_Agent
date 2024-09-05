import streamlit as st  
import openai  
import os  
from newsapi import NewsApiClient
# from dotenv import load_dotenv  # .env 파일에서 환경 변수를 불러오기 위한 라이브러리  

# 환경 변수에서 API 키 로드  
openai.api_key = st.secrets["OPENAI_API_KEY"] 

# from newsapi import NewsApiClient
# News API 클라이언트 초기화  
# newsapi = NewsApiClient(api_key='1330f0eaa57e4b6ca0d46dddc9d128ae')  # 여기에 본인의 API 키를 입력하세요.
news_api_key = '1330f0eaa57e4b6ca0d46dddc9d128ae'
# Set your News API key and OpenAI GPT-3 API key
# news_api_key = '3094972300d84af19391a45df51b23fc'
# openai.api_key = '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'

def get_news(query):
    try:
        newsapi = NewsApiClient(api_key=news_api_key)

        # Using the newsapi library to get news articles
        news_results = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=15)

        results = []
        for article in news_results['articles']:
            title = article['title']
            link = article['url']
            results.append({'title': title, 'link': link})

        return results

    except Exception as e:
        st.error(f"Error during fetching news: {str(e)}")
        return []

def generate_summary(article_title):
    try:
        # Use OpenAI API to generate a summary
        prompt = f"Summarize the news article: {article_title}"
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150
        )
        summary = response['choices'][0]['text'].strip()
        return summary

    except Exception as e:
        st.error(f"Error during summary generation: {str(e)}")
        return "Summary not available."

# Streamlit web app
def main():
    st.title("News Search Agent")
    
    # User input for the search query
    query = st.text_input("Enter your news search query:")
    
    if st.button("Search"):
        #news articles based on the search query
        news_results = get_news(query)
        
        # Displaying results
        if news_results:
            st.header("Search Results:")
            for result in news_results:
                st.subheader(result['title'])
                st.markdown(f"[Read More]({result['link']})")

                # Generating and displaying a summary using GPT-3
                summary = generate_summary(result['title'])
                st.write("Summary:", summary)
        else:
            st.warning("No results found.")

if __name__ == "__main__":
    main()
