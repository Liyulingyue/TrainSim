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
    def __init__(self, curve_radius_data, friction_coefficient=0.1):
        self.curve_radius_data = curve_radius_data  # 弯道数据
        self.default_curvature = float("inf")  # 默认曲率值为无穷大，表示直道
        self.friction_coefficient = friction_coefficient  # 摩擦系数

    def get_curvature(self, position):
        # 根据位置获取曲率值
        for curve in self.curve_radius_data:
            start_pos, end_pos, curvature = curve
            if start_pos <= position <= end_pos:
                return curvature
        return self.default_curvature  # 如果没有找到对应的位置，则返回默认曲率值

    def get_acceleration(self, position, velocity):
        # 根据位置获取曲率半径值
        curvature = self.get_curvature(position)

        # 将曲率半径转化为曲率
        if curvature == float("inf"):
            kappa = 0.0  # 直道情况下，曲率为0
        else:
            kappa = 1.0 / curvature  # 曲率是曲率半径的倒数

        # 根据曲率计算对应的摩擦阻力
        friction_force = (
            self.friction_coefficient * velocity**2 * kappa
        )  # 使用曲率来计算摩擦阻力
        # 将摩擦阻力转换为加速度（假设质量为1，单位为 N/kg）
        acceleration = -friction_force  # 负号表示方向与速度方向相反
        return acceleration


class SpeedLimitZone:
    def __init__(self, speed_limit_zones):
        self.speed_limit_zones = speed_limit_zones  # 限速区数据，是一个列表，每个元素包含起始位置、结束位置和最大允许速度
        self.default_speed_limit = float("inf")  # 默认最大允许速度为无穷大，表示没有限速

    def get_speed_limit(self, position):
        # 根据位置获取最大允许速度
        for zone in self.speed_limit_zones:
            start_pos, end_pos, speed_limit = zone
            if start_pos <= position <= end_pos:
                return speed_limit
        return self.default_speed_limit  # 如果没有找到对应的位置，则返回默认最大允许速度
