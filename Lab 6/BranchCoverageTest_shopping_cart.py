"""
Lab 6 - Branch coverage tests for shopping_cart.py
Run:
    coverage run --branch -m pytest BranchCoverageTest_shopping_cart.py
    coverage report -m
Every decision is exercised both True and False, including boundary values.
"""
import pytest
from shopping_cart import item_total, cart_discount, shipping_fee


# ---------- item_total ----------
def test_food_item():
    assert item_total("food", 100, 2) == 210


@pytest.mark.parametrize("category", ["toys", "", "FOOD"])
def test_unknown_category_raises(category):
    with pytest.raises(ValueError, match="unknown category"):
        item_total(category, 100, 1)


def test_negative_price_raises():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -1, 1)


@pytest.mark.parametrize("qty", [0, -5])
def test_non_positive_qty_raises(qty):
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, qty)


def test_zero_price_is_allowed():
    assert item_total("clothing", 0, 3) == 0


def test_qty_just_below_bulk_threshold():
    # qty 9 -> no bulk discount: 900 + 900*5//100 = 945
    assert item_total("food", 100, 9) == 945


def test_qty_at_bulk_threshold():
    # qty 10 -> 1000 - 100 = 900; GST 5% -> 945
    assert item_total("food", 100, 10) == 945


def test_bulk_discount_electronics():
    assert item_total("electronics", 100, 10) == 1062


def test_clothing_gst():
    # 100 + 100*12//100 = 112
    assert item_total("clothing", 100, 1) == 112


# ---------- cart_discount ----------
@pytest.mark.parametrize(
    "value, expected",
    [
        (5000, 500),   # top tier boundary
        (4999, 200),   # just below top tier
        (2000, 200),   # mid tier boundary
        (1999, 0),     # just below mid tier
        (0, 0),
    ],
)
def test_tier_boundaries(value, expected):
    assert cart_discount(value, False, None) == expected


def test_prime_bonus_added():
    assert cart_discount(100, True, None) == 100


def test_prime_bonus_not_added():
    assert cart_discount(100, False, None) == 0


def test_coupon_valid_at_threshold():
    # cart 1000, no tier, FLAT10 -> 100
    assert cart_discount(1000, False, "FLAT10") == 100


def test_coupon_below_min_cart_value():
    assert cart_discount(999, False, "FLAT10") == 0


def test_wrong_coupon_code_ignored():
    assert cart_discount(1000, False, "SAVE20") == 0


def test_no_coupon_ignored():
    assert cart_discount(3000, False, None) == 200


def test_all_discounts_stack():
    # 500 + 100 + 500 = 1100
    assert cart_discount(5000, True, "FLAT10") == 1100


# ---------- shipping_fee ----------
def test_prime_free_shipping():
    assert shipping_fee(10, True, False) == 0


def test_free_shipping_at_threshold():
    assert shipping_fee(500, False, False) == 0


def test_paid_shipping_below_threshold():
    assert shipping_fee(499, False, False) == 40


def test_express_non_prime_below_threshold():
    assert shipping_fee(100, False, True) == 140


def test_express_non_prime_above_threshold():
    assert shipping_fee(1000, False, True) == 100


def test_express_prime_discount():
    assert shipping_fee(100, True, True) == 50
