from NorenApi import NorenApi
import pyotp

def Shoonya_login():
    #credentials
    api = NorenApi()
    user    = 'FA11563'
    pwd     = 'Temp123'
    vc      = 'FA11563_U'
    otp_token = "K7KOF53MNQ7AUB27FCQ57E62A3B7M66"
    factor2=pyotp.TOTP(otp_token).now()
    app_key = '9146eb625874062c71f6225994cb48f'
    imei    = 'abc1234'
    accesstoken = ''

    #make the api call
    ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    print(ret)
    print(ret['susertoken'])
    print(api)


Shoonya_login()
