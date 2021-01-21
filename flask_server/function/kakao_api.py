#function file : ex) kakao api

import sys
import argparse
import requests
# from PIL import Image, ImageDraw, ImageFont
# from io import BytesIO

#예제 URL : https://bimage.interpark.com/milti/renewPark/evtboard/20190915174947722.jpg

API_URL = 'https://dapi.kakao.com/v2/vision/adult/detect'

#카카오 developers에 가서 앱 생성 뒤 rest api key 복붙
MYAPP_KEY = '2707f92b7cf29b30bd945e58b11160a6'

def detect_adult(image_url, image_type):
    print("in main function")
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}

    try:
        if image_type == 0:
            data = {'image_url':image_url}
            resp = requests.post(API_URL,headers=headers,data=data)
        elif image_type == 1:
            files = {'image':open(image_url,'rb')}
            resp = requests.post(API_URL,headers=headers,files=files)
        resp.raise_for_status()
        result = resp.json()['result']
        if result['adult']>result['soft'] and result['adult']>result['normal']:
            return 1
        else:
            return 0
        #return ("Adult Percentage : {:3f}%  Soft Percentage : {:3f}%  Normal Percentage {:3f}%".format(result['adult'] * 100, result['soft'] * 100, result['normal'] * 100))
        

    except Exception as e:
        print(str(e))
        sys.exit(0)

#이 파일이 main프로그램으로 사용될때 실행
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Classify adult image')
    parser.add_argument('image_url', type=str, nargs='?',
        # default="http://t1.daumcdn.net/alvolo/_vision/openapi/r2/images/10.jpg",
        default="././flask_server/data/2021-01-12_09-32-39.png",
        help='image url to classify')
    args = parser.parse_args()
    print(args)
    detect_adult(args.image_url,1)