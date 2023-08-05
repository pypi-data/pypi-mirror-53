"""
实现
  双界数值范围 (a,b)
  单界数值范围 (-inf, a) 或 (a, inf)
  无界数值范围 (-inf, inf)
  之间的一一映射

基本用法
  bm = BinaryMapping(x1=x1, x2=x2, y1=y1, y2=y2, refer_points=refer_points)
  print(bm(x))
  print(bm.f.plot())
"""
import math
from typing import List, Tuple

"""
f(x) = atan(x) 反正切函数的数学性质

1. 单调对称有界，f(-inf) = -0.5pi, f(0) = 0, f(inf) = 0.5pi
2. 导数 1/(1+x*x)
3. 积分 x atan(x) - 0.5 ln(1+x*x)
4. 曲率 = |f''| / (1 + f'^2) ^ 3/2

g(x) = 1 - atan(x) / 0.5pi 的性质
"""


class Function(object):
    """
    函数基类
    """

    def __init__(
            self,
            x1: float,  # 函数 basic 形态的左边界
            x2: float,  # 函数 basic 形态的右边界
            y1: float,  # 函数 basic 形态的 f(x1)
            y2: float,  # 函数 basic 形态的 f(x2)
            refer_point_count: int,  # 确定函数 final 形态需要的参考点数量
    ):
        """
        构造函数，设置函数 basic 形态的边界，可用于确定 basic 函数类型
        """

        # 边界，开始时是 basic 边界，set_border 后是 final 边界
        self.x1: float = x1
        self.x2: float = x2
        self.y1: float = y1
        self.y2: float = y2

        # 参考点
        self.refer_point_count: int = refer_point_count
        self.refer_points: List[Tuple[float, float]] = []

    def basic(
            self,
            x: float
    ) -> float:
        """
        计算函数 basic 形态的 f(x)
        """

        raise Exception('由子类实现')

    def calc(
            self,
            x: float
    ) -> float:
        """
        计算函数 final 形态的 f(x)
        """

        raise Exception('由子类实现')

    def plot(
            self
    ) -> str:
        """
        输出 SpeQ 的绘图表达式
        """

        raise Exception('由子类实现')

    def set_border(
            self,
            x1: float,
            x2: float,
            y1: float,
            y2: float,
    ):
        """
        设置 final 形态的边界
        """

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        # 检查参考点
        if len(self.refer_points) >= self.refer_point_count:
            self._get_final_params()

    def set_point(
            self,
            x: float,
            y: float,
    ) -> None:
        """
        检查参考点，可确定函数参数
        """

        self.refer_points.append((x, y))
        if len(self.refer_points) >= self.refer_point_count:
            self._get_final_params()

    def _get_final_params(
            self
    ) -> None:
        """
        获取函数 final 形态的参数
        """

        raise Exception('由子类实现')

    def _get_non_inf(
            self,
            n1: float,
            n2: float
    ) -> float:
        """
        获取两个数中非 inf 的数
        """

        return n2 if math.isinf(n1) else n1

    def _resolve(
            self,
            a1: float,
            b1: float,
            c1: float,
            a2: float,
            b2: float,
            c2: float
    ) -> Tuple[float, float]:
        """
        解方程组
            a1 x + b1 y = c1
            a2 x + b2 y = c2
        """

        x = (c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2)
        y = (a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2)

        return x, y


class FunctionNull(Function):
    """
    不包含实际计算功能，仅用于函数匹配的伪函数
    """

    def __init__(
            self,
            x1: float,
            x2: float,
            y1: float,
            y2: float
    ):
        super(FunctionNull, self).__init__(x1, x2, y1, y2, 0)

    def match(
            self,
            f: Function
    ) -> bool:
        """
        匹配函数范围
        """

        u1, u2 = self._get_tag(self.x1, self.x2)
        u3, u4 = self._get_tag(self.y1, self.y2)

        for w1, w2, w3, w4 in [
            (u1, u2, u3, u4),
            (-u2, -u1, u4, u3),
            (-u2, -u1, -u4, -u3),
            (u1, u2, -u3, -u4),
        ]:
            v1, v2 = self._get_tag(f.x1, f.x2)
            v3, v4 = self._get_tag(f.y1, f.y2)
            if v1 == w1 and v2 == w2 and v3 == w3 and v4 == w4:
                return True

        return False

    def _get_tag(
            self,
            n1: float,
            n2: float
    ) -> Tuple[float, float]:
        """
        获取 tag 用 -2 表示 -inf, 用 2 表示 inf, 用 -1,1 表示双界区间，用 0 表示单界的非无限侧
        """

        ct = {-math.inf: -2, math.inf: 2}

        if not math.isinf(n1) and not math.isinf(n2):
            return (-1, 1) if n1 < n2 else (1, -1)

        return ct.get(n1, 0), ct.get(n2, 0)


class FunctionX(Function):
    """
    无限区域，线性变换
    """

    def __init__(self):
        super(FunctionX, self).__init__(-math.inf, math.inf, -math.inf, math.inf, 2)
        self.a: float = 1
        self.b: float = 0

    def basic(
            self,
            x: float
    ) -> float:
        return x

    def calc(
            self, x: float
    ) -> float:
        return self.a * x + self.b

    def plot(self):
        return 'Plot(%s * x + %s)' % (self.a, self.b)

    def _get_final_params(
            self
    ) -> None:
        # y = c (ax+b) + d
        #   = ax + b
        x1, y1 = self.refer_points[0]
        x2, y2 = self.refer_points[1]

        self.a, self.b = self._resolve(x1, 1, y1, x2, 1, y2)


class FunctionDivX(Function):
    """
    正数域，倒数
    """

    def __init__(self):
        super(FunctionDivX, self).__init__(0, math.inf, math.inf, 0, 2)
        self.c = 1
        self.B = 0
        self.D = 0

    def basic(
            self,
            x: float
    ) -> float:
        return 1 / x

    def calc(
            self,
            x: float
    ) -> float:
        return self.c / (x + self.B) + self.D

    def plot(self):
        return 'Plot(%s / (x + %s) + %s' % (self.c, self.B, self.D)

    def _get_final_params(
            self
    ) -> None:
        # y = c 1/(ax+b) + d
        #   = c/(x+B) + D
        self.B = -(self.x1 if not math.isinf(self.x1) else self.x2)
        self.D = self.y1 if not math.isinf(self.y1) else self.y2

        x, y = self.refer_points[0]
        self.c = (y - self.D) * (x + self.B)


class FunctionTan(Function):
    """
    正切
    """

    def __init__(self):
        super(FunctionTan, self).__init__(-math.pi / 2, math.pi / 2, -math.inf, math.inf, 2)
        self.A = 1
        self.B = 0
        self.c = 1
        self.d = 0

    def basic(
            self,
            x: float
    ) -> float:
        return math.tan(x)

    def calc(
            self, x: float
    ) -> float:
        return self.c * math.tan(self.A * x + self.B) + self.d

    def plot(self):
        return 'Plot(%s * Tan(%s * x + %s) + %s)' % (self.c, self.A, self.B, self.d)

    def _get_final_params(
            self
    ) -> None:
        # y = c tan(ax+b) + d
        #   = c tan(Ax+B) + d
        # x1, x2 向两侧各扩展 1E-8
        self.A = math.pi / (self.x2 - self.x1 + 2E-8)
        self.B = -self.A * (self.x2 + self.x1) / 2

        x1, y1 = self.refer_points[0]
        x2, y2 = self.refer_points[1]

        self.c, self.d = self._resolve(math.tan(self.A * x1 + self.B), 1, y1, math.tan(self.A * x2 + self.B), 1, y2)


class FunctionAtan(Function):
    """
    反正切
    """

    def __init__(self):
        super(FunctionAtan, self).__init__(-math.inf, math.inf, -math.pi / 2, math.pi / 2, 2)
        self.a = 1
        self.b = 0
        self.C = 1
        self.D = 0

    def basic(
            self,
            x: float
    ) -> float:
        return math.atan(x)

    def calc(
            self,
            x: float
    ) -> float:
        return self.C * math.atan(self.a * x + self.b) + self.D

    def plot(self):
        return 'Plot(%s * ATan(%s * x + %s) + %s)' % (self.C, self.a, self.b, self.D)

    def _get_final_params(
            self
    ) -> None:
        # y = c arctan(ax+b) + d
        #   = C arctan(ax+b) + D
        # y1, y2 各向内侧缩减 1E-8
        self.C = (self.y2 - self.y1 - 2E-8) / math.pi
        self.D = (self.y1 + self.y2) / 2

        x1, y1 = self.refer_points[0]
        x2, y2 = self.refer_points[1]

        self.a, self.b = self._resolve(x1, 1, math.tan((y1 - self.D) / self.C), x2, 1, math.tan((y2 - self.D) / self.C))


class FunctionExp(Function):
    """
    指数
    """

    def __init__(self):
        super(FunctionExp, self).__init__(-math.inf, math.inf, 0, math.inf, 2)
        self.a = 1
        self.c = 1
        self.D = 0

    def basic(
            self,
            x: float
    ) -> float:
        return math.exp(x)

    def calc(
            self,
            x: float
    ) -> float:
        return self.c * math.exp(self.a * x) + self.D

    def plot(self):
        return 'Plot(%s * Exp(%s * x) + %s)' % (self.c, self.a, self.D)

    def _get_final_params(
            self
    ) -> None:
        # y = c e^{ax+b} + d
        #   = c e^{ax} + D
        self.D = self._get_non_inf(self.y1, self.y2)

        x1, y1 = self.refer_points[0]
        x2, y2 = self.refer_points[1]

        self.a = math.log((y2 - self.D) / (y1 - self.D)) / (x2 - x1)
        self.c = (y1 - self.D) / math.exp(self.a * x1)


class FunctionLn(Function):
    """
    对数
    """

    def __init__(self):
        super(FunctionLn, self).__init__(0, math.inf, -math.inf, math.inf, 2)
        self.A = 1
        self.B = 0
        self.c = 1
        self.d = 0

    def basic(
            self,
            x: float
    ) -> float:
        return math.log(x)

    def calc(
            self,
            x: float
    ) -> float:
        return self.c * math.log(self.A * x + self.B) + self.d

    def plot(self):
        return 'Plot(%s * Ln(%s * x + %s) + %s)' % (self.c, self.A, self.B, self.d)

    def _get_final_params(
            self
    ) -> None:
        # y = c ln(ax+b) + d
        #   = c ln(Ax+B) + d
        self.A = 1 if (self.x1 + self.x2) == math.inf else -1
        self.B = -self.A * self._get_non_inf(self.x1, self.x2)
        x1, y1 = self.refer_points[0]
        x2, y2 = self.refer_points[1]
        self.c, self.d = self._resolve(math.log(self.A * x1 + self.B), 1, y1, math.log(self.A * x2 + self.B), 1, y2)


class BinaryMapping(object):
    """
    二值映射
    """

    def __init__(
            self,
            x1: float = -math.inf,  # 函数 final 形态的左边界
            x2: float = math.inf,  # 函数 final 形态的右边界
            y1: float = -math.inf,  # 函数 final 形态的 f(x1)
            y2: float = math.inf,  # 函数 final 形态的 f(x2)
            refer_points: List[Tuple[float, float]] = None  # 函数 final 形态的参考点
    ):
        """
        构造函数，确定函数 final 形态
        """

        self.f = self.__get_function(x1, x2, y1, y2)
        self.f.set_border(x1, x2, y1, y2)

        if refer_points:
            for x, y in refer_points:
                self.f.set_point(x, y)

    def __call__(
            self,
            x: float
    ) -> float:
        return self.f.calc(x)

    def __get_function(
            self,
            x1: float,
            x2: float,
            y1: float,
            y2: float,
    ) -> Function:
        """
        根据目标特征查找对应的基本函数
        """

        target = FunctionNull(x1, x2, y1, y2)

        # 匹配 x1, x2, y1, y2 tag 属性
        for f in [
            FunctionX(),
            FunctionDivX(),
            FunctionTan(),
            FunctionAtan(),
            FunctionExp(),
            FunctionLn(),
        ]:
            if target.match(f):
                return f

        raise Exception('没有匹配的函数')


if __name__ == '__main__':
    import test.test_binary_mapping

    params = (None, -math.inf, -3, math.inf, -math.inf, [(-5, 5.0), (-6, 6.6218604324326575)],
              [(-7, 7.772588722239782), (-8, 8.66516292749662)])
    test.test_binary_mapping.test_mapping(params)
