# 奇门与紫微排盘环境

在 GitHub Codespaces 打开仓库后，运行以下命令。示例只使用公开书例和历法测试日期。

```sh
python -m unittest -v
python chart.py qimen 1995-05-07T20:00:00+08:00
python chart.py ziwei 2000-02-05T12:00:00+08:00 --sex 女
python chart.py dates 2000-01-01 2000-01-31 子
```

奇门采用时家转盘拆补、中五寄坤、天禽随芮，子初换日。原问时必须带 UTC 偏移。已有经校正的当地盘时可用 `--chart-time` 传入。公开测试取《神奇之门》世乒赛女团决赛例。

紫微提供命身宫、五行局、十四主星、主要辅曜、生年四化和大限。`dates` 用于将已经选定的地支折算为指定范围内的公历日期。具体事项的用神与时间单位需另按原书校核。

## 开源项目对照

- [lunar-python](https://github.com/6tail/lunar-python) 提供农历和节气，环境固定 1.4.8。
- [qimen-rs 的算法说明](https://github.com/SpenserCai/qimen-rs/blob/main/docs/algorithm-sources.md) 可对照时家拆补、转盘和寄宫口径。
- [iztro](https://github.com/SylarLong/iztro) 提供紫微三方四正和多层运限查询，可作为独立核盘参考。
