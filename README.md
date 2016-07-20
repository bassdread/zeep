# Zeep
Library to extract data from serial and send it various services.

# Supported Services
Services and things Zeep can send data to.

## Dweet https://dweet.io
Ridiculously simple messaging (and alerts) for the Internet of Things.

## IO https://io.adafruit.com/
Open beta of a simple to use graphing platform.

## Text File
A simple file in ```/tmp``` with a string of JSON.


# Setup
The below will get you going.
```
git clone git@github.com:bassdread/zeep.git
cd zeep
[sudo] pip install virtualenv
virtualenv .
source bin/activate

python src/zeep/collector.py
```

Assuming that works you will need to configure services.

# Configuring Third Party Services

```
cp src/zeep/settings/__init__.py.example src/zeep/settings/__init__.py


# populate the fields with the third party settings and uncomment the services you want
$EDITOR src/zeep/settings/__init__.py

```