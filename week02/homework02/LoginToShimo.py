import requests
import http.cookiejar as cookielib
from fake_useragent import UserAgent



shimoSession=requests.session()
shimoSession,cookies=cookielib.LWPCookieJar(filename='shimo.txt')

ua=UserAgent()


header={
    'Referer':'https://shimo.im/login?from=home',
    'User-Agent':ua.random()
}

def shimoLogin(account,password):
    postUrl = 'https://shimo.im/lizard-api/auth/code/login'
    postData = {
        'passport':account,
        'password':password,
    }
    responseRes = shimoSession.post(postUrl,data=postData,headers= header)
    responseRes.cookies.save()

if __name__ == '__main__':
    shimoSession.cookies.load()
    shimoLogin('','')