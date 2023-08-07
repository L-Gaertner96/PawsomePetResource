from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.category_model import Category  # Import Category from the model module

@app.route('/home')
def homepage():
    return render_template('homepage.html')

@app.route('/<category>')
def animal_pick(category):
    selected_category = Category.get_category_by_name(category)
    print(type(selected_category))  
    
    if selected_category:
        subcategories = Category.get_subcategories_by_category_id(selected_category.id)
        return render_template('subcats.html', category=selected_category, subcategories=subcategories)
    else:
        return "Category not found", 404
    
@app.route('/<category>/<subcategory>')
def subcategory_page(category, subcategory):
    selected_category = Category.get_category_by_name(category)
    
    if selected_category:
        subcategories = Category.get_subcategories_by_category_id(selected_category.id)
        selected_subcategory = None
        
        # Find the selected subcategory object
        for subcat in subcategories:
            if subcat.subcat_name == subcategory:
                selected_subcategory = subcat
                break
        
        if selected_subcategory:
            return render_template('threads.html', category=selected_category, subcategory=selected_subcategory)
        else:
            return "Subcategory not found", 404
    else:
        return "Category not found", 404
