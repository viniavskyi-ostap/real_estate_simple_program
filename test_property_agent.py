from property_classes import Agent


# test agent

if __name__ == '__main__':

    agent = Agent()

    for i in range(2):
        # add property for rent
        print('Fill in property for rent:')
        agent.add_property()
    # print sum of rental prices for both
    print('Rental sum: ', agent.calculate_rental_prices_sum())

    for i in range(2):
        # add house property
        print('Fill in house property:')
        agent.add_property()
    # print number of houses with garage
    print('Houses with garage num.: ', agent.count_houses_with_garage())

    agent.display_properties()