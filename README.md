<div align="center">

# nonebot-plugin-ocr
***

基于 [NoneBot2](https://v2.nonebot.dev/) 的文字识别插件

![](https://img.shields.io/badge/license-MIT-yellow)
[![Python Compatability](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![PyPI version](https://badge.fury.io/py/nonebot-plugin-ocr.svg)](https://pypi.org/project/nonebot-plugin-ocr/)
[![GitHub version](https://badge.fury.io/gh/NewYearPrism%2Fnonebot-plugin-ocr.svg)](https://github.com/NewYearPrism/nonebot-plugin-ocr)

</div>

## NoneBot 适配器支持
***
 + [OneBot V11](https://onebot.adapters.nonebot.dev/)

## OCR 应用支持
***
 + [百度智能云](https://cloud.baidu.com/product/ocr)（Web应用，内置）


## 部署指南
***
### 一. 安装插件
+ 方式一：使用 pip
  > 1.安装 nonebot-plugin-ocr
  > ```
  > pip install nonebot-plugin-ocr
  > ```
  > 2.使用 nonebot 加载插件 "nonebot_plugin_ocr" （[参考：加载插件](https://v2.nonebot.dev/docs/tutorial/plugin/load-plugin)）
+ 方式二：手动安装
  > 1.克隆本仓库
  > ```
  > git clone https://github.com/NewYearPrism/nonebot-plugin-ocr
  > ```
  > 2.安装依赖 requirements.txt
  > ```
  > pip install -r requirements.txt
  > ```
  > 3.复制插件本体到 Nonebot 环境中
  > ```
  > cp path/to/repo/nonebot-plugin-ocr/nonebot_plugin_ocr path/to/nonebot_plugins -r
  > ```
  > 4.使用 nonebot 加载插件（同上）
### 二. 创建配置文件
+ 需要手动创建配置文件，配置文件默认路径 ".ocr/config.toml" (相对当前工作目录)， 你可以在 NoneBot .env配置中使用变量OCR_CONFIG_PATH指定之：
  > <span># .env</span><br/>
  > HOST=0.0.0.0<br/>
  > PORT=8080<br/>
  > SUPERUSERS=["123456789", "987654321"]<br/>
  > <span># ...</span><br/>
  > OCR_CONFIG_PATH="path/to/config/ocr.toml"<br/>
    ```
    mkdir -p path/to/config
    vim path/to/config/ocr.toml 
    ```
+ 具体参考：[配置模板](config.template.toml)和[配置文档](docs/config.md)


# 使用方法
***
+ [使用演示](docs/usage.md)


# 特别感谢
***
+ [cq-picsearcher-bot](https://github.com/Tsuk1ko/cq-picsearcher-bot)
+ [baidu-aip](https://pypi.org/project/baidu-aip/)
