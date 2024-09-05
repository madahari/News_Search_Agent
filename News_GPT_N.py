import streamlit as st  
import requests  

# 네이버 뉴스 API 키 설정  
naver_client_id = st.secrets["naver"]["client_id"]  # secrets에서 클라이언트 ID 가져오기  
naver_client_secret = st.secrets["naver"]["client_secret"]  # secrets에서 클라이언트 시크릿 가져오기  

def get_news(query):  
    try:  
        url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=15&sort=sim"  
        headers = {  
            'X-Naver-Client-Id': naver_client_id,  
            'X-Naver-Client-Secret': naver_client_secret  
        }  
        response = requests.get(url, headers=headers)  
        news_results = response.json()  

        results = []  
        for article in news_results['items']:  
            title = article['title']  
            link = article['link']  
            results.append({'title': title, 'link': link})  

        return results  

    except Exception as e:  
        st.error(f"뉴스를 가져오는 중 오류 발생: {str(e)}")  
        return []  

# Streamlit 웹 앱  
def main():  
    st.title("뉴스 검색 에이전트")  
    
    # 사용자 입력을 위한 검색 쿼리  
    query = st.text_input("뉴스 검색어를 입력하세요:")  
    
    if st.button("검색"):  
        # 검색 쿼리를 기반으로 뉴스 기사 가져오기  
        news_results = get_news(query)  
        
        # 결과 표시  
        if news_results:  
            st.header("검색 결과:")  
            for result in news_results:  
                st.subheader(result['title'])  
                st.markdown(f"[더 읽기]({result['link']})")  
        else:  
            st.warning("결과가 없습니다.")  

if __name__ == "__main__":  
    main() 
