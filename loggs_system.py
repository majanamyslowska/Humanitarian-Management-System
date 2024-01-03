import datetime

class UserAuthenticationSystem:
    def __init__(self, login_log_file="login_log.txt", logout_log_file="logout_log.txt"):
        self.login_log_file = login_log_file
        self.logout_log_file = logout_log_file

    def log_in(self, username):
        self._log_event(self.login_log_file, f"{username} logged in at {self._get_current_time()}")

    def log_out(self, username):
        self._log_event(self.logout_log_file, f"{username} logged out at {self._get_current_time()}")

    def _log_event(self, log_file, message):
        with open(log_file, "a") as file:
            file.write(f"{message}\n")

    def _get_current_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# with open(authentication_system.login_log_file, "r") as file:
#     print("Login Log:")
#     print(file.read())

# with open(authentication_system.logout_log_file, "r") as file:
#     print("Logout Log:")
#     print(file.read())