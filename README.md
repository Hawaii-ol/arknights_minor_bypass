# Arknights minor bypass
使用[mitmproxy](https://github.com/mitmproxy/mitmproxy)实现，告别一周三小时探监生活
## 支持的服务器
官服，~~B服~~

**注意：由于最近B站回调接口的升级，目前的B服破解登录方式已不再有效。已登录的账号9点以后理论上仍可继续游戏，不受影响。官服破解不受影响。**
## 支持的系统
安卓，ios
## 使用方法
1. 下载安装python3
2. 运行安装必需组件.bat或手动执行pip3 install -r requirements.txt
3. 选择和你的服务器对应的bat启动
4. 在手机/模拟器上安装mitmproxy的系统证书（安卓7.0以上需要root），方法可以看下面的FAQ
5. 配置手机/模拟器代理为电脑IP的8888端口
6. have fun!
## FAQ
### 如何安装证书
首先需要生成证书。
#### Windows
打开命令提示符(cmd)，输入mitmproxy并执行。在Windows 7上这个命令可能会报错，不用管，执行后在C:\\Users\\你的用户名\\.mitmproxy目录下会生成若干证书文件。
#### Mac OS
打开终端，输入mitmproxy并执行。执行后在~/.mitmproxy目录下会生成若干证书文件。~代表你的用户目录，点击菜单栏的前往->个人即可打开。
#### Linux
拉倒吧，有人会用Linux运行这个？会用Linux的人需要看这个？

接下来需要把证书安装到设备上。
#### Android
1. 确保你的设备已经root，模拟器通常可以在设置中开启root
2. 将前一步生成的mitmproxy-ca-cert.cer文件拷贝到设备中
3. 点击这个证书文件即可安装，或从设置->安全->从SD卡安装选项选择证书文件并安装
4. 已安装的证书是用户证书，安卓7.0以上无法使用，我们需要将它重新安装为系统证书。使用具有root权限的文件管理器（如MT管理器）将/data/misc/user/0/cacerts-added目录下的以.0结尾的文件拷贝到/system/etc/security/cacerts目录。
5. 重启设备，检查设置->安全->信任的凭据->系统列表中是否有mitmproxy
#### iOS
1. 先在Wi-Fi设置中开启代理，服务器填电脑IP，端口填8888
2. 确保电脑上的脚本已在运行
3. 用Safari访问mitm.it这个网址
4. 在网页中找到iOS一项，点击绿色的`Get mitmproxy-ca-cert.pem`按钮，按提示完成下载安装
5. 进入设置->通用->关于本机->证书信任设置，启用mitmproxy的信任
### 为什么有时脚本看起来会卡住，网络无法正常连接
如果你是Windows系统，请注意脚本窗口的标题前是否有选择二字，如果有，说明你选中了窗口内的某些文本，导致脚本暂停运行。此时在窗口内单击鼠标右键即可恢复。
## 注意事项
### 关于B服登录
B服有两种登录方式，APP授权登录和账号密码登录。
#### APP授权登录
需要在模拟器上同时安装B站APP和游戏APP，首先登录B站，然后启动游戏，会出现一键授权提示，按提示授权即可登录。
#### 账号密码登录
直接从游戏SDK端账号密码登录无法绕过防沉迷。登录失败后，会自动弹出登陆脚本，请在登陆脚本中输入账号密码，如有手机验证码请一并输入。脚本登录成功后，重新回到游戏并输入任意账号密码即可登录。
### 关于风险
一、本程序仅供学习交流使用，请勿将本程序用于任何非法用途，由此造成的封号等一系列不利后果与本人无关

二、不建议在安卓真机上使用，原因有三：
1. 程序会无差别监听真机上的所有流量，某些使用了SSL pinning技术的APP可能出现证书无效、网页无法打开等问题
2. 安卓的安全政策已在逐渐收紧，从10.0开始system分区只能被挂载为只读，即使root也无法写入，需要另外解锁
3. root真机会产生一系列潜在的安全风险

作为代替，可以在安卓真机上安装vmos虚拟机，然后在虚拟机中安装B站APP和游戏。vmos虚拟机中默认的安卓版本为5.0，这意味着只需要将mitmproxy证书安装为用户证书即可实现抓包，甚至不需要开启root权限。
## 支持
本程序还在开发维护中，有遇到任何问题欢迎提issue，也欢迎pull request
