# ##################需要配置的变量###################
username = '用户名'
passwd = '密码'
transmission_user_pw = 'user:passwd'  # transmission的用户名和密码，按照格式填入
windows_download_path = './torrent'  # windows测试下载种子路径
linux_download_path = '<path_to_download_dir>'  # linux服务器下载种子的路径
torrent_infos = './torrent.pkl'  # 种子信息保存文件路径
max_torrent = 20  # 最大种子数
search_time = 120  # 轮询种子时间，默认120秒
# ##################################################
decaptcha_model = 'captcha_classifier.pkl'  # 验证码识别模型
cookies_save_path = 'ByrbtCookies.pickle'  # cookies保存路径