When ini config file looks like below:
```ini
[default]
debug = False

[mysql]
connection = sqlite:///test.db
#connection = mysql+pymysql://root:password@localhost:13306/project?charset=utf8
track_modifications = True

[secure]
secure_key = YjFjMDVkYzAtZGI4YS0xMWU5LWIwMjctMTdhNzg4ZjJiMGUyCg==

[jwt]
secret = YTgzNmM0OWUtNjllMS00MjI4LWFlZTMtNjgxNjAwNDdiNTBlCg==
algorithm = HS256

[test]
int_value = 1231
```

You need to create class based on ConfigOpts
```python
from flask_fastconfig import ConfigOpts, ConfigGroup
from flask_fastconfig.config_opt import BooleanOpt, StrOpt, IntOpt
import uuid


class CONF(ConfigOpts):
    """
    ini configs
    """

    class default(ConfigGroup):
        debug = BooleanOpt(default=True, app_config="DEBUG")

    class mysql(ConfigGroup):
        connection = StrOpt(default='sqlite:///gevoton.db', app_config="SQLALCHEMY_DATABASE_URI")
        track_modifications = BooleanOpt(default=False, app_config="SQLALCHEMY_TRACK_MODIFICATIONS")

    class secure(ConfigGroup):
        secure_key = StrOpt(default=uuid.uuid4().hex, app_config="SECRET_KEY")

    class jwt(ConfigGroup):
        secret = StrOpt(default=uuid.uuid4().hex)
        algorithm = StrOpt(default='HS256')

    class test(ConfigGroup):
        int_value = IntOpt(default=123)
```

Then you can init flask app like below
```python
from flask import Flask
from test import CONF

app = Flask(__name__)
cfg = CONF(app, "../system/etc/gevoton.ini")
app.config.from_mapping(cfg.get_app_config())
```

Finally, you can use cfg in other places:
```python
from app import cfg

print(cfg.mysql.connection)
```