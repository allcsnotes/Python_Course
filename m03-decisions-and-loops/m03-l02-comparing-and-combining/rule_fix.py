is_enrolled = False
has_paid = False
is_free = True
if is_enrolled and (has_paid or is_free):
    print("Video unlocked")
else:
    print("Video locked")
