import requests
import json
from kafka import KafkaProducer
import time
import datetime
from datetime import datetime

kafka_topic= "traffic_nairobi"
kafka_server= "localhost:9092"

#initialise kafka producer
producer= KafkaProducer(
    bootstrap_servers=[kafka_server],
    value_serializer= lambda v: json.dumps(v).encode('utf-8')
)

#fetching data from google maps API
api_key= 'AIzaSyAkHjjutiMqSBLZZ9sg8ohU4_L0txVovCw'

#Nairobi coordinates (KICC is our origin address)
Nairobi_lat= -1.2887
Nairobi_lng= 36.8233

#nairobi roads
destinations= [
    "Waiyaki Way, Nairobi",
    "Uhuru Highway, Nairobi",
    "Mombasa Road, Nairobi",
    "Mbagathi Road, Nairobi",
    "Langata Road, Nairobi",
    "Ngong Road, Nairobi",
    "Jogoo Road, Nairobi",
    "Kenyatta Avenue, Nairobi",
    "Uhuru Highway, Nairobi",
    "Moi Avenue, Nairobi",
    "Haile Selassie Avenue, Nairobi",
    "university Way, Nairobi",
    "Tom Mboya Street, Nairobi"
]

# Convert the list of roads to a string with pipes separating the locations
destinations_str = "|".join(destinations)

data_file= "appends.json"
def get_traffic_data():

    #fetch data from api
    url= f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={Nairobi_lat},{Nairobi_lng}&destinations={destinations_str}&departure_time=now&key={api_key}'
    response= requests.get(url)

    #check if its successful
    if response.status_code == 200:
        traffic_data= response.json()
        timestamp=datetime.now().isoformat() #adding current timestamp

        #restructure the data from api to make it more readable
        results=[]
        for i, destination in enumerate(destinations):

            #each destination data is in the element section of json file
            element= traffic_data["rows"][0]["elements"][i]

            #organising the data
            road_info={
                "origin":"KICC, Mairobi",
                "destination": destination,
                "distance_text": element["distance"]["text"],
                "distance_value": element["distance"]["value"],
                "duration_text": element["duration"]["text"],
                "duration_value": element["duration"]["value"],
                "duration_in_traffic_text": element.get("duration_in_traffic", {}).get("text", "N/A"),
                "duration_in_traffic_value": element.get("duration_in_traffic", {}).get("value", "N/A"),
                "congestion_level": calculate_congestion(element),
                "timestamp": timestamp
            }
            results.append(road_info)
       
        #save the data into a json file
        with open(data_file, 'w') as traffic_file:
            json.dump(results, traffic_file, indent=4)

        print(f'Data saved successfully')
        return results
    else:
        print(f'Unable to fetch data due to Error:', response.status_code)
        return None
    

def calculate_congestion(element):
    """Calculate congestion level based on duration with and without traffic."""
    try:
        normal_duration = element["duration"]["value"]
        traffic_duration = element["duration_in_traffic"]["value"]

        # Congestion level: Higher value means worse congestion
        congestion_level = (traffic_duration - normal_duration) / normal_duration
        return round(congestion_level, 2)  # Rounded to 2 decimal places
    except KeyError:
        return "N/A"  # If duration_in_traffic is not available

#  #fecth the data   
# traffic_data= get_traffic_data()

# #print the data
# if traffic_data:
#     print(f"Traffic current data successfully added to json file")

#message to kafka
# while True:
traffic_data = get_traffic_data ()
if traffic_data:
    producer.send('traffic_nairobi', traffic_data)
    print(f"Traffic data sent to Kafka")
        # time.sleep (30) #time between sending data

# Close the producer
producer.flush()  # Ensure data is sent before closing
producer.close()