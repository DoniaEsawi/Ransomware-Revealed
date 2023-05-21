import BingPython as ai
import asyncio
import re
import requests
import json
import time


# Cookies
# You can get with Cookie Editor
# - Enter to https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx
# - Open cookie editor
# - Write your cookie
# OR
# - Export your cookies as Netscape
# - Write your cookies inside of cookies.txt
#     try:
#         import cookielib
#     except:
#         import http.cookiejar
#         cookielib = http.cookiejar
# cookies = cookielib.MozillaCookieJar('cookies.txt')
# cookies.load()

# on Menna's labtop
cookies = {"MUID": "36533E0BFC73660837DF2EDEFD60673E", 
           "SRCHD": "AF=NOFORM", 
           "SRCHUID": "V=2&GUID=63146FDF79814B3FBDDA486DBF992A32&dmnchg=1", 
           "WLS": "C=2e95e26610e79c36&N=menna", 
           "_U": "1a_cnPsFS5Z3LmoGprrYsPO7I7swSXl3r_t9-OyVa6f9dN4vuByXGINRbvaaRCqoxRyJtk6EzoDaQSOnkNjD1RKcGaystR0zpEDF_D7AVc2K7OokUSP6HZ7x9TcF4T28s_3dq5uDuDcETU34KuT0yXxGCJLnQlX5FhlHgkAsjRE_1NF3tw_MvNm2Q_p_lg08GIQbdXXMCsX2AwVhAeBma7Q", 
           "ANON": "A=1C4E503CAC95368D687D21F1FFFFFFFF&E=1c45&W=1", 
           "NAP": "V=1.9&E=1beb&C=4SHWNUJxivzlp9OdZKzevcW0eXmqjZ4fr5oQKxwREUflDlu_XEhkDQ&W=1", 
           "SRCHS": "PC=U531", 
           "SRCHUSR": "DOB=20200826&T=1682701848000", 
           "_SS": "SID=2D2D30899052639814AF238891E062EB&PC=U531&R=6&RB=6&GB=0&RG=0&RP=6", 
           "ipv6": "hit=1682705456915&t=4", 
           "dsc": "order=News", 
           "_RwBf": "ilt=1&ihpd=0&ispd=1&rc=6&rb=6&gb=0&rg=0&pc=6&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=10&l=2023-04-28T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=BINGCOPILOTWAITLIST&c=MR000T&t=5215&s=2023-04-08T22:18:52.2187144+00:00&ts=2023-04-28T17:11:03.7554341+00:00&rwred=0&wls=2&lka=0&lkt=0&TH=&mta=0&e=uqYF2LMKTf1wiFdMJ67eKPmdt51Hhs-teAChzivwc5FekJDluSc_iZi3UODvIV7TwG1z3tOhZEsrhMOzM0apSrt8-SazoA4ELqafHxVHmB0&A=", 
           "SRCHHPGUSR": "BRW=NOTP&BRH=M&CW=460&CH=736&SCW=1164&SCH=3217&DPR=1.3&UTC=120&DM=1&SRCHLANG=en&PV=14.0.0&HV=1682701866&PRVCW=711&PRVCH=736&EXLTT=8&THEME=1"}
# on nada's labtop 
# cookies = {"MUID":"33C8D4C434DD67652E86C6C735A1660B","SRCHD":"AFNOFORM","SRCHUID":"V2&GUIDB0B7AAE05A2F4BBEA04920F71CE62D49&dmnchg1","MMCASM":"ID89FDFF3D72B94BF4B09B3707A5BE4ADD","ANON":"A6E488C976FA144D042EE83B0FFFFFFFF&E1c3e&W2","NAP":"V1.9&E1bdb&CyJddsyGFiWw5aNq4Ys9xBAHRjKV0KgUGcC_x40UFJx7S-lTdTbwHEQ&W2","_clck":"w12vib|1|fb2|0","_BINGNEWS":"SW1294&SH649","_clsk":"z270s7|1682451257904|1|0|o.clarity.ms/collect","_UR":"QS0&TQS0","_HPVN":"CSeyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMy0wNC0yNVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6Mn0","MicrosoftApplicationsTelemetryDeviceId":"c5abfcd0-6b3b-407e-bf13-496d828f7879","WLS":"C4ddb7eb0669548ea&NNada","_U":"1pDDKzachLCnbydbHiusBWe1-8CHW0mAyFWp-w3cCLSV4e6sEvaXSg1XNz_m8sLAUpFQ6WV3IVYZLzGP-lCXD3XL8hZEamm4Rovq1qMnO-nA1JMdDjW-lA6oZdsZETEyYu4o4LdlaJERTJF2QMwPyoDwQERLNn5VTGDzXG375VQHdDWWOIwbtg2WgxU3-nG60HtNFr4NfrOhUmqjf8oRDtehoQFN0qEgOYrtVdc0k0sI","ABDEF":"V13&ABDV13&MRNB1682509595197&MRB0","SRCHUSR":"DOB20220817&T1682509601000","_RwBf":"ilt1&ihpd0&ispd1&rc69&rb69&gb0&rg0&pc69&mtu0&rbb0.0&g0&cid&clo0&v3&l2023-04-26T07:00:00.0000000Z&lft0001-01-01T00:00:00.0000000&aof0&o0&pBINGCOPILOTWAITLIST&cMR000T&t211&s2023-04-21T20:08:16.8834563+00:00&ts2023-04-26T11:46:43.1380360+00:00&rwred0&wls2&lka0&lkt0&TH&mta0&esFNaluWPZ8-kRnduaPnY7Wl8i2QfW7F_ZLsfMOV2QaXL5aIVNh5db_bM4qgT_cX86NL55pNtUBpY8VzeBdxV7g&A","_SS":"SID0A6DD1A01BF4638B15B0C35F1A8862FB&R69&RB69&GB0&RG0&RP69","dsc":"orderNews","ipv6":"hit1682513205965&t4","SRCHHPGUSR":"SRCHLANGen&PV15.0.0&BRWXW&BRHM&CW1496&CH796&SCW1204&SCH316&DPR1.0&UTC120&DM1&EXLTT32&HV1682509608&WTS63817704304&PRVCW1496&PRVCH796&THEME1&THThHalo"}
# on raghed's labtop 
# cookies = {
#     'MUID': '3BA8B12BB7CC6D58391DA00FB6B06C29',
#     'MUIDB': '3BA8B12BB7CC6D58391DA00FB6B06C29',
#     'USRLOC': 'HS=1&ELOC=LAT=29.97455406188965|LON=31.260295867919922|N=Qesm%20El%20Basateen%2C%20Cairo|ELT=2|&CLOC=LAT=29.9745547908424|LON=31.260296034885485|A=733.4464586120832|TS=230426074216|SRC=W',
#     'SRCHD': 'AF=hpcodx',
#     'MMCASM': 'ID=33DF5FFA342842659368E1CEAE87E3D8',
#     'ANON': 'A=BF86ACCF614097E03333ADB8FFFFFFFF&E=1c28&W=1',
#     'ABDEF': 'V=13&ABDV=13&MRNB=1682459571185&MRB=0',
#     'PPLState': '1',
#     'KievRPSSecAuth': 'FACSBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACNA4tSFNzEOdUASBrv42DrRkmYw/gkxtgGJjw66oWfEi+Qe4RKH4UyKcP9t7mRIkHVl8SUs0hZp+11qr19bej5Ipz5WHWhOu70thxD87v4d6EJvIepJbby/PMXnFBfpcY4S3KGz1TLqVm96UUV2yt+tA/jxYX5/mXW7FxUNjyd6T9pg72Vh+M5Pvi2V/R4Z6vmIKwzAIHxR/8XDOmwOjdbY1/qXmxcdYDN+iRBExfBIRAjnpsomircj9aLIRj0U3SZ35DpxhlIT+IPYNuemKR7UAl7A7jJLMAh4lpIAsiC38umbL0q6eun22WGj8FtqLnlpzwRiwFneWBipQa3uSQFbWIkeGVb1mlXMpK+Okwf9mv+n9+1rqrTo9ZDKm0yXw0A59Kee0sryNPiQXosvjN2qWxVMn2gulmzvPGGVZPR1ficQSRlQuiKgju63mZst4MJ1+JPBp710aMyP+OPk8sHWqNRAvo2bj6mDzQlMIdR5zWdgfYeB6/mM56VWGQVp0xGXWdKRcN+gS7BEJjS0Ki2+DVjdfVGvvreBbplojE+gwRmSIg9eU8sITvfAZleHshkKgcAxvhAf7zmrgkf5N+sAMReAlynA5P04xoAqIIuaeKecHh43Y2nqHqeMOD7Iwa0dIW/Rz0BcKaVA/mE09tZhTU2yalIv/8o4Lk0heXrRcfwMMco09HYd7bkS7t5QgEZzPx+NLkfYYQIoAwG4M/ivGqn9clFhM1AS41i9v8tvHu3ub73uQ78XxN/P9TeTTvXUjLUbABBvDJozOF51ZDex68L92kEqeLbrIMuXfcdPcNsNhlnwOQ8P1zNIfZOFTEyMCJaNXoN6RPqWsO9mWl+zgnRjmejE4HzTSmzcEovJnsNwD2QYbqdIg9y9Mxp3aaGAxvRsU0YGpHKbaao2dHZ68Ci/otFr5OmJQB2ZgHQh7wyTwuutUpH0qTImfVSNqcFlv2YbEv1114CyqzktoVUgNSKHXqqRRAq8owQSJVd782JjRBisKpgMR+8dCENaibwbd/zr3LA1VhfBZss/Aiux5w0dXdrwwF77kp5VC8X9gIQXjOERHfq3f2L7Hh4fgqvZvU1AXHI/aWRPCE7rJxRNAwlFMxhYTYtEVuwXtcr23LnERauqjR1aXVS4eRxxSY5ffmhJwT81FgBrtvhm/l3VjmtZYugbYMBYteQthvxueOtDmO3RLo5E67oLCgdAVsR4pHD/Y7rA+u7CJtKamHehPKHe16gZGV1KpWQBHHqupuqHsDBm1hUkapKAng6ZU70vYPR5yBr2jAigcRx8lXDbC4lmNXdxsS5Iy+QmD94dqzswg0S3URbl6eqC7I7o4UJktduYpnurYhYKCskDZCCVjNJvgr5x1sOiL8Y0PT5hKX7O5voj5UJ3VR8KItFZWKEf2W8bxlkyCCPD2AAJFLzoNvJnJxByqV9dgJVg7Q+uZrl/RvnhewOdL9v3ERRckeNiX7VCJDVjknNIUAJnI9lZXquwct+VHTXOK8GVO6iDb',
#     '_U': '1LUmmuDx2Twpf_AV1JrVKfajnsVZmhZ86eaZ82N5aDv912WC-FxqNzKsE1RS9Hytv68H7fRXBhNrUA2T1diGTsvkQyDuImONpEX_Zk8-bkR3unrfFZiUt1viUjZB5cjOeSv-iZK2UVLiR3SbnOiWU_pn0WLcS6XHEGggVFsOthlDa-IWeNwqieIl4nTyQuvJZbZ0D2ekLeXN1ioBTOBTws0uyADBE0VVB8780dZTcGoc',
#     'SUID': 'A',
#     '_EDGE_S': 'SID=0ABCA05760CF63512F6BB2A861D1629C',
#     'WLS': 'C=5084018b0ae91b63&N=raghad',
#     '_SS': 'SID=0ABCA05760CF63512F6BB2A861D1629C&PC=EDBBAN&R=66&RB=66&GB=0&RG=0&RP=63',
#     '_clck': '1s6jqay|1|fam|0',
#     'SRCHUSR': 'DOB=20220107&T=1682495197000&POEX=W',
#     '_RwBf': 'ilt=125&ihpd=0&ispd=1&rc=66&rb=66&gb=0&rg=0&pc=63&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=4&l=2023-04-26T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&o=0&p=BINGCOPILOTWAITLIST&c=MR000T&t=5936&s=2023-03-15T18:45:39.0717082+00:00&ts=2023-04-26T07:55:00.7937897+00:00&rwred=0&wls=2&lka=0&lkt=0&TH=&mta=0&e=8JJEDbAGkGe-6-Asr0LUMYtU1HzfvpUoDEa7VZIFOAjswv6LFg9kO7mpeNvj_zWS4juDl03X4IvQK-9LxFEzPA&A=&mte=0',
#     'SRCHHPGUSR': 'SRCHLANG=en&BRW=XW&BRH=M&CW=1536&CH=754&SW=1536&SH=864&DPR=1.3&UTC=120&DM=0&EXLTT=31&WTS=63815762177&HV=1682495702&PV=10.0.0&PRVCW=770&PRVCH=754&SCW=1519&SCH=4015',
#     'ipv6': 'hit=1682498804047&t=4',
#     '_tarLang':'default=ar',
#     '_EDGE_V':'1',
#     '_TTSS_IN':'hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=',
#     '_TTSS_OUT':'hist=WyJhciJd',
#     'TTRSL':'en',
# }



# get the company info from https://api.orb-intelligence.com/
def get_company_info(company_website):
    url = "https://api.orb-intelligence.com/3/match/?api_key=c66c5dad-395c-4ec6-afdf-7b78eb94166a&website="

    try:
        time.sleep(2)
        response = requests.request("GET", url+company_website)
        print("response is: ",response.text)
        # print(response.text)
        data = json.loads(response.text)
        if (data["results_count"] > 0): 
            time.sleep(2)
            orb_number = data["results"][0]["orb_num"]
            #print("company orb_num")
            #print(data)
            url2 = "https://api.orb-intelligence.com/3/fetch/"+str(orb_number)+"/?api_key=c66c5dad-395c-4ec6-afdf-7b78eb94166a"

            response = requests.request("GET", url2)
            print("response 2 is: ",response.text)
            # print(response.text)
            data2 = json.loads(response.text)
            #print("company info")
            #print(data2)
            return data2  
        else:
            print("no company found")
            return None
    except Exception as e:

        print("error in getting company orb_num")
        print(e)
    
    return None

def get_revenue_sector(ask, answer):
    
    # print("question sent to bing:", ask)
    # command = ai.BingPython.sendcom_sydney(ai.BingPython.CreateSession(cookies), ask)
    # answer=asyncio.get_event_loop().run_until_complete(command)

    sectors = ["industrial goods and services", "technology", "construction and materials", "travel and leisure", "healthcare"]
    revenue = None
    sector = None
    year = None
    region = None
    print(answer)

    # if return answer is None re will throw error 
    try:
        # check if the answer has $numberM or $numberM-$numberM using regex
        result = re.search(r"(\$\d+(\.\d+)? ?(million|m)?(-\$\d+(\.\d+)? ?(million|m))?)", answer, re.IGNORECASE)
        if result:
            revenue = result.group(0)

        results = re.findall(r"(?<=\*\*)[^\*]*(?=\*\*)", answer, re.IGNORECASE)
        if len(results) > 0:
            for result in results:
                for given_sector in sectors:
                    if result.lower() in given_sector:
                        sector = given_sector
                        results.remove(result)
                        break

            for result in results:
                if result.isnumeric() and len(result) == 4:
                    year = result
                    results.remove(result)
                    break
            # regex : 
        # result = re.search(r"(located .*\.)", answer, re.IGNORECASE)
        results = re.findall(r"(?<=\<)[^\>\<]*(?=\>)", answer, re.IGNORECASE)

        if len(results) > 0:
            location = results[-1]
        else:
            location=  None
                
    except:
        print("bing didn't return an acceptable answer (compilation error)")

    # print("question sent to bing:", question)

    # command = ai.BingPython.sendcom_sydney(ai.BingPython.CreateSession(cookies), question)
    # answer=asyncio.get_event_loop().run_until_complete(command)
    # print(answer)  

    return revenue, sector, year, location

    

def get_year_of_foundation(question):
    print("question sent to bing:", question)

    command = ai.BingPython.sendcom_sydney(ai.BingPython.CreateSession(cookies), question)
    answer=asyncio.get_event_loop().run_until_complete(command)
    print(answer)
    # regex : was \w+ in (\d){4}
    result = re.search(r"(in \d{4})", answer, re.IGNORECASE)
    if result:
        return result.group(0)
    else:
        return None

# ans = get_revenue_sector("(industrial goods and services, technology, construction and materials, travel and leisure, healthcare) from these sectors could you tell me which sector is most related to r-pac.com company? and what is its avarge revenue?")
# ans = get_region("in what country is kaycan.com comapny located ? reply in one word")
# ans = get_year_of_foundation("when was regaltax.us comapny founded?")
# print(ans)