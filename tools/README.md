# tools · 工具链

> **状态：空目录，只有约定。**

PC 端的活全在这里：量化、评估、画图、数据检查。**板端一天测几十次，PC 端一天能跑几千帧——大部分结论应该先在 PC 上得到。**

---

## 目录

```
tools/
  quantize/          # 浮点 → INT8 量化、导出、精度标定
  eval/              # 算 S1–S4、风险—覆盖率曲线、A/B 对比
  requirements.txt   # 依赖（带版本号）
```

---

## 统一约定（三个脚本目录都适用）

1. **命令行参数化。** 不许把路径写死。用 `argparse`，`--input` / `--output` 必须支持。
2. **打印进度与统计。** 处理了多少、跳过多少、为什么跳过。
3. **固定随机种子。** 有随机性的地方都要 `--seed`，默认 42。
4. **输出可被下游读。** 中间结果存 CSV/JSON，不要只 print。
5. **依赖带版本号。** `numpy==1.26.4`，不是 `numpy`。**版本漂移会让三个月前的数复现不出来。**

---

## 环境

```bash
cd tools
python -m venv .venv
. .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`.venv/` 已在 `.gitignore` 里。

---

## 预计要写的脚本

| 脚本 | 里程碑 | 干什么 | 输出 |
|---|---|---|---|
| `quantize/quantize_int8.py` | M2 | 浮点模型 → INT8，校准集来自 val | `.tflite` + 量化参数 |
| `quantize/calibrate.py` | M2 | 标定量化范围，对比不同校准集 | 精度对比表 |
| `eval/metrics.py` | M2 | 算 mAP、逐帧错误判定 | `metrics.csv` |
| `eval/signals.py` | M2 | 逐帧算 S1–S4（PC 端模拟量化推理时顺手统计） | `signals.csv` |
| `eval/risk_coverage.py` | M2 | 画风险—覆盖率曲线，扫阈值 | 曲线 PNG + 目标点 |
| `eval/correlate.py` | M2 | S1–S4 相关系数矩阵（**可能是"只有两个信号有效"**） | 矩阵 + 结论 |
| `eval/ab_compare.py` | M5 | A/B 两组（补位开/关）统计与检验 | 分布图 + 检验结果 |

**`signals.py` 是核心**：它决定 [创新点 ①](../docs/03_技术方案/03_帧级可信度判定.md) 能不能在 PC 上先验证。PC 端能拿到中间激活，所以 S2 在这里可以做得比板端更细——**先用 PC 版证明"信号有用"，再去解决板端怎么拿**。顺序不能反。

---

## 相关文档

- [帧级可信度判定](../docs/03_技术方案/03_帧级可信度判定.md)（S1–S4 定义）
- [指标定义与验收口径](../docs/03_技术方案/06_指标定义与验收口径.md)（指标怎么算）
- [代码规范](../docs/05_规范/02_代码规范.md)（Python 部分）
