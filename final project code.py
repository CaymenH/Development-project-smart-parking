# importing libaries 
import RPi.GPIO as GPIO
from time import sleep
import time
from datetime import datetime as dt
from sqlalchemy import(Column, ForeignKey, Integer, String, Unicode, DateTime, Double, Float)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import asyncio
from azure.iot.device import  ProvisioningDeviceClient, IoTHubDeviceClient, Message 
from constant import scope_ID, device_ID, Primary_Key, PROVISIONING_HOST
import json
import logging
#import picamera2
from picamera2 import Picamera2, Preview
import base64
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()


# Use the BCM pin numbering scheme
GPIO.setmode(GPIO.BCM)


# seting gpio pin number 
RED_LED_PIN = 26
GREEN_LED_PIN = 24
GPIO_TRIGGER = 16
GPIO_ECHO = 25
MAGNET_PIN = 17

# setup of pins
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(MAGNET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class Base(DeclarativeBase):
    pass

class ParkingBay(Base):
    __tablename__ = 'parking_bay'
    id = Column(Integer, primary_key=True, index=True)
    number_bay = Column(Integer, nullable=False, default=1)
    bay_status = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    distance = Column(Float, nullable=True)
    magnet = Column(Integer, nullable=True)

    def __init__(self, bay_status, distance, magnet, timestamp):
        self.number_bay = 1
        self.bay_status = bay_status
        self.distance = distance
        self.magnet = magnet
        self.timestamp = timestamp
# database set up
engine = create_engine('sqlite:///parking.db', echo = True)
Session = sessionmaker(bind = engine)
session = Session()
Base.metadata.create_all(engine)


saved_status = "start"
def send_to_iot_central(status,distance,magnet, carimage1):
    try:
        #provision client for iot central
        provisioning_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host=PROVISIONING_HOST,
            registration_id=device_ID,      
            id_scope=scope_ID,                
            symmetric_key=Primary_Key
        )
        
        registration_result = provisioning_client.register()

        if registration_result.status == "assigned":
            device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=Primary_Key,
                hostname=registration_result.registration_state.assigned_hub,
                device_id=device_ID
            )

            
            telemetry_data = {
                "bay_status":status,
                "distance_cm": 0.0 if distance is None else float(distance),
                "magnet":int(magnet),
                "carimage": carimage1
                }
            device_client.connect()
            message = Message(json.dumps(telemetry_data))
            device_client.send_message(message)
            device_client.disconnect()
    except Exception as e:
        print(f"azure failed: {e}")


def distance():
    

    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.05)

    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001) 

    GPIO.output(GPIO_TRIGGER, False) 

    start_time = time.time()
    timeout = start_time + 0.1

    stop_time = time.time()


    # when the pin of triggered start the time
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
        if time.time() > timeout: 
          return None

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
        if time.time() > timeout: 
          return None

    # calulating the time
    time_elapsed = stop_time - start_time
    
    #calulating the distance 
    distance = (time_elapsed * 34300) / 2

    # if the distance is greater than 400 or less than 5 do triggers
    if distance > 25 or distance < 5:
        # refers to the main loop than defines distance is none
        return None

    return distance

# --- Main Test Loop ---
def main():
    global saved_status
    
    print("ultrasonic sensor is running")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            # reads sensors and added slight delay
            time.sleep(0.1)
            dist = distance()
            magnet = GPIO.input(MAGNET_PIN)
            bay_status = ""
            timestamp = dt.now()
            # result when ultrasonic and magnet are both detected
            if dist is not None and magnet == GPIO.LOW:
                print(f" {dist:.2f} cm")
                GPIO.output(RED_LED_PIN, GPIO.HIGH)
                GPIO.output(GREEN_LED_PIN, GPIO.LOW)
                bay_status= ("bay 1 occupied")
                print("red led on")
            # result when ultrasonic and magnet are not detected
            elif dist is None and magnet == GPIO.HIGH:
                bay_status = ("bay 1 vacant")
                GPIO.output(RED_LED_PIN, GPIO.LOW)
                GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
                print("green led on")
            # result when magnet is detected and ultrasonic isnt
            elif dist is None and magnet == GPIO.LOW:
                bay_status = ("ultrasonic not detecting")
                GPIO.output(RED_LED_PIN, GPIO.LOW)
                GPIO.output(GREEN_LED_PIN, GPIO.LOW)

            else:
                # when ultrasonic is detected and magnet isnt
                bay_status = ("magnetic not detecting")
                GPIO.output(RED_LED_PIN, GPIO.LOW)
                GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    # saves a record in the database if i car comes, goes or a sensor breaks
            if bay_status != saved_status:
                record = ParkingBay(
                    
                    bay_status=bay_status,
                    distance=dist,
                    magnet=magnet,
                    timestamp= dt.now()
                )
                session.add(record)
                session.commit()

                
                frame = picam2.capture_array()
                carimage = base64.b64encode(frame).decode('utf-8')

                send_to_iot_central(bay_status, dist, magnet, carimage)


                # saves bay status
                saved_status = bay_status
    except KeyboardInterrupt:
        print(" code stopped by user Cleaning up GPIO...")
    finally:
        session.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
