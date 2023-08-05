import luminati as lm

session=lm.session('{username}','{password}')

r=session.get('https://api.myip.com')#returns usual request object

print(r.json())

>> {'ip': '89.185.77.245', 'country': 'Romania', 'cc': 'RO'}


#Every time uses different proxy

#Also chrome header is set by default to make your ban chances minimal

#but you still can parse from specific country if you want

session.get('https://api.myip.com',cc="ru").text

>> {"ip":"84.22.150.132","country":"Russian Federation","cc":"RU"}

#or set your own header

session.get('https://api.myip.com',headers={"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)"}).text

>> {"ip":"178.173.228.210","country":"Australia","cc":"AU"}

#or timeout

session.get('https://api.myip.com',timeout=10)

#TODO
Change UserAgent every time just like it happens with countries of origin