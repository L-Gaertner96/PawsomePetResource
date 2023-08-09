from flask_app import connectToMySQL
from flask import session

class Comment:
    DB = 'pawsome_forum'
    
    def __init__(self, post_id, form_data):
        self.id = id
        self.post_id = post_id
        self.body = form_data['body']
        self.user_id = form_data['user_id']
        
    @classmethod
    def create_new_comment(cls, form_data, post_id):
        new_form_data = {
            'user_id': session['user_id'],
            'content': form_data['content'],
            'post_id': post_id
        }
        print(f"data => {new_form_data}")
        query = """
            INSERT INTO comments (content, users_id, posts_id)
            VALUES (%(content)s, %(users_id)s, %(post_id)s)
        """
        connectToMySQL(cls.DB).query_db(query, new_form_data)

    @classmethod
    def get_comments_by_post_id(cls, post_id):
        db = cls.DB
        connection = connectToMySQL(db)
        
        query = "SELECT * FROM comments WHERE posts_id = %(post_id)s;"
        data = {'post_id': post_id}
        
        comments = connection.query_db(query, data)
        
        return comments