# CLIMATE_DATA_GEN
This library is a hardware library intended to simulate climatic data. Currently provides atmospheric pressure data, humidity data and wind speed data.

## HOW TO USE

* To install:

```sh
pip install -i https://test.pipy.org/simple climateDataGen
```
* Testing

```sh
python import climateDataGen
```
### NOTE:

If python throws a 'ModuleNotFoundError',run
```sh
pip show climateDataGen
```
then copy the Location path,then append this to python sys.path

* Usage

Run
```sh
import climateDataGen.climate_data_generator as cl
```
* Example

To generate random climatic data:
```sh
import climateDataGen.climate_data_generator as cl
humidity = cl.humidity_data()
print(x)

