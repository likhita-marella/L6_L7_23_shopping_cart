"""
Lab 6 - Code (line) coverage tests for shopping_cart.py
Run:
    coverage run -m pytest CodeCoverageTest_shopping_cart.py
    coverage report -m
"""
import pytest
from shopping_cart import item_total, cart_discount, shipping_fee


# ---------- item_total ----------
def test_food_item():
    assert item_total("food", 100, 2) == 210


def test_unknown_category_raises():
    with pytest.raises(ValueError):
        item_total("toys", 100, 1)


def test_negative_price_raises():
    with pytest.raises(ValueError):
        item_total("food", -10, 1)


def test_bulk_discount_applied():
    # 100*10 = 1000, minus 10% = 900, GST 18% = 162 -> 1062
    assert item_total("electronics", 100, 10) == 1062


# ---------- cart_discount ----------
def test_discount_top_tier_prime_with_coupon():
    # 500 (>=5000) + 100 (prime) + 500 (FLAT10 -> 5000//10) = 1100
    assert cart_discount(5000, True, "FLAT10") == 1100


def test_discount_mid_tier():
    assert cart_discount(2000, False, None) == 200


def test_discount_no_tier():
    assert cart_discount(100, False, None) == 0


# ---------- shipping_fee ----------
def test_free_shipping():
    assert shipping_fee(1000, False, False) == 0


def test_standard_fee_with_express():
    # 40 + 100 = 140
    assert shipping_fee(100, False, True) == 140


def test_prime_express():
    # 0 + 100 - 50 = 50
    assert shipping_fee(100, True, True) == 50
