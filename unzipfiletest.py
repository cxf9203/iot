#__author:StevenChen
#__Date:2021/7/30
import zipfile
#解压缩实例

import os
import zipfile


zfile = zipfile.ZipFile('ceshibanben.zip', 'r')
            ###解压缩下载的文件
for filename in zfile.namelist():
    data = zfile.read(filename)
    print("data = ",data)

    file = open(filename, 'w+b')
    print("file = ",file)
    finame = file.name
    print(finame)
    file.write(data)

    file.close()

str=('python ceshibanben.py')
p=os.system(str)
print(p)
