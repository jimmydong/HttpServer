fork from https://github.com/freelamb/simple_http_server

# Python Http服务器实现
> 基于python的简单服务器

1. 接受静态请求，`html`，`png`等文件
2. 接受动态请求，脚本类型为`python`
3. 提供`Session`服务
4. `root`是根目录，包含资源文件，脚本等
5. 使用线程池来管理请求

改进：
1. 增加Debug方法
2. 增加controller/action模式

缺点：
1. 不支持上传
2. 不支持JSON模式POST
3. 不支持cookie读写
4. 不支持header定制
5. 不支持模板
