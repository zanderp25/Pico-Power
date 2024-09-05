# Raspberry Pi Pico W Remote Power Button with Web Server

This project implements a remote power button using a Raspberry Pi Pico W, allowing users to control a computer's power state via a web interface. The project also monitors the computer's LED state to reflect it on the Pico W, supporting features like sleep mode detection and LED fading.

The Raspberry Pi Pico is meant to be connected to the power button and LED pins of a computer's motherboard, allowing for remote control and monitoring of the computer's power state. The Pico W runs a web server that provides a user interface to toggle the power state of the connected computer and view real-time status updates.

## Features

- Remote power button functionality via a web interface.
- LED state monitoring and control with PWM fading for sleep mode.
- Web server running on Raspberry Pi Pico W.
- Real-time status updates of the computer's power state.
- Supports pass-through functionality for the physical power button.

## Components

- Raspberry Pi Pico W
- Connected GPIO pins for the power button and LED control
- Wi-Fi connection for remote access

## Prerequisites

- [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/)
- MicroPython installed on the Pico W
- A computer or device to remotely control the Pico W

## Setup

1. **Flash MicroPython**: Ensure your Raspberry Pi Pico W is flashed with MicroPython. Follow the official [MicroPython documentation](https://micropython.org/download/rp2-pico-w/) if needed.

2. **Clone or Download the Repository**:
    ```bash
    git clone https://github.com/yourusername/pico-w-power-button.git
    cd pico-w-power-button
    ```

3. **Upload the Code**:
    - Use a tool like [Thonny](https://thonny.org/) or [rshell](https://github.com/dhylands/rshell) to upload the files to your Pico W.
    - Alternatively, use the [MicroPico VSCode extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) to upload the files.

4. **Configure Wi-Fi**:
    - Update the `config.py` file with your Wi-Fi SSID and password:
    ```python
    SSID = "your_wifi_ssid"
    PASSWORD = "your_wifi_password"
    ```
    Note: The Raspberry Pi Pico W can only connect to 2.4GHz Wi-Fi networks.

5. **Connect Hardware**:
    - Connect the Raspberry Pi Pico W to the power button pins and LED of your motherboard as described in the project files.

## Usage

1. **Power On the Pico W**:
   - Connect the Raspberry Pi Pico W to power via USB.

2. **Connect to the Web Interface**:
   - Once the Pico W connects to your Wi-Fi network, it will print its IP address.
   - Open a browser and go to `http://<Pico_W_IP_Address>/` to access the web interface.

3. **Control the Power Button**:
   - Use the web interface to toggle the power state of the connected computer.

4. **Monitor LED State**:
   - The Pico W will reflect the current state of the computer's LED, including fading during sleep mode.

## Troubleshooting

- **Server Not Responding**: Ensure the Pico W is connected to the correct Wi-Fi network and that the IP address is correct.
- **Button Not Working**: Double-check the GPIO connections to ensure proper wiring between the Pico W and the computer.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you have any ideas for improvements or encounter any problems.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.