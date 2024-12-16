"""
Name: Theingi Myint
Class : T03
UOW ID:9097971

"""

import csv

class ResaleTransaction:
    """
    Represents a single resale transaction for an HDB flat.

    Attributes:
        __month (str): The month of the transaction.
        __town (str): The town where the flat is located.
        __flat_type (str): The type of flat (e.g., '4 ROOM').
        __block (str): The block number of the flat.
        __street_name (str): The street name of the flat.
        __storey_range (str): The range of storeys for the flat.
        __floor_area (float): The floor area of the flat in square meters.
        __flat_model (str): The model of the flat (e.g., 'Improved').
        __lease_commence_date (str): The year the lease commenced.
        __remaining_lease (str): The remaining lease of the flat.
        __resale_price (float): The resale price of the flat.

    Properties:
        town (str): Returns the town of the flat.
        flat_type (str): Returns the type of the flat.
        flat_model (str): Returns the model of the flat.
        price_psf (float): Calculates and returns the price per square foot (PSF).
    """
    def __init__(self, month, town, flat_type, block, street_name, storey_range, floor_area, flat_model, lease_commence_date, remaining_lease, resale_price, **kwargs):
        self.__month = month
        self.__town = town
        self.__flat_type = flat_type
        self.__block = block
        self.__street_name = street_name
        self.__storey_range = storey_range
        self.__floor_area = float(floor_area)
        self.__flat_model = flat_model
        self.__lease_commence_date = lease_commence_date
        self.__remaining_lease = remaining_lease
        self.__resale_price = float(resale_price)

    @property
    def town(self):
        return self.__town

    @property
    def flat_type(self):
        return self.__flat_type

    @property
    def flat_model(self):
        return self.__flat_model

    @property
    def price_psf(self):
        return self.__resale_price / self.__floor_area


class HDB_Resale_Admin:
    """
    Administer and manage a collection of HDB resale transactions.

    Attributes:
        _resale2024 (str): Log file for errors encountered while loading data.
        __resales (list): A list of ResaleTransaction objects.

    Methods:
        load(file_path):
            Loads HDB resale data from a CSV file.

        get_town():
            Returns a list of distinct towns in the dataset.

        get_flat_type():
            Returns a list of distinct flat types in the dataset.

        get_flat_model():
            Returns a list of distinct flat models in the dataset.

        search(town=None, flat_type=None, flat_model=None, price_psf=None):
            Searches for resale transactions based on given conditions.

        print_search_results(results):
            Prints the search results in a formatted output.
    """
    _resale2024 = "resale2024_log.txt"

    def __init__(self):
        """
        Initializes the HDB_Resale_Admin class with an empty resale transaction list.
        """
        self.__resales = []

    def load(self, file_path):
        """
        Loads the HDB resale data from a CSV file and logs any errors.

        Args:
            file_path (str): The path to the CSV file containing resale data.

        Raises:
            Exception: Logs errors if any required fields are missing or data conversion fails.
        """
        with open(self._resale2024, "w") as log_file:
            with open(file_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    try:
                        self.__resales.append(
                            ResaleTransaction(
                                month=row.get("month", ""),  # Handle optional fields
                                town=row["town"],
                                flat_type=row["flat_type"],
                                block=row["block"],
                                street_name=row["street_name"],
                                storey_range=row["storey_range"],
                                floor_area=row["floor_area_sqm"],
                                flat_model=row["flat_model"],
                                lease_commence_date=row["lease_commence_date"],
                                remaining_lease=row["remaining_lease"],
                                resale_price=row["resale_price"]
                            )
                        )
                    except Exception as e:
                        log_file.write(f"Error in row {row}: {e}\n")

    def get_town(self):
        """
        Returns a list of distinct towns in the dataset.

        Returns:
            list: A list of unique town names.
        """
        towns = []
        for resale in self.__resales:
            if resale.town not in towns:
                towns.append(resale.town)
        return towns

    def get_flat_type(self):
        """
        Returns a list of distinct flat types in the dataset.

        Returns:
            list: A list of unique flat types.
        """
        flat_types = []
        for resale in self.__resales:
            if resale.flat_type not in flat_types:
                flat_types.append(resale.flat_type)
        return flat_types

    def get_flat_model(self):
        """
        Returns a list of distinct flat models in the dataset.

        Returns:
            list: A list of unique flat models.
        """
        flat_models = []
        for resale in self.__resales:
            if resale.flat_model not in flat_models:
                flat_models.append(resale.flat_model)
        return flat_models

    def search(self, town=None, flat_type=None, flat_model=None, price_psf=None):
        """
        Searches for resale transactions based on given criteria.

        Args:
            town (str or list, optional): The town(s) to filter by.
            flat_type (str or list, optional): The flat type(s) to filter by.
            flat_model (str or list, optional): The flat model(s) to filter by.
            price_psf (float, optional): The minimum price per square foot.

        Returns:
            list: A list of matching ResaleTransaction objects, up to a maximum of 30.
        """
        results = self.__resales

        if town:
            if isinstance(town, str):
                town = [town]
            results = [resale for resale in results if resale.town in town]

        if flat_type:
            if isinstance(flat_type, str):
                flat_type = [flat_type]
            results = [resale for resale in results if resale.flat_type in flat_type]

        if flat_model:
            if isinstance(flat_model, str):
                flat_model = [flat_model]
            results = [resale for resale in results if resale.flat_model in flat_model]

        if price_psf is not None:
            results = [resale for resale in results if resale.price_psf >= price_psf]

        results = [resale for resale in results if resale.price_psf >= 0]
        return results[:30]

    def print_search_results(self, results):
        """
        Prints the search results in a formatted output.

        Args:
            results (list): A list of ResaleTransaction objects.
        """
        for result in results:
            print(f"Town: {result.town}, Flat Type: {result.flat_type}, Flat Model: {result.flat_model},  Price PSF: {result.price_psf:.2f}")


# Example usage
file_path = "resale2024.csv"  # Path to CSV file
admin = HDB_Resale_Admin()
admin.load(file_path)

# Search using all 4 parameters
search_results_4_params = admin.search(town=["YISHUN", "ANG MO KIO"], flat_type=["5 ROOM"], flat_model=["IMPROVED", "DBSS"], price_psf=2500)
print("\nSearch using all 4 parameters: ")
admin.print_search_results(search_results_4_params)

# Search using any 3 parameters
search_results_3_params = admin.search(town=["BISHAN"], flat_type=["4 ROOM"], flat_model=["NEW GENERATION", "STANDARD"])
print("\nSearch using any 3 parameters:")
admin.print_search_results(search_results_3_params)

# Search using any 2 parameters
search_results_2_params = admin.search(town=["ANG MO KIO"], flat_type=["EXECUTIVE"])
print("\nSearch using any 2 parameters:")
admin.print_search_results(search_results_2_params)

# Search using 1 parameter
search_results_1_param = admin.search(town=["BEDOK"])
print("\nSearch using 1 parameter:")
admin.print_search_results(search_results_1_param)
