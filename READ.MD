###1.运行环境
+ python 3+ [下载地址](https://www.python.org/downloads/)
+ 需要安装itchat
```pip install itchat```
###2.功能设计
* 查看群id
* 查看指定id群的好友
* 向指定群中所有自己的好友发送信息
###3.使用方法
+ 把代码复制粘贴,保存为 `wxhelper.py`
+ 在当前文件目录打开cmd指令窗口输入(windows系统)
```python wxhelper.py```
+ 扫码登陆
+ 手机端向文件助手发送以下指令
```
群好友助手指令：
1.[SendMode]:查看群id
2.[SendMode id]:查看指定id群的好友人数
3.[SendMode 参数0(群id) text 参数a(标题) 参数b(内容)]
4.[update]?or?4:更新数据
5.[help]:帮助信息\n【注意:参数间只能有一个空格】
```