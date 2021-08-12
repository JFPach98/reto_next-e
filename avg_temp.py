import pandas as pd
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('weather')

response = table.scan()
items = response['Items']

df = pd.DataFrame(items)
cols = df.columns.tolist()
cols = cols[1:] + cols[:-4]
df1 = df[cols]

df1['time'] = pd.to_datetime(df1['time'])
df1["temperature"] = pd.to_numeric(df1["temperature"], downcast="float")
df1["feels_like"] = pd.to_numeric(df1["feels_like"], downcast="float")
df1["pressure"] = pd.to_numeric(df1["pressure"], downcast="float")
df1["humidity"] = pd.to_numeric(df1["humidity"], downcast="float")

print("The first register is "+ str(df1['time'].min()) + ", the last register is " + str(df1['time'].max()))

start = input("Type a starting date: ")
end = input("Type an ending date: ")

query = df1[(df1['time'] > start) & (df1['time'] <= end)]
avg = query['temperature'].mean()

print("The average temperature during those two dates is: " + str(avg))