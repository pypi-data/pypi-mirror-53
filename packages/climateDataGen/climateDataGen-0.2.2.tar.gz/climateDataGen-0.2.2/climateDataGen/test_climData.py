import climate_data_generator as cl
def test_windspeed():
    test_wind_speed_values=[]
    for i in range(0, 10):
        test_wind_speed_values = cl.wind_speed_data(10)
        print(test_wind_speed_values[i])
        assert(test_wind_speed_values[i]<=0.0102 and test_wind_speed_values[i]>=0.0098)


