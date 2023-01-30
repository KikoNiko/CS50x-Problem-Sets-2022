# Foodster Plans
#### [Video Demo](https://youtu.be/C-sA-XkcIHc)
#### Description:
Foodster Plans is a web application where the user can save food items in an inventory, take notes, search for recipes, save recipes and check their nutritional value.

In the Home page there is "My Food Inventory" which is a table where you can perform CRUD operations. Then there is a note taking feature made with JavaScript, where the user can take notes or create grocery lists... Basicaly they can use it as they choose. It will store the data in LocalStorage so they don't disappear on page reload. The notes can be removed one by one or all at once.

Then there is the Recipes page. It contains a Search bar and a random food joke provided by Spoonacular Api. Here the user can search for recipes based on ingredients they have, keywords, or the recipe name itself. Then we get a list of recipes displayed as "recipe cards" for a simple clean look. When the user clicks on 'More info' button they access a page with the recipes image, a summary of the recipe, the recipe providor, Cooking time and how many servings it is for. There are also two buttons one for viewing the full recipe which will take you to the recipe webpage and another for saving the recipe. If you click on 'Add to Favourites' the recipe will be saved in the database as one of the current user's recipes. Then it takes you to the next page which is called 'Favourites'.

In the Favorites page there is a table with all the recipes the user has saved. They can check the full recipe info and if they click on 'Nutrients' a modal will pop-up containing a nutrition widget provided by Spoonacular Api with Nutritional Facts about the recipe per serving. There is and X button on each recipe so it can be deleted from the table and the database.

If a user is logged in there is a Logout button on the navbar. If user is not logged in there are Sign Up and Login buttons on the navbar.


_The project is made using Python with Flask framework, SQLAlchemy for database operations, JavaScript, HTML, CSS, Bootstrap for the front-end._

**All information about the recipes is provided by _Spoonacular API_**


#### Key Features:
- **Registration And Login System.** With basic authentication.
- **Food Inventory Management System.** Basic CRUD operations table with database.
- **Recipe search.** Search for recipes based on ingredients, keywords or the recipe name itself.
- **Save recipes and get nutritional data.** When user adds a recipe to favourites they will be able to access that recipe's nutritional facts.

#### In-Depth:
The file app.py is where the application is created and run

Then in the webapp folder are the main project files.

There is a __init__.py to initialize the Flask application and create the database.

The auth.py file is where all the user sign up and login features are implemented. I am using Flask-Login for some user management features and werkzeug.security for encrypting the passwords.

I made a models.py file where the database tables are created and initialized. I am using Flask-SQLAlchemy.

The main.py is the main python file where all the main functions and routes are. For convenience and simplicity I am using some imports like Blueprint, render_template, request, redirect, url_for, flash.

I am keeping all the html files in a templates folder. I use Jinja to use python code in my html and to help html templating. In the static folder I keep the .css and .js files. The app uses some bootstrap but also some clean css styling.
