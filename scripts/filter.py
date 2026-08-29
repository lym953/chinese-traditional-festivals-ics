#!/usr/bin/env python3
"""从 ChinaCalendar 的 cal_festival.ics 中筛出纯传统/古代节日。

用法: python scripts/filter.py <上游ics> <输出ics>

上游 cal_festival.ics 把传统节日和现代纪念日混在一起（元旦、国庆节、
全国爱耳日、中华慈善日……）。本脚本按标题白名单保留传统节日，
其余全部剔除。白名单是显式的——上游新增的条目默认被排除，
不会悄悄混进现代节日。
"""
import collections
import re
import sys

# 保留的节日。按标题前缀匹配（三伏/数九的标题带日期范围后缀）。
KEEP_PREFIXES = [
    # 年节
    "『除夕』", "『春节』", "『元宵节』", "『北方小年』", "『南方小年』",
    # 春
    "『龙抬头』", "『社日节』", "『花朝节』", "『上巳节』", "『寒食节』", "『清明节』",
    # 夏秋
    "『端午节』", "『七夕节』", "『中元节』", "『中秋节』", "『重阳节",
    # 冬
    "『下元节』", "『寒衣节』", "『腊八节』",
    # 杂节气：三伏、数九
    "『初伏』", "『中伏』", "『末伏』",
    "『冬一九』", "『冬二九』", "『冬三九』", "『冬四九』", "『冬五九』",
    "『冬六九』", "『冬七九』", "『冬八九』", "『冬九九』",
]

# “老年节”是 1989 年才追加的现代称谓，去掉。
RENAMES = [("SUMMARY:『重阳节（老年节）』", "SUMMARY:『重阳节』")]


def main(src_path: str, dst_path: str) -> int:
    with open(src_path, encoding="utf-8") as fh:
        lines = fh.read().splitlines(keepends=True)

    out: list[str] = []
    block: list[str] = []
    in_event = False
    kept: list[str] = []
    dropped: list[str] = []

    for line in lines:
        if line.startswith("BEGIN:VEVENT"):
            in_event, block = True, [line]
        elif in_event:
            block.append(line)
            if line.startswith("END:VEVENT"):
                summary = next(
                    (b[len("SUMMARY:"):].strip() for b in block if b.startswith("SUMMARY:")),
                    "",
                )
                if any(summary.startswith(p) for p in KEEP_PREFIXES):
                    out.extend(block)
                    kept.append(summary)
                else:
                    dropped.append(summary)
                in_event = False
        else:
            out.append(line)

    text = "".join(out)
    for old, new in RENAMES:
        text = text.replace(old, new)
    text = text.replace(
        "X-WR-CALNAME:中华人民共和国节日纪念日日历", "X-WR-CALNAME:中国传统节日"
    )
    text = re.sub(
        r"X-WR-CALDESC:[^\r\n]*",
        "X-WR-CALDESC:中国传统节日（不含现代纪念日）· 数据来自 YangH9/ChinaCalendar",
        text,
    )

    if not kept:
        print("错误：一条都没保留，上游格式可能变了", file=sys.stderr)
        return 1

    with open(dst_path, "w", encoding="utf-8") as fh:
        fh.write(text)

    names = collections.Counter(re.sub(r"』.*", "』", s) for s in kept)
    print(f"保留 {len(kept)} 条 / {len(names)} 种，剔除 {len(dropped)} 条")
    for name, count in sorted(names.items()):
        print(f"  {name} ×{count}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
