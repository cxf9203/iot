#__author:StevenChen
#__Date:2021/7/30

#!/usr/bin/python3

# pip install paho-mqtt
import paho.mqtt.client
import time,json,random
import hmac,hashlib
import wget
import os
import zipfile


#setting
ver=[]
#version = "1.0"
id = 9900001

# =====初始化======
class MQTT():
    def __init__(self,host,CcientID,username=None,password=None,port=1883,timeOut=60):
        self.Host = host
        self.Port = port
        self.timeOut = timeOut
        self.username =username
        self.password = password
        self.CcientID = CcientID

        self.mqttc = paho.mqtt.client.Client(self.CcientID)    #配置ID
        if self.username is not None:    #判断用户名密码是否为空
            self.mqttc.username_pw_set(self.username, self.password)    #不为空则配置账号密码

        self.mqttc.connect(self.Host, self.Port, self.timeOut) #初始化服务器  IP  端口  超时时间


    # 初始化
    def begin(self,message,connect):
        self.mqttc.on_connect = connect
        self.mqttc.on_message = message
        self.mqttc.loop_start()  # 后台新进程循环监听

# =====发送消息==========
    def push(self,tag,date,_Qos = 0):
        self.mqttc.publish(tag,date,_Qos)
        #print('OK',date)

# =======订阅tips=====
    def subscribe(self,_tag):
        self.mqttc.subscribe(_tag)   #监听标签

def linkiot(DeviceName,ProductKey,DeviceSecret,server = 'iot-as-mqtt.cn-shanghai.aliyuncs.com'):
    serverUrl = server
    ClientIdSuffix = "|securemode=3,signmethod=hmacsha256,timestamp="

    # 拼合
    Times = str(int(time.time()))  # 获取登录时间戳
    Server = ProductKey+'.'+serverUrl    # 服务器地址
    ClientId = DeviceName + ClientIdSuffix + Times +'|'  # ClientId
    userNmae = DeviceName + "&" + ProductKey
    PasswdClear = "clientId" + DeviceName + "deviceName" + DeviceName +"productKey"+ProductKey + "timestamp" + Times  # 明文密码

    # 加密
    h = hmac.new(bytes(DeviceSecret,encoding= 'UTF-8'),digestmod=hashlib.sha256)  # 使用密钥
    h.update(bytes(PasswdClear,encoding = 'UTF-8'))
    Passwd = h.hexdigest()
    return Server,ClientId,userNmae,Passwd

# 阿里Alink协议实现（字典传入，json str返回）
#def Alink(params):
  #  AlinkJson = {}
  ##  AlinkJson["id"] = id
  #  AlinkJson["version"] = version
  #  AlinkJson["params"] = params
 #   AlinkJson["method"] = "thing.event.property.post"
  #  return json.dumps(AlinkJson)


#发送一次当前版本号
def otaversion(paraversion):
    OTAversion = {
     "id": id,
     "params": {
     "version": paraversion,
     "module": "linuxEmbed" #写不写没关系
  }
}
    otaJsonUpdataMsn = json.dumps(OTAversion) #param OTA
    print(otaJsonUpdataMsn)
    mqtt.push(OTAVSEND,otaJsonUpdataMsn) #mqtt发送topic与json格式的消息

# 消息回调（云端下发消息的回调函数）
def on_message(client, userdata, msg):
    print(msg.payload)
    Msg = json.loads(msg.payload.decode('utf-8'))
    #check ota version check url to download newversion
    if ('url' in Msg["data"].keys()):
        newversion = str(Msg['data']['version'])
        version = newversion
        print('newversion = ', newversion)
        print("low version, request update")
        url = str(Msg['data']['url'])
        print('url address = ', url)
        if url is not None:
            print("prepare download")
            wget.download(url, out='newfile.zip')
            zfile = zipfile.ZipFile('newfile.zip', 'r')
            ###解压缩下载的文件
            for filename in zfile.namelist():
                data = zfile.read(filename)
                #print(data)

                file = open(filename, 'w+b')
                #print(file)
                file.write(data)

                file.close()
            #中断旧python脚本，需在这里完成工作，实现旧文件删除，执行下载的新文件。
            #Todo
            #print(os.popen('tasklist'))
            #syscmd = ('')
            #closeresult = os.system(syscmd)
            #print("systemcloseresult",closeresult)


            # 执行下载的.py文件#####
            pythonfile = ('python wanzheng.py')  #
            exrresult = os.system(pythonfile)
            print(exrresult)
            # 下载完成后推送进度
            mqtt.push(OTAPROCESS, JsonProgressMsn)

            # 退出当前的程序
            #exit()

        else:
            print("failure")
    else:
        print("already new version") #一般不会执行到这里
    return version






    #print(msg.payload)  # 开关值


# 连接回调（与阿里云建立链接后的回调函数）
def on_connect(client, userdata, flags, rc):
    pass




# 三元素（iot后台获取）
ProductKey = 'a1cQSE3paBi'
DeviceName = 'PC-office'
DeviceSecret = "927f46d3546f92cb3b5b6c4615b8ab57"
# topic (iot后台获取)
POST = '/sys/a1cQSE3paBi/PC-office/thing/event/property/post'  # 上报消息到云
POST_REPLY = '/sys/a1cQSE3paBi/PC-office/thing/event/property/post_reply'
SET = '/sys/a1cQSE3paBi/PC-office/thing/service/property/set'  # 订阅云端指令
####OTA TOPIC update####
OTAVSEND = '/ota/device/inform/a1cQSE3paBi/PC-office' #topic IOT后台获取
OTARECEIVE = '/ota/device/upgrade/a1cQSE3paBi/PC-office'
OTAPROCESS = '/ota/device/progress/a1cQSE3paBi/PC-office'



# 链接信息
Server, ClientId, userNmae, Password = linkiot(DeviceName, ProductKey, DeviceSecret)

# mqtt链接
mqtt = MQTT(Server, ClientId, userNmae, Password)
mqtt.subscribe(SET)  # 订阅服务器下发消息topic
mqtt.subscribe(OTARECEIVE)
mqtt.begin(on_message, on_connect)


#升级进度100%，用于之后OTA升级服务
JsonProgressMsn = {
  "id": id,
  "params": {
    "step": 100,
      "desc":"升级进度100%",
    "module": "linuxEmbed" #写不写没关系
  }
}
JsonProgressMsn = json.dumps(JsonProgressMsn) #param OTA



#ruian_field_temp = float(30.1)
# 信息获取上报，每10秒钟上报一次系统参数
pythonfile = ('python wanzheng.py')  #
exrresult = os.system(pythonfile)
print(exrresult)
while True:
    time.sleep(10)


    # 获取指示灯状态
    # power_stats=int(rpi.getLed())
    # if(power_stats==0):
    #	power_LED = 0
    # else:
    #	power_LED = 1

    # CPU 信息
    # CPU_temp = float(rpi.getCPUtemperature())  # 温度   ℃
    # CPU_usage = float(rpi.getCPUuse())         # 占用率 %

    # RAM 信息
    # RAM_stats =rpi.getRAMinfo()
    # RAM_total =round(int(RAM_stats[0]) /1000,1)    #
    # RAM_used =round(int(RAM_stats[1]) /1000,1)
    # RAM_free =round(int(RAM_stats[2]) /1000,1)

    # Disk 信息
    # DISK_stats =rpi.getDiskSpace()
    # DISK_total = float(DISK_stats[0][:-1])
    # DISK_used = float(DISK_stats[1][:-1])
    # DISK_perc = float(DISK_stats[3][:-1])

    # 构建与云端模型一致的消息结构
    """
    updateMsn = {
        # 'cpu_temperature':CPU_temp,
        #  'cpu_usage':CPU_usage,
        # 'RAM_total':RAM_total,
        # 'RAM_used':RAM_used,
        # 'RAM_free':RAM_free,
        # 'DISK_total':DISK_total,
        # 'DISK_used_space':DISK_used,
        # 'DISK_used_percentage':DISK_perc,
        # 'PowerLed':power_LED
       # 'guanghe': ruian_field_temp

    }
    JsonUpdataMsn = Alink(updateMsn)
    print(JsonUpdataMsn)

    mqtt.push(POST, JsonUpdataMsn)  # 定时向阿里云IOT推送我们构建好的Alink协议数据
    """