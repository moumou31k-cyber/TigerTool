#!/usr/bin/env python3
# Tiger Tools - Setup
import subprocess, sys, os, platform

DEPS = [
    "requests",
    "colorama",
    "Pillow",
]

def clr():
    os.system("cls" if platform.system()=="Windows" else "clear")

def main():
    clr()
    print("""
\033[31m
 ████████╗██╗ ██████╗ ███████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗
    ██╔══╝██║██╔════╝ ██╔════╝██╔══██╗       ██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
    ██║   ██║██║  ███╗█████╗  ██████╔╝       ██║   ██║   ██║██║   ██║██║     ███████╗
    ██║   ██║██║   ██║██╔══╝  ██╔══██╗       ██║   ██║   ██║██║   ██║██║     ╚════██║
    ██║   ██║╚██████╔╝███████╗██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
    ╚═╝   ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
\033[0m
  \033[2mSETUP - Installing dependencies...\033[0m
  \033[31m════════════════════════════════════════════════════════════\033[0m
""")

    for dep in DEPS:
        print(f"  \033[33m[~]\033[0m Installing {dep}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", dep,
             "--quiet", "--disable-pip-version-check"],
            capture_output=True
        )
        if result.returncode == 0:
            print(f"  \033[32m[+]\033[0m {dep} OK")
        else:
            print(f"  \033[31m[-]\033[0m {dep} FAILED (may already be installed)")

    os.makedirs("1-Output", exist_ok=True)
    os.makedirs("2-Input",  exist_ok=True)

    print(f"""
  \033[32m[+]\033[0m Setup complete.
  \033[33m[~]\033[0m Launching TigerTools...
""")
    input("  Press Enter to start > ")
    os.execv(sys.executable, [sys.executable, "TigerTools.py"])

if __name__ == "__main__":
    main()
