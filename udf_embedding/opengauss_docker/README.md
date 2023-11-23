
# 1 准备工作
> https://docs-opengauss.osinfra.cn/zh/docs/5.1.0/docs/InstallationGuide/%E5%8D%95%E8%8A%82%E7%82%B9%E5%AE%89%E8%A3%85_%E5%AE%B9%E5%99%A8.html
## 1.1 验证python enable-shared开启
`docker run -it centos/python-38-centos7 bash`
```
import sysconfig
sysconfig.get_config_vars('Py_ENABLE_SHARED')

```
验证镜像已开启python共享库

## 1.2 制作镜像 
### 下载opengauss二进制安装包
opengauss在5.1.0才较好支持PL/python
> git log 7b3c0feadd954bb564b7aabf742969931046f5d2
因此选择5.1.0企业版 ，在手动编译的configure添加执行参数`--with-python`
手动编译后的结果已打包为openGauss-5.1.0-pl-CentOS-64bit.tar.bz2
下载后放在openGauss-server/docker/dockerfiles/5.1.0目录
### 修改Dockerfile
1. 基础镜像改为`FROM centos/python-38-centos7`
将openGauss-server/docker/dockerfiles/5.0.0/dockerfile_amd中的5.0.0全部改为5.1.0，并将文件夹名修改为5.1.0
2. 添加root权限
3. 添加python共享库软链接
   ```
   ln -s /opt/rh/rh-python38/root/usr/lib64/libpython3.so.rh-python38 /opt/rh/rh-python38/root/usr/lib64/libpython3.so
   ```
4. 安装依赖pyarrow
### 启动镜像制作脚本
```
sh buildDockerImage.sh  -v 5.1.0 -i
```
## 1.3 启动镜像
```
docker run --network host --name opengauss --privileged=true -d -e GS_PASSWORD=Root@123 opengauss:5.1.0
```

之后进入容器bash，切换omm，启动gsql即可连接数据库
```
gsql -r -d postgres -U gaussdb -W 'Root@123' -p5432
```
# 2 添加UDF
```
create Extension plpython3u;
```
其他和postgre一致