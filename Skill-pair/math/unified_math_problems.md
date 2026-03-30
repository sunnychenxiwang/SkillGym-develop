# Unified Math 数学问题整理（按 `/math` 技能能力模块）

说明：本文件根据你上传的 `math` skill 覆盖的能力模块整理，题目按 **符号计算、矩阵线性代数、数论、组合数学、约束求解/证明、单位换算、解释型数学主题** 分类。  
这些题目适合用作 `/math` 路由技能的输入样例，也方便后续整理成 benchmark。每一类后面都标注了**来源**。

---

## 1. 符号计算：方程、微积分、化简

### 1.1 方程求解
1. 求解方程：`x^2 - 4 = 0`
2. 求解方程：`x^2 - 5*x + 6 = 0`
3. 求解方程：`sin(x) = 1/2`
4. 求解参数方程：`a*x + b = 0`

### 1.2 微积分
5. 计算不定积分：`∫ sin(x) dx`
6. 计算定积分：`∫_0^π sin(x) dx`
7. 求导：`d/dx (x^3)`
8. 求极限：`lim_(x→0) sin(x)/x`
9. 求级数展开：`exp(x)` 在 `x=0` 处展开到 5 阶
10. 求常微分方程：`f''(x) + f(x) = 0`
11. 求拉普拉斯变换：`L{sin(t)}`

### 1.3 化简与因式分解
12. 化简：`sin(x)^2 + cos(x)^2`
13. 因式分解：`x^2 - 1`
14. 化简分式：`(x^2 - 1)/(x - 1)`
15. 计算多项式因式分解：`x^4 - 16`

**来源：**
- https://github.com/sympy/sympy
- https://www.sympy.org/
- https://github.com/google-deepmind/mathematics_dataset
- https://www.tensorflow.org/datasets/catalog/math_dataset

---

## 2. 矩阵与线性代数

1. 求矩阵 `[[1, 2], [3, 4]]` 的行列式
2. 求矩阵 `[[1, 2], [3, 4]]` 的逆矩阵
3. 求矩阵 `[[1, 2], [3, 4]]` 的转置
4. 求矩阵 `[[2, 1], [1, 2]]` 的特征值
5. 求矩阵 `[[2, 1], [1, 2]]` 的特征向量
6. 求矩阵的 rref：`[[1, 2, 3], [2, 4, 6], [1, 1, 1]]`
7. 求矩阵的秩：`[[1, 2], [2, 4]]`
8. 求矩阵 `[[1, 2], [2, 4]]` 的零空间
9. 求解线性系统 `Ax = b`，其中：
   - `A = [[1, 2], [3, 4]]`
   - `b = [5, 6]`
10. 求矩阵 `[[1, 2], [3, 4]]` 的特征多项式

**来源：**
- https://github.com/sympy/sympy
- https://www.sympy.org/

---

## 3. 数论

1. 对整数 `360` 进行质因数分解
2. 判断 `101` 是否为素数
3. 计算 `gcd(84, 126)`
4. 计算 `lcm(12, 18)`
5. 求 `3` 在模 `11` 下的乘法逆元
6. 判断 `9973` 是否为素数
7. 计算 `gcd(123456, 7890)`

**来源：**
- https://github.com/sympy/sympy
- https://www.sympy.org/
- https://github.com/google-deepmind/mathematics_dataset

---

## 4. 组合数学

1. 计算二项式系数 `C(10, 3)`
2. 计算阶乘 `8!`
3. 计算排列数 `P(10, 3)`
4. 计算整数划分数 `p(7)`
5. 计算第 6 个 Catalan 数
6. 计算第 5 个 Bell 数

**来源：**
- https://github.com/sympy/sympy
- https://www.sympy.org/

---

## 5. 约束求解 / 逻辑证明（Z3 方向）

1. 判断约束是否可满足：`x > 0 ∧ x < 1`
2. 判断命题是否恒真：`x^2 + y^2 >= 2*x*y`
3. 判断命题是否恒真：`x^2 + 1 > 0`
4. 证明 `(x - y)^2 >= 0`
5. 求满足约束的最小值：
   - 目标：最小化 `x + y`
   - 约束：`x >= 0, y >= 0, x + 2y >= 10`
6. 判断整型约束是否可满足：
   - `x + y = 7`
   - `x > 0`
   - `y > 0`
   - `x, y ∈ Z`

**来源：**
- https://github.com/Z3Prover/z3
- https://microsoft.github.io/z3guide/docs/logic/intro/
- https://theory.stanford.edu/~nikolaj/programmingz3.html
- https://github.com/Z3Prover/doc/tree/master/programmingz3/code

---

## 6. 单位换算（Pint 方向）

1. 将 `5 miles` 转换为 `kilometers`
2. 将 `26.2 miles` 转换为 `kilometers`
3. 将 `1 joule` 转换为 `millijoule`
4. 将 `100 parsec` 转换为 `kilometer`
5. 将 `1 hour` 转换为 `second`
6. 将 `25 degree_Celsius` 转换为 `kelvin`
7. 将 `1 liter` 转换为 `milliliter`

**来源：**
- https://github.com/hgrecco/pint
- https://pint.readthedocs.io/en/stable/advanced/defining.html
- https://github.com/hgrecco/pint/blob/master/pint/default_en.txt

---

## 7. 解释型数学主题（Explain / What is）

### 7.1 代数与分析
1. 什么是群？
2. 什么是环和域？
3. 什么是 Banach 空间？
4. 什么是 Lebesgue 积分？
5. 什么是一致收敛？

### 7.2 拓扑与逻辑
6. 什么是紧致性？
7. 什么是连通性？
8. 什么是命题逻辑和谓词逻辑的区别？

### 7.3 范畴论与优化
9. 什么是函子（functor）？
10. 什么是自然变换？
11. 什么是凸优化？
12. 什么是梯度下降？

### 7.4 图论与信息论
13. 什么是欧拉路径？
14. 什么是熵（entropy）？
15. 什么是信道容量？

**来源：**
- https://aimath.org/textbooks/approved-textbooks/
- https://openstax.org/subjects/math
- https://ocw.mit.edu/courses/mathematics/

---

## 8. 适合做 benchmark 的统一输入格式建议

### 8.1 符号计算
```json
{
  "task_type": "symbolic_math",
  "input": {
    "operation": "solve",
    "expression": "x**2 - 5*x + 6",
    "variable": "x"
  },
  "expected_output": ["2", "3"]
}
```

### 8.2 矩阵计算
```json
{
  "task_type": "linear_algebra",
  "input": {
    "operation": "eigenvalues",
    "matrix": [[2, 1], [1, 2]]
  },
  "expected_output": {"1": 1, "3": 1}
}
```

### 8.3 证明/约束
```json
{
  "task_type": "logic_prove",
  "input": {
    "operation": "prove",
    "formula": "x**2 + y**2 >= 2*x*y"
  },
  "expected_output": "PROVED"
}
```

### 8.4 单位换算
```json
{
  "task_type": "unit_conversion",
  "input": {
    "value": 26.2,
    "from_unit": "miles",
    "to_unit": "kilometers"
  },
  "expected_output": "42.1648128 kilometer"
}
```

### 8.5 解释型问题
```json
{
  "task_type": "explanation",
  "input": {
    "topic": "functor"
  },
  "expected_output": "structured_explanation"
}
```

---

## 9. 说明

- 本文件是按 `/math` skill 的路由能力整理的 **问题清单**。
- 它不是单一数学题库，而是把：
  1. 符号计算
  2. 线性代数
  3. 数论与组合
  4. 逻辑/约束求解
  5. 单位换算
  6. 数学概念解释  
  统一放到一个问题集合里。
- 后续如果你要做 benchmark，可以把这里的题目进一步拆成：
  - `sympy_tasks.json`
  - `z3_tasks.json`
  - `pint_tasks.json`
  - `explain_tasks.json`

