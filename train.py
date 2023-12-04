class Train:
    def __init__(self, initial_velocity=0, initial_position=0, initial_acceleration=0):
        self.velocity = initial_velocity
        self.position = initial_position
        self.acceleration = initial_acceleration

    def update_velocity(self, acceleration, time_period):
        self.velocity += acceleration * time_period

    def update_position(self, time_period):
        self.position += self.velocity * time_period

    def update_acceleration(self, train_acceleration):
        self.acceleration = train_acceleration
