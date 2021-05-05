from tools.my_dict import MyDict
from users.user import User


class Post(MyDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.votes = []
        self.comments = []
        self.upvotePercentage = 100
        if self.author:
            self.author = User(**self.author)
