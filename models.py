# models.py

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(name='{self.name}', email='{self.email}')"

class iPad:
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description

    def __repr__(self):
        return f"iPad(id='{self.id}', description='{self.description}')"

class Period:
    def __init__(self, id: str, start_time: str, end_time: str):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"Period(id='{self.id}', start_time='{self.start_time}', end_time='{self.end_time}')"

class Booking:
    def __init__(self, user: User, ipad: iPad, date: str, period: Period):
        # For simplicity, date is stored as a string e.g., "YYYY-MM-DD"
        self.user = user
        self.ipad = ipad
        self.date = date
        self.period = period

    def __repr__(self):
        return f"Booking(user='{self.user.name}', ipad_id='{self.ipad.id}', date='{self.date}', period_id='{self.period.id}')"
