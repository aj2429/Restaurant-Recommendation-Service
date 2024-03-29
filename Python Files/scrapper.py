import httplib
import urllib
import base64
import json
import boto3
import decimal
import csv
import time

headers = {
    'Authorization': 'Bearer BearerToken'
}

#client = boto3.client('dynamodb')

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('yelp-restaurant')

CustomCuisine = 'french'

print "came here"

def fetchData():
	try:
		with open('File_data.csv', "a") as csvfile:
			mywriter = csv.writer(csvfile)

			conn = httplib.HTTPSConnection("api.yelp.com")
			for i in range(0,1000,20):
				url = "/v3/businesses/search?limit=20&offset="+ str(i+1) +"&categories="+ CustomCuisine +"&location=NYC"
	
				conn.request("GET", url, headers=headers)
				response = conn.getresponse()
				data = response.read()
				data = json.loads(data.decode("utf-8"))
				restaurant_data = data["businesses"]
            	
				for restaurants in restaurant_data:
					#print restaurants
					Restaurantid = restaurants['id']
					Cuisine = restaurants['categories']
					Rating = decimal.Decimal(restaurants['rating'])
					NumberofReviews = restaurants['review_count']
					Name = restaurants['name']
					Location = restaurants['location']['address1']
					Coordinates = restaurants['coordinates']	
					#print Name, Coordinates
                			
					if Location == "" or Location == None:
						Location = "N/A"		
		
					#Push the record in the database
					response = table.put_item(
               	 				Item={
		                    		"restaurantId": Restaurantid,
	                		    	"Name" : Name,
					    	"Rating": Rating,
               		 		    	"Cuisine":CustomCuisine,
			  			"Reviews": NumberofReviews,
        				        "Location" : Location,
						"insertedAtTime" : decimal.Decimal(time.time())
						#"Coordinates" : Coordinates
					})
	
					dataList = [CustomCuisine, NumberofReviews, Rating, Restaurantid]
					mywriter.writerow(dataList)			
			
			conn.close()
			
	except Exception as e:
      	  	print e

	

fetchData()
