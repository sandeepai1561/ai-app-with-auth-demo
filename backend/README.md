* 注意事项一
> 在连接数据库的时候，定义大模型，如果你使用的是 mysql ，那么对于 String --> varchar

> 根据 mysql 的要求，我们需要指定长度的呐

> sqlalchemy 的话是默认支持连接 psql 和 sqlite3 数据库的，但是对于 mysql 来说

> 需要安装 mysql-connector-python： pymysql 或者 mysql-connector-python

> 以及连接 mysql 的时候一定要进行指定本次使用的驱动是什么
---

* 注意事项二
> `pip install uv`

> `uv add`

> `uv run main.py`
---

* 注意事项三

> 多个包之间的话可能会因为依赖包之间的不同，导致 pydantic 出现问题，此时需要统一使用相同版本的解析器

> `nv python install 3.12`

> `project realize at 2025-07-20`