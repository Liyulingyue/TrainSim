# simulation.py
import train
import track


class Simulation:
    def __init__(self, train_instance: train, track_instance: track, time_step: float):
        self.train = train_instance
        self.track = track_instance
        self.time_step = time_step

    def run_simulation(self, num_steps):
        for step in range(num_steps):
            acceleration = self.track.get_acceleration(self.train.position, self.train.velocity)
            self.train.update_velocity(acceleration, self.time_step)
            self.train.update_position(self.time_step)
            print(f"Step {step}: Acceleration={acceleration}, Velocity={self.train.velocity}, Position={self.train.position}")