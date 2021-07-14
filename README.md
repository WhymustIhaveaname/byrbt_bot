# brybt_bot

**上一个作者 [lipssmycode](https://github.com/lipssmycode) 不强调这个机器人会删除文件，一上来连警告都没有就把我1个T的文件给删了！！！
而且原来仓库代码质量低、README 英文和汉字之间没空格、issue 没人理，我决定放弃原来的仓库，慢慢重写全部代码。**

- [x] 更新 requirements.txt、README
- [x] 移动配置至 config.py，与主要逻辑分离
- [x] 重写 spaghetti codes、解决代码复用低的问题、lipssmycode 不会用一行 list 的语法导致程序变长和可读性降低
- [x] 删除文件的问题：只会删除 linux_download_path 下并且所有 tracker 都是北邮人的文件
- [x] 改为限制总大小而不是文件数
- [x] 降低请求失败重试次数至3或者2，失败两三次就得了，默认是 5 太烦人了
- [x] 清除无用命令，那些可以用网页控制台的命令有必要再写一遍吗？而且好多代码竟然不是复用的！
- [x] 重命名部分函数，原来所有函数都是 get 开头，改成更具有意义的 select、parse 等
- [x] 增加日志机制
- [x] 重写下载种子的逻辑：按种子平均每天增加作种率期望排序，不同的 free 加不同的 buff，下最受欢迎的
- [x] 重写空间满时删除种子的逻辑：按我做种以来平均每天的上传比排序，使用 MCTS 中的 UCB 算法删没人要的
- [x] 获取更多页的种子而不仅仅是第一页
- [x] 删除没用的神经网络文件
- [x] 解决种子下载名字不对的问题：byr 的 headers 是用 iso8859-1 编码的，requests 会试图用 utf-8 解码，导致很多乱码。
可怜的 lipssmycode 并不能解决这个问题，只能把乱码都忽略，最后就出现了一堆点组成的文件名——因为只有点不会被忽略。
- [ ] 进行广泛的测试

**更新：我发现上一个作者 lipssmycode 基本上就是个贼。
主体代码都来自 [Jason2031/byrbt_bot](https://github.com/Jason2031/byrbt_bot)，
她隐藏 fork 痕迹，淡化原仓库的贡献，甚至最后的鸣谢都没有带原作者 Jason2031 的名字。
还把协议 从 GPL 换成了 MIT，这都是非常不道德的。
最让我生气的还是她的代码质量太低了，读她的代码就像手榴弹在大脑中爆炸一样上头。**

代码移至 [WhymustIhaveaname/ByrBtAutoDownloader](https://github.com/WhymustIhaveaname/ByrBtAutoDownloader)。
