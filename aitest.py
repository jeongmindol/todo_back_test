import requests
from datetime import datetime
import xmltodict
import json  # JSON 응답을 위해 추가
from flask import Flask, request, jsonify  # Flask를 추가하여 API 서버로 사용할 수 있도록 함
import sys
from dotenv import load_dotenv
import os

load_dotenv()  # 환경 변수를 로드합니다.
keys = os.getenv("OPEN_KEY")  # 환경 변수에서 키를 가져옵니다.

app = Flask(__name__)

# 지역 좌표 설정
location_coords = {
    '서울': {'nx': '60', 'ny': '127'},
    '부산': {'nx': '98', 'ny': '76'},
    '대구': {'nx': '89', 'ny': '90'},
    '인천': {'nx': '55', 'ny': '124'},
    '광주': {'nx': '58', 'ny': '74'},
    '대전': {'nx': '67', 'ny': '100'},
    '울산': {'nx': '102', 'ny': '84'},
    '세종': {'nx': '66', 'ny': '103'},
    '경기도': {'nx': '60', 'ny': '120'},
    '강원도': {'nx': '73', 'ny': '134'},
    '충청북도': {'nx': '69', 'ny': '107'},
    '충청남도': {'nx': '68', 'ny': '100'},
    '전라북도': {'nx': '63', 'ny': '89'},
    '전라남도': {'nx': '50', 'ny': '67'},
    '경상북도': {'nx': '89', 'ny': '91'},
    '경상남도': {'nx': '91', 'ny': '77'},
    '제주도': {'nx': '52', 'ny': '38'},
}

def get_current_date_string():
    current_date = datetime.now().date()
    return current_date.strftime("%Y%m%d")

def get_current_hour_string():
    now = datetime.now()
    if now.minute < 45:
        if now.hour == 0:
            base_time = "2330"
        else:
            pre_hour = now.hour - 1
            base_time = f"{pre_hour:02}30"
    else:
        base_time = f"{now.hour:02}30"
    return base_time


url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'

def forecast(location):
    coords = location_coords.get(location)
    if not coords:
        return {"error": f"지역 '{location}'에 해당하는 좌표값을 찾을 수 없습니다."}

    params = {
        'serviceKey': keys,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'XML',
        'base_date': get_current_date_string(),
        'base_time': get_current_hour_string(),
        'nx': coords['nx'],
        'ny': coords['ny']
    }

    res = requests.get(url, params=params)

    xml_data = res.text
    try:
        dict_data = xmltodict.parse(xml_data)
    except Exception as e:
        return {"error": f"XML 파싱 오류: {e}"}

    if 'response' not in dict_data:
        return {"error": "'response' 키가 API 응답에서 발견되지 않음."}

    weather_data = {}
    for item in dict_data['response']['body']['items']['item']:
        if item['category'] == 'T1H':
            weather_data['tmp'] = item['fcstValue']
        if item['category'] == 'REH':
            weather_data['hum'] = item['fcstValue']
        if item['category'] == 'SKY':
            weather_data['sky'] = item['fcstValue']
        if item['category'] == 'PTY':
            weather_data['sky2'] = item['fcstValue']

    return weather_data

def translate_weather_info(data):
    if 'error' in data:
        return data  # 오류 메시지 반환

    sky_status = {
        "1": "맑음",
        "2": "구름 조금",
        "3": "구름 많음",
        "4": "흐림"
    }

    precipitation_status = {
        "0": "강수형태 없음",
        "1": "비",
        "2": "비와 눈",
        "3": "눈",
        "5": "빗방울",
        "6": "빗방울과 눈",
        "7": "눈날림"
    }

    temperature = f"온도: {data['tmp']}ºC"
    humidity = f"습도: {data['hum']}%"
    sky = f"하늘 상태: {sky_status.get(data['sky'], '알 수 없음')}"
    precipitation = f"강수형태: {precipitation_status.get(data['sky2'], '알 수 없음')}"

    return {
        "temperature": temperature,
        "humidity": humidity,
        "sky": sky,
        "precipitation": precipitation
    }

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])  # JSON 형식의 입력 받기
    location = input_data['location']  # 지역 이름 추출
    weather_info = forecast(location)  # 날씨 정보 가져오기
    translated_info = translate_weather_info(weather_info)  # 정보를 한글로 변환
    print(json.dumps(translated_info))  # JSON 형식으로 출력
