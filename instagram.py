import os, sys, json
import requests, random, sqlite3
import time as t
from datetime import datetime

try: users = open("users.text", "r").read().replace(" ", "").split(",")
except FileNotFoundError: users = ["muratkazgan", "misrapower", "crnozden", "aselsan", "roketsan", "baykartech"]
if len(users) == 0: users = ["muratkazgan", "misrapower", "crnozden", "aselsan", "roketsan", "baykartech"]

try: dont = open("dont.text", "r").read().replace(" ", "").split(",")
except FileNotFoundError: dont = [""] # Listeyi buradan da belirleyebilirsiniz. 
if len(dont) == 0: dont = [""]

db = sqlite3.connect("instagram.sql")
ix = db.cursor()
ix.execute("CREATE TABLE IF NOT EXISTS users(uid, username, status)")
db.commit()

def Login():
    username = "kullaniciAdi"
    password = "sifre"

    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    time = int(datetime.now().timestamp())
    response = requests.get(link)
    csrf = response.cookies['csrftoken']

    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }

    login_response = requests.post(login_url, data=payload, headers=login_header)
    json_data = json.loads(login_response.text)

    try:json_data["authenticated"]
    except KeyError:
        if "password was incorrect" in login_response.text: print("Hatali sifre!")
        else: print(login_response.text)

        sys.exit()

    if json_data["authenticated"]:
        print("Giris basarili!")
        cookies = login_response.cookies
        cookie_jar = cookies.get_dict()
        csrf_token = cookie_jar['csrftoken']
        session_id = cookie_jar['sessionid']
        ds_user_id = cookie_jar['ds_user_id']
        ig_did = cookie_jar['ig_did']
        mid = cookie_jar['mid']
        rur = cookie_jar['rur']
        print("csrf_token: ", csrf_token)
        print("session_id: ", session_id)
        print()

        return (csrf_token, session_id, ds_user_id, ig_did, mid, rur)
    else:
        print("Giris basarisiz!")
        print(login_response.text)
        print()
        sys.exit()

def unameFinder(loginData, cookies):
    csrf_token, session_id, ds_user_id, ig_did, mid, rur  = loginData[0], loginData[1], loginData[2], loginData[3], loginData[4], loginData[5]
    current = random.choice(users)
    print("unameFinder(): {0}".format(current))

    headers= {
        'Host': 'www.instagram.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.instagram.com/{0}/'.format(current),
        'Cookie': 'csrftoken={0}; dpr=1.25; ig_did={1}; datr=AG1vZT9gY_J1zGua7G7o4VRt; mid={2}; ig_nrcb=1; rur={3}; ds_user_id={4}; sessionid={5}; shbid="10526\05448077411425\0541733391084:01f7912a893826d5e49754cf693c018ee1d381827d0a24610eb9d2933a5f2fd98afa073b"; shbts="1701855084\05448077411425\0541733391084:01f79b357141c444cbede30c0d9ed417448f9330fa28ff840b47d5423643221c9da69bd1"'.format(csrf_token, ig_did, mid, rur, ds_user_id, session_id),
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': '*/*',
        'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-IG-App-ID': '936619743392459',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'X-CSRFToken':csrf_token,
        'X-Requested-With': 'XMLHttpRequest'
    }

    imagesPk, codes = set(), dict()
    url = "https://www.instagram.com/api/v1/feed/user/{0}/username/?count=12".format(current)
    response = requests.request("GET", url, headers=headers, cookies=cookies)
    allof = response.json()["items"]
    for all in allof:
        imagesPk.add(all["pk"])
        codes[all["pk"]] = all["code"]

    print("Founded Post: " + str(len(imagesPk)))

    unameList = set()

    for pk in imagesPk:
        headers={
            'Host': 'www.instagram.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/p/{0}/'.format(codes[pk]),
            'Cookie': 'csrftoken={0}; dpr=1.25; ig_did={1}; datr=AG1vZT9gY_J1zGua7G7o4VRt; mid={2}; ig_nrcb=1; rur={3}; ds_user_id={4}; sessionid={5}; shbid="10526\05448077411425\0541733391084:01f7912a893826d5e49754cf693c018ee1d381827d0a24610eb9d2933a5f2fd98afa073b"; shbts="1701855084\05448077411425\0541733391084:01f79b357141c444cbede30c0d9ed417448f9330fa28ff840b47d5423643221c9da69bd1"'.format(csrf_token, ig_did, mid, rur, ds_user_id, session_id),
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': '*/*',
            'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
            'X-IG-App-ID': '936619743392459',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'X-CSRFToken':csrf_token,
            'X-Requested-With': 'XMLHttpRequest'
        }

        url = "https://www.instagram.com/api/v1/media/{0}/likers/".format(pk)
        response = requests.request("GET", url, headers=headers, cookies=cookies)
        allof = response.json()["users"]
        for all in allof:
            if all["is_private"] == True:
                if all["username"] not in dont:
                    ix.execute("SELECT * FROM users WHERE uid='{0}'".format(all["pk"]))
                    if ix.fetchone() == None:
                        turp = (all["pk"], all["username"], "pending")
                        ix.execute("INSERT INTO users VALUES (?, ?, ?)", turp)
                        db.commit()
                
        ix.execute("SELECT * FROM users WHERE status='pending'")
        totalLen = len(ix.fetchall())
        print("Total Pending: " + str(totalLen))
        t.sleep(60)
    

def Cleaner(loginData, cookies):
    csrf_token, session_id, ds_user_id, ig_did, mid, rur  = loginData[0], loginData[1], loginData[2], loginData[3], loginData[4], loginData[5]

    ix.execute("SELECT uid, username FROM users WHERE status='req'")
    fromDb = ix.fetchall()
    for fdb in fromDb:
        uid, uname = fdb[0], fdb[1]
        print("{0} -> {1}".format(uid, uname))
        headers={
        'Host': 'www.instagram.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.instagram.com/{0}/'.format(uname),
        'Cookie': 'csrftoken={0}; dpr=1.25; ig_did={1}; datr=AG1vZT9gY_J1zGua7G7o4VRt; mid={2}; ig_nrcb=1; rur={3}; ds_user_id={4}; sessionid={5}; shbid="10526\05448077411425\0541733391084:01f7912a893826d5e49754cf693c018ee1d381827d0a24610eb9d2933a5f2fd98afa073b"; shbts="1701855084\05448077411425\0541733391084:01f79b357141c444cbede30c0d9ed417448f9330fa28ff840b47d5423643221c9da69bd1"'.format(csrf_token, ig_did, mid, rur, ds_user_id, session_id),
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': '*/*',
        'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-IG-App-ID': '936619743392459',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'X-CSRFToken':csrf_token,
        }
        url = "https://www.instagram.com/api/v1/friendships/destroy/{0}/".format(uid)
        data = "container_module=profile&nav_chain=PolarisProfileNestedContentRoot%3AprofilePage%3A3%3Atopnav-link%2CPolarisProfileNestedContentRoot%3AprofilePage%3A4%3Aunexpected%2CPolarisProfileNestedContentRoot%3AprofilePage%3A6%3Aunexpected&user_id=" + uid
        response = requests.post(url, data=post, headers=headers, cookies=cookies)
        if response.json()["following"] == False:
            ix.execute("UPDATE users SET status='ok' WHERE uid='{0}'".format(uid))
            db.commit()
    print("+ Takip edilen hesaplar takipten cikarildi.")

loginData = Login() # Kontrole gerek yok, başarısız olursa çıkamaz.
csrf_token, session_id, ds_user_id, ig_did, mid, rur  = loginData[0], loginData[1], loginData[2], loginData[3], loginData[4], loginData[5]
cookies = {"sessionid": session_id, "csrftoken": csrf_token, "ds_user_id": ds_user_id, "ig_did": ig_did, "mid": mid, "rur" : rur}


clean = input("Temizlik yapmak ister misiniz (y/n): ").lower()
if clean == "y": Cleaner(loginData, cookies)

ix.execute("SELECT uid, username FROM users WHERE status='pending'")
unameList = ix.fetchall()
currentList = []
if len(unameList) < 100:
    unameFinder(loginData, cookies)
    ix.execute("SELECT uid, username FROM users WHERE status='pending'")
    currentUList = ix.fetchall()
    if len(currentUList) < 100:
        if len(currentUList) > len(unameList):
            unameFinder(loginData, cookies)
            ix.execute("SELECT uid, username FROM users WHERE status='pending'")
            currentUList2 = ix.fetchall()
            if len(currentUList2) < 100:
                print("Toplam KullaniciAdi: {0}".format(str(len(currentUList))))
                sys.exit()
            else: currentList = currentUList2
        elif len(currentUList) == len(unameList):
            print("Toplam KullaniciAdi: {0}".format(str(len(currentUList))))
            sys.exit()
    else: currentList = currentUList
else: currentList = unameList


counter = 1
for cList in currentList:
    id, uname = cList[0], cList[1]

    print(str(counter) + "-> " + uname)

    headers={
        'Host': 'www.instagram.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.instagram.com/{0}/'.format(uname),
        'Cookie': 'csrftoken={0}; dpr=1.25; ig_did={1}; datr=AG1vZT9gY_J1zGua7G7o4VRt; mid={2}; ig_nrcb=1; rur={3}; ds_user_id={4}; sessionid={5}; shbid="10526\05448077411425\0541733391084:01f7912a893826d5e49754cf693c018ee1d381827d0a24610eb9d2933a5f2fd98afa073b"; shbts="1701855084\05448077411425\0541733391084:01f79b357141c444cbede30c0d9ed417448f9330fa28ff840b47d5423643221c9da69bd1"'.format(csrf_token, ig_did, mid, rur, ds_user_id, session_id),
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': '*/*',
        'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-IG-App-ID': '936619743392459',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'X-CSRFToken':csrf_token,
        'X-Requested-With': 'XMLHttpRequest'
    }

            
    url = "https://www.instagram.com/api/v1/friendships/create/{0}/".format(id)
    post = "container_module=profile&nav_chain=PolarisDirectInboxRoot%3ADirectInboxPage%3A2%3Atopnav-link%2CPolarisDirectMessageRequestRoot%3ADirectRequestPage%3A3%3Aunexpected%2CPolarisProfileNestedContentRoot%3AprofilePage%3A4%3Aunexpected%2CPolarisProfileNestedContentRoot%3AprofilePage%3A5%3Aunexpected%2CPolarisProfileNestedContentRoot%3AprofilePage%3A6%3Aunexpected&user_id=" + id

    go = 0
    for r in range(3):
        try: 
            response = requests.post(url, data=post, headers=headers, cookies=cookies)
            go = 1
            break
        except requests.exceptions.TooManyRedirects: 
            print("TooManyRedirects") # CheckPoint kaynaklı olabilir

    if go == 1:
        try:
            if response.json()["friendship_status"]["outgoing_request"] == True: print("        -> Istek gonderildi.")
            else:
                if response.json()["friendship_status"]["following"] == True: 
                    print("Zaten takip ediliyor.")
                    ix.execute("UPDATE users SET status='req' WHERE uid='{0}'".format(id))
                    db.commit()
                else: print(response.json())
        except KeyError:
            print("KeyError 1")
            print(response.text)
            print(response.json())
            if 'require_login":true' in response.text:
                loginData = Login()
                csrf_token, session_id, ds_user_id, ig_did, mid, rur  = loginData[0], loginData[1], loginData[2], loginData[3], loginData[4], loginData[5]
                cookies = {"sessionid": session_id, "csrftoken": csrf_token, "ds_user_id": ds_user_id, "ig_did": ig_did, "mid": mid, "rur" : rur}
                try:
                    if response.json()["friendship_status"]["outgoing_request"] == True: print("        -> istek gonderildi.")
                    else: 
                        if response.json()["friendship_status"]["following"] == True: 
                            print("Zaten takip ediliyor.")
                            ix.execute("UPDATE users SET status='req' WHERE uid='{0}'".format(id))
                            db.commit()
                        else: print(response.json())
                except KeyError:
                    print("KeyError 2")
                    print(response.json())
                    print(response.text)
                    sys.exit()

        ix.execute("UPDATE users SET status='req' WHERE username='{0}'".format(uname))
        db.commit()
        counter+=1
        if counter == 100:
            print("100 istek gonnderildi.")
            sys.exit()

        t.sleep(96)
    else: 
        t.sleep(30)