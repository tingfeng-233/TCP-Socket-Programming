TCP Socket Programming Experiment

一、运行环境
操作系统：
Windows 11

Python版本：
Python 3.14

开发工具：
Visual Studio Code

网络协议：
TCP

二、项目文件
reversetcpclient.py
客户端程序

reversetcpserver.py
服务器程序

sample.txt
测试文件

run_log.txt
运行日志文件

output.txt
客户端输出文件

三、报文类型
1. Initialization（Type=1）
Client向Server发送初始化报文。
字段：
Type（2 Bytes）
N（4 Bytes）
其中N表示本次需要进行reverse操作的数据块数量。

2. Agree（Type=2）
Server向Client返回确认报文。
字段：
Type（2 Bytes）

3. reverseRequest（Type=3）
Client向Server发送需要反转的数据块。
字段：
Type（2 Bytes）
Length（4 Bytes）
Data（Length Bytes）

4. reverseAnswer（Type=4）
Server向Client返回反转后的数据。
字段：
Type（2 Bytes）
Length（4 Bytes）
reverseData（Length Bytes）