#!/bin/bash

# 定义安装包
install_package=("PyYAML-3.12.tar.gz" "certifi-2018.4.16-py2.py3-none-any.whl" "chardet-3.0.4-py2.py3-none-any.whl" "idna-2.7-py2.py3-none-any.whl" "shellescape-3.4.1-py2.py3-none-any.whl" "urllib3-1.23-py2.py3-none-any.whl" "requests-2.19.1-py2.py3-none-any.whl" "Naked-0.1.31-py2.py3-none-any.whl" "PyMySQL-0.8.1.tar.gz" "crypto-1.4.1.tar.gz" "pycrypto-2.6.1.tar.gz")

checkPython()
{
    #推荐版本V2.6.5
    V1=3
    V2=4
    V3=6

    echo need python version is : $V1.$V2.$V3
    
    #获取本机python版本号。这里2>&1是必须的，python -V这个是标准错误输出的，需要转换
    U_V1=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
    U_V2=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $2}'`
    U_V3=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $3}'`
    
    if hash python3 2>/dev/null; then
        U_V1=`python3 -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
        U_V2=`python3 -V 2>&1|awk '{print $2}'|awk -F '.' '{print $2}'`
        U_V3=`python3 -V 2>&1|awk '{print $2}'|awk -F '.' '{print $3}'`
        v=0
    else
        v=1
    fi
    echo your python version is : $U_V1.$U_V2.$U_V3
    if [ $U_V1 -eq 2 ];then
       echo 'Your python version is not OK!'
       exit 0
    fi
    if [ $U_V1 -lt $V1 ];then
        echo 'Your python version is not OK!(1)'
        exit 1
    elif [ $U_V1 -eq $V1 ];then     
        if [ $U_V2 -lt $V2 ];then 
            echo 'Your python version is not OK!(2)'
            exit 1
        elif [ $U_V2 -eq $V2 ];then
            if [ $U_V3 -lt $V3 ];then 
                echo 'Your python version is not OK!(3)'
                exit 1
            fi
        fi    
    fi

    echo Your python version is OK!
}
CheckUser()  
{  
    check_user=`whoami`  
    if [ "$check_user" == "root" ]  
    then   
        echo "You are $check_user user"  
        echo "You are a super amdin"  
    else  
        echo "You are $check_user user"  
        echo "Installing software requires higher authority"
        exit 0
    fi  
} 
checkpip()
{
 if hash pip3 2>/dev/null; then
    p=0
    echo "Did not find the pip3 command"
    exit 0
 else
    p=1
 fi
}

checkPython
CheckUser
if [ $v -eq 0 ];then
   for i in ${install_package[@]}
    do
       echo "install ...............................................  $i"
	   install_pk=`ls ${i}`
       pip3 install $install_pk
       command_status=$?
       if [ $command_status -eq 0 ];then
         echo "Install $i package successfully"
        else
         echo "Failed to install $i package"
         exit 0
       fi
    done
else
  echo "install fail"
fi
cd mysql-replication-0.15
python3 setup.py install
echo "-------------------------------------------------------------------------------"
echo "Run `which python3` `cd ../..&&pwd`/startup.py to start the real-time synchronization program"
echo "Read the readme file before running"
echo "-------------------------------------------------------------------------------"
