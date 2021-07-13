# brybt_bot

**上一个作者 [lipssmycode](https://github.com/lipssmycode) 不强调这个机器人会删除文件，一上来连警告都没有就把我1个T的文件给删了！！！
而且原来仓库代码质量低、README 英文和汉字之间没空格、issue 没人理，我决定放弃原来的仓库，慢慢重写全部代码。**

- [x] 更新 requirements.txt
- [x] 更新 README
- [x] 移动配置至 config.py，与主要逻辑分离
- [x] 重写 spaghetti codes
- [x] 解决代码复用低的问题
- [x] 删除文件的问题：只会删除 linux_download_path 下并且所有 tracker 都是北邮人的文件
- [x] 改为限制总大小而不是文件数
- [x] 把交互改好看一些
- [x] 降低请求失败重试次数至3或者2，失败两三次就得了，默认是 5 太烦人了
- [x] 原作者似乎不会用一行 list 的语法，导致程序变长和可读性降低
- [x] 清除无用命令，那些可以用网页控制台的命令有必要再写一遍吗？而且好多代码竟然不是复用的！
- [x] 重命名部分函数，原来所有函数都是 get 开头，改成更具有意义的 select、parse 等
- [x] 增加日志机制
- [ ] 重写下载种子的逻辑
- [ ] 重写空间满时删除种子的逻辑
- [x] 获取更多页的种子而不仅仅是第一页
- [x] 删除没用的神经网络文件
- [ ] 进行广泛的测试

**更新：我发现上一个作者 lipssmycode 基本上就是个贼。
主体代码都来自 [Jason2031/byrbt_bot](https://github.com/Jason2031/byrbt_bot)，
她隐藏 fork 痕迹，对原仓库的贡献只字不提，甚至最后的鸣谢都没有带原作者 Jason2031 的名字。
还把协议 从 GPL 换成了 MIT，这都是非常不道德的。**

- [x] 支持识别验证码登录（感谢 [bumzy/decaptcha](https://github.com/bumzy/decaptcha) 项目）
- [x] 支持下载种子(感谢 [Jason2031/byrbt_bot](https://github.com/Jason2031/byrbt_bot) 项目)
- [x] 支持自动寻找合适的免费种子（默认条件：种子文件大于1G小于1TB大小，下载人数比做种人数大于0.6）
- [x] 支持识别 Free，提高下载种子的条件，择优选取，避免频繁更换下载种子
- [x] 支持自动删除旧种子，下载新种子
- [x] 支持使用 Transmission Web 管理种子

### Usage

* 安装相应依赖包

   ```shell
   python3 -m pip install -r requirements.txt
   ```
   sklearn版本为0.22.1可以使用captcha_classifier_sklearn0.22.1.pkl模型，改名为captcha_classifier.pkl即可

* 安装 Transmission

   [Transmission 搭建笔记](https://github.com/WhymustIhaveaname/Transmission-Block-Xunlei/blob/main/%E6%90%AD%E5%BB%BA%E7%AC%94%E8%AE%B0.md)

* 在 byrbt.py 配置信息

   复制 config-example.py 至 config.py，并更改以下信息。**注意 download_path 千万不要填自己正在用的文件夹，里面的文件会被任意更改甚至删除！**

   ```python
    username = '用户名'
    passwd = '密码'
    transmission_user_pw = 'user:passwd'  # transmission的用户名和密码，按照格式填入
    #windows_download_path = ''  # 暂不支持
    linux_download_path = '<path_to_download_dir>'  # linux服务器下载种子的路径
    max_torrent_size = 1024  # 最大文件大小，MB
    search_time = 120  # 轮询种子时间
   ```

* 启动！

   ```shell
   python3 byrbt.py
   ```

   之后会打印 help 然后弹出命令提示符“$”，输入相应命令即可，一般“main”是大家需要的。

### Acknowledgements

* [lipssmycode/byrbt_bot](https://github.com/lipssmycode/byrbt_bot)
~~虽然她代码质量很低并且删了我1个T文件，但是爬虫的部分的确节约了我的时间。~~
基本上就是个贼。
主体代码都来自 [Jason2031/byrbt_bot](https://github.com/Jason2031/byrbt_bot)，
她隐藏 fork 痕迹，对原仓库的贡献只字不提，甚至最后的鸣谢都没有带原作者 Jason2031 的名字。
* [Jason2031/byrbt_bot](https://github.com/Jason2031/byrbt_bot)
* [bumzy/decaptcha](https://github.com/bumzy/decaptcha)
