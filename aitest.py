import os # 파일 경로 설정 등에 사용
import sys # 한글 출력 인코딩에 사용
import io # 한글 출력 인코딩에 사용
import json
import openai


from dotenv import load_dotenv
load_dotenv()
os.getenv("OPENAI_API_KEY")
# os.getenv("OPENAI_API_KEY")

#출력의 인코딩을 utf-8로 설정한다
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def analyze_sentiment(question):
    try:
        # OpenAI 최신 API 호출
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "사용자가 작성하는 문장을 영어, 독일어, 일본어, 이탈리아어로 번역한후 밑에 ()를 통해 한국어 발음도 만들어줘."},
                # {"role": "assistant", "content": "부정적인 문구가 들어가있으면 안 돼 부정을 하고싶다면 '당신은 역시 대단해요 !!' 라는 문구가 나왔으면 좋겠어"},
                {"role": "user", "content": question}
            ]
        )

        sentiment = response.choices[0].message.content
        return sentiment
    except Exception as e:
        # 오류 발생 시 로그 출력
        print(f"Error during API call: {str(e)}")  # 오류를 콘솔에 출력
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # 질문을 명령줄 인자로 받기
    question = sys.argv[1]

    # 감정 분석 결과 생성
    result = analyze_sentiment(question)

    # 결과를 JSON 형식으로 출력
    print(json.dumps({"answer": result}))