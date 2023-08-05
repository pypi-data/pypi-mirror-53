#-*-coding:utf-8 -*-
import os
import sys
import time
import shutil
text = sys.argv[0]
textTemp = text[::-1]
textTemp = textTemp[textTemp.index('\\'):]
rootFile=text[len(textTemp):]
text = textTemp[::-1]
packagesList=[]
data_files=[text[:-1]]
def Check():
    for root, dirs, files in os.walk(text):
        isT=True
        if os.path.basename(root) == 'dist':
            if not os.path.exists(text+'olddist'):
                os.makedirs(text+'olddist')
            for x in files:
                print(root+'\\'+x)
                shutil.move(root+'\\'+x,text+'olddist')
        if os.path.basename(root) == 'build' or os.path.basename(root) == '__pycache__' or os.path.basename(root)[-9:] == '.egg-info' or os.path.basename(root) == 'dist' or os.path.basename(root) == 'olddist':
            dirs[:] = []
        else:
            if os.path.exists(root):
                if root != text:
                    packagesList.append(root[len(text):])
                    file = open(root+'\\__init__.py',"w+")
                    temp='__all__=['
                    for x in files:
                        if x != '__init__.py':
                            if x[-3:]=='.py':
                                temp=temp+'\''+x[:-3]+'\''+','
                            else:
                                if isT:
                                    isT=False
                                    data_files.append(root)
                    temp=temp[:-1]
                    temp=temp+']'
                    file.write(temp)
                    file.close()
    #print(root) #当前目录路径  
    #print(files) #当前路径下所有非目录子文件
    pass
def CheckDateFile(file: str):
    for root, dirs, files in os.walk(file):
        myFile=[]
        if root == file:
            for x in files:
                if x != 'setup.py' and x != rootFile:
                    if root == text[:-1] and x[-3:] == '.py':
                        myFile.append(x)
                    if x[-3:] != '.py' and x[-7:] != '.pyproj':
                        myFile.append(x)

        if myFile != []:
            temp='(\''+root[len(text):]+'\',['
            if root[len(text):] != '':
                for x in myFile:
                    temp=temp+'\''+root[len(text):]+'\/'+x+'\','
            else:
                for x in myFile:
                    temp=temp+'\''+x+'\','
            temp=temp[:-1]
            temp=temp+'])'
            return temp
    pass
def Create(libraryName: str,version: str, author: str):
    file = open(text+'\\setup.py',"w+")
    temp='from setuptools import setup\n'+'setup(\n'+'    '
    temp=temp+'name='+'\''+libraryName+'\''+',\n'+'    '
    temp=temp+'version='+'\''+version+'\''+',\n'+'    '
    temp=temp+'author='+'\''+author+'\''+',\n'+'    '
    temp=temp+'packages=['
    for x in packagesList:
        temp=temp+'\''+x+'\''+','
    temp=temp[:-1]
    temp=temp+'],\n'+'    '
    if data_files != []:
        temp=temp+'data_files=['
        index=0
        for x in data_files:
            index+=1
            if index != len(data_files):
                temp=temp+CheckDateFile(x)+',\n'+'                '
            else:
                temp=temp+CheckDateFile(x)+'\n'+'                '
            pass
        temp=temp+'],\n'+'    '
    temp=temp+'include_package_data=True,\n'+'    '
    temp=temp+'zip_safe=False,\n'+'    '
    temp=temp+')'
    file.write(temp)
    file.close()
    pass
def Pack():
    os.chdir(text)
    os.system(r"python setup.py sdist bdist_wheel")
    pass
def Update():
    os.system(r"python -m twine upload dist/*")
    pass


Check()#检出补全文件
Create('textTTT','0.0.1','Hugn')#创建规则文件（库的名称，版本，作者）
Pack()#生成/打包安装文件
#Update()#上传库文件