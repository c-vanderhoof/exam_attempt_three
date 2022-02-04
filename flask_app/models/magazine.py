from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Magazine:
    db = "magazine_db"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM magazines INNER JOIN users on magazines.user_id = users.id;"
        result = connectToMySQL(cls.db).query_db(query)
        if len(result) == 0:
            return []
        magazines = []
        for i in result:
            u = cls(i)
            some_user= {
            'id':i['users.id'],
            'first_name':i['first_name'],
            'last_name':i['last_name'],
            'email':i['email'],
            'password':i['password'],
            'created_at':i['users.created_at']
            }
            t = user.User(some_user)
            u.User=t
            magazines.append(u)
        return magazines

    @classmethod
    def delete_magazine(cls,data):
        query ="DELETE FROM magazines WHERE id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM magazines WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_by_user_id(cls,data):
        query = "SELECT * FROM magazines WHERE user_id = %(user_id)s"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def save(cls,data):
        query = "INSERT INTO magazines (title,description,user_id) VALUES (%(title)s,%(description)s,%(user_id)s);"
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @staticmethod
    def validate_mag(self):
        is_valid = True
        if len(self['title']) <2:
            is_valid = False
            flash("Title should be at least 2 characters","magazine")
        if len(self['description'])<10:
            is_valid = False
            flash("Description must be at least 10 characters long.","magazine")
        return is_valid
