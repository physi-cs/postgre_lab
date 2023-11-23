# postgre\opengauss扩展plpython
参考各模块README
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