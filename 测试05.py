import network
from umqttrobust import MQTTClient	#导入同目录下的umqttrobust.py文件
import machine
import time

clientID = "ESP32"	#连接ID
server = "192.168.3.31"	#MQTT服务器地址
port = 1883	#MQTT服务器端口号
userName= "admin"
passWord= "admin"
keepAlive = 60	#心跳周期
wifiSSID = "DreamBoxDev"	#WIFI SSID
wifiPassWord = "dreambox12345"	#WIFI密码
subTopic = "ms/report"	#订阅的主题
pubTopic = "ms/report"	#发布的主题

feed_pin = machine.Pin(26, machine.Pin.OUT)
light_pin = machine.Pin(25, machine.Pin.OUT)
fan_pin = machine.Pin(33, machine.Pin.OUT)

#连接WLAN
def wifiConnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("开始连接...")
        wlan.connect(wifiSSID, wifiPassWord)
        i = 1
        while not wlan.isconnected():
            print("正在连接中...".format(i))
            i += 1
            time.sleep(1)
    print("网络信息为：", wlan.ifconfig())
 
# 解析MQTT消息
def parse_message(msg):
    # 确保消息长度正确
    if len(msg) != 9:
        print('Invalid message length')
        return None
    
    # 提取起始位和截止位
    start_byte = msg[0:2]
    end_byte = msg[7:9]
    mode_byte = msg[2]
    print(start_byte)
    print(end_byte)
    # 检查起始位和截止位
    if start_byte != b'FF' or end_byte != b'EE':
        print('Invalid start or end byte')
        return None
    
    # 提取运行时间（假设为4位十六进制数，转换为十进制秒）
    time_hex = msg[3:7]
    print(time_hex)
    try:
        time_seconds = int(time_hex)
    except ValueError:
        print('Invalid time format')
        return None
    
    return time_seconds 
 
#订阅主题回调函数 收到消息时在此处理
def subCallBack(subTopic, msg):
    
    print('Received message:', pubTopic, msg)
    time_seconds = parse_message(msg)
    if time_seconds is not None:
        light_pin.value(1)
        time.sleep(2)
        fan_pin.value(1)
        time.sleep(10)
        control_led(time_seconds)
        fan_pin.value(0)
        time.sleep(100)
        light_pin.value(0)
        time.sleep(1)
    
 
def control_led(duration):
    
    feed_pin.value(1)  # 打开feed
    time.sleep(duration)
    feed_pin.value(0)  # 关闭feed
    time.sleep(10)
    
 
wifiConnect()
mqtt = MQTTClient(clientID,server,port,userName,passWord,keepAlive)
mqtt.set_callback(subCallBack)
mqtt.connect()
mqtt.subscribe(subTopic)
print("订阅成功")

 
while True:
    mqtt.check_msg()
    time.sleep(1)