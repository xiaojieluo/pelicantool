pelicantool 是一个自动化管理 pelican 博客的工具， 使用 Python 3 编写

pelicantool 支持命令行与配置文件参数，
当命令行参数与配置文件冲突时， 取命令行参数

配置文件名为 pelicantool.toml， 配置文件格式为 `toml`

命令行参数：
    -c --config_dir : 指定 配置文件所在的目录名称， 若不存在， 默认读取当前运行目录下的 pelicantool.toml
    -v 输出版本

usage example:
    pelicantool create article
