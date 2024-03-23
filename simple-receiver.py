import argparse
from datetime import datetime
import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *


if __name__ == "__main__":

    print("Python NRF24 Simple Receiver Example.")
    # Parse command line argument.
    parser = argparse.ArgumentParser(prog="simple-receiver.py", description="Simple NRF24 Receiver Example.")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
    parser.add_argument('address', type=str, nargs='?', default='1SNSR', help="Address to listen to (3 to 5 ASCII characters)")

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    address = args.address
    
    # Create NRF24 object.
    pi = pigpio.pi(hostname, port)
    nrf = NRF24(pi, ce=17, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.MIN)
    nrf.set_address_bytes(len(address))

    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)
    

    # Enter a loop receiving data on the address specified.
    try:
        print(f'Receive from {address}')
        count = 0
        while True:

            # As long as data is ready for processing, process it.
            while nrf.data_ready():
                # Count message and record time of reception.            
                count += 1
                now = datetime.now()
                
                # Read pipe and payload for message.
                pipe = nrf.data_pipe()
                payload = nrf.get_payload().decode()

                # Show message received as hex.
                print(f"{now:%Y-%m-%d %H:%M:%S.%f}, load:{payload} , count: {count}")

                
            # Sleep 100 ms.
            time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()
