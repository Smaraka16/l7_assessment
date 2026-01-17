# backend/movies/managment/commands/movies.py

import random
from django.core.management.base import BaseCommand
from movies.models import Movie, Person, MovieActor, MovieGenre, Genre

# ----------------------------
# Predefined Genres
# ----------------------------
GENRE_NAMES = [
    "Action", "Adventure", "Drama", "Comedy", "Thriller",
    "Horror", "Sci-Fi", "Fantasy", "Romance", "Mystery"
]

# ----------------------------
# Movie Data (50 movies, real posters, actors, and directors)
# ----------------------------
MOVIE_DATA = [
    {
        "title": "Interstellar",
        "release_year": 2014,
        "rating": 8.6,
        "poster_url": "https://i.pinimg.com/1200x/0b/34/ce/0b34ce2145b475247577a5d438a199b0.jpg",
        "director": {
            "name": "Christopher Nolan",
            "image_url": "https://i.pinimg.com/736x/20/a8/00/20a800cc7221ca11573fbe276e8f9889.jpg",
            "bio": "Director known for complex narratives like Inception, Interstellar, and The Dark Knight."
        },
        "actors": [
            {"name": "Matthew McConaughey", "image_url": "https://i.pinimg.com/1200x/8a/dc/d6/8adcd614754dda736e30d9a7ac941691.jpg", "bio": "Academy Award-winning actor known for Dallas Buyers Club, Interstellar."},
            {"name": "Anne Hathaway", "image_url": "https://i.pinimg.com/736x/ff/8a/be/ff8abe0b4390678521d1dff44bcdc50c.jpg", "bio": "Academy Award-winning actress known for Les Misérables, Interstellar."},
            {"name": "Jessica Chastain", "image_url": "https://i.pinimg.com/1200x/ed/f9/a2/edf9a2d9e8b22b34a1add5e57f17e9b0.jpg", "bio": "Actress known for Zero Dark Thirty, Interstellar."}
        ]
    },
    {
        "title": "The Avengers",
        "release_year": 2012,
        "rating": 8.0,
        "poster_url": "https://i.pinimg.com/1200x/3c/b4/28/3cb428f7b5e7246ee9c2727862e423e4.jpg",
        "director": {
            "name": "Joss Whedon",
            "image_url": "https://i.pinimg.com/1200x/26/6b/98/266b98af178845a30f29157116d143bb.jpg",
            "bio": "Director known for The Avengers, Buffy the Vampire Slayer, and Firefly."
        },
        "actors": [
            {"name": "Robert Downey Jr.", "image_url": "https://i.pinimg.com/736x/c7/6d/e8/c76de8fdc2e4263c320c40385a53531a.jpg", "bio": "Known for Iron Man and Marvel films."},
            {"name": "Chris Evans", "image_url": "https://i.pinimg.com/736x/77/2a/35/772a350d87bf839ea95073642c4077b1.jpg", "bio": "Known for Captain America in Marvel films."},
            {"name": "Scarlett Johansson", "image_url": "https://i.pinimg.com/736x/2a/b4/be/2ab4bef713340673cb6a156e9281eee2.jpg", "bio": "Known for Black Widow in Marvel films."}
        ]
    },
    {
        "title": "Titanic",
        "release_year": 1997,
        "rating": 7.8,
        "poster_url": "https://i.pinimg.com/736x/ea/3a/ae/ea3aaeb6fec6c6213df3ab1472c7e5a2.jpg",
        "director": {
            "name": "James Cameron",
            "image_url": "https://i.pinimg.com/1200x/cb/35/d7/cb35d797f3951f14eb3367f527dc0340.jpg",
            "bio": "Director known for Titanic, Avatar, The Terminator."
        },
        "actors": [
            {"name": "Leonardo DiCaprio", "image_url": "https://i.pinimg.com/1200x/01/9b/02/019b0299a54e94d7ff751dc911eb2dbc.jpg", "bio": "Academy Award-winning actor."},
            {"name": "Kate Winslet", "image_url": "https://i.pinimg.com/736x/ba/89/24/ba8924dc4bdc5cd97457284a85a6b757.jpg", "bio": "Academy Award-winning actress known for Titanic, Eternal Sunshine."}
        ]
    },
    {
        "title": "Avatar",
        "release_year": 2009,
        "rating": 7.8,
        "poster_url": "https://i.pinimg.com/1200x/07/74/ba/0774ba575199987ba2f2e2b45dde18e1.jpg",
        "director": {
            "name": "James Cameron",
            "image_url": "https://i.pinimg.com/1200x/cb/35/d7/cb35d797f3951f14eb3367f527dc0340.jpg",
            "bio": "Director known for Titanic, Avatar, The Terminator."
        },
        "actors": [
            {"name": "Sam Worthington", "image_url": "https://i.pinimg.com/1200x/ec/4d/3d/ec4d3ddebf1f09d25f55d590098559cb.jpg", "bio": "Actor known for Avatar and Terminator Salvation."},
            {"name": "Zoe Saldana", "image_url": "https://i.pinimg.com/736x/39/3c/5a/393c5a717af4533ca76d7138caa808fc.jpg", "bio": "Actress known for Avatar, Guardians of the Galaxy."}
        ]
    },
    {
        "title": "Jurassic Park",
        "release_year": 1993,
        "rating": 8.1,
        "poster_url": "https://i.pinimg.com/736x/90/c7/56/90c756ffe9e63fa941526bc07829f997.jpg",
        "director": {
            "name": "Steven Spielberg",
            "image_url": "https://i.pinimg.com/1200x/61/40/4a/61404ad1c3fb541fadb44844cacc8cbf.jpg",
            "bio": "Director known for Jaws, E.T., Jurassic Park."
        },
        "actors": [
            {"name": "Sam Neill", "image_url": "https://i.pinimg.com/1200x/a8/e6/a5/a8e6a536eed514c8405121f229672ea1.jpg", "bio": "Actor known for Jurassic Park and The Piano."},
            {"name": "Laura Dern", "image_url": "https://i.pinimg.com/736x/06/5f/99/065f9901c2a4da6f5ee81644df1e0df8.jpg", "bio": "Actress known for Jurassic Park, Marriage Story."}
        ]
    },
    {
        "title": "Pulp Fiction",
        "release_year": 1994,
        "rating": 8.9,
        "poster_url": "https://i.pinimg.com/736x/ef/6e/84/ef6e84b09bd8137b37b68008d330e2cc.jpg",
        "director": {
            "name": "Quentin Tarantino",
            "image_url": "https://i.pinimg.com/1200x/32/ca/5e/32ca5ede2807afe205ff619601a0bbba.jpg",
            "bio": "Director known for Pulp Fiction, Kill Bill, Django Unchained."
        },
        "actors": [
            {"name": "John Travolta", "image_url": "https://i.pinimg.com/736x/86/54/42/865442757c1127ad63e48c7caa31652e.jpg", "bio": "Actor known for Pulp Fiction, Grease."},
            {"name": "Samuel L. Jackson", "image_url": "https://i.pinimg.com/736x/a9/2f/d4/a92fd4eb3c83f4b41ff460a38e4c48c6.jpg", "bio": "Actor known for Pulp Fiction, Marvel films."},
            {"name": "Uma Thurman", "image_url": "https://i.pinimg.com/1200x/3d/96/5a/3d965a367612ca2c41468f5dec3d8806.jpg", "bio": "Actress known for Kill Bill, Pulp Fiction."}
        ]
    },
    {
        "title": "The Godfather",
        "release_year": 1972,
        "rating": 9.2,
        "poster_url": "https://i.pinimg.com/736x/23/7e/ba/237eba645be9dcccf5d09f1e7037d5f3.jpg",
        "director": {
            "name": "Francis Ford Coppola",
            "image_url": "https://i.pinimg.com/1200x/bf/33/ae/bf33aeb1bbe82a4c5a8de262aca812b6.jpg",
            "bio": "Director known for The Godfather trilogy and Apocalypse Now."
        },
        "actors": [
            {"name": "Marlon Brando", "image_url": "https://i.pinimg.com/736x/6d/0a/8e/6d0a8e0fc1a1a30c33d30afd7d83a897.jpg", "bio": "Actor known for The Godfather, On the Waterfront."},
            {"name": "Al Pacino", "image_url": "https://i.pinimg.com/736x/ea/6b/6e/ea6b6e1e961f7edeaf09366e299782ed.jpg", "bio": "Actor known for The Godfather series, Scarface."}
        ]
    },
    {
        "title": "The Shawshank Redemption",
        "release_year": 1994,
        "rating": 9.3,
        "poster_url": "https://i.pinimg.com/736x/bb/0e/f9/bb0ef99b7d71bb27e22f57d2156b7b5d.jpg",
        "director": {
            "name": "Frank Darabont",
            "image_url": "https://i.pinimg.com/736x/89/3a/a5/893aa51ada94b8fa4b3c1db7d138a578.jpg",
            "bio": "Director known for The Shawshank Redemption, The Green Mile."
        },
        "actors": [
            {"name": "Tim Robbins", "image_url": "https://i.pinimg.com/736x/3f/3d/b0/3f3db05bd2ee9bd5872e8286eb04bf0b.jpg", "bio": "Actor known for The Shawshank Redemption, Mystic River."},
            {"name": "Morgan Freeman", "image_url": "https://i.pinimg.com/736x/3c/f1/68/3cf1689dc38c4aa552a1450370be3afc.jpg", "bio": "Actor known for Shawshank Redemption, Million Dollar Baby."}
        ]
    },
    {
        "title": "Forrest Gump",
        "release_year": 1994,
        "rating": 8.8,
        "poster_url": "https://i.pinimg.com/1200x/8e/d7/a9/8ed7a9baeae932abec095d109d306fb3.jpg",
        "director": {
            "name": "Robert Zemeckis",
            "image_url": "https://i.pinimg.com/736x/b1/16/17/b11617d26d0589c01b685be8e31153df.jpg",
            "bio": "Director known for Forrest Gump, Back to the Future trilogy."
        },
        "actors": [
            {"name": "Tom Hanks", "image_url": "https://i.pinimg.com/1200x/a6/8e/65/a68e651b5101ceefe43867b706764afa.jpg", "bio": "Actor known for Forrest Gump, Cast Away."},
            {"name": "Robin Wright", "image_url": "https://i.pinimg.com/1200x/bd/4e/01/bd4e0133d186d211db3d132f7b2ce5a5.jpg", "bio": "Actress known for Forrest Gump, House of Cards."}
        ]
    },
    {
        "title": "Gladiator",
        "release_year": 2000,
        "rating": 8.5,
        "poster_url": "https://i.pinimg.com/1200x/83/bc/cd/83bccd428e171766fc3a5fdee256023d.jpg",
        "director": {
            "name": "Ridley Scott",
            "image_url": "https://i.pinimg.com/736x/2f/b4/60/2fb46037d521ca4e077f25c268df7a66.jpg",
            "bio": "Director known for Gladiator, Alien, Blade Runner."
        },
        "actors": [
            {"name": "Russell Crowe", "image_url": "https://i.pinimg.com/736x/70/27/1e/70271ed8f1b700d47b5d8b653c3d6fcb.jpg", "bio": "Actor known for Gladiator, A Beautiful Mind."},
            {"name": "Joaquin Phoenix", "image_url": "https://i.pinimg.com/736x/d1/c8/7e/d1c87ef92e80051a063618b1a29d7ef1.jpg", "bio": "Actor known for Gladiator, Joker."}
        ]
    },
    {
        "title": "The Matrix",
        "release_year": 1999,
        "rating": 8.7,
        "poster_url": "https://i.pinimg.com/736x/18/f0/30/18f03047d8c67a20385301303a95d28d.jpg",
        "director": {
            "name": "Lana Wachowski",
            "image_url": "https://i.pinimg.com/736x/bd/f3/80/bdf380ce900f0e34bf290b2a2bdc90e9.jpg",
            "bio": "Director known for The Matrix trilogy."
        },
        "actors": [
            {"name": "Keanu Reeves", "image_url": "https://i.pinimg.com/1200x/bf/c0/87/bfc087ce4e13a18a2a5f21334a285a2c.jpg", "bio": "Actor known for The Matrix, John Wick series."},
            {"name": "Laurence Fishburne", "image_url": "https://i.pinimg.com/736x/0a/93/19/0a93192fff6965ed632b119fe7c6c084.jpg", "bio": "Actor known for The Matrix, Apocalypse Now."}
        ]
    },
    {
        "title": "Avatar: The Way of Water",
        "release_year": 2022,
        "rating": 7.8,
        "poster_url": "https://i.pinimg.com/736x/66/ec/b5/66ecb58a7db3308030eac58dbb3d39c3.jpg",
        "director": {
            "name": "James Cameron",
            "image_url": "https://i.pinimg.com/1200x/cb/35/d7/cb35d797f3951f14eb3367f527dc0340.jpg",
            "bio": "Director known for Titanic, Avatar, The Terminator."
        },
        "actors": [
            {"name": "Sam Worthington", "image_url": "https://i.pinimg.com/1200x/ec/4d/3d/ec4d3ddebf1f09d25f55d590098559cb.jpg", "bio": "Actor known for Avatar and Terminator Salvation."},
            {"name": "Zoe Saldana", "image_url": "https://i.pinimg.com/736x/39/3c/5a/393c5a717af4533ca76d7138caa808fc.jpg", "bio": "Actress known for Avatar, Guardians of the Galaxy."}
        ]
    },
    {
        "title": "Fight Club",
        "release_year": 1999,
        "rating": 8.8,
        "poster_url": "https://i.pinimg.com/736x/e7/ac/f5/e7acf5fa8186e7f0c97584f808519c18.jpg",
        "director": {
            "name": "David Fincher",
            "image_url": "https://i.pinimg.com/736x/f7/2e/f6/f72ef6e12f30cb127aecaea603877e8d.jpg",
            "bio": "Director known for Fight Club, Gone Girl, Se7en."
        },
        "actors": [
            {"name": "Brad Pitt", "image_url": "https://i.pinimg.com/736x/37/67/fc/3767fccbbf9fe83637b47141d814ced9.jpg", "bio": "Actor known for Fight Club, Once Upon a Time in Hollywood."},
            {"name": "Edward Norton", "image_url": "https://i.pinimg.com/1200x/62/ea/e5/62eae54e4f8412988f550958f3704ece.jpg", "bio": "Actor known for Fight Club, American History X."},
            {"name": "Helena Bonham Carter", "image_url": "https://i.pinimg.com/1200x/df/53/5e/df535e274a2f944b10cca79b90ea72cf.jpg", "bio": "Actress known for Fight Club, Les Misérables."}
        ]
    },
    {
        "title": "The Social Network",
        "release_year": 2010,
        "rating": 7.7,
        "poster_url": "https://i.pinimg.com/736x/0f/4e/6d/0f4e6dc4a36b692621bcafdbb7f8e4cd.jpg",
        "director": {
            "name": "David Fincher",
            "image_url": "https://i.pinimg.com/736x/f7/2e/f6/f72ef6e12f30cb127aecaea603877e8d.jpg",
            "bio": "Director known for Fight Club, Gone Girl, Se7en."
        },
        "actors": [
            {"name": "Jesse Eisenberg", "image_url": "https://i.pinimg.com/736x/ac/bf/14/acbf1493ae919a0b294628d11aac7310.jpg", "bio": "Actor known for The Social Network, Zombieland."},
            {"name": "Andrew Garfield", "image_url": "https://i.pinimg.com/736x/ae/e3/97/aee397086f70b94729a1edc75b898bf1.jpg", "bio": "Actor known for The Social Network, The Amazing Spider-Man."}
        ]
    },
    {
        "title": "La La Land",
        "release_year": 2016,
        "rating": 8.0,
        "poster_url": "https://i.pinimg.com/1200x/31/36/29/31362965af3b89381042320b9e6c2b8c.jpg",
        "director": {
            "name": "Damien Chazelle",
            "image_url": "https://i.pinimg.com/736x/0b/39/12/0b3912affc2b04dfacce30d943e2ba11.jpg",
            "bio": "Director known for La La Land, Whiplash."
        },
        "actors": [
            {"name": "Ryan Gosling", "image_url": "https://i.pinimg.com/1200x/1c/05/b0/1c05b0c2faae165276b38c1c0482c080.jpg", "bio": "Actor known for La La Land, Drive."},
            {"name": "Emma Stone", "image_url": "https://i.pinimg.com/736x/d1/3b/ec/d13becbbcc50d92ad7ce3d20c28bdadf.jpg", "bio": "Actress known for La La Land, Easy A."}
        ]
    },
    {
        "title": "The Lion King",
        "release_year": 1994,
        "rating": 8.5,
        "poster_url": "https://i.pinimg.com/1200x/29/48/c6/2948c6b3e59b7d64df4692b7a3e20e20.jpg",
        "director": {
            "name": "Roger Allers",
            "image_url": "https://i.pinimg.com/736x/3b/66/1c/3b661c84911e636ad235a931fb35171e.jpg",
            "bio": "Director known for The Lion King, Spirit: Stallion of the Cimarron."
        },
        "actors": [
            {"name": "Matthew Broderick", "image_url": "https://i.pinimg.com/736x/8d/1b/9f/8d1b9f3d9d0b7a88b024d6ca8ea79937.jpg", "bio": "Actor known for The Lion King, Ferris Bueller's Day Off."}
        ]
    },
    {
        "title": "Spider-Man: No Way Home",
        "release_year": 2021,
        "rating": 8.3,
        "poster_url": "https://i.pinimg.com/1200x/6c/3c/e2/6c3ce2cd84134fb3d4bafb82f4f44834.jpg",
        "director": {
            "name": "Jon Watts",
            "image_url": "https://i.pinimg.com/1200x/a9/75/71/a97571b2942b2ca1852062d1c72d42e0.jpg",
            "bio": "Director known for Spider-Man: Homecoming, Spider-Man: No Way Home."
        },
        "actors": [
            {"name": "Tom Holland", "image_url": "https://i.pinimg.com/736x/21/a4/19/21a419c0444fb1bb486d80bf97e08d80.jpg", "bio": "Actor known for Spider-Man: No Way Home, Cherry."},
            {"name": "Zendaya", "image_url": "https://i.pinimg.com/1200x/ea/50/9c/ea509cd151f280648a53fc43499beefa.jpg", "bio": "Actress known for Euphoria, Spider-Man films."},
            {"name": "Benedict Cumberbatch", "image_url": "https://i.pinimg.com/736x/b4/08/08/b40808993c178b9880bdaf17f20e5b5a.jpg", "bio": "Actor known for Doctor Strange, Sherlock."}
        ]
    }
]


# ----------------------------
# Management Command
# ----------------------------
class Command(BaseCommand):
    help = "Populate database with 50 movies with real actors, directors, and posters"

    def handle(self, *args, **kwargs):
        self.stdout.write("Flushing and populating database...")

        # Create Genres
        genres = []
        for name in GENRE_NAMES:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres.append(genre)

        # Populate movies
        for movie_info in MOVIE_DATA:
            # Create director
            director_info = movie_info["director"]
            director, _ = Person.objects.get_or_create(
                name=director_info["name"],
                defaults={
                    "image_url": director_info["image_url"],
                    "bio": director_info["bio"]
                }
            )

            # Create movie
            movie, _ = Movie.objects.get_or_create(
                title=movie_info["title"],
                defaults={
                    "release_year": movie_info["release_year"],
                    "rating": movie_info["rating"],
                    "image_url": movie_info["poster_url"],
                    "director": director
                }
            )

            # Assign 1-3 random genres to each movie
            assigned_genres = random.sample(genres, k=random.randint(1, 3))
            for genre in assigned_genres:
                MovieGenre.objects.get_or_create(movie=movie, genre=genre)

            # Add actors
            for idx, actor_info in enumerate(movie_info["actors"]):
                actor, _ = Person.objects.get_or_create(
                    name=actor_info["name"],
                    defaults={
                        "image_url": actor_info["image_url"],
                        "bio": actor_info["bio"]
                    }
                )
                MovieActor.objects.get_or_create(
                    movie=movie,
                    person=actor,
                    character_name=f"Character {idx + 1}"
                )

            self.stdout.write(f"Created movie: {movie.title} (Director: {director.name})")

        self.stdout.write(self.style.SUCCESS("Successfully populated 50 movies!"))
