from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.category_model import Category  # Import Category from the model module

@app.route('/home')
def homepage():
    return render_template('homepage.html')

@app.route('/<category>')
def animal_pick(category):
    selected_category = Category.get_category_by_name(category)
    print(type(selected_category))  # Add this line to check the type of selected_category
    
    if selected_category:
        subcategories = Category.get_subcategories_by_category_id(selected_category.id)
        return render_template('subcats.html', category=selected_category, subcategories=subcategories)
    else:
        return "Category not found", 404
