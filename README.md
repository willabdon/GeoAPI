# Django GeoAPI

## Kickstart

1. Start dev server without building it

   ```
   $ make start
   ```

1. Access the backend container (while running it)

   ```
   $ make ssh-backend
   ```

1. Access the database container (while running it)
   ```
   $ make ssh-db
   ```

Explanation: This project should have API endpoints to create, update, delete, and retreive information about providers. A provider should contain the following information:

- Name
- Email
- Phone Number
- Language
- Currency

Once a provider is created it should be able to start defining service areas. These service areas will be geojson polygons. There should be endpoints to create, update, delete, and get a polygon. A polygon should contain a name and price as well as the geojson information.

API endpoint should take a lat/lng pair as arguments and return a list of all polygons that include the given lat/lng. The name of the polygon, provider's name, and price should be returned for each polygon. This operation should be FAST.

Stack:

- Django
- PostgreSQL / Postgis

Requirements:

- Docker
- Docker Compose
- Python

# API

 You can verify the API running in a EC2 instace here: http://18.228.199.200/