#!/usr/bin/python3

import aliLink,mqttd     # pip install paho-mqtt -i https://mirrors.aliyun.com/pypi/simple/ 复制链接在终端shell或者terminal中安装mqttd
import time,json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT) #green light
GPIO.output(17,GPIO.LOW)
GPIO.setup(27,GPIO.OUT)	#yellow light
GPIO.output(27,GPIO.LOW)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,GPIO.LOW)
GPIO.setup(24,GPIO.OUT)
GPIO.output(24,GPIO.LOW)
GPIO.setup(25,GPIO.OUT)
GPIO.output(25,GPIO.LOW)
# 三元素（iot后台获取）
ProductKey = 'a13WzATBVrq'
DeviceName = 'zheajing_anyang'
DeviceSecret = "bbcf9645edf5cce04444c5dc5e32e977"
# topic (iot后台获取)
POST = '/sys/a13WzATBVrq/zheajing_anyang/thing/event/property/post'  # 上报消息到云
POST_REPLY = '/sys/a13WzATBVrq/Swenden_bohan/thing/event/property/post_reply'
SET = '/sys/a13WzATBVrq/zheajing_anyang/thing/service/property/set'  # 订阅云端指令



# 消息回调（云端下发消息的回调函数）
def on_message(client, userdata, msg):
    print(msg.payload)
    Msg = json.loads(msg.payload.decode('utf-8'))
    #callback powerled
    if ('PowerLed' in Msg["params"].keys()):
        print("PowerLed right")
        switch = Msg['params']['PowerLed']
        print(switch)
        if(switch==1):
            GPIO.output(17,GPIO.HIGH)
        else:
            GPIO.output(17,GPIO.LOW)
    else:
        print("PowerLed not find")

     #callback jidianqiyi
    if ('jidianqiyi' in Msg["params"].keys()):
        print("jidianqiyi right")
        jidianqiyi = Msg['params']['jidianqiyi']
        print(jidianqiyi)
        if (jidianqiyi == 1):
            GPIO.output(27,GPIO.HIGH)
        else:
            GPIO.output(27,GPIO.LOW)
    else:
        print("jidianqiyi not find")

    #callback jidianqier
    if ('jidianqier' in Msg["params"].keys()):
        print("jidianqier right")
        jidianqier = Msg['params']['jidianqier']
        print(jidianqier)
    else:
        print("jidianqier not find")

    #switch = Msg['params']['PowerLed']
    # jidianqier = Msg['params']['jidianqier']
    #print(switch)
    # print( jidianqier)
    print(msg.payload)  # 开关值

#连接回调（与阿里云建立链接后的回调函数）
def on_connect(client, userdata, flags, rc):
    pass

ruian_field_temp = float(30.1)


# 链接信息
Server,ClientId,userNmae,Password = aliLink.linkiot(DeviceName,ProductKey,DeviceSecret)

# mqtt链接
mqtt = mqttd.MQTT(Server,ClientId,userNmae,Password)
mqtt.subscribe(SET) # 订阅服务器下发消息topic
mqtt.begin(on_message,on_connect)


# 信息获取上报，每10秒钟上报一次系统参数
while True:
    time.sleep(10)

#获取指示灯状态
	#power_stats=int(rpi.getLed())
	#if(power_stats==0):
	#	power_LED = 0
	#else:
	#	power_LED = 1

    # CPU 信息
   # CPU_temp = float(rpi.getCPUtemperature())  # 温度   ℃
   # CPU_usage = float(rpi.getCPUuse())         # 占用率 %
 
    # RAM 信息
    #RAM_stats =rpi.getRAMinfo()
    #RAM_total =round(int(RAM_stats[0]) /1000,1)    #
   # RAM_used =round(int(RAM_stats[1]) /1000,1)
    #RAM_free =round(int(RAM_stats[2]) /1000,1)
 
    # Disk 信息
   # DISK_stats =rpi.getDiskSpace()
   # DISK_total = float(DISK_stats[0][:-1])
   # DISK_used = float(DISK_stats[1][:-1])
   # DISK_perc = float(DISK_stats[3][:-1])

    # 构建与云端模型一致的消息结构
    updateMsn = {
        #'cpu_temperature':CPU_temp,
      #  'cpu_usage':CPU_usage,
       # 'RAM_total':RAM_total,
       # 'RAM_used':RAM_used,
       # 'RAM_free':RAM_free,
       # 'DISK_total':DISK_total,
       # 'DISK_used_space':DISK_used,
       # 'DISK_used_percentage':DISK_perc,
       # 'PowerLed':power_LED
        'SWfield_temp':ruian_field_temp


    }
    JsonUpdataMsn = aliLink.Alink(updateMsn)
    print(JsonUpdataMsn)

    mqtt.push(POST,JsonUpdataMsn) # 定时向阿里云IOT推送我们构建好的Alink协议数据
