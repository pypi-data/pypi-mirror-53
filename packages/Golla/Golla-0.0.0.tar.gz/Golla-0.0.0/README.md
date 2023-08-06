# Golla

* A SQL Query free ORM
* Support SQLAlchemy ORM 

### Create Connection 

```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host = 'localhost'
user = 'postgres'
password = 'root'
data_base = 'postgres'
port = '5432'
URL = 'postgresql://{}:{}@{}:{}/{}'
URL = URL.format(user, password, host, port, data_base)
ds_schema = 'public'

engine = create_engine(URL, encoding='utf8')
engine.connect()
Connection = sessionmaker(bind=engine)()

```

### Create Model class

```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column

from golla.table import BaseChild

Base = declarative_base()

BaseChild.Connection = Connection


class Employee(Base, BaseChild):
    __tablename__ = "employee"
    EMPID = Column("emp_id", Integer, primary_key=True)
    NAME = Column("NAME", String)
    Age = Column("Age", Integer)

```


### Save object into DB

```
e = Employee()
e.EMPID = 203
e.Age = 20
e.NAME = "b"

Employee.save(e)

``` 

### Get records from table by id

```
emp = Employee().get_by_id(EMPID=100)
```

### Get all records 

```
emps = Employee().get_all()
```

### Delete records from table by id

```
Employee().delete_by_id(EMPID=201)
```
