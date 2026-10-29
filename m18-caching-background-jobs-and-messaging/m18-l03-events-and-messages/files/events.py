def enrolled(student, course):
    return {
        "id": f"{student}-{course}",
        "type": "student.enrolled",
        "student": student,
        "course": course,
    }
