import http.server
import socketserver
import requests
import time
import threading
import os
import configparser
import socket

#cd "c:/Users/Shadow/Downloads/WSML/" && C:/Users/Shadow/AppData/Local/Microsoft/WindowsApps/python3.11.exe "main.py"

WEBProto = "HTTP"
WEBVer = "5, 4"
exit_flag = False

config = configparser.ConfigParser()

def GetLatency():
    while not exit_flag:
        url = f"http://{localIp}:{CurPort}"
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        latency_text = "\r["+Fore.DEFAULT+"!"+Fore.RESET+"] Latency: "+Fore.DEFAULT+f"{latency_ms:.2f}"+Fore.RESET+" ms".ljust(80)
        print(latency_text, end="", flush=True)
        time.sleep(1)

def SaveData():
    config['Data'] = {
        'serverPort': CurPort,
        'folderPath': html_directory,
        'defaultColor' : default_color,
        'firstFile' : first_file,
        'localIP' : localIp,
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

config_exists = config.read('config.ini')

if config_exists and config.has_option('Data', 'serverPort'):
   CurPort = config.get('Data', 'serverPort')
   CurPort = int(CurPort)
else:
   CurPort = 8080
   CurPort = int(CurPort)

if config_exists and config.has_option('Data', 'folderPath'):
   html_directory = config.get('Data', 'folderPath')
else:
   html_directory = "HTML"

if config_exists and config.has_option('Data', 'defaultColor'):
   default_color = config.get('Data', 'defaultColor')
else:
   default_color = "GREEN"

if config_exists and config.has_option('Data', 'firstFile'):
   first_file = config.get('Data', 'firstFile')
else:
   first_file = "test.html"

if config_exists and config.has_option('Data', 'localIP'):
    localIp = config.get('Data', 'localIP')
    if localIp == "localhost":
        pass
    else:
        localIp = socket.gethostbyname(socket.gethostname())
else:
   localIp = "localhost"

if default_color == "GREEN":
    class Fore:
        DEFAULT = "\u001b[32m"
        RESET = "\u001b[37m"
elif default_color == "RED":
    class Fore:
        DEFAULT = "\u001b[31m"
        RESET = "\u001b[37m"
elif default_color == "BLACK":
    class Fore:
        DEFAULT = "\u001b[30m"
        RESET = "\u001b[37m"
elif default_color == "YELLOW":
    class Fore:
        DEFAULT = "\u001b[33m"
        RESET = "\u001b[37m"
elif default_color == "BLUE":
    class Fore:
        DEFAULT = "\u001b[34m"
        RESET = "\u001b[37m"
elif default_color == "MAGENTA":
    class Fore:
        DEFAULT = "\u001b[35m"
        RESET = "\u001b[37m"
elif default_color == "CYAN":
    class Fore:
        DEFAULT = "\u001b[36m"
        RESET = "\u001b[37m"

#Verification of server folder presence
try:
    fileCheck = os.listdir(html_directory)
    if fileCheck:
        first_file = fileCheck[0]
except FileNotFoundError:
    html_directory = "HTML"

while True:
    os.system("cls")
    print(Fore.DEFAULT+""" _ _ _  ___  __ __  _   
| | | |/ __>|  \  \| |  
| | | |\__ \|     || |_ 
|__/_/ <___/|_|_|_||___|"""+Fore.RESET)
    main = input(Fore.DEFAULT+"W"+Fore.RESET+"eb "+Fore.DEFAULT+"S"+Fore.RESET+"erver "+Fore.DEFAULT+"M"+Fore.RESET+"anager/"+Fore.DEFAULT+"L"+Fore.RESET+"auncher - "+Fore.DEFAULT+"V1.1"+Fore.RESET+"\n\n"+Fore.DEFAULT+"INFORMATIONS"+Fore.RESET+":\nCurrent server IP : "+Fore.DEFAULT+f"{localIp}"+Fore.RESET+"\nServer root folder : "+Fore.DEFAULT+f"{html_directory}"+Fore.RESET+"\nStandard Web protocol : "+Fore.DEFAULT+f"{WEBProto}"+Fore.RESET+"\nSupported HTML versions : "+Fore.DEFAULT+f"{WEBVer}"+Fore.RESET+"\nCurrent port : "+Fore.DEFAULT+f"{CurPort}"+Fore.RESET+"\n\n"+Fore.DEFAULT+"MAIN FEATURES"+Fore.RESET+":\n["+Fore.DEFAULT+"1"+Fore.RESET+"]- Launch\n["+Fore.DEFAULT+"2" + Fore.RESET+"]- Server settings\n["+Fore.DEFAULT+"3"+Fore.RESET+"]- Settings\n["+Fore.DEFAULT+"4"+Fore.RESET+"]- Quit\n\n["+Fore.DEFAULT+"WSML 1.0"+Fore.RESET+"] >>>"+Fore.DEFAULT+" ")
    print(Fore.RESET)

    if main == "1":
        try:
            print("["+Fore.DEFAULT+"!"+Fore.RESET+"] "+Fore.DEFAULT+"Launching"+Fore.RESET+" web server...\n")
            time.sleep(2.5)
            class MyHandler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=html_directory, **kwargs)
                def log_message(self, format, *args):
                    pass
            with socketserver.TCPServer((localIp, CurPort), MyHandler) as httpd:
                print(f"["+Fore.DEFAULT+"!"+Fore.RESET+"] Server "+Fore.DEFAULT+"running"+Fore.RESET+" on : "+Fore.DEFAULT+f"http://{localIp}:{CurPort}/{first_file}"+Fore.RESET)
                print("["+Fore.DEFAULT+"!"+Fore.RESET+"] Server port : "+Fore.DEFAULT+f"{CurPort}"+Fore.RESET)
                print("["+Fore.DEFAULT+"!"+Fore.RESET+"] Your server is online since :")
                print("["+Fore.DEFAULT+"!"+Fore.RESET+"] Press "+Fore.DEFAULT+"CTRL+C"+Fore.RESET+" to stop the server ("+Fore.DEFAULT+"If this doesn't work, please refresh the server's web page"+Fore.RESET+")\n")
                latency_thread = threading.Thread(target=GetLatency)
                latency_thread.start()
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n["+Fore.DEFAULT+"!"+Fore.RESET+"] "+Fore.DEFAULT+"Shutting"+Fore.RESET+" down server...")
            exit_flag = True
            latency_thread.join()
            print("["+Fore.DEFAULT+"!"+Fore.RESET+"] Server "+Fore.DEFAULT+"successfully"+Fore.RESET+" stopped !")
            time.sleep(3.2)
            exit_flag = False

    elif main == "2":
        while True:
            ss_input = input("["+Fore.DEFAULT+"1"+Fore.RESET+"]- Change server port\n["+Fore.DEFAULT+"2"+Fore.RESET+"]- Change server root folder\n["+Fore.DEFAULT+"3"+Fore.RESET+"]- Change server IP\n["+Fore.DEFAULT+"4"+Fore.RESET+"]- Back\n\n["+Fore.DEFAULT+"Server settings"+Fore.RESET+"] >>>"+Fore.DEFAULT+" ")
            print(Fore.RESET)

            if ss_input == "1":
                while True:
                    SaveCurPort = CurPort
                    print("Current port : "+Fore.DEFAULT+f"{CurPort}"+Fore.RESET)
                    CurPort = input("Enter a port ("+Fore.DEFAULT+"0-65535"+Fore.RESET+") :"+Fore.DEFAULT+" ")
                    CurPort = int(CurPort)
                    print(Fore.RESET)
                    if CurPort > 65535 or CurPort < 0:
                        print("\n["+Fore.DEFAULT+"X"+Fore.RESET+"] Choose a number "+Fore.DEFAULT+"between"+Fore.RESET+" 0 and 65535")
                        CurPort = SaveCurPort
                    else:
                        print("Port "+Fore.DEFAULT+"successfully"+Fore.RESET+" changed to "+Fore.DEFAULT+f"{CurPort}"+Fore.RESET+" !\n")
                        SaveData()
                        break

            elif ss_input == "2":
                while True:
                    print("Current root folder : "+Fore.DEFAULT+f"{html_directory}"+Fore.RESET)
                    html_directory = input("Enter a folder path ("+Fore.DEFAULT+"C:/Users/User/Downloads/test/HTML"+Fore.RESET+") :"+Fore.DEFAULT+" ")
                    print(Fore.RESET)
                    try:
                        file_check = os.listdir(html_directory)
                        if file_check:
                            first_file = file_check[0]
                            print("Server folder path "+Fore.DEFAULT+"successfully"+Fore.RESET+" changed to "+Fore.DEFAULT+f"{html_directory}"+Fore.RESET+" !\n")
                            SaveData()
                            break
                    except FileNotFoundError:
                        print("["+Fore.DEFAULT+"X"+Fore.RESET+"] Choose an "+Fore.DEFAULT+"existing"+Fore.RESET+" folder !\n")
                        time.sleep(1.9)

            elif ss_input == "3":
                while True:
                    SavelocalIP = localIp
                    print("Current server IP : "+Fore.DEFAULT+f"{localIp}"+Fore.RESET)
                    localIp = input("Choose between '"+Fore.DEFAULT+"localip"+Fore.RESET+"' or '"+Fore.DEFAULT+"localhost"+Fore.RESET+"' :"+Fore.DEFAULT+" ")
                    print(Fore.RESET)
                    if localIp == "localip":
                        localIp = socket.gethostbyname(socket.gethostname())
                        print("Server IP "+Fore.DEFAULT+"successfully"+Fore.RESET+" changed to "+Fore.DEFAULT+f"{localIp}"+Fore.RESET+" !\n")
                        SaveData()
                        break
                    elif localIp == "localhost":
                        localIp = "localhost"
                        print("Server IP "+Fore.DEFAULT+"successfully"+Fore.RESET+" changed to "+Fore.DEFAULT+f"{localIp}"+Fore.RESET+" !\n")
                        SaveData()
                        break
                    else:
                        localIp = SavelocalIP
                        print("["+Fore.DEFAULT+"X"+Fore.RESET+"] Please select an "+Fore.DEFAULT+"existing"+Fore.RESET+" option between '"+Fore.DEFAULT+"localip"+Fore.RESET+"' or '"+Fore.DEFAULT+"localhost"+Fore.RESET+"' !\n")
                        time.sleep(1.9)
            elif ss_input == "4":
                break
            else:
                print("["+Fore.DEFAULT+"X"+Fore.RESET+"] Please select an "+Fore.DEFAULT+"existing"+Fore.RESET+" option !\n")
                time.sleep(1.9)
    
    elif main == "3":
        while True:
            s_input = input("["+Fore.DEFAULT+"1"+Fore.RESET+"]- Change default color\n["+Fore.DEFAULT+"2"+Fore.RESET+"]- Back\n\n["+Fore.DEFAULT+"Settings"+Fore.RESET+"] >>>"+Fore.DEFAULT+" ")
            print(Fore.RESET)

            if s_input == "1":
                color_s = input("["+Fore.DEFAULT+"1"+Fore.RESET+"]- Green (Default)\n["+Fore.DEFAULT+"2"+Fore.RESET+"]- Red\n["+Fore.DEFAULT+"3"+Fore.RESET+"]- Black\n["+Fore.DEFAULT+"4"+Fore.RESET+"]- Yellow\n["+Fore.DEFAULT+"5"+Fore.RESET+"]- Blue\n["+Fore.DEFAULT+"6"+Fore.RESET+"]- Magenta\n["+Fore.DEFAULT+"7"+Fore.RESET+"]- Cyan\n\n["+Fore.DEFAULT+"Colors"+Fore.RESET+"] >>>"+Fore.DEFAULT+" ")
            
                if color_s == "1":
                    default_color = "GREEN"
                    class Fore:
                        DEFAULT = "\u001b[32m"
                        RESET = "\u001b[37m"
                elif color_s == "2":
                    default_color = "RED"
                    class Fore:
                        DEFAULT = "\u001b[31m"
                        RESET = "\u001b[37m"
                elif color_s == "3":
                    default_color = "BLACK"
                    class Fore:
                        DEFAULT = "\u001b[30m"
                        RESET = "\u001b[37m"
                elif color_s == "4":
                    default_color = "YELLOW"
                    class Fore:
                        DEFAULT = "\u001b[33m"
                        RESET = "\u001b[37m"
                elif color_s == "5":
                    default_color = "BLUE"
                    class Fore:
                        DEFAULT = "\u001b[34m"
                        RESET = "\u001b[37m"
                elif color_s == "6":
                    default_color = "MAGENTA"
                    class Fore:
                        DEFAULT = "\u001b[35m"
                        RESET = "\u001b[37m"
                elif color_s == "7":
                    default_color = "CYAN"
                    class Fore:
                        DEFAULT = "\u001b[36m"
                        RESET = "\u001b[37m"
                else:
                    print("["+Fore.DEFAULT+"X"+Fore.RESET+"] Choose a "+Fore.DEFAULT+"correct"+Fore.RESET+" color !")
                SaveData()
                print(Fore.RESET)
                break

            elif s_input == "2":
                break
            else:
                print("["+Fore.DEFAULT+"X"+Fore.RESET+"] Please select an "+Fore.DEFAULT+"existing"+Fore.RESET+" option !\n")
                time.sleep(1.9)

    elif main == "4":
        print("["+Fore.DEFAULT+"!"+Fore.RESET+"] Thank you for using "+Fore.DEFAULT+"WSML"+Fore.RESET+" 1.1\n")
        time.sleep(0.8)
        break
    else:
        print("["+Fore.DEFAULT+"X"+Fore.RESET+"] Please select an "+Fore.DEFAULT+"existing"+Fore.RESET+" option !\n")
        time.sleep(1.9)