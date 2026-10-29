from datetime import datetime

text = "03/11/2026"
print(datetime.strptime(text, "%d/%m/%Y").date())
print(datetime.strptime(text, "%m/%d/%Y").date())
