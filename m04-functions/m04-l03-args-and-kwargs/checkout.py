def checkout(student, *courses, **options):
    print(student)
    print(courses)
    print(options)

checkout("Lukas", "Python Basics", "SQL Basics",
         coupon="NEW10", gift=True)
