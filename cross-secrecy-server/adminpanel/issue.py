
class Issue():
    def __init__(self, author, subject, description, image, id=None, date=None):
        self.id          = id
        self.date        = date
        self.author      = author
        self.subject     = subject
        self.description = description
        self.image       = image
