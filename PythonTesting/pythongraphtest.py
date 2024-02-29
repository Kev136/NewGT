import random
import time
import matplotlib.pyplot as plt


def generate_cost(climate_type):
    if climate_type == "Climate Friendly":
        carbon_emission = 0
        cost = random.randint(2, 6)
    elif climate_type == "Balanced Climate":
        carbon_emission = 1.5
        cost = random.uniform(0.7, 4)
    elif climate_type == "Price Worthy":
        carbon_emission = 3
        cost = random.uniform(0.1, 1.3)
    else:
        print("Invalid climate type")
        return None

    return carbon_emission, cost


def update_program(iterations):
    climate_types = ["Climate Friendly", "Balanced Climate", "Price Worthy"]

    # Lists to store data for plotting
    carbon_emissions = {
        "Climate Friendly": [],
        "Balanced Climate": [],
        "Price Worthy": [],
    }
    costs = {"Climate Friendly": [], "Balanced Climate": [], "Price Worthy": []}

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()

    for _ in range(iterations):
        for climate_type in climate_types:
            carbon_emission, cost = generate_cost(climate_type)
            print(
                f"_____________________________________\n{climate_type}: {carbon_emission}g CE kWh\nCost: {cost}\n_____________________________________"
            )

            # Store data for plotting
            carbon_emissions[climate_type].append(carbon_emission)
            costs[climate_type].append(cost)

            # Plotting
            ax.clear()  # Clear previous plot
            for c_type in climate_types:
                if carbon_emissions[c_type]:  # Check if the list is not empty
                    ax.plot(
                        costs[c_type],
                        label=f"{c_type} - {carbon_emissions[c_type][0]}g CE kWh",
                    )
                else:
                    ax.plot(costs[c_type], label=f"{c_type}")

            # Calculate average for the best carbon emission
            best_cost = float("inf")
            best_climate_type = ""
            for c_type in carbon_emissions:
                if carbon_emissions[c_type] and costs[c_type]:
                    current_cost = costs[c_type][-1]
                    if current_cost < best_cost:
                        best_cost = current_cost
                        best_climate_type = c_type

            # Calculate average across all climate types
            avg_all_cost = sum([sum(costs[c_type]) for c_type in climate_types]) / sum(
                len(costs[c_type]) for c_type in climate_types
            )
            ax.text(
                1,
                0.95,
                f"Avg Cost (All): {avg_all_cost}",
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
            )

            if best_climate_type:
                avg_cost = sum(costs[best_climate_type]) / len(costs[best_climate_type])
                ax.text(
                    1,
                    1,
                    f"Avg Cost ({best_climate_type}): {avg_cost}",
                    transform=ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
                )

            ax.set_xlabel("Iterations")
            ax.set_ylabel("Cost")
            ax.legend()
            plt.pause(0.1)  # Pause to allow the plot to update

        # Delay for 1 second before the next update
        time.sleep(1)

    plt.ioff()  # Turn off interactive mode after the loop


# Run the program for a specified number of iterations
update_program(30)
