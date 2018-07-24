-----  程序说明:\<br>
本程序实时监控MySQL binlog解析event SQL同步至另外一个实例或者另一库或表中\<br>
-----  版本号:\<br>
v 1.0.0\<br>
    1、初始化版本提交\<br>

v 1.0.1\<br>
    1、修复同步删除语句更新检查点bug\<br>
    2、增加批量组提交功能\<br>

-----  功能说明:\<br>

1、支持分库分表合并到单个库表中
2、支持一比一实时同步\<br>
3、支持DDL同步\<br>
4、支持库表同步切换同步\<br>
5、支持脱敏字段加密同步\<br>
6、支持批量组提交、加快同步速度\<br>

-----  依赖环境：\<br>
程序基于Python 3.6开发，运行环境不能低于Python 3.0版本\<br>

-----  安装:\<br>
在install目录执行: sh install.sh\<br>

-----  目录解构描述:\<br>
py_sync_binlog_mysql\<br>
|-- auto_cnf\<br>
|   `-- auto.cnf\<br>
|-- checkpoint  // 检查点文件\<br>
|-- encryption // 密码加密模块\<br>
|   `-- passwd_encryption.py\<br>
|-- install //安装目录\<br>
|   |-- certifi-2018.4.16-py2.py3-none-any.whl\<br>
|   |-- chardet-3.0.4-py2.py3-none-any.whl\<br>
|   |-- crypto-1.4.1.tar.gz\<br>
|   |-- idna-2.7-py2.py3-none-any.whl\<br>
|   |-- install.sh\<br>
|   |-- mysql-replication-0.15  //复制模块\<br>
|   |   |-- setup.cfg\<br>
|   |   `-- setup.py\<br>
|   |-- Naked-0.1.31-py2.py3-none-any.whl\<br>
|   |-- pycrypto-2.6.1.tar.gz\<br>
|   |-- PyMySQL-0.8.1.tar.gz\<br>
|   |-- PyYAML-3.12.tar.gz\<br>
|   |-- requests-2.19.1-py2.py3-none-any.whl\<br>
|   |-- shellescape-3.4.1-py2.py3-none-any.whl\<br>
|   `-- urllib3-1.23-py2.py3-none-any.whl\<br>
|-- LICENSE\<br>
|-- logs \<br>
|-- README.md\<br>
|-- startup.py  // 启动文件\<br>
|-- sync_binlog //主目录\<br>
|   |-- AES_Encryption.py //同步加密模块\<br>
|   |-- analysis_binlog_main.py // 分析模块\<br>
|   |-- analysis_binlogs.py 
|   |-- analysis_rows.py // 行解析模块\<br>
|   |-- batch_analysis_insert_sql.py // 批量提交模块\<br>
|   |-- Decrypt.py //同步加密模块\<br>
|   |-- global_transaction_insert_batch_id.py // 全局ID模块\<br>
|   |-- main_multi_threading.py // 多线程模块(暂时没有用)\<br>
|   |-- merge_dbname_tables.py // 合并模块\<br>
|   |-- output_log.py // 日志模块\<br>
|   |-- parameter_check.py // 参数检查模块\<br>
|   |-- safe_shutdown.py // 安全关闭模块\<br>
|   |-- send_binlog.py // 发送SQL模块\<br>
|   `-- update_post.py // 更新检查点模块\<br>
`-- sync_conf.py // 配置文件\<br>

----- 常见问题\<br>
1、同步出现更新未找到匹配行或者删除未匹配行，程序自动自动退出\<br>
处理步骤：检查上下游数据是否一致，并且在日志中找到出错SQL语句，如果是下游不存在数据则需要添加该数据\<br>
重启程序，程序默认跳过出错语句\<br>
2、同步出现主键冲突\<br>
处理步骤与问题1一致\<br>
3、如果有加密字段出现问题\<br>
处理步骤：方式有两个\<br>
一、重启程序默认跳过。\<br>
二、找到上游数据在Navicat中查询数据复制为insert语句，删除上游数据，重新插入，确保下游也无该数据，再重启同步程序\<br>

