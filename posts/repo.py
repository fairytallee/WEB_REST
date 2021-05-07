from datetime import datetime


class InMemoryPostsRepo:
    def __init__(self):
        self.next_id = 1
        self.by_id = {}

    def get_all(self):
        return tuple(self.by_id.values())

    def get_by_id(self, post_id):
        return self.by_id.get(post_id, None)

    def get_by_username(self, username):
        result = []
        for value in self.by_id.values():
            if value.author.username == username:
                result.append(value)
        return tuple(result)

    def get_by_category(self, category):
        result = []
        for value in self.by_id.values():
            if value.category == category:
                result.append(value)
        return tuple(result)

    def request_create(self, post):
        post.id = self.next_id
        post.created = datetime.now()

        self.by_id[post.id] = post
        self.next_id += 1

        return post

    def request_delete(self, post_id, user):
        post = self.get_by_id(post_id)
        if not post:
            return f"post doesn't exist for id: {post_id}"
        if post.author.id != user.id:
            return f"you aren't author of this post id: {post_id}"

        del self.by_id[post_id]
        return None
