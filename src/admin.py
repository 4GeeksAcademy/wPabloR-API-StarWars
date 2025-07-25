import os
from flask_admin import Admin
from models import db, User, Planet, Starship, Character, FavoritePlanet,FavoriteCharacter, FavoriteStarship
from flask_admin.contrib.sqla import ModelView


class FavoritePlanetView(ModelView):
    column_list = ("user", "planet")
    form_columns = ("user", "planet")

class FavoriteCharacterView(ModelView):
    column_list = ("user", "character")
    form_columns = ("user", "character")

class FavoriteStarshipView(ModelView):
    column_list = ("user", "starship")
    form_columns = ("user", "starship")

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Starship, db.session))
    admin.add_view(ModelView(Character, db.session))

    admin.add_view(FavoritePlanetView(FavoritePlanet, db.session))
    admin.add_view(FavoriteCharacterView(FavoriteCharacter, db.session))
    admin.add_view(FavoriteStarshipView(FavoriteStarship, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))