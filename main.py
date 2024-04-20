import time
import threading
from combined_flask import app
from nrf_receiver import receive_nrf

if __name__ == "__main__":
    flask_thread = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000})
    flask_thread.start()

    # Start NRF receiver
    nrf_thread = threading.Thread(target=receive_nrf)
    nrf_thread.start()

    while True:
        #received_messages = receive_nrf()  # Get received messages
        #for message in received_messages:
        #    print("Received message:", message)

        #print("Doing other calculations while Flask server and NRF receiver are running...")
        time.sleep(1)

