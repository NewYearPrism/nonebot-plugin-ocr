# 演示
  > 演示环境：Onebot V11，百度智能云OCR，nonebot-plugin-ocr 0.3.0
+ 发送命令消息 -> 发送图片消息

<a href="https://sm.ms/image/5RNIeojZ3bvd2E4" target="_blank"><img src="https://s2.loli.net/2022/09/29/5RNIeojZ3bvd2E4.jpg" width="300px"/></a>

+ 使用命令消息回复图片消息

<a href="https://sm.ms/image/5mQMT8KyRutjFZk" target="_blank"><img src="https://s2.loli.net/2022/09/29/5mQMT8KyRutjFZk.jpg" width="300px"/></a>

+ 发送含图片的命令消息

<a href="https://sm.ms/image/OYzbUXq8mGufBDc" target="_blank"><img src="https://s2.loli.net/2022/09/29/OYzbUXq8mGufBDc.jpg" width="300px"/></a>

+ 发送命令 -> 发送任意不含图片的消息取消

<a href="https://sm.ms/image/8wzJjh5gufIq4Hb" target="_blank"><img src="https://s2.loli.net/2022/09/29/8wzJjh5gufIq4Hb.jpg" width="300px"></a>


# 提示
+ 默认命令为 "ocr"，可在[配置](config.md)中修改
+ 如图所示，OCR命令接受以空格隔开的参数，可用于指定识别语言种类等，支持的值取决于OCR应用
    + 目前暂定命令格式为 ocr \[语言\] \[模式\]，暂时只支持位置参数 