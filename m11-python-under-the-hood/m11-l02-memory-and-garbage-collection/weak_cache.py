import weakref


class Course:
    def __init__(self, title):
        self.title = title


strong = {}
weak = weakref.WeakValueDictionary()
python = Course("Python")
sql = Course("SQL")
strong["py"] = python
weak["sql"] = sql
del python
del sql
print(len(strong), len(weak))
print(strong["py"].title)
print(weak.get("sql"))
