# firmware · 固件目录

> **当前状态：空目录，只有约定。** 第一行代码出现在里程碑 1（2026-11-30）前后。

---

## 为什么先定目录再写代码

因为这块板子会被重新生成很多次（每次改 CubeMX 配置、每次换 Cube.AI 模型）。**如果不把"生成的东西"和"手写的东西"分开，手写代码迟早会被生成器覆盖掉。**

这是很多人踩过的坑：改了三天的手写逻辑，重新生成一次工程，全没了。

---

## 目录约定

```
firmware/
  perception/            # 感知板 · STM32H743VIT6
    Core/                # CubeMX 生成（可以重新生成，尽量不手改）
      Inc/  Src/
    App/                 # ★ 我们手写的全部代码
      Inc/
      Src/
        judge.c          # S1–S4 → 三档判定（M6）
        postproc.c       # 反量化 + NMS（M5）
        sonar.c          # 超声触发与测距（M7）
        comm.c           # 板间串口协议（M5）
        mem_plan.c       # 静态内存分配表（M5）
    ai/                  # Cube.AI 生成的模型代码（不手改，不提交权重大文件）
    README.md
  chassis/               # 底盘板 · STM32F103C8T6
    Core/
    App/
      Src/
        ctrl.c           # 100 Hz 控制环 + PID（M9）
        extrap.c         # 帧间运动学补位（M8）
        enc_imu.c        # 编码器与 IMU 采集（M10）
        log.c            # 环形缓冲日志（M4 要用）
    README.md
```

## 三条硬规则

1. **`App/` 里的文件绝不手改生成代码，`Core/` 里的文件绝不手写业务逻辑。** 边界一旦模糊，重新生成时就得靠记忆恢复。
2. **`ai/` 与编译产物不入库。** 只提交生成命令与配置（见 [models/README](../models/README.md)）。
3. **每块板一个 README**，写清：用什么版本的 CubeIDE、烧录方式、依赖哪个 Cube.AI 版本、当前能不能编译通过。

---

## 编译与烧录（待 M1 定型后补全）

```bash
# 预期形态，现在不可用
cd firmware/perception
# 用 STM32CubeIDE 打开 .project，或：
make -j8            # 如果生成了 Makefile 工程
```

烧录：ST-Link V2 + STM32CubeProgrammer。**烧录前确认目标板电压与 SWD 接线**——接错烧 IO 口是常见事故。

---

## 相关文档

- [系统架构](../docs/03_技术方案/01_系统架构.md)（任务划分与协议）
- [硬件选型与资源账](../docs/03_技术方案/02_硬件选型与资源账.md)（内存账）
- [代码规范](../docs/05_规范/02_代码规范.md)
