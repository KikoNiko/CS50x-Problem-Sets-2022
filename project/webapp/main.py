from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
import requests
from . import db
from .models import FoodItems, Recipes

main = Blueprint("main", __name__)

api_key = "02f0f5fef8a54a34a3c9fc26ed5c78b7"

@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    items = current_user.foods
    return render_template("home.html", items=items, user=current_user)


@main.route("/add-items", methods=['GET', 'POST'])
def add_items():
    if request.method == 'POST':
        fname = request.form['fname']
        category = request.form['category']
        units = request.form['units']
        quantity = request.form['quantity']

        # Check if item exists in the database
        # exists = db.session.query(FoodItems.id).filter_by(fname=fname).first() is not None

        #if exists:
            #flash("Item already exist. Try 'Edit' to update information", category='error')
            #return redirect(url_for("main.home"))

        # If item doesn't exist in db check if all fields are filled
        #else:
        if not request.form.get('fname'):
            flash("Excuse me, what did you want to add? ('hint': the name is missing) :] ", category='error')
            return redirect(url_for("main.home"))

        elif not request.form.get('quantity'):
            flash("Hmm... Looks like you didn't set the quantity :)", category='error')
            return redirect(url_for("main.home"))
            
        elif not request.form.get('category'):
            flash("Hmm... What about the category? :)) ", category='error')
            return redirect(url_for("main.home"))

        # If everything is correctly inputed add item to database
        else:
            data = FoodItems(fname=fname, category=category, units=units, quantity=quantity, owner=current_user.id)
            db.session.add(data)
            db.session.commit()

            flash("Woohoo! Item Added! :) ", category='success')
            return redirect(url_for("main.home"))



@main.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = FoodItems.query.get(request.form.get('id'))
        data.fname = request.form['fname']
        data.quantity = request.form['quantity']
        data.units = request.form['units']
        data.category = request.form['category']

        db.session.commit()
        flash("Item Updated!", category='success')
        return redirect(url_for("main.home"))



@main.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    item = FoodItems.query.get(id)
    db.session.delete(item)
    db.session.commit()

    flash("Item Deleted!", category='success')
    return redirect(url_for("main.home"))



def search_recipes(query):
    # Contact API
    try:
        response = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?number=30&query={query}&apiKey={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        recipe = response.json()
        return {
            "recipes": recipe["results"]
        }
    except (KeyError, TypeError, ValueError):
        return None



def get_recipe_info(id):
    # Contact API
    try:
        response = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?includeNutrition=true&apiKey={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        recipe = response.json()
        return {
            "recipe": recipe
        }
    except (KeyError, TypeError, ValueError):
        return None



@main.route("/recipes", methods=['GET', 'POST'])
@login_required
def recipes():
    if request.method == 'POST':
        query = request.form.get("recipes")
        response = search_recipes(query)
        if response == None:
            return render_template("recipes.html", user=current_user)
        else:
            recipes = response["recipes"]
            return render_template("recipes.html", recipes=recipes, user=current_user)

    #add jokes
    random_joke = "https://api.spoonacular.com/food/jokes/random?&apiKey=02f0f5fef8a54a34a3c9fc26ed5c78b7"
    joke_response = str(requests.request("GET", random_joke).json()['text'])

    return render_template("recipes.html", joke=joke_response, user=current_user)



@main.route("/recipeinfo", methods=['GET', 'POST'])
@login_required
def recipe_info():
    if request.method == 'POST':
        id = request.form.get("recid")
        recipe = get_recipe_info(id)

        if recipe == None:
            return redirect("/recipes")
        else:
            return render_template("recipeinfo.html", recipe=recipe["recipe"], user=current_user)



@main.route("/favourites", methods=['GET', 'POST'])
@login_required
def favourites():
    if request.method == 'POST':
        id = request.form.get("recipeid")
        recipe = get_recipe_info(id)

        try:
            recipe_info = f"https://api.spoonacular.com/recipes/{id}/information?includeNutrition=false&apiKey={api_key}"
        except requests.RequestException:
            return None
            

        uri = str(requests.request("GET", recipe_info).json()['id'])
        title = str(requests.request("GET", recipe_info).json()['title'])
        url = str(requests.request("GET", recipe_info).json()['sourceUrl'])
        
        rec = Recipes(uri=uri, title=title, url=url, owner=current_user.id)

        db.session.add(rec)
        db.session.commit()
        flash("Recipe added!")

        return render_template("favourites.html", recipe=recipe["recipe"], user=current_user)  
    
    favs = current_user.recipes
    return render_template("favourites.html", favs=favs, user=current_user)
    
    # random_trivia = "https://api.spoonacular.com/food/trivia/random?&apiKey=02f0f5fef8a54a34a3c9fc26ed5c78b7"
    # trivia = str(requests.request("GET", random_trivia).json()['text'])
    # return render_template('favourites.html', trivia=trivia, user=current_user)
    #return redirect(url_for("main.home"))
    
    
@main.route('/delete-rec/<id>', methods=['GET', 'POST'])
def delete_rec(id):
    rec = Recipes.query.get(id)
    db.session.delete(rec)
    db.session.commit()

    flash("Recipe Deleted!", category='success')
    return redirect(url_for("main.favourites"))
    



    