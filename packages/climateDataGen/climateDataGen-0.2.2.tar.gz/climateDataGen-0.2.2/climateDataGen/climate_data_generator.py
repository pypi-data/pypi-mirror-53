import random
import math
import matplotlib.pyplot as plt

humidity_values = []
wind_speed_values = []
pressure_values = []


def humidity_data(count):
    for i in range(0, count):
        relative_humidity = random.randrange(55.0, 77.0)
        dew_point = (100 - relative_humidity) / 5
        temperature = random.randrange(15.0, 42.0)
        humidity = 100.00 * ((611 * math.exp(5423 * ((1 / 273)) - (1 / (dew_point + 273)))
                              ) / (611 * math.exp(5423 * ((1 / 273) - (1 / temperature)))))
        humidity_values.append(humidity)
    return humidity_values


def wind_speed_data(count):
    for i in range(0, count):
        longitude = random.randrange(98.0, 102.0)
        wind_speed = 0.0001 * longitude
        wind_speed_values.append(wind_speed)
    return wind_speed_values


def pressure_data(count):

    for i in range(0, count):
        temperature = random.randrange(15.0, 42.0)
        pressure = 101325 * math.exp(((0.00 - 9.81) * 0.0289644 * (200)) /
                                     (8.31444598 * (temperature + 273)))
        pressure_values.append(pressure)
    return pressure_values


def makeFig(timer, climate_data, argument):
    plt.title('Simulated climate data over time')
    plt.grid(True)
    plt.ylabel(argument)
    plt.plot(timer, climate_data)
    plt.show()


def data_visualization(argument):
    timer = []
    if(argument == 'pressure'):
        data = pressure_values
    if(argument == 'humidity'):
        data = humidity_values
    if(argument == 'wind_speed'):
        data = wind_speed_values
    for i in range(0, len(data)):
        timer.append(5 * i)

    makeFig(timer, data, argument)

