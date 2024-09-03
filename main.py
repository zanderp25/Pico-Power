import machine, network, time
import uasyncio as asyncio
import ujson as json
from config import SSID, PASSWORD

# Pin setup
IN_BUTTON = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)
OUT_BUTTON = machine.Pin(2, machine.Pin.OUT)
IN_LED = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
OUT_LED = machine.Pin(0, machine.Pin.OUT)

OUT_BUTTON.on() # Turn off button because it's active low

pwm = machine.PWM(OUT_LED)
pwm.freq(1000)  # Set PWM frequency to 1kHz

# Global state
power_state = 'off'
server = None

# Network setup
network = network.WLAN(network.STA_IF)
network.active(True)
network.connect(SSID, PASSWORD)

async def fade_led():
    # print('Fading LED...')
    global power_state
    while True:
        if power_state == 'sleeping':
            # Fade in
            for duty in range(1024, 49152, 64):
                pwm.duty_u16(duty)
                await asyncio.sleep_ms(5)
                if power_state != 'sleeping': break
            # Fade out
            for duty in range(49152, 1024, -64):
                pwm.duty_u16(duty)
                await asyncio.sleep_ms(5)
                if power_state != 'sleeping': break
        elif power_state == 'on':
            pwm.duty_u16(65535)
        else:
            pwm.duty_u16(0)
        await asyncio.sleep(0.2)

async def monitor_button():
    # print('Monitoring button...')
    while True:
        if IN_BUTTON.value() == 0:  # Button is pressed (active low)
            while IN_BUTTON.value() == 0:
                OUT_BUTTON.off() # active low
                await asyncio.sleep(0.1)
            OUT_BUTTON.on()
        await asyncio.sleep(0.1)

async def monitor_led():
    # print('Monitoring LED...')
    global power_state
    last_state = -1
    last_time = time.ticks_ms()
    while True:
        current_state = not IN_LED.value() # Active low
        if current_state != last_state:  # LED state changed
            current_time = time.ticks_ms()
            elapsed_time = time.ticks_diff(current_time, last_time)
            if 500 <= elapsed_time <= 750:
                power_state = 'sleeping'
            else:
                power_state = 'on' if current_state == 1 else 'off'
            last_time = current_time
            last_state = current_state
            print('Power state:', power_state, '| LED:', current_state, '| Elapsed ms:', elapsed_time)
        elif power_state is not 'sleeping' or time.ticks_diff(time.ticks_ms(), last_time) > 750:
            power_state = 'on' if current_state == 1 else 'off'
        await asyncio.sleep(0.1)

async def handle_client(reader, writer):
    print('Client connected')
    request = await reader.read(1024)
    request = request.decode('utf-8')
    print('Request:', request)

    # Handle different requests
    if request.startswith('GET / '):
        response = 'HTTP/1.0 200 OK\n\nHello World!'
    elif request.startswith('GET /status'):
        response = f"HTTP/1.0 200 OK\n\n{json.dumps({'power': power_state})}"
    elif request.startswith('GET /toggle'):
        OUT_BUTTON.off() # active low
        await asyncio.sleep(0.1)
        OUT_BUTTON.on()
        response = "HTTP/1.0 200 OK\n\n{'result': 'power toggled'}"
    else:
        response = 'HTTP/1.0 404 Not Found\n\nNot Found'
    
    print('Response:', response)
    await writer.awrite(response)
    await writer.aclose()
    print('Client disconnected')

async def main():
    global server

    server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
    addr = network.ifconfig()[0]
    print('Server started on', addr)
    
    # Start tasks
    await asyncio.gather(
        monitor_button(),
        monitor_led(),
        fade_led(),
    )

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
finally:
    if server:
        print('Stopping server...')
        server.close()
        asyncio.run(server.wait_closed())
        asyncio.new_event_loop()
    pwm.deinit()
    OUT_LED.off()
    OUT_BUTTON.on()
    print('Stopped')
