import json


class JsonHandler:
    # Class for reading from and writing to a JSON file
    def __init__(self, movies_json: str = 'movies.json', users_json: str = 'users.json'):
        self.movies_json = movies_json
        self.users_json = users_json

    def write_movies(self, movies: {str}):
        # This function takes a dictionary of movie dictionaries and writes them to the location file

        with open(self.movies_json, 'w') as file:
            json.dump(movies, file, indent=4)

    def write_users(self, users: {}):
        # This function takes a dictionary of users and writes them to the location file
        with open(self.users_json, 'w') as file:
            json.dump(users, file, indent=4)

    def read_movies(self):
        # This function takes whatever is written on the location file and returns it
        with open(self.movies_json, 'r') as file:
            return json.load(file)

    def read_users(self):
        with open(self.users_json, 'r') as file:
            return json.load(file)


class UserHandler:
    def __init__(self, json_handler):
        self.json_handler = json_handler
        self.user_dict = self.get_users_from_json(self.json_handler)

    def get_users_from_json(self, json_handler: JsonHandler):
        return json_handler.read_users()


class MovieHandler:
    def __init__(self, json_handler):
        self.json_handler = json_handler
        self.movie_dict = self.get_movies_from_json(self.json_handler)

    def get_movies_from_json(self, json_handler: JsonHandler):
        return json_handler.read_movies()
