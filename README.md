# brybt_bot

**他不强调这个机器人会删除文件，一上来连警告都没有就把我1个T的文件给删了！！！而且原来仓库代码质量也不高，README 英文和汉字之间也没空格，issue 也没人理，我决定放弃原来的仓库，慢慢重写全部代码。**

- [ ] 更新 requirements.txt
- [x] 更新 README
- [ ] 重写 spaghetti codes

本机器人可以利用校园里的服务器进行全自动做种（本人亲测已上传96TB），采用 transmission 作为下载器，可以从 Web 端查看种子下载情况

![image-20200330163255569](https://github.com/lipssmycode/byrbt_bot/blob/master/images/image-20200330163255569.png)

（疫情期间，免费种子较少）

![image-20200330163105285](https://github.com/lipssmycode/byrbt_bot/blob/master/images/image-20200330163105285.png)

- [x] 支持识别验证码登录（感谢**[decaptcha](https://github.com/bumzy/decaptcha)**项目）
- [x] 支持下载种子(感谢**[byrbt_bot](https://github.com/Jason2031/byrbt_bot)**项目)
- [x] 支持自动寻找合适的免费种子（默认条件：种子文件大于1G小于1TB大小，下载人数比做种人数大于0.6）
- [x] 支持识别Free，提高下载种子的条件，择优选取，避免频繁更换下载种子
- [x] 支持自动删除旧种子，下载新种子
- [x] 支持使用Transmission Web管理种子

### Usage

1. #### 用户权限问题

   由于需要使用 Transmission，在 root 用户下配置会比较方便，一般用户可以采用docker实现，将下载数据的文件夹挂载到docker上即可。

2. #### 安装Python3

   安装相应依赖包

   ```shell
   python3 -m pip install -r requirements.txt
   ```
   sklearn版本为0.22.1可以使用captcha_classifier_sklearn0.22.1.pkl模型，改名为captcha_classifier.pkl即可

3. #### 安装Transmission

   [Transmission 搭建笔记](https://github.com/WhymustIhaveaname/Transmission-Block-Xunlei/blob/main/%E6%90%AD%E5%BB%BA%E7%AC%94%E8%AE%B0.md)

4. #### 在byrbt.py配置信息

   主要配置如下信息。**注意 download_path 千万不要填自己正在用的文件夹，里面的文件会被任意更改甚至删除！**

   ```python
   _username = '用户名'
   _passwd = '密码'
   _transmission_user_pw = 'user:passwd'  # transmission的用户名和密码，按照格式填入
   _windows_download_path = './torrent'  # windows测试下载种子路径
   _linux_download_path = '<path_to_download_dir>'  # linux服务器下载种子的路径
   _torrent_infos = './torrent.pkl'  # 种子信息保存文件路径
   max_torrent = 20  # 最大种子数
   search_time = 120  # 轮询种子时间，默认120秒
   ```

5. #### 启动

   ```shell
   python3 byrbt.py
   ```

### Acknowledgements

* [Jason2031/byrbt_bot](https://github.com/Jason2031/byrbt_bot)
* [bumzy/decaptcha](https://github.com/bumzy/decaptcha)
