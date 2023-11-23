**运行镜像**
```
docker run --net=host -e POSTGRES_PASSWORD=root -d $image_id
```
**连接数据库**
```
docker exec -it $container_id psql -U postgres
```