## ECommerceComparison

Used Django rest framework for backend with sqlite as database.

**Note:** I have generated random data and used them to do the mentioned operations.

## APIs
### Generate Data API
http://127.0.0.1:8000/api/generate_data/
### Create/View Companies
http://127.0.0.1:8000/api/company/
### Get Products with search
- http://127.0.0.1:8000/api/products/?search=phone
- http://127.0.0.1:8000/api/products/?search=watch
- http://127.0.0.1:8000/api/products/?search=shirt
- http://127.0.0.1:8000/api/products/?search=headset
### Get products with search and sort
- http://127.0.0.1:8000/api/products/?search=phone&sort=lowest_price
- http://127.0.0.1:8000/api/products/?search=phone&sort=highest_rating
### Get products of specific companies along with search and sort
- http://127.0.0.1:8000/api/products/?search=phone&sort=highest_price&company=Amazon,Flipkart
