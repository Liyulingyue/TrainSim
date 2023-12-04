class Track:
    def __init__(self, length, slope_info, curve_info, speed_limit_zones, max_acceleration, min_acceleration):
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


class SlopeInfo:
    def __init__(self, slope_data):
        self.slope_data = slope_data  # 坡道数据，是一个列表，每个元素包含起始位置、结束位置和坡道值
        self.default_slope = 0  # 默认坡道值为0

    def get_slope(self, position):
        # 根据位置获取斜率
        for slope in self.slope_data:
            start_pos, end_pos, slope_value = slope
            if start_pos <= position <= end_pos:
                return slope_value
        return self.default_slope  # 如果没有找到对应的位置，则返回默认坡道值

    def get_acceleration(self, position):
        # 获取斜率并计算对应的加速度
        slope = self.get_slope(position)
        acceleration = -slope * 9.8  # 假设斜率以角度表示，转换为加速度，上坡加速，下坡减速
        return acceleration


class CurveInfo:
    def __init__(self, curve_radius_data):
        self.curve_radius_data = curve_radius_data  # 弯道数据
        self.default_curvature = float('inf')  # 默认曲率值为无穷大，表示直道

    def get_curvature(self, position):
        # 根据位置获取曲率值
        for curve in self.curve_radius_data:
            start_pos, end_pos, curvature = curve
            if start_pos <= position <= end_pos:
                return curvature
        return self.default_curvature  # 如果没有找到对应的位置，则返回默认曲率值

    def get_acceleration(self, position, velocity):
        # 获取曲率并计算对应的加速度（向心加速度）
        curvature = self.get_curvature(position)
        acceleration = (velocity ** 2) / curvature  # 向心加速度公式
        return acceleration


class SpeedLimitZone:
    def __init__(self, speed_limit_zones):
        self.speed_limit_zones = speed_limit_zones  # 限速区数据，是一个列表，每个元素包含起始位置、结束位置和最大允许速度
        self.default_speed_limit = float('inf')  # 默认最大允许速度为无穷大，表示没有限速

    def get_speed_limit(self, position):
        # 根据位置获取最大允许速度
        for zone in self.speed_limit_zones:
            start_pos, end_pos, speed_limit = zone
            if start_pos <= position <= end_pos:
                return speed_limit
        return self.default_speed_limit  # 如果没有找到对应的位置，则返回默认最大允许速度