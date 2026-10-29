def checkout(student, *courses, **options):
    print(student)
    print(courses)
    print(options)

checkout("Lukas", "Python Basics", "SQL Basics",
         cupon="NEW10")
