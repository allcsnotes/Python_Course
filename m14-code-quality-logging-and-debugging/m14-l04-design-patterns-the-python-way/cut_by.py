def cut_by(percent):
    def rule(price):
        return price * (100 - percent) // 100

    return rule


student = cut_by(20)
festival = cut_by(10)
print(student(1000), festival(1000))
print(student(500))
