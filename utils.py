from kavenegar import *






def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('464A41356F656344324951476B42494B594C6E6A6A666A6A4E63456C3441452F3344317479356575614B673D')
        params = {
        'sender': '',
        'receptor': phone_number,
        'message': f'your code:{code}',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)