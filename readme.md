# domian update 
certbot manual aliyun dns manual hook scripts

1. 使用python 实现aliyun dns验证
2. 支持docker部署,打包到certbot镜像的工作目录下

# 注意
测试证书安装必须使用 --staging参数，防止正式环境没法申请证书


# docker 环境安装
``` shell
curl -sSL https://get.docker.com | sh -
DOCKER_COMPOSE_VERSION=1.22.0
curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
-o /usr/local/bin/docker-compose
#修改用户组及权限
chown :docker /usr/local/bin/docker-compose
chmod ug+x /usr/local/bin/docker-compose
usermod -aG docker $Username
``` 


# Run

```
docker build -t test .
docker run -it -e "ALI_ID=xxx" -e "ALI_KEY=xxx" test certonly --staging -d test.demo.pub --preferred-challenges dns  --manual -m linwu@live.cn --agree-tos --manual-auth-hook "./alidns.py" --manual-cleanup-hook "./alidns.py" --non-interactive --manual-public-ip-logging-ok
```