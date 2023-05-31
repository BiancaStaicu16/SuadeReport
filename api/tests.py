import pytest
import pandas as pd
from report import Report


@pytest.fixture
def sample_data():
    # Sample data for testing.
    order_df = pd.DataFrame(
        {"id": [1, 2, 3], "vendor_id": [1, 2, 3], "customer_id": [101, 102, 103]}
    )
    order_lines_df = pd.DataFrame(
        {
            "order_id": [1, 1, 2, 3],
            "quantity": [2, 3, 4, 1],
            "full_price_amount": [10, 20, 15, 5],
            "discounted_amount": [8, 18, 12, 5],
            "discount_rate": [0.2, 0.1, 0.2, 0.0],
            "total_amount": [16, 54, 48, 5],
        }
    )
    commission_df = pd.DataFrame({"vendor_id": [1, 2, 3], "rate": [0.1, 0.2, 0.15]})

    return {
        "order_df": order_df,
        "order_lines_df": order_lines_df,
        "commission_df": commission_df,
    }


def test_get_number_of_orders(sample_data):
    report = Report()
    order_df = sample_data["order_df"]
    assert report.get_number_of_orders(order_df) == 3


def test_get_number_of_items_sold(sample_data):
    report = Report()
    order_lines_df = sample_data["order_lines_df"]
    assert report.get_number_of_items_sold(order_lines_df) == 10


def test_get_number_of_customers(sample_data):
    report = Report()
    order_df = sample_data["order_df"]
    assert report.get_number_of_customers(order_df) == 3


def test_get_total_amount_of_discount(sample_data):
    report = Report()
    order_lines_df = sample_data["order_lines_df"]
    assert report.get_total_amount_of_discount(order_lines_df) == 7


def test_get_average_discount_rate(sample_data):
    report = Report()
    order_lines_df = sample_data["order_lines_df"]
    report.get_number_of_items_sold(order_lines_df)
    assert report.get_average_discount_rate(order_lines_df) == 0.15


def test_get_average_order_total(sample_data):
    report = Report()
    order_lines_df = sample_data["order_lines_df"]
    report.get_number_of_orders(order_lines_df)
    assert report.get_average_order_total(order_lines_df) == 30.75


def test_get_commission_total(sample_data):
    report = Report()
    order_lines_df = sample_data["order_lines_df"]
    order_df = sample_data["order_df"]
    commission_df = sample_data["commission_df"]
    assert report.get_commission_total(order_lines_df, order_df, commission_df) == 17.35


def test_get_commission_average_per_order(sample_data):
    report = Report()
    order_df = sample_data["order_df"]
    report.get_number_of_orders(order_df)
    report.total_commission = 9
    assert report.get_commission_average_per_order(report.total_commission) == 3
