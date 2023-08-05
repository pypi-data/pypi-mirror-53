from setuptools import setup, find_packages

setup(
    name = "pianyuan",
    version = "1.0.0",  #版本号，数值大的会优先被pip
    keywords = ["pip", "pianyuan.la","mysql","spider","web"],
    description = "An spider for pianyuan.la which can save to mysql",
    long_description = "Get bt in pianyuan.la, save to mysql",
    license = "MIT Licence",

    url = "https://github.com/ptrtonull-workshop/PianYuan",     #项目相关文件地址，一般是github
    author = "WangTingZheng",
    author_email = "wangtingzheng@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["bs4","beautifulsoup4","flake8","mysqlclient","black"]          #这个项目需要的第三方库
)
