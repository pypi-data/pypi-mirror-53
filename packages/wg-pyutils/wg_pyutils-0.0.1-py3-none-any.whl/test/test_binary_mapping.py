from pytest import approx, fixture

from wg_pyutils.binary_mapping import (
    FunctionX,
    FunctionDivX,
    FunctionTan,
    FunctionAtan,
    FunctionExp,
    FunctionLn,
    BinaryMapping
)


def function_under_test():
    for Func, refer_xs, check_xs in [
        (FunctionX, [5, 6], [7, 8]),
        (FunctionDivX, [5, 6], [7, 8]),
        (FunctionTan, [5, 6], [7, 8]),
        (FunctionAtan, [5, 6], [7, 8]),
        (FunctionExp, [5, 6], [7, 8]),
        (FunctionLn, [5, 6], [7, 8]),
    ]:
        yield (Func, refer_xs, check_xs, False, False)
        yield (Func, refer_xs, check_xs, False, True)
        yield (Func, refer_xs, check_xs, True, False)
        yield (Func, refer_xs, check_xs, True, True)


@fixture(scope='function', params=list(function_under_test()))
def range_and_refer(request):
    # 函数，参考点，验证点
    Func, refer_xs, check_xs, mirror_x, mirror_y = request.param
    func = Func()
    refer_ys = [func.basic((x - 3) / 2) * 4 + 5 for x in refer_xs]
    check_ys = [func.basic((x - 3) / 2) * 4 + 5 for x in check_xs]
    refer_xy = list(zip(refer_xs, refer_ys))
    check_xy = list(zip(check_xs, check_ys))

    # 标准型，x 放大 2 倍，右移 3，y 放大 4 倍，上移 5
    x1, x2, y1, y2 = func.x1, func.x2, func.y1, func.y2
    x1 = x1 * 2 + 3
    x2 = x2 * 2 + 3
    y1 = y1 * 4 + 5
    y2 = y2 * 4 + 5

    # x 镜像
    if mirror_x:
        y1 = -y1
        y2 = -y2
        refer_xy = [(x, -y) for x, y in refer_xy]
        check_xy = [(x, -y) for x, y in check_xy]

    if mirror_y:
        x1, x2 = -x2, -x1
        y1, y2 = y2, y1
        refer_xy = [(-x, y) for x, y in refer_xy]
        check_xy = [(-x, y) for x, y in check_xy]

    yield Func, x1, x2, y1, y2, refer_xy, check_xy


def test_mapping(range_and_refer):
    Func, x1, x2, y1, y2, refer_points, check_xy = range_and_refer
    info = 'params = (None, %s, %s, %s, %s, %s, %s)' % (x1, x2, y1, y2, refer_points, check_xy)
    info = info.replace('inf', 'math.inf')
    print(Func)
    print(info)

    bm = BinaryMapping(x1=x1, x2=x2, y1=y1, y2=y2, refer_points=refer_points)

    if Func is not None:
        assert isinstance(bm.f, Func)
        bm.f.plot()

    for x, y in check_xy:
        assert bm(x) == approx(y)
