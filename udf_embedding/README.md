# postgre扩展plpython

**Dockerfile**
```
FROM postgres:12

# Create plpython3u when the db starts.
RUN echo 'CREATE EXTENSION IF NOT EXISTS plpython3u;' > /docker-entrypoint-initdb.d/py3.sql
# Installing last python and plpython3 for current version
RUN apt update && apt install python3 python3-pip postgresql-plpython3-${PG_MAJOR} -y
RUN su - postgres\
    && pip3 install ray pyarrow --break-system-packages\
    && exit
```
**运行镜像**
```
docker run --net=host -e POSTGRES_PASSWORD=root -d $image_id
```
**连接数据库**
```
docker exec -it $container_id psql -U postgres
```


# 创建自定义函数
**创建函数**
将`plpython_embed_client.py`的代码在psql命令行执行，出现`CREATE FUNCTION`即成功。
**创建表**
```
CREATE TABLE mytable(slice1 TEXT);
INSERT INTO mytable (slice1) VALUES ('hello Postgre');
```

# 启动服务端
在宿主机命令行运行```python udf_server.py```，启动udf-server。

# 执行udf进行测试
```
select embed(slice1) from mytable;

```
返回
```
{-0.540918,-0.3623047,-0.018339634,0.6466797,-0.20214844,0.038217165,0.13275146,0.7792969,-0.04244232,0.18013915,0.61743164,-0.14133301,-0.3885742,-0.4790039,0.44997558,-0.7,-0.101724245,......}
(1 row)
```
测试成功