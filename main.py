from letterboxdpy import movie, user
import data_handler as dh


class App:
    def __init__(self):
        self.json_handler = dh.JsonHandler()
        self.user_handler = dh.UserHandler(self.json_handler)
        self.movie_handler = dh.MovieHandler(self.json_handler)
        self.users_list = self.json_handler.read_users()
        self.movies_list = self.json_handler.read_movies()
        self.login_user()

        while True:
            self.options()

    def login_user(self):
        if bool(self.users_list) is False:
            print("Welcome to LetterboxdHelper!")
            user_input = input("What is your Letterboxd username? ")
            self.add_to_users(str(user_input))
            return user_input

        else:
            print("Welcome back to LetterboxdHelper!")

    def options(self):
        user_input = input("\nWhat would you like to do?\n[1] Check watchlist \n[2] Compare watchlists "
                           "\n[3] Get user stats \n[4] Recommend movies \n[5] Update user ")
        if user_input == '1':
            self.options_check_watchlist()
        elif user_input == '2':
            self.options_compare_watchlists()
        elif user_input == '3':
            self.options_get_user_stats()
        elif user_input == '4':
            self.options_recommend_movies()
        elif user_input == '5':
            self.options_update_user()

    def options_check_watchlist(self):
        user_input = input("Whose Letterboxd watchlist would you like to view? ")
        if 'watchlist' in self.users_list[str(user_input)]:
            print(self.users_list[str(user_input)]['watchlist_length'], "items found")
            print([x[0] for x in self.users_list[str(user_input)]['watchlist']])
        else:
            self.update_user_watchlist(str(user_input))
            print(self.users_list[str(user_input)]['watchlist_length'], "items found")
            print([x[0] for x in self.users_list[str(user_input)]['watchlist']])

    def options_compare_watchlists(self):
        user_input1 = input("Whose Letterboxd watchlist would you like to view? ")
        user_input2 = input("Whose Letterboxd watchlist would you like to view? ")

        if str(user_input1) in self.users_list:
            if 'watchlist' in self.users_list[str(user_input1)]:
                user1_watchlist = self.users_list[str(user_input1)]['watchlist']
            else:
                self.update_user_watchlist(str(user_input1))
                user1_watchlist = self.users_list[str(user_input1)]['watchlist']
        else:
            self.add_to_users(str(user_input1))
            self.update_user_watchlist(str(user_input1))
            user1_watchlist = self.users_list[str(user_input1)]['watchlist']

        if str(user_input2) in self.users_list:
            if 'watchlist' in self.users_list[str(user_input2)]:
                user2_watchlist = self.users_list[str(user_input2)]['watchlist']
            else:
                self.update_user_watchlist(str(user_input2))
                user2_watchlist = self.users_list[str(user_input2)]['watchlist']

        else:
            self.add_to_users(str(user_input2))
            self.update_user_watchlist(str(user_input2))
            user2_watchlist = self.users_list[str(user_input2)]['watchlist']

        items_found = 0
        movie_list = []
        for m in user1_watchlist:
            if m in user2_watchlist:
                items_found += 1
                movie_list.append(m[0])
        print(f"{items_found} movies in common found: {movie_list}")

    def options_get_user_stats(self):
        user_input = input("Whose Letterboxd stats would you like to view? ").lower()
        if user_input in self.users_list:
            print(self.users_list[str(user_input)]['stats'])
        else:
            self.add_to_users(str(user_input))
            print(self.users_list[str(user_input)]['stats'])

    def options_recommend_movies(self):
        username = input("Whose Letterboxd account would you like to generate recommendations for? ")
        user_input = input("\nHow would you like to filter through your watchlist? \n[1] By genre \n[2] By director \n"
                           "[3] By rating \n[4] Randomly ")
        self.generate_movies(self.users_list[str(username)]['watchlist'])
        if user_input == '1':
            genre = input("Which genre would you like to filter for? ")
            for m in self.users_list[str(username)]['watchlist']:
                if str(genre) in self.movies_list[m[1]]['genres']:
                    print(self.movies_list[m[1]]['name'], end='   ')
        elif user_input == '2':
            director = input("Which director would you like to filter for? ")
            for m in self.users_list[str(username)]['watchlist']:
                if str(director) in self.movies_list[m[1]]['directors']:
                    print(self.movies_list[m[1]]['name'], end='   ')
        elif user_input == '3':
            filter_rating = float(input("What minimum rating would you like to filter for? "))
            for m in self.users_list[str(username)]['watchlist']:
                movie_rating = self.movies_list[m[1]]['rating'][:4]
                if movie_rating != 'None':
                    if filter_rating <= float(movie_rating):
                        print(self.movies_list[m[1]]['name'], end='   ')
        elif user_input == '4':
            director = input("Which director would you like to filter for? ")
            for m in self.users_list[str(username)]['watchlist']:
                if str(director) in self.movies_list[m[0]]['directors']:
                    print(self.movies_list[m[1]]['name'], end='   ')

    def options_update_user(self):
        username = input("Which account would you like to update? ")
        self.update_user(username)
        self.update_user_watchlist(username)

    def generate_movies(self, movielist):
        for m in movielist:
            if m[1] not in self.movies_list:
                self.add_to_movies(m[1], m[0])

    def update_user_watchlist(self, username):
        new_user = user.User(str(username))
        self.users_list[str(username)]['watchlist'] = user.user_watchlist_list(new_user)
        self.json_handler.write_users(self.users_list)

    def add_to_users(self, username):
        new_user = user.User(str(username))
        self.users_list[str(username)] = new_user.__dict__
        self.json_handler.write_users(self.users_list)

    def update_user(self, username):
        new_user = user.User(str(username))
        del self.users_list[str(username)]
        self.users_list[str(username)] = new_user.__dict__
        self.json_handler.write_users(self.users_list)

    def add_to_movies(self, movie_title, movie_name):
        new_movie = movie.Movie(movie_title)
        self.movies_list[str(movie_title)] = new_movie.__dict__
        self.movies_list[str(movie_title)]['name'] = str(movie_name)
        self.json_handler.write_movies(self.movies_list)


def main():
    App()


if __name__ == '__main__':
    main()
