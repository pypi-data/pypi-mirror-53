Example:

```python
from xzqhotspot import manager
m = manager()

# start mobile hotspot
# returns TetheringOperationStatus, for details, refer to the table below
result=m.start_hotspot()

# stop mobile hotspot
# returns TetheringOperationStatus, for details, refer to the table below
result=m.stop_hotspot()

# get current status instantly
# 0 for Unknown, 1 for On, 2 for Off, 3 for Transition between On and Off
s = m.hotspot_status()

# test Internet connectivity
# True for connected, False otherwise
flag = is_internet_available()

# get connected network ssid
ssid = get_wifi_ssid()

# keyword is a part of network adpater name
# in order to identify specific network adpater
disable_network_adapter(keyword)
enable_network_adapter(keyword)
```

| Result                     | Value | Description                                                  |
| -------------------------- | ----- | ------------------------------------------------------------ |
| BluetoothDeviceOff         | 7     | The operation could not begin because Bluetooth or a required Bluetooth device is turned off. |
| EntitlementCheckFailure    | 5     | The operation did not complete because the account does not currently support tethering operations. |
| EntitlementCheckTimeout    | 4     | The operation did not complete because the mobile operator could not be contacted to confirm tethering capabilities are provided for this account. |
| MobileBroadbandDeviceOff   | 2     | The operation could not begin because the mobile broadband device is turned off. |
| NetworkLimitedConnectivity | 8     | The operation did not complete because of limited network connectivity. |
| OperationInProgress        | 6     | The operation is still in progress.                          |
| Success                    | 0     | The operation completed successfully.                        |
| Unknown                    | 1     | The status of the operation is unknown.                      |
| WiFiDeviceOff              | 3     | The operation could not begin because the Wifi device is turned off. |