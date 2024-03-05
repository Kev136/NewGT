import random
import time
from datetime import datetime
from threading import Thread, Lock
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize locks for thread-safe operations on global variables
cost_lock = Lock()

# Global variables with initial values
cost1 = 6
cost2 = 3
cost3 = 0.3

climate_types = ["Climate Friendly", "Balanced Climate", "Price Worthy"]
cost_data_dict = {climate_type: [] for climate_type in climate_types}

# Global list with initial value
cost_data_1 = [6]
cost_data_2 = [3]
cost_data_3 = [0.3]

# cost1 = 6
# cost2 = 3
# cost3 = 0.3

cost_data = [cost_data_1, cost_data_2, cost_data_3]

# Idea min max factor
# Weight factor
d1 = {"environment": 0.1, "cost": 0.9}
d2 = {"environment": 0.5, "cost": 0.5}
d3 = {"environment": 0.9, "cost": 0.1}

list_of_dicts = [d1, d2, d3]


# jämförelse
f1 = d1["environment"] ** 2 + d1["cost"] ** 2
f2 = d2["environment"] ** 2 + d2["cost"] ** 2
f3 = d3["environment"] ** 2 + d3["cost"] ** 2

# List of Factors for comparison (custom made)
list_of_factors = [f1, f2, f3]
fc_env = 0.4
fc_price = 0.6
fc = fc_env**2 + fc_price**2
diffs = []
for f in list_of_factors:
    diffs.append(abs(f - fc))

min_index = min(enumerate(diffs), key=lambda x: x[1])[0]

print(min_index)

min_id = min_index


def generate_cost(climate_type):
    global cost1, cost2, cost3, cost_data_1
    with cost_lock:
        temp_cost1 = cost1 + random.uniform(-0.2, 0.2)
        temp_cost2 = cost2 + random.uniform(-0.26, 0.26)
        temp_cost3 = cost3 + random.uniform(-0.13, 0.13)

        cost1 = temp_cost1 if temp_cost1 > 0 else cost1
        cost2 = temp_cost2 if temp_cost2 > 0 else cost2
        cost3 = temp_cost3 if temp_cost3 > 0 else cost3

        cost_data_1.append(cost1)

        climateValues = {
            "Climate Friendly": cost1,
            "Balanced Climate": cost2,
            "Price Worthy": cost3,
        }
        return climateValues[climate_type]

# def generate_cost(climate_type):
#     global cost1, cost2, cost3
#     with cost_lock:
#         temp_cost1 = cost1 + random.uniform(-0.2, 0.2)
#         temp_cost2 = cost2 + random.uniform(-0.26, 0.26)
#         temp_cost3 = cost3 + random.uniform(-0.13, 0.13)

#         cost1 = temp_cost1 if temp_cost1 > 0 else cost1
#         cost2 = temp_cost2 if temp_cost2 > 0 else cost2
#         cost3 = temp_cost3 if temp_cost3 > 0 else cost3

#         climateValues = {
#             "Climate Friendly": cost1,
#             "Balanced Climate": cost2,
#             "Price Worthy": cost3,
#         }
#         return climateValues[climate_type]


def get_data_values():
    global min_id
    while True:
        try:
            # for climate_type in climate_types:
            climate_type = climate_types[min_id]
            result = generate_cost(climate_type)
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with cost_lock:
                cost_data_dict[climate_type].append([time_str, result])
                # Ensure the list does not grow indefinitely
                if len(cost_data_dict[climate_type]) > 60:
                    cost_data_dict[climate_type].pop(0)

            socketio.emit(
                "cost_update",
                {"climate_type": climate_type, "cost": result, "time": time_str},
            )
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred in get_data_values: {e}")
    # while True:
    #         try:
    #             for climate_type in climate_types:
    #                 result = generate_cost(climate_type)
    #                 time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #                 with cost_lock:
    #                     cost_data_dict[climate_type].append([time_str, result])
    #                     # Ensure the list does not grow indefinitely
    #                     if len(cost_data_dict[climate_type]) > 60:
    #                         cost_data_dict[climate_type].pop(0)

    #                 socketio.emit(
    #                     "cost_update",
    #                     {"climate_type": climate_type, "cost": result, "time": time_str},
    #                 )
    #             time.sleep(5)
    #         except Exception as e:
    #             print(f"An error occurred in get_data_values: {e}")


# @app.route("/")
# def home():
#     return "Real-time Cost Data Visualization"


@app.route("/")
def home():
    return render_template("index.html")

# @app.route('/update_cost_data', methods=['POST'])
# def update_cost_data():
#     percentage = int(request.json['percentage'])
#     percentage /= 100
#     fc_price = 1 - percentage
#     round(fc_price)
#     fc_env = 1 - fc_price
    
#     # round the values
#     # Make sure they always add up to 1 even after rounding
    
#     print("environment", fc_env)
#     print("price", fc_price)
    
#     # Do whatever you need to do with the percentage value
#     return jsonify({'message': 'Received percentage: {}'.format(percentage)}), 200

@app.route('/update_cost_data', methods=['POST'])
def update_cost_data():
    percentage = int(request.json['percentage'])
    percentage /= 100
    fc_price = 1 - percentage
    round(fc_price)
    fc_env = 1 - fc_price
    
    # Emit an event to update the graph with fc_env and fc_price
    socketio.emit('update_graph', {'fc_env': fc_env, 'fc_price': fc_price})
    
    # Do whatever you need to do with the percentage value
    return jsonify({'message': 'Received percentage: {}'.format(percentage)}), 200

# @app.route("/temp")
# def temp():
#     cost_avg = sum(cost_data_1) / len(cost_data_1)
#     return render_template("temp.html", cost_avg=cost_avg)


@app.route("/cost_data", methods=["GET"])
def cost_data():
    return jsonify(cost_data_dict)


@socketio.on("get_cost_data")
def send_cost_data():
    emit("cost_data", cost_data_dict)


if __name__ == "__main__":
    data_thread = Thread(target=get_data_values)
    data_thread.start()
    socketio.run(app, debug=True)
