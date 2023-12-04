from trackinfo import SlopeInfo, CurveInfo, SpeedLimitZone


class Track:
    def __init__(self, length, slope_info: SlopeInfo, curve_info: CurveInfo, speed_limit_zones: SpeedLimitZone, max_acceleration, min_acceleration):
        self.length = length
        self.slope_info = SlopeInfo(slope_info)  # 轨道坡道信息
        self.curve_info = CurveInfo(curve_info)  # 轨道弯道信息
        self.speed_limit_zones = SpeedLimitZone(speed_limit_zones)  # 限速区信息
        self.max_acceleration = max_acceleration  # 列车最大加速度（牵引性能）  
        self.min_acceleration = min_acceleration  # 列车最小加速度（制动性能）  

    def get_acceleration(self, position, velocity):
        # 根据轨道坡道信息、弯道信息和限速区信息计算理论加速度  
        theoretical_acceleration = self._calculate_theoretical_acceleration(position, velocity)

        # 根据限速区信息调整加速度以满足限速要求  
        actual_acceleration = self._adjust_acceleration(theoretical_acceleration, position, velocity)

        return actual_acceleration

    def _calculate_theoretical_acceleration(self, position, velocity):
        # 获取轨道坡道信息对应位置的加速度
        slope_acceleration = self.slope_info.get_acceleration(position)

        # 获取轨道弯道信息对应位置的加速度
        # curve_acceleration = self.curve_info.get_acceleration(position, velocity)
        # 暂时不考虑
        curve_acceleration = 0

        # 计算理论加速度（道路情况）
        theoretical_acceleration = slope_acceleration + curve_acceleration

        return theoretical_acceleration

    def _adjust_acceleration(self, theoretical_acceleration, position, velocity):
        # 获取当前位置的限速
        speed_limit = self.speed_limit_zones.get_speed_limit(position)

        # 如果当前速度已经超过限速，将加速度调整为制动加速度，否则进行加速
        if speed_limit <= velocity:
            actual_acceleration = self.min_acceleration + theoretical_acceleration
        else:
            actual_acceleration = self.max_acceleration + theoretical_acceleration

        return actual_acceleration