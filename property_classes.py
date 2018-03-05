class Property:
    def __init__(self, square_feet='', beds='', baths='', **kwargs):
        """
        initialize property object
        :param square_feet: area of property
        :param beds: number of beds in property
        :param baths: number of bathroom in property
        :param kwargs: other key-word arguments that might be passed
        """
        super().__init__(**kwargs)
        self.square_feet = square_feet
        self.num_bedrooms = beds
        self.num_baths = baths

    def display(self):
        print("PROPERTY DETAILS")
        print("================")
        print("square footage: {}".format(self.square_feet))
        print("bedrooms: {}".format(self.num_bedrooms))
        print("bathrooms: {}".format(self.num_baths))
        print()

    def prompt_init():
        """
        :return: dictionary of prompted parameters
        """
        return dict(square_feet=input("Enter the square feet: "),
                    beds=input("Enter number of bedrooms: "),
                    baths=input("Enter number of baths: "))

    prompt_init = staticmethod(prompt_init)


def get_valid_input(input_string, valid_options):
    """
    :param input_string: string to print on input
    :param valid_options: options for correct input
    :return: one of valid options selected by user
    """
    input_string += " ({}) ".format(", ".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response


class Apartment(Property):
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")

    def __init__(self, balcony='', laundry='', **kwargs):
        """
        :param balcony: type of balcony of apartment
        :param laundry: type of laundry of apartment
        :param kwargs: argument passed to Property __init__
        """
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry

    def display(self):
        """
        Display information about apartment
        """
        super().display()
        print("APARTMENT DETAILS")
        print("laundry: %s" % self.laundry)
        print("has balcony: %s" % self.balcony)

    def prompt_init():
        """
        :return: dictionary of prompted parameters for apartment
        """
        parent_init = Property.prompt_init()
        laundry = get_valid_input("What laundry facilities does "
                                  "the property have? ",
                                  Apartment.valid_laundries)
        balcony = get_valid_input("Does the property have a balcony? ",
                                  Apartment.valid_balconies)
        parent_init.update({
            "laundry": laundry,
            "balcony": balcony
        })
        return parent_init
    prompt_init = staticmethod(prompt_init)


class House(Property):

    valid_garage = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")

    def __init__(self, num_stories='', garage='', fenced='', **kwargs):
        """
        :param num_stories: number of floors in the house
        :param garage: bool value of garage presence
        :param fenced: bool value of fence presence
        :param kwargs: other parameters passed
        """
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced = fenced
        self.num_stories = num_stories

    def display(self):
        """
        display information about house
        """
        super().display()
        print("HOUSE DETAILS")
        print("# of stories: {}".format(self.num_stories))
        print("garage: {}".format(self.garage))
        print("fenced yard: {}".format(self.fenced))

    def prompt_init():
        """
        :return: dictionary of prompted parameters for house
        """
        parent_init = Property.prompt_init()
        fenced = get_valid_input("Is the yard fenced? ", House.valid_fenced)
        garage = get_valid_input("Is there a garage? ", House.valid_garage)
        num_stories = input("How many stories? ")
        parent_init.update({
            "fenced": fenced,
            "garage": garage,
            "num_stories": num_stories
        })
        return parent_init
    prompt_init = staticmethod(prompt_init)


class Purchase:
    def __init__(self, price='', taxes='', **kwargs):
        """
        :param price: price of purchase
        :param taxes: taxes for purchase
        :param kwargs: other kw arguments that will be passed further
        """
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes

    def display(self):
        """
        Display info about purchase
        """
        super().display()
        print("PURCHASE DETAILS")
        print("selling price: {}".format(self.price))
        print("estimated taxes: {}".format(self.taxes))

    def prompt_init():
        """
        :return: dictionary of prompted parameters for purchase
        """
        return dict(
                price=input("What is the selling price? "),
                taxes=input("What are the estimated taxes? "))
    prompt_init = staticmethod(prompt_init)


class Rental:

    def __init__(self, furnished='', utilities='', rent='', **kwargs):
        """
        :param furnished: bool value of property being furnished
        :param utilities: utilities of the property
        :param rent: rental payment for property
        :param kwargs: other kw arguments that will be passed further
        """
        super().__init__(**kwargs)
        self.furnished = furnished
        self.rent = rent
        self.utilities = utilities

    def display(self):
        """
        display info about rent
        """
        print("RENTAL DETAILS")
        print("rent: {}".format(self.rent))
        print("estimated utilities: {}".format(
            self.utilities))
        print("furnished: {}".format(self.furnished))

    def prompt_init():
        return dict(
            rent=input("What is the monthly rent? "),
            utilities=input(
                "What are the estimated utilities? "),
            furnished=get_valid_input(
                "Is the property furnished? ",
                ("yes", "no")))

    prompt_init = staticmethod(prompt_init)


class HouseRental(Rental, House):

    def prompt_init():
        """
        :return: dictionary of values for rental of specific house
        """
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class ApartmentRental(Rental, Apartment):

    def prompt_init():
        """
        :return: dictionary of values for rental of specific apartment
        """
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class ApartmentPurchase(Purchase, Apartment):

    def prompt_init():
        """
        :return: dictionary of values for purchase of specific apartment
        """
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class HousePurchase(Purchase, House):

    def prompt_init():
        """
        :return: dictionary of values for purchase of specific house
        """
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class Agent:

    type_map = {
        ("house", "rental"): HouseRental,
        ("house", "purchase"): HousePurchase,
        ("apartment", "rental"): ApartmentRental,
        ("apartment", "purchase"): ApartmentPurchase
    }

    def __init__(self):
        """
        Initialize new agent
        """
        self.property_list = []

    def display_properties(self):
        """
        display information about all property that agent manages
        """
        for property in self.property_list:
            property.display()

    def add_property(self):
        """
        Method that allows to add new property
        """
        property_type = get_valid_input(
            "What type of property? ",
            ("house", "apartment")).lower()

        payment_type = get_valid_input(
            "What payment type? ",
            ("purchase", "rental")).lower()

        PropertyClass = self.type_map[(property_type, payment_type)]
        print("Debugging init_args")
        init_args = PropertyClass.prompt_init()
        print(init_args)
        self.property_list.append(PropertyClass(**init_args))

    def calculate_purchase_prices_sum(self):
        """
        :return: sum of prices of all property for sale
        """
        price_sum = 0
        for property in self.property_list:
            if issubclass(type(property), Purchase):
                try:
                    price_sum += int(property.price)
                except ValueError:
                    continue
        return price_sum

    def calculate_rental_prices_sum(self):
        """
        :return: sum of rental prices of all property for rent
        """
        rental_sum = 0
        for property in self.property_list:
            if issubclass(type(property), Rental):
                try:
                    rental_sum += int(property.rent)
                except ValueError:
                    continue
        return rental_sum

    def count_houses_with_garage(self):
        """
        :return: number of hauses with garage
        """
        number = 0
        for property in self.property_list:
            if issubclass(type(property), House):
                if property.garage != 'none':
                    number += 1
        return number

