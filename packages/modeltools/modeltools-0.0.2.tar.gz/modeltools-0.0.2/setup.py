
#############################################
# File Name: setup.py
# Author: wangxup
# Mail: wang_xup@163.com
# Created Time:  2019-9-26
#############################################

from setuptools import setup, find_packages            

setup(
    name = "modeltools",      #这里是pip项目发布的名称
    version = "0.0.2",  
    keywords = ("modeltools"),
    description = "常用的",
    long_description = "常用的",
    license = "MIT Licence",

    #url = "None",     
    author = "wangxup",
    author_email = "wang_xup@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    # install_requires = ['random', 'pandas', 'numpy', 'sklearn']
)
