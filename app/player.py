from datetime import date, datetime


class Player:
    def __init__(self, idx, name, team_name, birth, position, number, height, weight, jump, site):
        self.idx = idx
        self.name = name
        self.team_name = team_name
        self.birth = birth
        self.position = position
        self.number = number
        self.height = height
        self.weight = weight
        self.jump = jump
        self.site = site
        self.team = None
        self.age = self.calculate_age(self.birth)

    @staticmethod
    def calculate_age(birth_date):
        today = date.today()

        birth_date = datetime.strptime(birth_date, '%d.%m.%Y')
        
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
