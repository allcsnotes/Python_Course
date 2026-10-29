class Course:
    pass


Product = Course
first = Product()
print(type(first))
print(type(Course))
print(Product is Course)
