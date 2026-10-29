from checkout_hard import checkout


def test_checkout():
    receipt = checkout("Priya", 590)
    assert receipt == "card: charged Priya Rs 590"
