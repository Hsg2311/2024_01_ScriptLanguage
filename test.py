import requests

def get_lat_lng(address, api_key):
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    headers = {
        'Authorization': f'KakaoAK {api_key}'
    }
    params = {
        'query': address
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        result = response.json()
        if result['documents']:
            address_info = result['documents'][0]
            lat = address_info['y']
            lng = address_info['x']
            return lat, lng
        else:
            return None, None
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# 사용 예제
api_key = 'f804f4f49762a45caf1a6da83490efa9'  # 카카오 디벨로퍼스에서 발급받은 API 키
address = '서울특별시 강남구 테헤란로 152'

lat, lng = get_lat_lng(address, api_key)
print(lat, lng)

s = 'abc'
print(s[-1:])
print(s[s.find('x'):])