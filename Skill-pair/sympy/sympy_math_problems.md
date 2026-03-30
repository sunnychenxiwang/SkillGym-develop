# SymPy 数学问题整理（按能力模块）

说明：本文件根据你上传的 `sympy` skill 所覆盖的能力模块整理，题目按 **符号方程、微积分、代数化简、矩阵线性代数、物理、数论、几何、代码生成、LaTeX 输出、精确结果** 分类。  
这些题目是为 **SymPy / 符号计算 benchmark** 整理的训练与测试输入样例；题目表述为整理后的版本，**来源**标在每个部分下方。

---

## 1. 符号方法解方程

### 1.1 代数方程
1. 求解方程：`x^2 - 5x + 6 = 0`
2. 求解方程：`x^4 - 16 = 0`
3. 求解方程：`sin(x) = 1/2`
4. 求解参数方程：`a*x + b = 0`

### 1.2 方程组
5. 求解线性方程组：
   - `x + y = 2`
   - `x - y = 0`
6. 求解非线性方程组：
   - `x^2 + y = 2`
   - `x + y^2 = 3`

### 1.3 微分方程
7. 求解微分方程：`f'(x) - f(x) = 0`
8. 求解微分方程：`f''(x) + f(x) = 0`

**来源：**
- https://docs.sympy.org/latest/tutorials/intro-tutorial/solvers.html
- https://docs.sympy.org/latest/modules/solvers/solvers.html
- https://github.com/sympy/sympy/tree/master/examples

---

## 2. 微积分运算

### 2.1 导数
1. 求 `x^2` 关于 `x` 的导数
2. 求 `sin(x^2)` 关于 `x` 的导数
3. 求 `x^2*y^3` 关于 `x`、`y` 的偏导数

### 2.2 积分
4. 计算不定积分：`∫ x^2 dx`
5. 计算定积分：`∫_0^1 x^2 dx`
6. 计算反常积分：`∫_0^∞ exp(-x) dx`

### 2.3 极限与级数
7. 计算极限：`lim_{x→0} sin(x)/x`
8. 求 `exp(x)` 在 `x=0` 处展开到 `x^5` 的泰勒级数

**来源：**
- https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html
- https://docs.sympy.org/latest/modules/series/series.html
- https://github.com/facebookresearch/SymbolicMathematics
- https://storage.googleapis.com/mathematics-dataset/mathematics_dataset-v1.0.tar.gz

---

## 3. 代数表达式运算与简化

1. 展开：`(x + 1)^3`
2. 因式分解：`x^2 - 1`
3. 化简：`sin(x)^2 + cos(x)^2`
4. 约分：`(x^2 - 1)/(x - 1)`
5. 化简带假设的表达式：在 `x > 0` 条件下化简 `sqrt(x^2)`

**来源：**
- https://docs.sympy.org/latest/tutorials/intro-tutorial/simplification.html
- https://github.com/facebookresearch/SymbolicMathematics
- https://github.com/sympy/sympy/tree/master/examples

---

## 4. 矩阵与线性代数

1. 构造矩阵：`[[1, 2], [3, 4]]`
2. 求矩阵的逆矩阵
3. 求矩阵的行列式
4. 求矩阵的转置
5. 求矩阵的特征值和特征向量
6. 求解线性系统 `Ax = b`，其中：
   - `A = [[1, 2], [3, 4]]`
   - `b = [5, 6]`

**来源：**
- https://docs.sympy.org/latest/tutorials/intro-tutorial/matrices.html
- https://docs.sympy.org/latest/modules/matrices/matrices.html
- https://github.com/sympy/sympy/tree/master/examples

---

## 5. 物理计算（力学 / 矢量 / 量子）

### 5.1 力学
1. 建立单摆系统的拉格朗日量：
   - 广义坐标 `q`
   - 质量 `m`
   - 重力加速度 `g`
   - 摆长 `l`

### 5.2 矢量分析
2. 计算向量点积：
   - `v1 = 3*N.x + 4*N.y`
   - `v2 = 1*N.x + 2*N.z`
3. 计算上述两个向量的叉积

### 5.3 量子力学
4. 构造对易子 `Commutator(A, B)` 并求值

**来源：**
- https://docs.sympy.org/latest/tutorials/physics/mechanics/index.html
- https://docs.sympy.org/latest/explanation/modules/physics/mechanics/index.html
- https://courses.physics.illinois.edu/tam210/sp2024/sympy_tutorial.pdf
- https://github.com/sympy/sympy/tree/master/examples

---

## 6. 数论计算

1. 判断一个整数是否为素数
2. 对整数做质因数分解
3. 计算两个整数的最大公因数和最小公倍数
4. 进行模运算：求 `a mod n`
5. 求解简单丢番图方程

**来源：**
- https://docs.sympy.org/latest/modules/ntheory.html
- https://github.com/sympy/sympy/tree/master/examples
- https://storage.googleapis.com/mathematics-dataset/mathematics_dataset-v1.0.tar.gz

---

## 7. 几何计算（二维 / 三维 / 解析几何）

1. 创建二维点、直线、圆
2. 求两条直线的交点
3. 求点到直线的距离
4. 求三角形面积
5. 判断点是否在线段上
6. 做基本解析几何变换

**来源：**
- https://docs.sympy.org/latest/modules/geometry/index.html
- https://github.com/sympy/sympy/tree/master/examples

---

## 8. 数学表达式转可执行代码

1. 将表达式 `x^2 + 2x + 1` 转成 NumPy 可执行函数
2. 将同一表达式生成 C 代码
3. 将同一表达式生成 Fortran 代码
4. 对一个符号表达式执行 `lambdify`

**来源：**
- https://docs.sympy.org/latest/modules/codegen.html
- https://docs.sympy.org/latest/modules/utilities/codegen.html
- https://github.com/sympy/sympy/blob/master/sympy/utilities/codegen.py

---

## 9. LaTeX / 其他数学输出

1. 将表达式 `x^2 + 2x + 1` 输出为 LaTeX
2. 将定积分表达式输出为 LaTeX
3. 将矩阵输出为 LaTeX
4. 对表达式做 pretty print

**来源：**
- https://docs.sympy.org/latest/tutorials/intro-tutorial/printing.html
- https://docs.sympy.org/latest/modules/printing.html
- https://github.com/sympy/sympy/tree/master/examples

---

## 10. 精确数学结果

1. 保持 `sqrt(2)` 为精确形式，而不是小数近似
2. 使用 `Rational(1, 2)` 表示精确分数
3. 对 `pi + sqrt(8)` 先保持精确形式，再做数值近似
4. 在假设条件下做精确符号化简

**来源：**
- https://docs.sympy.org/
- https://docs.sympy.org/latest/tutorials/intro-tutorial/index.html
- https://github.com/sympy/sympy/tree/master/examples

---

## 11. 适合做 benchmark 的统一输入格式建议

```json
{
  "task_type": "calculus",
  "input": {
    "expression": "sin(x**2)",
    "operation": "differentiate",
    "variable": "x"
  },
  "expected_output": "2*x*cos(x**2)"
}
```

```json
{
  "task_type": "solve_equation",
  "input": {
    "equation": "x**2 - 5*x + 6",
    "variable": "x"
  },
  "expected_output": ["2", "3"]
}
```

```json
{
  "task_type": "codegen",
  "input": {
    "expression": "x**2 + 2*x + 1",
    "language": "C"
  },
  "expected_output": "generated_code"
}
```

---

## 12. 说明

- 本文件是按 SymPy skill 的能力范围整理的 **问题清单**，方便你后续直接做 benchmark、构造测试集或写 workflow。
- 题目以“可作为输入”的形式组织，适合转成 JSON / YAML / Markdown 表格。
- 来源优先采用：
  1. SymPy 官方文档
  2. SymPy 官方 examples
  3. 更贴合符号数学任务的数据集（如 SymbolicMathematics、DeepMind mathematics dataset）
