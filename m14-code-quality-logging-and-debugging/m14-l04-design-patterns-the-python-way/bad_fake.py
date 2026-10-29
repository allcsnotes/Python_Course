from checkout import checkout


class BrokenGateway:
    def pay(self, student, amount):
        return "ok"


checkout("Priya", 590, BrokenGateway())
