import pytest

from pricing import BundleFree, Cart, FlatOff, Item, PercentOff, Rule


def cart(*items, rules=()):
    c = Cart(rules=list(rules))
    for item in items:
        c.add(item)
    return c


def test_item_total_and_validation():
    assert Item("Python", 499, 2).total == 998
    with pytest.raises(ValueError):
        Item("Python", -1)
    with pytest.raises(ValueError):
        Item("Python", 499, 0)


def test_adding_same_course_merges_quantity():
    c = cart(Item("Python", 499), Item("Python", 499, 2))
    assert len(c.items) == 1 and c.items[0].qty == 3


def test_no_rules_only_gst():
    assert cart(Item("Python", 500)).summary() == {
        "subtotal": 500, "discount": 0, "net": 500, "gst": 90, "total": 590}


def test_percent_with_minimum():
    rule = PercentOff(10, min_subtotal=1000)
    assert cart(Item("A", 500), rules=[rule]).summary()["discount"] == 0
    assert cart(Item("A", 1000), rules=[rule]).summary()["discount"] == 100


def test_rules_stack_and_are_listed():
    c = cart(Item("A", 600), Item("B", 400), rules=[PercentOff(10), FlatOff(50)])
    assert c.discounts() == [("10% off", 100), ("Rs 50 off", 50)]
    assert c.summary()["net"] == 850


def test_discount_never_exceeds_the_subtotal():
    c = cart(Item("A", 100), rules=[FlatOff(80), FlatOff(80)])
    assert c.summary()["net"] == 0 and c.summary()["total"] == 0


def test_bundle_cheapest_free():
    c = cart(Item("A", 500), Item("B", 300), Item("C", 800), rules=[BundleFree(3)])
    assert c.discounts() == [("cheapest of the bundle free", 300)]
    assert cart(Item("A", 500), Item("B", 300), rules=[BundleFree(3)]).discounts() == []


def test_rule_is_abstract_and_extendable():
    with pytest.raises(TypeError):
        Rule()

    class Tenner(Rule):
        label = "Rs 10 off"
        def discount(self, items, subtotal):
            return 10

    assert cart(Item("A", 100), rules=[Tenner()]).summary()["net"] == 90
