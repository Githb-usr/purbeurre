# ORIGIN #
This project is an exercise done as part of an OpenClassrooms training course for developers in the Python language.
It corresponds to project 8 of the training.

# GOAL OF THE APPLICATION #
This application makes it possible to choose a food for which one wishes to obtain a better quality substitute, in order to improve one's diet. It's based on the Open Food Facts database. It's a free and collaborative database referencing food products from all over the world.

The Open Food Facts website (FR): https://fr.openfoodfacts.org/

# FEATURES #
* Display of the search field on the home page.
* The search must not be done in AJAX.
* Responsive interface.
* User authentication: account creation by entering an email and a password, without the possibility to change the password for the moment.
* The user can see a detailed sheet of each product using a button.
* From the detailed description of a product, he/she can access the complete description on the Open Food facts website.
* He/She can delete a favourite.

# USER PATH #
The application is online. The user can search for a product to be relocated directly from the homepage.
1. He/She is looking for a product to replace
2. He/She selects the product among those that correspond to his/her search
3. He/She selects the product he/she wants in order to discover the substitutes that are proposed to him/her for this product (From this step he must be connected to his/her account).
4. He/She selects a substitute to save it in his/her favourites.

# CONSTRAINTS #
* The project must include tests.
* The project use a PostgreSql database and not MySQL in order to deploy the application on Heroku.
* The project include a "Legal Notice" page which will contain the contact details of the host as well as the authors of the different free resources used (template, photos, icons, ...).
* The project should follow PEP 8 best practice.
* Code written entirely in English: functions, variables, comments, etc.
* Use an agile project methodology to work in project mode.

# DEPLOYMENT #
* PostGreSQL must be installed on the server, with "unaccent" extension.
* Create a "purbeurre" database and a user with password
* Creating a virtual environment with Python 3.8
* Clone the application
* Run the following command to install the necessary libraries : pip install -r requirements.txt
* Create an .env file with these environment variables (replace the xxx with your values):
  DJANGO_SETTINGS_MODULE=config.settings
  SECRET_KEY=xxx
  DB_NAME=xxx
  DB_USER=xxx
  DB_PASSWORD=xxx
  DB_HOST=xxx
  DB_PORT=xxx
* Generate the static files: [python3] manage.py collectstatic
* Create the database tables: [python3] manage.py migrate
* Populating the database: [python3] manage.py import_data

# EXAMPLE OF JSON RESPONSE FROM OPEN FOOD FACTS API #
JSON can contain several results but only the first one is shown in the examples

Example URL : Search for products by popularity

https://fr.openfoodfacts.org/cgi/search.pl?action=process&json=true&page_size=1&page=1&sort_by=unique_scans_n

Excerpt from the JSON response (otherwise there are several hundred lines for a single product) :  

```json
{
    "count": 817313,
    "page": 1,
    "page_count": 24,
    "page_size": 24,
    "products": [
        {
            "brands": "Cristaline",
            "categories": "Băuturi, en:Waters, en:Spring waters, en:Mineral waters, en:Natural mineral waters",
            "code": "3274080005003",
            "image_url": "https://static.openfoodfacts.org/images/products/327/408/000/5003/front_fr.626.400.jpg",
            "nutrient_levels": {
                "fat": "low",
                "salt": "low",
                "saturated-fat": "low",
                "sugars": "low"
            },
            "nutriments": {
                "fat": 0,
                "fat_100g": 0,
                "fat_serving": 0,
                "fat_unit": "g",
                "fat_value": 0,
                "magnesium": 0.026,
                "magnesium_100g": 0.026,
                "magnesium_label": "Magnésium",
                "magnesium_serving": 0.26,
                "magnesium_unit": "mg",
                "magnesium_value": 26,
                "proteins": 0,
                "proteins_100g": 0,
                "proteins_serving": 0,
                "proteins_unit": "g",
                "proteins_value": 0,
                "salt": 0,
                "salt_100g": 0,
                "salt_serving": 0,
                "salt_unit": "g",
                "salt_value": 0,
                "saturated-fat": 0,
                "saturated-fat_100g": 0,
                "saturated-fat_serving": 0,
                "saturated-fat_unit": "g",
                "saturated-fat_value": 0,
                "sugars": 0,
                "sugars_100g": 0,
                "sugars_serving": 0,
                "sugars_unit": "g",
                "sugars_value": 0,
            },
            "nutriscore_grade": "a",
            "product_name": "Cristaline",
            "stores": "Carrefour,Leclerc,Auchan",
            "url": "https://fr.openfoodfacts.org/produit/3274080005003/cristaline-eau-de-source"
        },
    ]
}
```
