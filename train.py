class Train:
    def __init__(self, initial_velocity, initial_position):
        self.velocity = initial_velocity
        self.position = initial_position

    def update_velocity(self, acceleration, time_period):
        self.velocity += acceleration * time_period

    def update_position(self, time_period):
        self.position += self.velocity * time_period