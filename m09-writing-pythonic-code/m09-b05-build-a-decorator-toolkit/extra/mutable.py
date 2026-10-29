from toolkit import cache_for


@cache_for(10)
def lessons(course_id):
    return ["Intro", "Loops"]


mine = lessons("C101")
mine.append("Oops")
print(lessons("C101"))
