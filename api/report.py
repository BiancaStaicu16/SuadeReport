import pandas as pd
from preprocess_data import Data
from typing import Dict, Any


class Report:
    """A class used to compute and encapsulate the report for a particular date.

    Attributes:
        number_of_items_sold (int): Total number of items sold on a specific date.
        number_of_customers (int): Total number of customers that made an order on a specific date.
        total_discount (float): Total amount of discount given on a specific date.
        average_discount_rate (float): Average discount rate applied to the items sold on a specific date.
        number_of_orders (int): Total number of orders executed on a specific date.
        total_commission (float): Total amount of commissions generated on a specific date.
        average_commission (float): Average commission per order for a specific date.
    """

    def __init__(self):
        self.number_of_items_sold = 0
        self.number_of_customers = 0
        self.total_discount = 0
        self.average_discount_rate = 0
        self.number_of_orders = 0
        self.total_commission = 0
        self.average_commission = 0

    def get_number_of_orders(self, order_df):
        """Compute and return the total number of orders.

        Parameters:
            order_df (pd.DataFrame): Dataframe containing the order data.

        Returns:
            int: Total number of orders.
        """
        self.number_of_orders = len(order_df)
        return self.number_of_orders

    def get_number_of_items_sold(self, order_lines_df: pd.DataFrame) -> int:
        """Compute and return the total number of items sold on a specific day.

        Parameters:
            order_lines_df (pd.DataFrame): Dataframe containing the order lines data.

        Returns:
            int: Total number of items sold.
        """
        self.number_of_items_sold = sum(order_lines_df["quantity"])
        return self.number_of_items_sold

    def get_number_of_customers(self, order_df: pd.DataFrame) -> int:
        """Compute and return the total number of customers that made an order on a specific day.

        Parameters:
            order_df (pd.DataFrame): Dataframe containing the order data.

        Returns:
            int: Total number of customers.
        """
        self.number_of_customers = len(pd.unique(order_df["customer_id"]))
        return self.number_of_customers

    def get_total_amount_of_discount(self, order_lines_df: pd.DataFrame) -> float:
        """Compute and return the total amount (value) of discount given on a specific day.

        Parameters:
            order_lines_df (pd.DataFrame): Dataframe containing the order lines data.

        Returns:
            float: Total amount discount.
        """
        self.total_discount = sum(
            order_lines_df["full_price_amount"] - order_lines_df["discounted_amount"]
        )
        return self.total_discount

    def get_average_discount_rate(self, order_lines_df: pd.DataFrame) -> float:
        """Compute and return the average discount rate applied to the items sold on a specific day.

        Parameters:
            order_lines_df (pd.DataFrame): Dataframe containing the order lines data.

        Returns:
            float: Average discount rate.
        """
        total_discount_rate = sum(
            order_lines_df["discount_rate"] * order_lines_df["quantity"]
        )
        self.average_discount_rate = total_discount_rate / self.number_of_items_sold
        return self.average_discount_rate

    def get_average_order_total(self, order_lines_df: pd.DataFrame) -> float:
        """Compute and return the average order total for a specific day.

        Parameters:
            order_lines_df (pd.DataFrame): Dataframe containing the order lines data.

        Returns:
            float: Average order total.
        """
        total_order = sum(order_lines_df["total_amount"])
        self.average_order_total = total_order / self.number_of_orders
        return self.average_order_total

    def get_commission_total(
        self,
        order_lines_df: pd.DataFrame,
        order_df: pd.DataFrame,
        commission_df: pd.DataFrame,
    ) -> float:
        """Compute and return the total amount of commissions generated for a specific day.

        Parameters:
            order_lines_df (pd.DataFrame): Dataframe containing the order lines data.
            order_df (pd.DataFrame): Dataframe containing the order data.
            commission_df (pd.DataFrame): Dataframe containing the commission data.

        Returns:
            float: The total commission.
        """
        # Get the totals based on the order ids to get the order total.
        order_id_and_total = (
            order_lines_df[["order_id", "total_amount"]].groupby("order_id").sum()
        )
        merge_vendor_id = order_id_and_total.merge(
            order_df, left_on="order_id", right_on="id"
        )

        # Sum the order totals.
        vendor_id_and_total = (
            merge_vendor_id[["vendor_id", "total_amount"]].groupby("vendor_id").sum()
        )
        merge_commission_rate = vendor_id_and_total.merge(
            commission_df, on="vendor_id", how="left"
        )

        # Compute total commissions.
        self.total_commission = sum(
            merge_commission_rate["total_amount"] * merge_commission_rate["rate"]
        )

        return self.total_commission

    def get_commission_average_per_order(self, total_commission: float) -> float:
        """
        Compute and return the average amount of commissions per order for a specific day.

        Args:
            total_commission (float): Total commission computed previously.

        Returns:
            float: The average commission per order.
        """
        self.average_commission = total_commission / self.number_of_orders
        return self.average_commission

    def get_report(self, data: Data) -> Dict[str, Any]:
        """
        Populate the Report object and return a dictionary with the required data.

        Args:
            data (Data): Data class object which has already been filtered to only contain
                        information about the date being inquired.

        Returns:
            dict: A dictionary with the required data.
        """
        self.get_number_of_orders(data.orders)
        self.get_number_of_items_sold(data.order_lines)
        self.get_number_of_customers(data.orders)
        self.get_total_amount_of_discount(data.order_lines)
        self.get_average_discount_rate(data.order_lines)
        self.get_average_order_total(data.order_lines)

        self.get_commission_total(data.order_lines, data.orders, data.commissions)
        self.get_commission_average_per_order(self.total_commission)
        return {
            "customers": self.number_of_customers,
            "total_discount_amount": self.total_discount,
            "items": self.number_of_items_sold,
            "order_total_avg": self.average_order_total,
            "discount_rate_avg": self.average_discount_rate,
            "commissions": {
                "total": self.total_commission,
                "order_average": self.average_commission,
            },
        }
