#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020 July
# @Author  : smyyan & ghoskno & WhymustIhaveaname
# @Software: Sublime Text

import time,os,re,pickle,requests,platform,sys,traceback,math
from io import BytesIO
from contextlib import ContextDecorator
from PIL import Image
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from decaptcha import DeCaptcha
from config import *

# 判断平台
osName = platform.system()
if osName not in ('Linux',):
    raise Exception('not support this system : %s'%(osName,))

LOGLEVEL={0:"DEBUG",1:"INFO",2:"WARN",3:"ERR",4:"FATAL"}
LOGFILE=sys.argv[0].split(".")
LOGFILE[-1]="log"
LOGFILE=".".join(LOGFILE)

def log(msg,l=1,end="\n",logfile=LOGFILE):
    st=traceback.extract_stack()[-2]
    lstr=LOGLEVEL[l]
    #now_str="%s %03d"%(time.strftime("%y/%m/%d %H:%M:%S",time.localtime()),math.modf(time.time())[0]*1000)
    now_str="%s"%(time.strftime("%y/%m/%d %H:%M:%S",time.localtime()),)
    perfix="%s [%s,%s:%03d]"%(now_str,lstr,st.name,st.lineno)
    if l<3:
        tempstr="%s %s%s"%(perfix,str(msg),end)
    else:
        tempstr="%s %s:\n%s%s"%(perfix,str(msg),traceback.format_exc(limit=5),end)
    print(tempstr,end="")
    if l>=1:
        with open(logfile,"a") as f:
            f.write(tempstr)

# 常量
_BASE_URL = 'https://bt.byr.cn/'
_tag_map = {
    'free': '免费',
    'twoup': '2x上传',
    'twoupfree': '免费&2x上传',
    'halfdown': '50%下载',
    'twouphalfdown': '50%下载&2x上传',
    'thirtypercent': '30%下载',
}
_cat_map = {
    '电影': 'movie',
    '剧集': 'episode',
    '动漫': 'anime',
    '音乐': 'music',
    '综艺': 'show',
    '游戏': 'game',
    '软件': 'software',
    '资料': 'material',
    '体育': 'sport',
    '记录': 'documentary',
}


# 全局变量
download_path = None
byrbt_cookies = None

if osName == 'Windows':
    download_path = os.path.abspath(windows_download_path)
elif osName == 'Linux':
    download_path = os.path.abspath(linux_download_path)

decaptcha = DeCaptcha()
decaptcha.load_model(decaptcha_model)

existed_torrent = []
transmission_cmd='transmission-remote -n %s '%(transmission_user_pw)

def get_url(url):
    return _BASE_URL + url


def login():
    url = get_url('login.php')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    session = requests.session()
    for i in range(3):
        login_content = session.get(url)
        login_soup = BeautifulSoup(login_content.text, 'lxml')

        img_url = _BASE_URL + login_soup.select('#nav_block > form > table > tr:nth-of-type(3) img')[0].attrs['src']
        img_file = Image.open(BytesIO(session.get(img_url).content))

        captcha_text = decaptcha.decode(img_file)

        login_res = session.post(get_url('takelogin.php'), headers=headers,
                                 data=dict(username=username, password=passwd, imagestring=captcha_text,
                                           imagehash=img_url.split('=')[-1]))
        if '最近消息' in login_res.text:
            cookies = {}
            for k, v in session.cookies.items():
                cookies[k] = v
            with open(cookies_save_path, 'wb') as f:
                pickle.dump(cookies, f)
            break
        log("failed the %dth try, retry in 3 seconds"%(i),l=2)
        time.sleep(3)
    else:
        raise Exception('Failed to get Cookies!')
    return cookies


def load_cookie():
    global byrbt_cookies
    if os.path.exists(cookies_save_path):
        log('%s found, loading cookies...'%(cookies_save_path,))
        read_path = open(cookies_save_path, 'rb')
        byrbt_cookies = pickle.load(read_path)
    else:
        log('%s not find, getting cookies...'%(cookies_save_path,))
        byrbt_cookies = login()
    return byrbt_cookies


def _get_tag(tag):
    try:
        if tag == '':
            return ''
        else:
            tag = tag.split('_')[0]

        return _tag_map[tag]
    except KeyError:
        return ''


def parse_torrent_info(table):
    assert isinstance(table, list)
    torrent_infos = []
    for item in table:
        torrent_info = {}
        tds = item.select('td')
        cat = tds[0].select('img')[0].attrs['title']
        main_td = tds[1].select('table > tr > td')[0]
        href = main_td.select('a')[0].attrs['href']
        seed_id = re.findall(r'id=(\d+)&', href)[0]
        title = main_td.text
        title = title.split('\n')
        if len(title) == 2:
            sub_title = title[1]
            title = title[0]
        else:
            sub_title = ''
            title = title[0]

        tags = set([font.attrs['class'][0] for font in main_td.select('b > font') if 'class' in font.attrs.keys()])
        if '' in tags:
            tags.remove('')

        is_seeding = len(main_td.select('img[src="pic/seeding.png"]')) > 0
        is_finished = len(main_td.select('img[src="pic/finished.png"]')) > 0

        is_hot = False
        if 'hot' in tags:
            is_hot = True
            tags.remove('hot')
        is_new = False
        if 'new' in tags:
            is_new = True
            tags.remove('new')
        is_recommended = False
        if 'recommended' in tags:
            is_recommended = True
            tags.remove('recommended')

        if 'class' in tds[1].select('table > tr')[0].attrs.keys():
            tag = _get_tag(tds[1].select('table > tr')[0].attrs['class'][0])
        else:
            tag = ''

        file_size = tds[6].text.split('\n')

        seeding = int(tds[7].text) if tds[7].text.isdigit() else -1

        downloading = int(tds[8].text) if tds[8].text.isdigit() else -1

        finished = int(tds[9].text) if tds[9].text.isdigit() else -1

        torrent_info['cat'] = cat
        torrent_info['is_hot'] = is_hot
        torrent_info['tag'] = tag
        torrent_info['is_seeding'] = is_seeding
        torrent_info['is_finished'] = is_finished
        torrent_info['seed_id'] = seed_id
        torrent_info['title'] = title
        torrent_info['sub_title'] = sub_title
        torrent_info['seeding'] = seeding
        torrent_info['downloading'] = downloading
        torrent_info['finished'] = finished
        torrent_info['file_size'] = file_size
        torrent_info['is_new'] = is_new
        torrent_info['is_recommended'] = is_recommended
        torrent_infos.append(torrent_info)

    return torrent_infos


def select_ok_torrent(torrent_infos):
    if len(torrent_infos) >= 20:  # 遇到free或者免费种子太多了，择优选取
        log('ok 种子过多，怀疑 free 了。。。')
    ok_infos = []
    for torrent_info in torrent_infos:
        if torrent_info['seed_id'] in existed_torrent:
            continue
        if 'GB' not in torrent_info['file_size'][0]:
            continue
        if torrent_info['seeding'] <= 0 or torrent_info['downloading'] < 0:
            continue
        ds_ratio=float(torrent_info['downloading']) / float(torrent_info['seeding'])
        if ds_ratio>0:
            ok_infos.append((ds_ratio,torrent_info))
    ok_infos.sort(key=lambda x:x[0],reverse=True)
    return [j for i,j in ok_infos[0:min(5,len(ok_infos))]]


def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


def op_help():
    return """
    byrbt bot: a bot that handles basic usage of bt.byr.cn
    usage:
        1. main - run main program
        5. refresh - refresh cookies
        6. help - print this message
        7. exit
    """


def get_info(text):
    text = text.split('\n')
    text = text[1:-2]
    text_s = []
    for t in text:
        ts = t.split()
        torrent = {'id':ts[0],'done':ts[1],'name':ts[-1]}

        tracker_info=os.popen(transmission_cmd+"-t %s -it"%(torrent['id'])).read()
        byr_flag=True
        for i in tracker_info.split("\n\n"):
            if "tracker.byr.cn" not in i:
                byr_flag=False
                break
        if not byr_flag:
            continue

        location_info=os.popen(transmission_cmd+"-t %s -i"%(torrent['id'])).read()
        for i in location_info.split("\n"):
            if i.strip().startswith("Location"):
                location_info=i.split(":")[-1].strip()
                break
        else:
            log("failed to get location info for id %s\n%s"%(torrent['id'],location_info))
            continue
        if not os.path.samefile(location_info,linux_download_path):
            continue

        if ts[3]=="GB":
            torrent['size']=float(ts[2])
        elif ts[3]=="TB":
            torrent['size']=float(ts[2])*1024
        elif ts[3]=="MB":
            torrent['size']=float(ts[2])/1024
        elif ts[3]=="Unknown":
            torrent['size']=1.0
        else:
            log("torrent size unit is neither GB nor TB not MB?\n%s"%(ts),l=2)
            torrent['size']=1.0
        text_s.append(torrent)
    log("可能删除：%s"%(text_s,))
    return text_s


class TorrentBot(ContextDecorator):
    def __init__(self):
        super(TorrentBot, self).__init__()
        self.cookie_jar = RequestsCookieJar()
        for k, v in byrbt_cookies.items():
            self.cookie_jar[k] = v
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    def remove(self):
        text=execCmd(transmission_cmd+'-l')
        text_s=get_info(text) #text_s: list of {'id': '153', 'done': '0%', 'size': '1GB', 'name': 'dadada'}
        text_s.sort(key=lambda x: int(x['id'].strip("*")), reverse=False) # 删除最久之前的种子
        while sum([i['size'] for i in text_s]) > max_torrent_size:
            remove_torrent_info = text_s.pop(0)
            log("removing %s"%(remove_torrent_info['name']))
            res = execCmd(transmission_cmd+'-t %s --remove-and-delete'%(remove_torrent_info['id'],))
            if "success" not in res:
                log('remove torrent failed: %s'%(remove_torrent_info))
                continue

            if os.path.exists(os.path.join(download_path, remove_torrent_info['name'])):
                log('remove %s from transmission-daemon success, but cat not remove it from disk!'%(remove_torrent_info['name']),l=2)
            else:
                log('remove %s from transmission-daemon success!'%(remove_torrent_info['name'],))

    def download(self, torrent_id):
        global byrbt_cookies
        download_url = 'download.php?id={}'.format(torrent_id)
        download_url = get_url(download_url)
        torrent_file_name = None
        for i in range(2):
            try:
                torrent = requests.get(download_url, cookies=self.cookie_jar, headers=self.headers)
                torrent_file_name = str(torrent.headers['Content-Disposition']\
                                            .split(';')[1]\
                                            .strip().split('=')[-1][1:-1]\
                                            .encode('ascii','ignore').decode('ascii')
                                        ).replace(' ', '#')
                log("正在下载 %s"%(torrent_file_name,))
                with open(os.path.join(download_path, torrent_file_name), 'wb') as f:
                    f.write(torrent.content)
                break

            except:
                log('login failed')
                byrbt_cookies = load_cookie()
                self.__init__()

        if torrent_file_name is not None and os.path.exists(os.path.join(download_path, torrent_file_name)):
            torrent_file_path = os.path.join(download_path, torrent_file_name)
            cmd_str = transmission_cmd+'-a %s'%(torrent_file_path,)
            ret_val = os.system(cmd_str)
            if ret_val != 0:
                log('script %s returns %s'%(cmd_str, ret_val))
                return False
            else:
                existed_torrent.append(torrent_id)
                return True
        else:
            return True

    def start(self):
        global byrbt_cookies
        while True:
            try:
                log('正在扫描 %s'%(get_url('torrents.php'),))
                getemp=requests.get(get_url('torrents.php'),cookies=self.cookie_jar,headers=self.headers).content
                torrents_soup = BeautifulSoup(getemp,features='lxml')
                torrent_table = torrents_soup.select('.torrents > form > tr')[1:]
            except:
                byrbt_cookies = load_cookie()
                self.__init__()
                continue

            torrent_infos = parse_torrent_info(torrent_table)

            free_infos = [torrent_info for torrent_info in torrent_infos if torrent_info['tag'] in ('免费', '免费&2x上传')]
            #s_temp=['%s : %s %s %s'%(i, info['seed_id'], info['file_size'][0], info['title']) for i, info in enumerate(free_infos)]
            #log('Free 种子列表：\n%s'%("\n".join(s_temp)))

            ok_torrent = select_ok_torrent(free_infos)
            s_temp=['%s : %s %s %s'%(i, info['seed_id'], info['file_size'][0], info['title']) for i,info in enumerate(ok_torrent)]
            log('将要下载：\n%s'%("\n".join(s_temp)))
            for torrent in ok_torrent:
                self.download(torrent['seed_id'])
            self.remove()
            time.sleep(search_time)


def main():
    byrbt_bot=TorrentBot()
    byrbt_bot.start()


if __name__ == '__main__':
    byrbt_cookies = load_cookie()
    log(op_help())
    while True:
        action_str = input("$ ")
        if action_str == 'refresh':
            log('refresh cookie by login!')
            byrbt_cookies = login()
        elif action_str == 'exit':
            break
        elif action_str == 'help':
            log(op_help())
        elif action_str == 'main':
            main()
        else:
            log('invalid operation')
            log(op_help())