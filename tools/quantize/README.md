# quantize · 量化脚本

> **状态：未开始。** 里程碑 2（2027-02-19）的核心工作。

---

## 要做什么

把浮点检测模型转成 INT8，并标定精度损失。

```
浮点模型 (.onnx / .h5)
   │  ① 校准集（来自 dataset 的 val，不能是 train）
   ▼
训练后量化 (PTQ)  →  scale / zero-point
   │  ② 导出
   ▼
INT8 模型 (.tflite / Cube.AI 可读格式)
   │  ③ 评估
   ▼
精度报告（浮点 vs INT8，按类别分解）
```

**关键选择：校准集必须是 val，不能是 train。** 用 train 校准会让量化范围"见过"所有样本，测出来的精度虚高——这是量化流程里最常见的自欺。

---

## 配置文件（预想形态）

`configs/yolo_lc_192.yaml`：

```yaml
model:
  name: st_yolo_lc_v1
  input_size: 192
  classes: 3

quantize:
  scheme: int8_ptq          # 训练后量化，不做 QAT（时间不够）
  calibration:
    dataset: dataset/v1.0
    split: val              # ★ 必须是 val
    n_samples: 200          # 校准样本数，少了不稳、多了没必要
    method: minmax          # 先 minmax，再试 percentile(99.9)
  per_channel: true         # 逐通道量化，精度更好
  
eval:
  dataset: dataset/v1.0
  split: val
  metric: map50
  report_per_class: true
```

---

## 预计脚本

| 脚本 | 干什么 | 输出 |
|---|---|---|
| `quantize_int8.py` | 主流程：加载 → 校准 → 量化 → 导出 | INT8 模型 |
| `calibrate.py` | 对比不同校准集 / 不同方法（minmax vs percentile） | 精度对比表 |
| `check_ops.py` | 检查模型里有没有 Cube.AI 不支持的算子 | 算子清单 + 风险提示 |

**`check_ops.py` 建议尽早写**——如果模型里有不支持的算子，越早知道越好，别等到部署那天才发现要换模型。

---

## 量化掉了多少

**必须按类别分解**，不只看总 mAP。

小目标、少见类别在量化后掉得最快。如果 total mAP 只掉 2 个点但 hand 类掉了 15 个点，那对手类误检的实验就没法做了——而 hand 恰好是我们专门用来测误检的类。

报告表格长这样：

| 类别 | 浮点 mAP | INT8 mAP | 损失 |
|---|---|---|---|
| material_box | | | |
| obstacle | | | |
| hand | | | |
| **总体** | | | |

**目标：总体损失 < 3 个点**（[验收标准](../../docs/03_技术方案/06_指标定义与验收口径.md)）。任一单类掉超过 8 个点，要在报告里单独说明。

---

## 常见坑（先记着，省得到时候现查）

1. **校准样本太少**（< 50）→ 量化范围估不准，精度随机波动。
2. **校准集与测试集分布不一致** → 板上一跑就崩。校准集要覆盖逆光、模糊这些困难样本。
3. **输入预处理对齐**：训练时是 `(x-127.5)/127.5`，部署时忘了减均值 → 结果全是垃圾，而且看起来像"模型坏了"。
4. **后处理没改定点**：NMS 里还在用 `float`，在 F103 上会慢十倍（H743 有 FPU 好一些，但没必要）。
5. **量化前后标签顺序变化**：有些工具会重排类别，务必用同一张图对比前后框的位置和类别。
