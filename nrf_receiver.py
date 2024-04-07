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
    nrf.open_writing_pipe(address)
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
                
                # Send a response back to the sender
                response = "temp=37"  # Example response
                nrf.reset_packages_lost()
                nrf.send(response.encode())
                nrf.wait_until_sent()

                if nrf.get_packages_lost() == 0:
                    print(f"Response sent: {response}")
                else:
                    print("Error sending response")

            # Sleep 100 ms.
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Transmission interrupted.")
    except Exception as e:
        traceback.print_exc()
    finally:
        nrf.power_down()
        pi.stop()

if __name__ == "__main__":
    receive_nrf()

