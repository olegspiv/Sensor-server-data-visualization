# Sensor Server Data Visualization & Logging

## Overview
This Python application is an **enhanced version** of the real-time plotting example from the **[SensorServer project](https://github.com/umer0586/SensorServer/wiki/Real-Time-Plot-Example-(-Python))**. It extends the original project by introducing new features, including:

✅ **Support for multiple sensors** – Easily add and switch between any number of sensors.  
✅ **Dynamic sensor switching** – Switch between different sensors without restarting the application.  
✅ **Efficient data logging** – Save sensor data to CSV files without affecting real-time visualization.  

## Features
- **Connects to SensorServer via WebSocket** to receive real-time sensor data.
- **Supports multiple sensor types**, including:
  - Accelerometer
  - Gyroscope
  - Magnetometer
- **Live plotting with PyQtGraph**, ensuring smooth visualization.
- **Buffered data writing to CSV** to prevent performance issues.
- **Interactive GUI** with a button to switch sensors dynamically.

## Installation
### Prerequisites
Ensure you have the required dependencies installed:
```bash
pip install pyqt5 pyqtgraph websocket-client
```

### Running the Script
1. **Start SensorServer** on your Android device.
2. **Note the WebSocket address** (e.g., `ws://192.168.x.x:8080`).
3. **Modify the script** if needed to match your WebSocket address:
   ```python
   ADDRESS = "Your-Device-Address:8080"
   ```
4. **Run the script:**
   ```bash
   python read_from_sensor.py
   ```

## Usage
- The GUI automatically starts visualizing data from the **default sensor**.
- Click the **"Switch Sensor"** button to cycle through available sensors.
- The script logs data into **separate CSV files** for each sensor, e.g.,:
  - `android.sensor.accelerometer_data.csv`
  - `android.sensor.gyroscope_data.csv`
  - `android.sensor.magnetic_field_data.csv`

## Customization
- **Add more sensors** by modifying the `SensorType` enumeration in the script:
  ```python
  class SensorType(Enum):
      ACCELEROMETER = "android.sensor.accelerometer"
      GYROSCOPE = "android.sensor.gyroscope"
      MAGNETOMETER = "android.sensor.magnetic_field"
      LIGHT_SENSOR = "android.sensor.light"  # Example of adding a new sensor
  ```
- **Change the plotting settings** (update interval, colors, etc.).
- **Modify CSV buffer size** by changing `BUFFER_SIZE` in the script:
  ```python
  BUFFER_SIZE = 100  # Adjust for performance
  ```

## Troubleshooting
### WebSocket Connection Issues
- Ensure **your phone and computer are on the same Wi-Fi network**.
- Check the **correct WebSocket address** from SensorServer.
- If connection fails, disable the **firewall** or add a rule to allow WebSocket traffic.

### Performance Issues
- If the GUI lags, try **reducing the update rate** or **increasing `BUFFER_SIZE`**.
- Ensure **no other application is overloading the network**.

## License
This project is an expansion of [SensorServer’s Real-Time Plot Example](https://github.com/umer0586/SensorServer/wiki/Real-Time-Plot-Example-(-Python)) and follows the original license.

## Acknowledgments
- **SensorServer Project** – for providing the foundation.
- **PyQt & PyQtGraph** – for real-time visualization.

🚀 Happy coding!

