is_enrolled = True
has_paid = False
if is_enrolled:
    print("Welcome back, Lukas.")
    if has_paid:
        print("Playing the video.")
    else:
        print("Please complete the payment.")
else:
    print("Please enrol first.")
