import pandas as pd


class Data:
    """A class used to load and handle the order, order lines, and commission data.

    This class includes methods to manipulate and filter data. It loads CSV files into pandas DataFrames
    and includes methods for extracting dates from the 'created_at' field and isolating data by date.

    Attributes:
        commissions (pd.DataFrame): DataFrame representing the data from commissions.csv.
        order_lines (pd.DataFrame): DataFrame representing the data from order_lines.csv.
        orders (pd.DataFrame): DataFrame representing the data from orders.csv.
    """

    def __init__(self):
        self.commissions = pd.read_csv("data/commissions.csv")
        self.order_lines = pd.read_csv("data/order_lines.csv")
        self.orders = pd.read_csv("data/orders.csv")
        self.promotions = pd.read_csv("data/promotions.csv")

    def extract_order_dates(self):
        """
        Extract order dates from the 'created_at' column.

        The 'created_at' column in the order.csv file combines the date and time of an order.
        This method extracts the date and appends it as an additional column named 'date' to the order DataFrame.
        """
        self.orders["date"] = self.orders["created_at"].str.split(" ", n=1).str[0]

    def isolate_data_by_date(self, date):
        """Isolate the data for a specific date.

        This method extracts the rows that contain data for the specified date.

        Parameters:
            date (str): A date string in the format 'YYYY-MM-DD'.
        """
        self.extract_order_dates()
        self.commissions = self.commissions[self.commissions["date"] == date]
        self.orders = self.orders[self.orders["date"] == date]
        order_ids_for_date = self.orders["id"]
        self.order_lines = self.order_lines[
            self.order_lines["order_id"].isin(order_ids_for_date)
        ]
