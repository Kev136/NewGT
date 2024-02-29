import random
import time


def generate_cost(climate_type):
    if climate_type == "Climate Friendly":
        carbon_emission = 0
        cost = random.randint(2, 10)
    elif climate_type == "Balanced Climate":
        carbon_emission = 1.5
        cost = random.uniform(0.7, 6)
    elif climate_type == "Price Worthy":
        carbon_emission = 3
        cost = random.uniform(0.1, 1.3)
    else:
        print("Invalid climate type")
        return None


def update_program():
    climate_types = ["Climate Friendly", "Balanced Climate", "Price Worthy"]

    while True:
        for climate_type in climate_types:
            result = generate_cost(climate_type)
            if result:
                print(result)

        # Delay for 5 seconds before the next update
        time.sleep(5)


# Run the program
update_program()
