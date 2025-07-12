from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    signup_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)

    # Relaciones
    favorite_planets: Mapped[List["FavoritePlanet"]] = relationship(back_populates="user")
    favorite_characters: Mapped[List["FavoriteCharacter"]] = relationship(back_populates="user")
    favorite_starships: Mapped[List["FavoriteStarship"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "signup_date": self.signup_date.isoformat(),
            "name": self.name,
            "last_name": self.last_name
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    population: Mapped[str] = mapped_column(String(80), nullable=False)
    region: Mapped[str] = mapped_column(String(80), nullable=False)
    appears_in_episodes: Mapped[str] = mapped_column(nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)

    # Relación
    favorited_by: Mapped[List["FavoritePlanet"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "region": self.region,
            "appears_in_episodes": self.appears_in_episodes,
            "diameter": self.diameter
        }

class Starship(db.Model):
    __tablename__ = 'starships'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    starship_class: Mapped[str] = mapped_column(String(80), nullable=False)
    crew: Mapped[int] = mapped_column(nullable=False)
    passengers: Mapped[int] = mapped_column(nullable=False)
    length: Mapped[float] = mapped_column(nullable=False)

    # Relación
    favorited_by: Mapped[List["FavoriteStarship"]] = relationship(back_populates="starship")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "starship_class": self.starship_class,
            "crew": self.crew,
            "passengers": self.passengers,
            "length": self.length
        }

class Character(db.Model):
    __tablename__ = 'characters'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    species: Mapped[str] = mapped_column(String(80), nullable=False) 
    planet_from: Mapped[str] = mapped_column(String(80), nullable=False)
    appears_in: Mapped[str] = mapped_column(nullable=False)
    usual_starship: Mapped[str] = mapped_column(String(80), nullable=False)

    # Relación
    favorited_by: Mapped[List["FavoriteCharacter"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "planet_from": self.planet_from,
            "appears_in": self.appears_in,
            "usual_starship": self.usual_starship
        }

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=False)
    added_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "added_on": self.added_on.isoformat(),
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_characters'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'), nullable=False)
    added_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="favorite_characters")
    character: Mapped["Character"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "added_on": self.added_on.isoformat(),
        }

class FavoriteStarship(db.Model):
    __tablename__ = 'favorite_starships'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'), nullable=False)
    added_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="favorite_starships")
    starship: Mapped["Starship"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id,
            "added_on": self.added_on.isoformat(),
        }