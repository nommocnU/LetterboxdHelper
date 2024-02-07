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



        #self.json_handler.write_users({str(self.username): self.user_object.__dict__})
        #self.json_handler.write_movies({'ids': [x[1] for x in self.user_watchlist], 'movies': 'movie dicts'})

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
        user_input = input("\nWhat would you like to do?\n""[1] Check watchlist\n""[2] Compare watchlists\n""[3] Get user stats\n")
        if user_input == '1':
            self.options_check_watchlist()
        elif user_input == '2':
            self.options_compare_watchlists()
        elif user_input == '3':
            self.options_get_user_stats()

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
        user1_watchlist = []
        user2_watchlist = []
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
        print(f"{items_found} movies found: {movie_list}")

    def options_get_user_stats(self):
        user_input = input("Whose Letterboxd stats would you like to view? ")
        if user_input in self.users_list:
            print(self.users_list[str(user_input)]['stats'])
        else:
            self.add_to_users(str(user_input))
            print(self.users_list[str(user_input)]['stats'])

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




def main():
    app = App()


if __name__ == '__main__':
    main()
