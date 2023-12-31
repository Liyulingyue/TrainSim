from train import Train
from track import Track, SlopeInfo, CurveInfo, SpeedLimitZone
from simulation import Simulation


def main():
    # 创建Train对象
    my_train = Train(0, 0)

    # 创建Track对象，传入CurveInfo、SpeedLimitZone和SlopeData数据
    curve_radius_data = [(0, 100, 50), (100, 200, 30), (200, 300, 0)]
    speed_limit_zones = [(0, 50, 30), (50, 150, 40), (150, float('inf'), float('inf'))]
    slope_data = [(0, 50, 0.02), (50, 100, 0.05), (100, 150, -0.03), (150, float('inf'), 0)]
    my_track = Track(300, slope_data, curve_radius_data, speed_limit_zones, 1, -1)

    # 创建Simulation对象，传入Train和Track对象
    my_simulation = Simulation(my_train, my_track, 0.1)

    # 运行模拟
    my_simulation.run_simulation(num_steps=100)


if __name__ == '__main__':
    main()