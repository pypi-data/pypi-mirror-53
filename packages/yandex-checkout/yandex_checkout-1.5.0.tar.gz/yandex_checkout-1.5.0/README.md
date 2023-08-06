# Yandex.Checkout API Python Client Library

[![Build Status](https://travis-ci.org/yandex-money/yandex-checkout-sdk-python.svg?branch=master)](https://travis-ci.org/yandex-money/yandex-checkout-sdk-python)
[![Latest Stable Version](https://img.shields.io/pypi/v/yandex-checkout.svg)](https://pypi.org/project/yandex-checkout/)
[![Total Downloads](https://img.shields.io/pypi/dm/yandex-checkout.svg)](https://pypi.org/project/yandex-checkout/)
[![License](https://img.shields.io/pypi/l/yandex-checkout.svg)](https://github.com/yandex-money/yandex-checkout-sdk-python)

Russian | [English](https://github.com/yandex-money/yandex-checkout-sdk-python/blob/master/README.en.md)

Клиент для работы с платежами по [API Яндекс.Кассы](https://kassa.yandex.ru/docs/checkout-api/)
Подходит тем, у кого способ подключения к Яндекс.Кассе называется API.

## Требования

1. Python 2.7 or Python 3.x
2. pip

## Установка
### C помощью pip

1. Установите pip.
2. В консоли выполните команду
```bash
pip install --upgrade yandex_checkout
```

### С помощью easy_install
1. Установите easy_install.
2. В консоли выполните команду
```bash
easy_install --upgrade yandex_checkout
```

### Вручную

1. В консоли выполните команды:
```bash
wget https://pypi.python.org/packages/5a/be/5eafdfb14aa6f32107e9feb6514ca1ad3fe56f8e5ee59d20693b32f7e79f/yandex_checkout-1.0.0.tar.gz#md5=46595279b5578fd82a199bfd4cd51db2
tar zxf yandex_checkout-1.0.0.tar.gz
cd yandex_checkout-1.0.0
python setup.py install
```

## Начало работы

1. Импортируйте модуль
```python
import yandex_checkout
```
2. Установите данные для конфигурации
```python
from yandex_checkout import Configuration

Configuration.configure('<Идентификатор магазина>', '<Секретный ключ>')
```

или

```python
from yandex_checkout import Configuration

Configuration.account_id = '<Идентификатор магазина>'
Configuration.secret_key = '<Секретный ключ>'
```

или через oauth

```python
from yandex_checkout import Configuration

Configuration.configure_auth_token('<Oauth Token>')
```

Если вы согласны участвовать в развитии SDK, вы можете передать данные о вашем фреймворке, cms или модуле:
```python
from yandex_checkout import Configuration
from yandex_checkout.domain.common.user_agent import Version

Configuration.configure('<Идентификатор магазина>', '<Секретный ключ>')
Configuration.configure_user_agent(
    framework=Version('Django', '2.2.3'),
    cms=Version('Wagtail', '2.6.2'),
    module=Version('Y.CMS', '0.0.1')
)
```

3. Вызовите нужный метод API. [Подробнее в документации к API Яндекс.Кассы](https://kassa.yandex.ru/docs/checkout-api/)


