from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys
import websocket
import json
import threading
import csv
import os
from enum import Enum

x_data = []
y_data = []
z_data = []
time_data = []

x_data_color = "#d32f2f"  # red
y_data_color = "#7cb342"  # green
z_data_color = "#0288d1"  # blue

background_color = "#fafafa"  # white

BUFFER_SIZE = 100  # Adjust this value to change how often data is written
ADDRESS = "Your-Device-Address:8080"

data_buffer = []
buffer_lock = threading.Lock()


class SensorType(Enum):
    ACCELEROMETER = "android.sensor.accelerometer"
    GYROSCOPE = "android.sensor.gyroscope"
    MAGNETOMETER = "android.sensor.magnetic_field"


class Sensor:
    def __init__(self, address, sensor_type):
        self.address = address
        self.sensor_type = sensor_type
        self.csv_file = f"{sensor_type}_data.csv"
        self.ws = None  # Store the WebSocket object
        self.init_csv()

    def init_csv(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "X", "Y", "Z"])

    def append_to_buffer(self, timestamp, x, y, z):
        global data_buffer

        with buffer_lock:
            data_buffer.append([timestamp, x, y, z])

        if len(data_buffer) >= BUFFER_SIZE:
            self.flush_buffer_to_csv()

    def flush_buffer_to_csv(self):
        global data_buffer

        with buffer_lock:
            if not data_buffer:
                return  # No data to write

            with open(self.csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data_buffer)

            data_buffer = []  # Clear buffer after writing

    def on_message(self, ws, message):
        data = json.loads(message)
        values = data["values"]
        timestamp = float(data["timestamp"]) / 1000000

        x_data.append(values[0])
        y_data.append(values[1])
        z_data.append(values[2])
        time_data.append(timestamp)

        # Save to buffer instead of writing immediately
        self.append_to_buffer(timestamp, values[0], values[1], values[2])

    def on_error(self, ws, error):
        print("Error occurred:", error)

    def on_close(self, ws, close_code, reason):
        print("Connection closed:", close_code, reason)

    def on_open(self, ws):
        print(f"Connected to: {self.address}")
        self.ws = ws  # Save WebSocket instance

    def stop(self):
        if self.ws:
            self.ws.close()
            self.ws = None  # Reset WebSocket instance

    def make_websocket_connection(self):
        ws = websocket.WebSocketApp(
            f"ws://{self.address}/sensor/connect?type={self.sensor_type}",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        ws.run_forever()

    def connect(self):
        thread = threading.Thread(target=self.make_websocket_connection)
        thread.start()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.sensor_types = list(SensorType)
        self.current_sensor = self.sensor_types[0]
        self.sensor = Sensor(address=ADDRESS, sensor_type=self.current_sensor.value)
        self.sensor.connect()

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QtWidgets.QVBoxLayout()
        self.centralWidget.setLayout(layout)

        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)
        self.graphWidget.setBackground(background_color)
        self.update_plot_title()

        styles = {"color": "#f00", "font-size": "15px"}
        self.graphWidget.setLabel("left", "m/s^2", **styles)
        self.graphWidget.setLabel("bottom", "Time (milliseconds)", **styles)
        self.graphWidget.addLegend()

        self.x_data_line = self.graphWidget.plot([], [], name="x", pen=pg.mkPen(color=x_data_color))
        self.y_data_line = self.graphWidget.plot([], [], name="y", pen=pg.mkPen(color=y_data_color))
        self.z_data_line = self.graphWidget.plot([], [], name="z", pen=pg.mkPen(color=z_data_color))

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.switch_button = QtWidgets.QPushButton("Switch Sensor")
        self.switch_button.clicked.connect(self.switch_sensor)
        layout.addWidget(self.switch_button)

    def update_plot_title(self):
        self.graphWidget.setTitle(f"{self.current_sensor}", color="#8d6e63", size="20pt")

    def update_plot_data(self):
        limit = -1000
        self.x_data_line.setData(time_data[limit:], x_data[limit:])
        self.y_data_line.setData(time_data[limit:], y_data[limit:])
        self.z_data_line.setData(time_data[limit:], z_data[limit:])

    def switch_sensor(self):
        # Stop previous sensor connection
        if self.sensor:
            self.sensor.stop()

        # Clear existing data to avoid distortion
        global x_data, y_data, z_data, time_data
        x_data.clear()
        y_data.clear()
        z_data.clear()
        time_data.clear()

        # Switch to the next sensor
        self.current_sensor = self.sensor_types[
            (self.sensor_types.index(self.current_sensor) + 1) % len(self.sensor_types)]

        # Create a new sensor instance and connect
        self.sensor = Sensor(address=ADDRESS, sensor_type=self.current_sensor.value)
        self.sensor.connect()

        # Update the plot title
        self.update_plot_title()

        # Reset the plot data
        self.x_data_line.setData([], [])
        self.y_data_line.setData([], [])
        self.z_data_line.setData([], [])


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
