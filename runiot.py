#!/usr/bin/python3

# 运行环境为Windows7&Python3.7

import aliLink,mqttd     # pip install paho-mqtt -i https://mirrors.aliyun.com/pypi/simple/ 复制链接在终端shell或者terminal中安装mqttd
import time,json
import serial
import time
import RPi.GPIO as GPIO
time.sleep(20)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT) #green light
GPIO.output(17,GPIO.HIGH)
GPIO.setup(27,GPIO.OUT)	#yellow light
GPIO.output(27,GPIO.HIGH)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,GPIO.HIGH)
GPIO.setup(24,GPIO.OUT)
GPIO.output(24,GPIO.HIGH)
GPIO.setup(25,GPIO.OUT)
GPIO.output(25,GPIO.HIGH)
GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.HIGH)
GPIO.setup(19,GPIO.OUT)
GPIO.output(19,GPIO.HIGH)
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,GPIO.HIGH)
  # 选择串口，并设置波特率


# 三元素（iot后台获取）
ProductKey = 'a13WzATBVrq'
DeviceName = 'zheajing_anyang'
DeviceSecret = "bbcf9645edf5cce04444c5dc5e32e977"
# topic (iot后台获取)
POST = '/sys/a13WzATBVrq/zheajing_anyang/thing/event/property/post'  # 上报消息到云
POST_REPLY = '/sys/a13WzATBVrq/zheajing_anyang/thing/event/property/post_reply'
SET = '/sys/a13WzATBVrq/zheajing_anyang/thing/service/property/set'  # 订阅云端指令



# 消息回调（云端下发消息的回调函数）
def on_message(client, userdata, msg):
    
    Msg = json.loads(msg.payload.decode('utf-8'))
    #callback powerled
    if ('jidianqi1' in Msg["params"].keys()):
        print("jidianqi1 right")
        switch1 = Msg['params']['jidianqi1']
        print(switch1)
        if(switch1==1):
            GPIO.output(17,GPIO.LOW)
        else:
            GPIO.output(17,GPIO.HIGH)
    else:
        print("jidianqi1 not find")

     #callback jidianqiyi
    if ('jidianqi2' in Msg["params"].keys()):
        print("jidianqi2 right")
        switch2 = Msg['params']['jidianqi2']
        print(switch2)
        if (switch2 == 1):
            GPIO.output(27,GPIO.LOW)
        else:
            GPIO.output(27,GPIO.HIGH)
    else:
        print("switch2 not find")

    #callback jidianqier
    if ('jidianqi3' in Msg["params"].keys()):
        print("jidianqi3 right")
        switch3 = Msg['params']['jidianqi3']
        print(switch3)
        if (switch3 == 1):
            GPIO.output(23,GPIO.LOW)
        else:
            GPIO.output(23,GPIO.HIGH)
    else:
        print("jidianqi3 not find")

   #callback jidianqisi
    if ('jidianqi4'in Msg["params"].keys()):
        print("jidianqi4 right")
        switch4 = Msg['params']['jidianqi4']
        print(switch4)
        if (switch4 == 1):
            GPIO.output(24,GPIO.LOW)
        else:
            GPIO.output(24,GPIO.HIGH)
    else:
        print("jidianqi4 not find")

    if ('jidianqi5' in Msg["params"].keys()):
        switch5 = Msg['params']['jidianqi5']
        if (switch5 == 1):
            GPIO.output(25,GPIO.LOW)
        else:
            GPIO.output(25,GPIO.HIGH)
    else:
        print("jidianqi5 not find")

    if ('jidianqi6' in Msg['params'].keys()):
        switch6 = Msg['params']['jidianqi6']
        if (switch6 ==1):
            GPIO.output(26,GPIO.LOW)
        else:
            GPIO.output(26,GPIO.HIGH)
    else:
        print("jidianqi6 not find")

    if ('jidianqi7' in Msg['params'].keys()):
        switch7 = Msg['params']['jidianqi7']
        if (switch7 ==1):
            GPIO.output(19,GPIO.LOW)
        else:
            GPIO.output(19,GPIO.HIGH)
    else:
        print("jidianqi7 not find")

    if ('jidianqi8' in Msg['params'].keys()):
        switch8 = Msg['params']['jidianqi8']
        if (switch8 ==1):
            GPIO.output(13,GPIO.LOW)
        else:
            GPIO.output(13,GPIO.HIGH)
    else:
        print("jidianqi8 not find")
    #switch = Msg['params']['PowerLed']
    # jidianqier = Msg['params']['jidianqier']
    #print(switch)
    # print( jidianqier)
    print(msg.payload)  # 开关值

#连接回调（与阿里云建立链接后的回调函数）
def on_connect(client, userdata, flags, rc):
    pass

#field_temp = float(20.1)
field_pres = float(1.0)
#field_air_moisture = float(68.3)

# 链接信息
Server,ClientId,userNmae,Password = aliLink.linkiot(DeviceName,ProductKey,DeviceSecret)

# mqtt链接
mqtt = mqttd.MQTT(Server,ClientId,userNmae,Password)
mqtt.subscribe(SET) # 订阅服务器下发消息topic
mqtt.begin(on_message,on_connect)
ser = serial.Serial("/dev/device4", 9600) 
def sensor():
    if ser.is_open:
        print("port open success")
        send_data = bytes.fromhex('01 03 00 00 00 02 C4 0B')  # 发送数据转换为b'\xff\x01\x00U\x00\x00V'
        ser.write(send_data)  # 发送命令
        time.sleep(0.2)  # 延时，否则len_return_data将返回0，此处易忽视！！！
        len_return_data = ser.inWaiting()  # 获取缓冲数据（接收数据）长度

        if len_return_data:
            return_data = ser.read(len_return_data)  # 读取缓冲数据
            print(return_data)
            # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
            str_return_data = str(return_data.hex())
            feedback_data = str_return_data
            feedback_data_temp = str_return_data[6:10]
            feedback_data_wet = str_return_data[10:14]

            feedback_data = int(str_return_data[-6:-2], 16)
            print(feedback_data)
            #print(feedback_data_temp)
            #print(feedback_data_wet)
            # hex -> shijinzhi
            field_temp = (int(feedback_data_temp, 16)) / 100
            field_air_moisture = (int(feedback_data_wet, 16)) / 100
            return field_temp,field_air_moisture
            #print("field_temp",field_temp)
            #print("field_air_mois",field_air_moisture)
        else:
            field_temp = float(20.1)
            field_air_moisture = float(80)
            return field_temp,field_air_moisture
    
        
        # hex(16进制)转换为bytes(2进制)，应注意Python3.7与Python2.7此处转换的不同
    else:
        print("port open failed")
    
    
# 信息获取上报，每10秒钟上报一次系统参数
while True:
    time.sleep(10)
    ssor =sensor()
    print(ssor)
    field_temp=ssor[0]
    field_air_moisture=ssor[1]
    

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
        'field_temp':field_temp,
        'field_pres':field_pres,
        'filed_air_moisture':field_air_moisture

    }
    JsonUpdataMsn = aliLink.Alink(updateMsn)
    print(JsonUpdataMsn)

    mqtt.push(POST,JsonUpdataMsn) # 定时向阿里云IOT推送我们构建好的Alink协议数据


