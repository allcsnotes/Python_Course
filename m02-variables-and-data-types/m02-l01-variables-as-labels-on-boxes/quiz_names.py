import keyword
for n in ["student_name","total_price","price2","Price","2nd_course","course name","price-2","class"]:
    print(n, n.isidentifier() and not keyword.iskeyword(n))
