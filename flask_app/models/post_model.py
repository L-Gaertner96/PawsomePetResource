from flask import session
from flask_app import connectToMySQL
from flask_app.models.user_model import User
from flask_app.models.subcat_model import Subcategory


class Post:
    DB = 'pawsome_forum'

    def __init__(self, id, subcategories_id, form_data):
        self.id = id
        self.subcategories_id = subcategories_id
        self.title = form_data['title']
        self.body = form_data['body']
        self.users_id = form_data['user_id']

    @classmethod
    def create_new_post(cls, form_data, category, subcategory):
        # Find the id of the desired subcategory
        query = """
            SELECT subcategories.id
            FROM subcategories
            JOIN categories ON subcategories.categories_id = categories.id
            WHERE categories.category_name = %(category)s AND subcategories.subcat_name = %(subcategory)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, {'category': category, 'subcategory': subcategory})
        print(result)
        
        if result:
            subcategory_id = result[0]['id']  # Access the first dictionary in the list and get the 'id' value

            # Create a new dictionary with modified data
            new_form_data = {
                'users_id': session['user_id'],
                'title': form_data['title'],
                'body': form_data['body'],
                'subcategories_id': subcategory_id
            }

            # Insert the new post into the database
            query = """
                INSERT INTO posts (title, body, users_id, subcategories_id)
                VALUES (%(title)s, %(body)s, %(users_id)s, %(subcategories_id)s)
            """
            connectToMySQL(cls.DB).query_db(query, new_form_data)
        else:
            return redirect("/home")














    # @classmethod
    # def get_posts_by_thread_id(cls, thread_id):
    #     query = "SELECT * FROM posts WHERE thread_id = %s;"
    #     data = (thread_id,)
    #     results = connectToMySQL(cls.DB).query_db(query, data)
    #     return [cls(**row) for row in results]
