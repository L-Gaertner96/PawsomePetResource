from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.category_model import Category
from flask_app.models.post_model import Post
from flask_app.models.user_model import User
from flask_app.models.subcat_model import Subcategory 
from flask_app.models.comment_model import Comment

@app.route('/home')
def homepage():
    return render_template('homepage.html')

@app.route('/<category>')
def animal_pick(category):
    selected_category = Category.get_category_by_name(category) 
    
    if selected_category:
        subcategories = Category.get_subcategories_by_category_id(selected_category.id)
        return render_template('subcats.html', category=selected_category, subcategories=subcategories)
    else:
        return "Category not found", 404
    
@app.route('/<category>/<subcategory>/', methods=['GET'])
def view_subcategory(category, subcategory):
    # Get category ID by category name
    category_obj = Category.get_category_by_name(category)


    if category_obj:
        category_id = category_obj.id
    else:
        flash("Category not found.", "error")
        return redirect("/home")

    # Get subcategory ID by category ID and subcategory name
    subcategory_obj = Subcategory.get_subcat_by_name(category_id, subcategory)
    if subcategory_obj:
        subcategory_id = subcategory_obj.id
    else:
        flash("Subcategory not found.", "error")
        return redirect("/home")

    threads = Post.get_threads_by_subcategory(subcategory_id)
    return render_template('threads.html', threads=threads, category=category_obj, subcategory=subcategory_obj)

    
@app.route('/<category>/<subcategory>/new_thread', methods=['GET'])
def new_post_form(category, subcategory):
    return render_template('newpost.html', category=category, subcategory=subcategory)

@app.route('/<category>/<subcategory>/create_post', methods=['POST'])
def create_post(category, subcategory):
    # Get the form data from the request
    form_data = request.form

    # Create a new post using the Post model
    Post.create_new_post(form_data, category, subcategory)

    # Redirect to the post list page
    return redirect("/home")

@app.route('/<category>/<subcategory>/<int:post_id>', methods=['GET'])
def view_one(category, subcategory, post_id):
    post = Post.get_post_by_id(post_id)
    if post:
        return render_template('viewthread.html', post=post, category=category, subcategory=subcategory)
    else:
        flash("Post not found.", "error")
        return redirect("/home")
    
@app.route('/<category>/<subcategory>/<int:post>/new_comment', methods=['POST'])
def create_comment(category, subcategory, post):
    # Get the user ID from the session
    print("Session contents:", session)
    print("Session user_id:", session.get('user_id'))
    # Make sure the user is logged in

    # Get the comment body from the form data
    content = request.form.get('content')
    user_id = session.get('user_id')

    # Create a new comment
    Comment.create_new_comment({'content': content, 'user_id': user_id}, post)

    flash("Comment added successfully.", "success")
    return redirect(url_for('view_one', category=category, subcategory=subcategory, post_id=post))

