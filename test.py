import requests as req
u='http://81.192.236.26:8080/dom/transport_dom.php'
d={
    "permission_date": "03/06/2022"
}

h={
    "Content-Type": "application/x-www-form-urlencoded",
"Cookie": "idterm=937710; local=__105.67.129.173__; __utma=110305868.303806262.1651445820.1651445820.1651445820.1; __utmz=110305868.1651445820.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=glu87jlgca3748ou6g02er39d6",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}
print('req')
res=req.post(u, headers=h, data=d).content.decode('utf-8')
with open('f.html', 'w', encoding='utf-8') as ff:
    print(res, file=ff)