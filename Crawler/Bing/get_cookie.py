import json

def strToJSON(cookie_string):
    

    cookies = {}
    for cookie in cookie_string.split('; '):
        name, value = cookie.split('=', 1)
        cookies[name] = value

    cookies_json = json.dumps(cookies)

    print(cookies_json)

    return cookies_json

strToJSON('MUID=36533E0BFC73660837DF2EDEFD60673E; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=63146FDF79814B3FBDDA486DBF992A32&dmnchg=1; WLS=C=2e95e26610e79c36&N=menna; _U=1a_cnPsFS5Z3LmoGprrYsPO7I7swSXl3r_t9-OyVa6f9dN4vuByXGINRbvaaRCqoxRyJtk6EzoDaQSOnkNjD1RKcGaystR0zpEDF_D7AVc2K7OokUSP6HZ7x9TcF4T28s_3dq5uDuDcETU34KuT0yXxGCJLnQlX5FhlHgkAsjRE_1NF3tw_MvNm2Q_p_lg08GIQbdXXMCsX2AwVhAeBma7Q; ANON=A=1C4E503CAC95368D687D21F1FFFFFFFF&E=1c45&W=1; NAP=V=1.9&E=1beb&C=4SHWNUJxivzlp9OdZKzevcW0eXmqjZ4fr5oQKxwREUflDlu_XEhkDQ&W=1; SRCHS=PC=U531; SRCHUSR=DOB=20200826&T=1682701848000; _SS=SID=2D2D30899052639814AF238891E062EB&PC=U531&R=6&RB=6&GB=0&RG=0&RP=6; ipv6=hit=1682705456915&t=4; dsc=order=News; _RwBf=ilt=1&ihpd=0&ispd=1&rc=6&rb=6&gb=0&rg=0&pc=6&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=10&l=2023-04-28T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=BINGCOPILOTWAITLIST&c=MR000T&t=5215&s=2023-04-08T22:18:52.2187144+00:00&ts=2023-04-28T17:11:03.7554341+00:00&rwred=0&wls=2&lka=0&lkt=0&TH=&mta=0&e=uqYF2LMKTf1wiFdMJ67eKPmdt51Hhs-teAChzivwc5FekJDluSc_iZi3UODvIV7TwG1z3tOhZEsrhMOzM0apSrt8-SazoA4ELqafHxVHmB0&A=; SRCHHPGUSR=BRW=NOTP&BRH=M&CW=460&CH=736&SCW=1164&SCH=3217&DPR=1.3&UTC=120&DM=1&SRCHLANG=en&PV=14.0.0&HV=1682701866&PRVCW=711&PRVCH=736&EXLTT=8&THEME=1')