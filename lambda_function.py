import boto3, requests, json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

table_name = 'weather'

api_key = "44ddcd172064f45d3c25066cf35f80e8"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = "Monterrey,MX"
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    response = requests.get(complete_url)

    x = response.json()

    now = datetime.now() 

    register = x["main"]
    register["time"] = now.strftime("%d/%m/%Y %H:%M:%S")
    table.put_item(
        Item={
            'time': register['time'],
            'temperature': str(register['temp']),
            'pressure': str(register['pressure']),
            'humidity': str(register['humidity']),
            'feels_like': str(register['feels_like'])
            
        }
        )
    print('Success')
    return{
        'statusCode': 200,
        'body': 'Item added'
    }