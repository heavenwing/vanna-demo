tag=$(date +%s)
docker build -t vanna-demo:$tag .
docker tag vanna-demo:$tag vanna-demo:latest
docker tag vanna-demo:$tag msyoz.azurecr.cn/demo/vanna-demo:$tag
docker tag vanna-demo:$tag msyoz.azurecr.cn/demo/vanna-demo:latest
docker push msyoz.azurecr.cn/demo/vanna-demo:$tag
docker push msyoz.azurecr.cn/demo/vanna-demo:latest