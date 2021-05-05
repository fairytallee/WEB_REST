from users.user import User


class InMemoryUsersRepo:
    def __init__(self):
        self.next_id = 1
        self.by_id = {}

    def get_by_name(self, name):
        for _, value in self.by_id.items():
            if value.username == name:
                return value
        return None

    def request_create(self, username, password):
        found = self.get_by_name(username)

        if found is not None:
            return None  # пользователь с таким именем уже есть

        new_user = User(id=self.next_id, username=username, password=password)
        self.by_id[new_user.id] = new_user
        self.next_id += 1

        return new_user

    def authorize(self, username, password):
        found = self.get_by_name(username)

        if found is None:
            return None, "user not found"  # пользователя не нашлось

        if found.password != password:
            return None, "bad password"

        return found, ""
