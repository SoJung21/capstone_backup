from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 카카오톡 플러스친구 REST API 호출 함수
def send_kakao_message(access_token, receiver_uuids, message_text):
    url = 'https://kapi.kakao.com/v1/api/talk/friends/message/send'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    payload = {
        'receiver_uuids': receiver_uuids,
        'template_object': {
            'object_type': 'text',
            'text': message_text,
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return {'status': 'success', 'message': '카카오톡 메시지가 성공적으로 전송되었습니다.'}
    else:
        return {'status': 'error', 'message': f'오류 발생 - {response.status_code}'}

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    
    access_token = data.get('access_token')
    receiver_uuids = data.get('receiver_uuids')
    
    # 테스트용 메시지
    message_text = "테스트용 메시지입니다."
    
    if not access_token or not receiver_uuids:
        return jsonify({'status': 'error', 'message': '필수 입력값이 누락되었습니다.'}), 400
    
    result = send_kakao_message(access_token, receiver_uuids, message_text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5002, debug=True)
