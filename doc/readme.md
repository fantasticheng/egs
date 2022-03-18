## EGS Diag

### 环境搭建
1. 代码拉取
    ```shell
    git clone superadmin@10.105.72.12:/home/superadmin/work/Diag/egs
    ```
2. 登陆远程服务器
    ```shell
    Server IP: 10.55.26.24      root@123456
    HOST IP:192.168.2.22        root@1
    BMC IP: 192.168.2.83        sangfor@sangfor123
    ```

### 代码提交规则
1. 设置自己提交代码的名字和邮箱

    ```shell
    git config --global user.name  "工号"
    git config --global user.email  "公司邮箱"
    git config ---global core.editor vim #此命令可以不执行,看个人习惯使用什么编辑器
    ```

2. commit提交格式
    ```c
    Author: Wangjianlong
    Date: 2022-01-25
    Commit Reason: init repository.
    ```

### 目录详解

1. `bin`:项目源码
2. `common`:通用类库
3. `configs`:配置文件
4. `doc`:项目文档
5. `log`:log文件
