#!/usr/bin/env python3
# coding: utf-8

from requests import Session
from bs4 import BeautifulSoup as bs
from os import environ, system
from os.path import join, isdir, split
from os import makedirs as mkdir
from json import loads
from sys import argv
from sys import stderr
import winreg
from pprint import pprint
from ctypes import windll
from threading import Thread
from subprocess import Popen, DEVNULL

baseurl = "https://bandori.fandom.com"
downloadBasePath = join(environ["homepath"], "BandoriWiki")
artistCorresp = {
    "Hello, Happy World!": "ハロー、ハッピーワールド!",
    "Pastel*Palettes": "Pastel✽Palettes"
}
ffplay_path = join("bin", "ffplay.exe")
ffplay_path = join(split(__file__)[0], ffplay_path)
appname = "BanG Dream Music Player"
play_legacy = False
console_string = "bandoriplay>"


class Player():
    def __init__(self, url=None):
        self.url = url
        self.ps = None
        self.playing = False
        self.loop = False

    def setURL(self, url):
        self.url = url

    def waitFunc(self):
        self.wait()
        self.playing = False
        if self.loop:
            self.play()

    def play(self, url=None):
        if url:
            self.setURL(url)
        if not self.url:
            return
        if self.playing:
            self.stop()
        self.command = "ffplay -i {} -nodisp -autoexit".format(self.url)
        envcopy = environ.copy()
        if global_proxy is not None:
            envcopy["http_proxy"] = global_proxy["http"]
            envcopy["https_proxy"] = global_proxy["https"]
        if play_legacy:
            system(self.command)
        else:
            self.ps = Popen(self.command.split(), stderr=DEVNULL, env=envcopy)
            self.wait = self.ps.wait
            self.playing = True
            self.waitThread = Thread(target=self.waitFunc)
            self.waitThread.start()

    def stop(self):
        if not self.ps:
            return
        self.ps.terminate()
        self.ps = None


def get_proxy():
    if "--proxy" in argv:
        try:
            p = argv[argv.index("--proxy") + 1]
            proxy = {
                "http": p,
                "https": p
            }
            print("Option  : Using proxy \"" + p + "\"")
        except IndexError:
            print("Warning: The proxy has been disabled because the \"--proxy\" option was specified but no value was entered")
            pass
    elif "--disable-proxy" in argv:
        return None
    elif "http_proxy" in [x.lower() for x in list(environ.keys())]:
        proxy = {
            "http": environ["http_proxy"].replace("http://", "").replace("/", ""),
            "https": environ["https_proxy"].replace("https:", "").replace("http:", "").replace("/", "")
        }
        print("Option  : Using proxy", str(proxy), "(environ)")
    elif "https_proxy" in [x.lower() for x in list(environ.keys())]:
        proxy = {
            "http": environ["https_proxy"].replace("http://", "").replace("/", ""),
            "https": environ["https_proxy"].replace("https://", "").replace("/", "")
        }
        print("Option  : Using proxy \"" + proxy["http"] + "\" (environ)")
    else:
        path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, path)
        p, regtype = winreg.QueryValueEx(key, 'ProxyServer')
        e, regtype = winreg.QueryValueEx(key, 'ProxyEnable')
        e = bool(e)
        winreg.CloseKey(key)  # key.Close() と書いても同じ
        if bool(e):
            proxy = {
                "http": p,
                "https": p
            }
            print("Option  : Using proxy \"" + proxy["http"] + "\" (System Setting)")
        else:
            proxy = None
    return proxy


def getSongList(s=Session()):
    g = s.get(baseurl + "/wiki/BanG_Dream!_Girls_Band_Party!/Playable_Songs",
              proxies=global_proxy)
    f = bs(g.text, "lxml")
    f = f.find("div", class_="mw-content-text").find_all("table")
    songlist = list()
    for x in f:
        lt = list()
        for y in x.find_all("a"):
            lt.append({
                "title": y.get("title"),
                "url": y.get("href"),
            })
        songlist += lt
    return songlist


def getSongInfo(url, s=Session()):
    g = s.get(baseurl + url, proxies=global_proxy)
    f = bs(g.text, "lxml")
    audio = list()
    for x in f.find("table", class_="article-table").find_all("tr")[1:]:
        t = x.find_all("td")
        title = t[1].text.replace("\n", "")
        audio.append({
            "title": title,
            "length": t[2].text.replace("\n", ""),
            "url": x.find("span", class_="ogg_custom").button.get("onclick").split("rl\":\"")[1].split("\",\"")[0],
            "inst": "instrumental" in title,
            "gamever": "(Game Version)" in title
        })
        del title
    try:
        title = f.find("div", class_="mw-content-text").i.span.text
    except AttributeError:
        try:
            title = f.find("div", class_="pi-data-value pi-font").text
        except AttributeError:
            title = f.find("div", class_="page-header__main").h1.text
    try:
        artist = artistCorresp[f.find(
            "div", class_="mw-content-text").p.find_all("a")[0].text]
    except KeyError:
        artist = f.find(
            "div", class_="mw-content-text").p.find_all("a")[0].text
    try:
        _bpm = f.find("div", class_="mw-content-text").find("div", style="float:left;").find_all("table")[2].tr.find_all("td")[1].text.replace("\n", "").replace(" BPM", "")
        bpm = int(_bpm)
    except AttributeError:
        try:
            bpm = f.find("div", attrs={"id": "mw-content-text"}).find("div", style="float:left;").find_all("table")[2].tr.find_all("td")[1].text.replace("\n", "").replace(" BPM", "").replace(" ~ ", "-")
        except AttributeError:
            try:
                bpm = f.find("div", attrs={"id": "mw-content-text"}).table.find_all("table")[-1].find_all("td")[-1].text.replace("\n", "").replace(" BPM", "").replace(" ~ ", "-")
            except AttributeError:
                bpm = "Unacquirable"
                stderr.write("Error: BPM unacquirable.\n")
    except ValueError:
        bpm = _bpm
    info = {
        "title": title,
        "artwork": f.find("a", class_="image-thumbnail").get("href"),
        "bpm": bpm,
        "audio": audio,
        "artist": artist
    }
    return info


def suggestSearch(q, s=Session()):
    g = s.get(baseurl + "/index.php", params={
        "action": "ajax",
        "rs": "getLinkSuggest",
        "format": "json",
        "query": q
    }, proxies=global_proxy)
    return loads(g.text)["suggestions"]


def searchAudio(q, s=Session()):
    if q == "q" or q is None or len(q) == 0:
        return False
    sug = suggestSearch(q=q, s=s)
    ss = True
    if len(sug) != 0:
        n = 0
        for x in sug:
            print(n, "\t" + x)
            n += 1
    else:
        if s.get(baseurl + "/wiki/" + q).status_code != 404:
            r = "/wiki/" + q
            ss = False
        else:
            print("No hit.")
            return False
    if ss:
        while True:
            try:
                i = input("Whitch?[0] : ")
                if len(i) == 0:
                    i = 0
                elif i.lower() == "q":
                    return False
                else:
                    i = int(i)
                break
            except ValueError:
                print("Please enter valid number.")
                pass
        r = "/wiki/" + sug[i]
    info = getSongInfo(r, s=s)
    print("Title : \t", info["title"])
    print("Artist :\t", info["artist"])
    return info


def playAudio(d, num=None):
    global global_proxy
    if global_proxy is None:
        _global_proxy = None
    else:
        _global_proxy = global_proxy.copy()
    if global_proxy is not None:
        if global_proxy["http"][:7] != "http://":
            global_proxy["http"] = "http://" + global_proxy["http"]
        environ["http_proxy"] = global_proxy["http"]
        if global_proxy["https"][:8] != "https://":
            global_proxy["https"] = "https://" + global_proxy["https"]
        environ["https_proxy"] = global_proxy["https"]
    print("Title : \t", d["data"]["title"])
    print("Artist :\t", d["data"]["artist"])
    if num is None:
        n = 0
        for x in d["data"]["audio"]:
            print(n, "\t" + x["title"])
            n += 1
        i = input("Whitch?[0] : ")
        if len(i) == 0:
            i = 0
        else:
            i = int(i)
    else:
        i = int(num)
    url = d["data"]["audio"][i]["url"]
    global_proxy = _global_proxy
    windowtitle = appname + " : Playing \""+ d["data"]["title"] +"\"."
    windll.kernel32.SetConsoleTitleW(windowtitle)
    player.setURL(url)
    player.play()
    return i


def downloadAudio(d, num=None, s=Session()):
    print("Title : \t", d["data"]["title"])
    print("Artist :\t", d["data"]["artist"])
    n = 0
    for x in d["data"]["audio"]:
        print(n, "\t" + x["title"])
        n += 1
    while True:
        try:
            i = input("Whitch?[0] : ")
            if len(i) == 0:
                i = 0
            elif i.lower() == "q":
                return
            else:
                i = int(i)
            break
        except ValueError:
            print("Please enter number")
            pass
    print("Download :", d["data"]["audio"][i]["url"])
    path = downloadBasePath
    if not isdir(path):
        mkdir(path)
    filename = d["data"]["title"].replace(" ", "_")
    if d["data"]["audio"][i]["gamever"]:
        filename += "_gamever"
    elif d["data"]["audio"][i]["inst"]:
        filename += "_inst"
    filename += ".ogg"
    with open(join(path, filename), "wb") as fp:
        with s.get(d["data"]["audio"][i]["url"], proxies=global_proxy) as g:
            fp.write(g.content)


def _console(i=None):
    global current
    if i is None:
        i = input(console_string).split(" ")
    while "" in i:
        i.remove("")
    if len(i) == 0:
        return False
    elif i[0].lower() in ["search", "s"]:
        if len(i) >= 2:
            q = " ".join(i[1:])
        else:
            q = input("search>")
        d = searchAudio(q=q)
        if d is False:
            return d
        current["data"] = d
        current["set"] = True
    elif i[0].lower() in ["play", "p"]:
        if not current["set"]:
            print("Error: Please set current song.")
            pass
        else:
            if len(i) == 1:
                playAudio(current)
            else:
                try:
                    playAudio(current, num=int(i[1]))
                except ValueError:
                    playAudio(current)
    elif i[0].lower() in ["download", "d"]:
        if not current["set"]:
            print("Error: Please set current song.")
            pass
        else:
            if len(i) == 1:
                n = None
            else:
                try:
                    n = int(i[1])
                except ValueError:
                    n = None
            downloadAudio(current, num=n)
    elif i[0].lower() == "stop":
        player.stop()
        windll.kernel32.SetConsoleTitleW(appname)
    elif i[0].lower() == "showproxy":
        print("proxy :", global_proxy)
        pass
    elif i[0].lower() == "showurl":
        print("Status :", "set" if current["set"] else "not set")
        return
        if current["set"]:
            pprint(current["data"])
            pass
    elif i[0].lower() == "loop":
        if len(i) <= 1:
            player.loop = not player.loop
            print("Loopmode :", player.loop)
        elif i[1].lower() == "on":
            player.loop = True
            print("Loopmode \"Loop\"")
        else:
            player.loop = False
            print("Loopmode \"no Loop\"")
    elif i[0].lower() == "clear":
        current = {"set": False, "data": {}}
    elif i[0].lower() in ["quit", "exit", "q"]:
        player.stop()
        print("Bye.")
        return True
    else:
        print("Unknown command:", i[0])
        pass


def console():
    global current
    current = {"set": False, "data": {}}
    while True:
        cr = _console()
        if cr:
            return cr


def start():
    global global_proxy
    global player
    windll.kernel32.SetConsoleTitleW(appname)
    global_proxy = get_proxy()
    player = Player()
    console()


if __name__ == "__main__":
    start()
