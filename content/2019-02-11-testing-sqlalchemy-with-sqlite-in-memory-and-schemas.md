---
title: Testing SQLAlchemy with SQLite in memory and schemas 
date: 2019-02-11
slug: testing-sqlalchemy-with-sqlite-in-memory-and-schemas
tags: python, sqlalchemy, programming, sqlite, testing
---

[SQLAlchemy](https://www.sqlalchemy.org/) is a very popular and common option in Python to handle databases and map them into objects (or well, a fully featured ORM in Python), it is super flexible and easy to learn and use.

One option when testing SQLAlchemy models and objects, is to use an [in-memory database](https://en.wikipedia.org/wiki/In-memory_database) with something like [SQLite](https://www.sqlite.org/index.html) (and it comes [included in your Python standard library](https://docs.python.org/2/library/sqlite3.html)), overall the process to test your database in your unit tests looks something like this:

```python
import unittest
from myapp import db, User

class TestDb(unittest.TestCase):
    def setUp(self):
        db.init_app('sqlite://')
        db.create_all()
        db.session.add(User(name='Cristian'))
        db.commit()
        
    def test_it(self):
        user = User.query.filter_by(name='Cristian')
        assert user is not None
        
    def tearDown(self):
        # TODO: clean up your test
```

Of course, your unit test probably will look very different than this, and well, testing against SQLAlchemy is very well described in the SQLAlchemy documentation and [book](https://www.oreilly.com/library/view/essential-sqlalchemy-2nd/9781491916544/ch04.html).

As you may see, we test _against_ an in-memory database instead of having to attach to a running db, this will speed up all our data operations in the test and reconstruct the db for every test keeping atomicity in our tests.

Recently I found a problem with testing and using schemas (a common feature in RDBMS like PostgreSQL to separate different business concerns in the same database, by the way, in MySQL they are synomim of a database), this is because SQLite doesn't support schemas, and the idea of a schema is just as metadata included in the entity with SQLAlchemy, for example, in our hypotethical case for `User`:

```python
class User(Model):
    __table__ = 'users'
    __table_args__ = {
        'schema': 'authentication'
    }
```

I was looking around about alternatives to continue testing with in-memory SQLite without having to get rid of the schemas in each table or having to install a db server in our CI, then, reading the SQLite documentation I found about the command [`ATTACH`](https://www.sqlite.org/lang_attach.html):

> The ATTACH DATABASE statement adds another database 
> file to the current [database connection](https://www.sqlite.org/c3ref/sqlite3.html). 
> Database files that were previously attached can be removed using
> the [DETACH DATABASE](https://www.sqlite.org/lang_detach.html) command.

In fact, we can even attach an in-memory database to the current database session using `":memory:"` as the database file name. This is very useful because in this case the _attached database_ will _emulate_ the schema in a bigger RDBMS like PostgreSQL or MySQL.

To do so, we have to change our `setUp` method just a little to issue a few commands after setting our database connection:

```python
def setUp(self):
    db.init('sqlite://')
    db.execute("ATTACH ':memory:' DATABASE AS authentication")
    db.create_all()
```

And that will work as expected, now the queries designed to go to `authentication.users` will go to the in-memory database attached to the "main" in-memory database (the in-memory database we started the session with is identified by the name _main_).

You can have as many attached emulated schemas as you want, this trick saved me a lot of time when writing unit tests using schemas and SQLAlchemy.