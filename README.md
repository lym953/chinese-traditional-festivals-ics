# 中国传统节日日历（ICS 订阅）

只含**传统与古代节日**的 iCalendar 订阅源，不含任何现代纪念日。

上巳节、花朝节、社日节、寒衣节、下元节、龙抬头这些今天已经少有人过、
但在古代很重要的节日，现有的中文日历订阅源要么没有，要么和"全国爱耳日""中华慈善日"
一类的现代纪念日混在一起。这个仓库从上游数据里把它们筛出来，每周自动更新。

## 订阅

**一键订阅（macOS / iOS）**

<webcal://lym953.github.io/chinese-traditional-festivals-ics/cal_traditional.ics>

**手动添加**

```
https://lym953.github.io/chinese-traditional-festivals-ics/cal_traditional.ics
```

- **Apple Calendar（macOS）**：`文件 > 新建日历订阅…`，粘贴上面的地址
- **Apple Calendar（iOS）**：`设置 > 日历 > 账户 > 添加账户 > 其他 > 添加已订阅的日历`
- **Google Calendar**：`其他日历 + > 通过网址`
- **Outlook**：`添加日历 > 从 Internet 订阅`

> 订阅是**只读**的，会自动跟随本仓库更新；不想要了直接删掉整个订阅日历即可。
> 如果用「导入」而不是「订阅」，事件会被复制成你自己的事件，之后不再更新，
> 而且只能一条条删除。

## 收录内容

『中伏』 『初伏』 『春节』 『末伏』 『除夕』 『七夕节』 『上巳节』 
『下元节』 『中元节』 『中秋节』 『元宵节』 『冬一九』 『冬七九』 
『冬三九』 『冬九九』 『冬二九』 『冬五九』 『冬八九』 『冬六九』 
『冬四九』 『寒衣节』 『寒食节』 『清明节』 『社日节』 『端午节』 
『腊八节』 『花朝节』 『重阳节』 『龙抬头』 『北方小年』 『南方小年』 

按时序分组：

| 时节 | 节日 |
|---|---|
| 年节 | 腊八节 · 北方小年 · 南方小年 · 除夕 · 春节 · 元宵节 |
| 春 | 龙抬头 · 社日节 · 花朝节 · 上巳节 · 寒食节 · 清明节 |
| 夏 | 端午节 · 七夕节 |
| 秋 | 中元节 · 中秋节 · 重阳节 · 下元节 · 寒衣节 |
| 杂节气 | 三伏（初伏 · 中伏 · 末伏）· 数九（冬一九 … 冬九九） |

**明确排除**：元旦、劳动节、国庆节、妇女节、儿童节、青年节、建军节、教师节、
记者节、护士节、植树节、情人节、母亲节、父亲节，以及各类"全国 X 日""世界 X 日"
"国际 X 日"和周年纪念日。

每个事件都保留了上游的详细说明（典故、历史沿革）。

## 数据来源

数据全部来自 **[YangH9/ChinaCalendar](https://github.com/YangH9/ChinaCalendar)**，
上游订阅地址：

```
https://yangh9.github.io/ChinaCalendar/cal_festival.ics
```

该项目以 MIT 许可证发布，感谢作者。本仓库**不生产任何日历数据**，
只做一件事：按标题白名单从上游筛掉现代纪念日。

如果你想要完整版（含现代纪念日）、二十四节气、法定节假日调休、农历干支，
请直接访问上游项目，它提供了更多文件。

## 工作原理

```
上游 cal_festival.ics  ──每周一──▶  scripts/filter.py  ──▶  docs/cal_traditional.ics
      (208 条)                        白名单过滤              (62 条)
```

[`.github/workflows/update.yml`](.github/workflows/update.yml) 每周一抓取上游、
重新过滤、校验后提交。GitHub Pages 从 `docs/` 目录发布。

白名单是**显式**的（见 [`scripts/filter.py`](scripts/filter.py) 的 `KEEP_PREFIXES`）：
上游新增的条目默认被排除，不会有现代节日悄悄混进来。代价是上游若新增传统节日，
需要手动加进白名单。

CI 里有一道校验，输出文件如果混进了标题含"纪念日/国庆/建军/劳动节/元旦"等字样的
事件，构建直接失败。

### 为什么需要每周更新

iCalendar 的 `RRULE`（重复规则）**只支持公历**。像国庆节可以写成
`RRULE:FREQ=YEARLY` 一劳永逸，但七夕（农历七月初七）、上巳（三月初三）、
中元节在公历上的日期每年都不同，无法用 RRULE 表达 —— 只能逐年枚举。

所以上游是一个滚动窗口（当前覆盖 2025–2027），需要定期补充新年份的数据，
订阅端也就必须持续跟进。这正是"订阅"相对"导入"的价值。

### 关于时间戳文件

`LAST_RUN` 每次运行都会更新并提交。这不是多余的 —— GitHub 会**停用 public 仓库中
60 天没有新 commit 的定时工作流**，且只有 commit 能重置计时器。上游一年才更新几次，
没有这个文件的话，工作流会在最需要它之前被悄悄关掉。

## 本地运行

```bash
curl -fsSL -o upstream.ics https://yangh9.github.io/ChinaCalendar/cal_festival.ics
python3 scripts/filter.py upstream.ics docs/cal_traditional.ics
```

无第三方依赖，Python 3.9+ 即可。

## 许可证

代码以 MIT 发布，见 [LICENSE](LICENSE)。

日历数据版权归 [YangH9/ChinaCalendar](https://github.com/YangH9/ChinaCalendar) 所有，
同为 MIT 许可证。
