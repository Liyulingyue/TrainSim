from trackinfo import SlopeInfo, CurveInfo, SpeedLimitZone


class Track:
    def __init__(
        self,
        length,
        slope_info: SlopeInfo,
        curve_info: CurveInfo,
        speed_limit_zones: SpeedLimitZone,
        max_acceleration,
        min_acceleration,
        max_jerk=0.75,
        air_resistance_coefficient=0.005,
    ):
        self.length = length
        self.slope_info = SlopeInfo(slope_info)  # 轨道坡道信息
        self.curve_info = CurveInfo(curve_info)  # 轨道弯道信息
        self.speed_limit_zones = SpeedLimitZone(speed_limit_zones)  # 限速区信息
        self.max_acceleration = max_acceleration  # 列车最大加速度（牵引性能）
        self.min_acceleration = min_acceleration  # 列车最小加速度（制动性能）
        self.max_jerk = max_jerk  # 加速度变化速率限制
        self.air_resistance_coefficient = air_resistance_coefficient  # 空气阻力系数

    def get_acceleration(
        self, position, velocity, previous_train_acceleration, time_period
    ):
        # 根据轨道坡道信息、弯道信息和限速区信息计算理论加速度
        theoretical_acceleration = self._calculate_theoretical_acceleration(
            position, velocity
        )

        # 根据限速区信息调整加速度以满足限速要求
        actual_acceleration = self._adjust_acceleration(
            theoretical_acceleration,
            position,
            velocity,
            previous_train_acceleration,
            time_period,
        )

        return actual_acceleration

    def _calculate_theoretical_acceleration(self, position, velocity):
        # 获取轨道坡道信息对应位置的加速度
        slope_acceleration = self.slope_info.get_acceleration(position)

        # 获取轨道弯道信息对应的弯道阻力
        curve_acceleration = self.curve_info.get_acceleration(position, velocity)

        # 计算空气阻力加速度（假设与速度的平方成正比）
        air_resistance_acceleration = -self.air_resistance_coefficient * velocity**2

        # 计算理论加速度（道路情况）
        theoretical_acceleration = (
            slope_acceleration + curve_acceleration + air_resistance_acceleration
        )

        return theoretical_acceleration

    def _adjust_acceleration(
        self,
        theoretical_acceleration,
        position,
        velocity,
        previous_train_acceleration,
        time_period,
    ):
        # 计算接下来十个点的位置
        future_positions = [position + velocity * i for i in range(11)]

        # 获取未来的限速情况
        future_speed_limits = []
        for future_position in future_positions:
            future_speed_limit = self.speed_limit_zones.get_speed_limit(future_position)
            future_speed_limits.append(future_speed_limit)

        # 根据未来的限速情况调整加速度
        min_future_speed_limit = min(future_speed_limits)
        if min_future_speed_limit <= velocity:
            train_acceleration = (
                previous_train_acceleration - self.max_jerk * time_period
            )
            train_acceleration = max(train_acceleration, self.min_acceleration)
        else:
            train_acceleration = (
                previous_train_acceleration + self.max_jerk * time_period
            )
            train_acceleration = min(train_acceleration, self.max_acceleration)
        actual_acceleration = train_acceleration + theoretical_acceleration

        return actual_acceleration, train_acceleration
