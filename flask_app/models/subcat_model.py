from flask_app import connectToMySQL

class Subcategory:
    
    DB='pawsome_forum'
    
    def __init__(self, id, subcat_name):
        self.id = id
        self.subcat_name = subcat_name

    @classmethod
    def get_subcat_id_by_name(cls, category_id, subcategory_name):
        query = "SELECT id FROM subcategories WHERE categories_id = %(category_id)s AND name = %(subcategory_name)s;"
        print(f"query => {query}")
        data = {'categories_id': category_id, 'subcat_name': subcategory_name}
        result = connectToMySQL(cls.DB).query_db(query, data)
        print(f"subcat model data => {data}")
        print(f"subcat_model => {result}")
        return result[0][''] if result else None

    
    

