# models · 模型说明

> **模型文件不入库**（.tflite / .onnx / .h5 都是 MB 级）。这里放模型卡与"怎么生成它"的命令。

---

## 候选模型

| 模型 | 来源 | 输入 | 大小（INT8） | 状态 |
|---|---|---|---|---|
| `st_yolo_lc_v1` | ST model zoo [R2] | 192×192 | RAM 174.38 KiB / Flash 330.21 KiB | **首选**：官方给全了资源账，先用它跑通链路 |
| SSD-MobileNetV1-0.25 | 常见开源权重 | 192×192 | 约 533 KB Flash / 270 KB RAM（H735 口径） | 备选，[R1] 的复现用的就是这一类 |
| NanoDet-Plus-m-1.0 | [R3] | 320×320 | 约 980 KB | 备选，精度更高但更吃资源 |

**先用最小的跑通，再换大的。** 反过来做，卡住的时候分不清是链路问题还是模型太大。

---

## 模型卡（每个入选用模型填一份）

### `st_yolo_lc_v1`（待补全）

| 项 | 内容 |
|---|---|
| 来源与版本 | ST model zoo，commit `待填` |
| 原始训练数据 | 待查（**报告里必须写清是 COCO 还是别的，我们没有自己训练**） |
| 输入 | 1×192×192×3，INT8，scale/zero-point 待填 |
| 输出 | 待填（几个头、格式、是否需要自己写后处理） |
| 参数量 | 待填 |
| 量化方式 | 训练后量化（PTQ），校准集来自 `val`（版本 v__） |
| mAP（浮点 / INT8） | 待测 |
| 端到端时延（板端） | 待测，见 `results/` |
| 已知问题 | 待填 |

**"我们用的模型是别人训练的"这件事必须写清楚。** 报告里不许含糊成"我们的模型"——我们做的是部署与判定，不是训练。这一点在答辩时被问到，答错就是硬伤。

---

## 生成流程（M1–M2 建立后补全）

```bash
# 1) 下载 / 导出浮点模型（具体命令 M1 完成后填）
# 2) 量化
python tools/quantize/quantize_int8.py \
    --model models/float/st_yolo_lc_v1.onnx \
    --data dataset/v1.0 \
    --input-size 192 \
    --seed 42 \
    --out models/int8/

# 3) 生成 Cube.AI 工程（在 CubeIDE 里操作，步骤见 firmware/perception/README.md）
```

**大文件不进 git。** 需要分发时用 GitHub Release 或学校网盘，并在 Release 说明里写清生成命令与校验和：

```bash
sha256sum models/int8/st_yolo_lc_v1_192_int8.tflite > models/int8/SHA256SUMS
```

`SHA256SUMS` 这类小文本文件**要入库**——它让别人能验证手里的文件是不是同一个。

---

## 许可

| 模型 | 原始许可 | 我们能不能改 / 再分发 |
|---|---|---|
| `st_yolo_lc_v1` | 待查（ST model zoo 仓库 LICENSE） | **用前必查** |
| NanoDet-Plus | Apache-2.0（以仓库为准） | 可以，需保留声明 |

**引用他人的模型，在报告里注明来源与许可。** 见 [引用与学术诚信](../docs/05_规范/06_引用与学术诚信.md)。
