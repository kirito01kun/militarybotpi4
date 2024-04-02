import argparse
import traceback
import time
import pigpio
from nrf24 import *

def receive_nrf(hostname='localhost', port=8888, address='1SNSR'):
    # Create NRF24 object.
    pi = pigpio.pi(hostname, port)
    nrf = NRF24(pi, ce=17, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.MIN)
    nrf.set_address_bytes(len(address))

    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)
    
    # Enter a loop receiving data on the address specified.
    try:
        count = 0
        while True:
            # As long as data is ready for processing, process it.
            while nrf.data_ready():
                # Read pipe and payload for message.
                pipe = nrf.data_pipe()
                payload = nrf.get_payload().decode()

                # Show message received as hex.
                print(payload)
                
            # Sleep 100 ms.
            time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()

