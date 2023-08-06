# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nemcore']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.9,<4.0',
 'pycryptodomex>=3.9,<4.0',
 'requests-cache>=0.5.2,<0.6.0',
 'requests>=2.22,<3.0',
 'six>=1.12,<2.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'nemcore',
    'version': '0.1.2',
    'description': 'NetEase Cloud Music ApiClient extracted from NetEase-MusicBox',
    'long_description': '# NetEase Cloud Music ApiClient\n\n网易云音乐核心 API 客户端。\n\n这个项目的目的是抽离一个干净的 API Client，便于二次开发和维护。\n\n主要代码来自[NetEase-MusicBox](https://github.com/darknessomi/musicbox/)，非常感谢每一位该项目的贡献者。\n\n## v1.0 开发计划\n\n- [x] 添加测试用例\n- [x] 规范命名和返回值结构\n- [ ] 提供助手函数，实现一些常用操作\n- [ ] 移除 python2 支持(`__future__`等)，迁移到 python3.6+\n- [ ] 支持异步(考虑`aiohttp`)\n',
    'author': 'weak_ptr',
    'author_email': 'weak_ptr@163.com',
    'url': 'https://github.com/nnnewb/NEMCore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
