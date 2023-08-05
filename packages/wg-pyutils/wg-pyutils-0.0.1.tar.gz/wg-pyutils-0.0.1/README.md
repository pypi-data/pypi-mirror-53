# wg-pyutils

This is a Python package containing lots of small and useful functions for reuse

## binary-mapping

自动构造合适的函数，实现

* 双界数值范围 (a,b)
* 单界数值范围 (-inf, c) 或 (c, inf)
* 无界数值范围 (-inf, inf)

之间的一一映射

基本用法

`
bm = BinaryMapping(x1=x1, x2=x2, y1=y1, y2=y2, refer_points=refer_points)

print(bm(x))

print(bm.f.plot())
`
