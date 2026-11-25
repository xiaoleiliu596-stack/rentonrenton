"""奇门、紫微排盘与候选日期。"""
import argparse
import json
from datetime import date, datetime, timedelta, timezone
from lunar_python import Solar
import qimen
import ziwei

BRANCHES = qimen.Z
STEMS = qimen.G
BEIJING = timezone(timedelta(hours=8))
TERMS = {
    '冬至': (1,7,4), '小寒': (2,8,5), '大寒': (3,9,6),
    '立春': (8,5,2), '雨水': (9,6,3), '惊蛰': (1,7,4),
    '春分': (3,9,6), '清明': (4,1,7), '谷雨': (5,2,8),
    '立夏': (4,1,7), '小满': (5,2,8), '芒种': (6,3,9),
    '夏至': (-9,-3,-6), '小暑': (-8,-2,-5), '大暑': (-7,-1,-4),
    '立秋': (-2,-5,-8), '处暑': (-1,-4,-7), '白露': (-9,-3,-6),
    '秋分': (-7,-1,-4), '寒露': (-6,-9,-3), '霜降': (-5,-8,-2),
    '立冬': (-6,-9,-3), '小雪': (-5,-8,-2), '大雪': (-4,-7,-1),
}


def cycle(day):
    return (day-date(2000,1,7)).days % 60


def ganzhi(index):
    return STEMS[index%10] + BRANCHES[index%12]


def chart_clock(local, corrected):
    if local.utcoffset() is None:
        raise ValueError('原钟表时间必须带 UTC 偏移，例如 +08:00。')
    if corrected is not None and corrected.tzinfo is not None:
        raise ValueError('校正后的当地盘时请省略 UTC 偏移。')
    return corrected if corrected is not None else local.replace(tzinfo=None)


def lunar_time(dt):
    return Solar.fromYmdHms(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second).getLunar()


def qimen_chart(local, corrected=None):
    clock = chart_clock(local,corrected)
    solar_term = lunar_time(local.astimezone(BEIJING)).getPrevJieQi()
    term = solar_term.getName()
    day = cycle(clock.date()+timedelta(days=int(clock.hour==23)))
    branch = ((clock.hour+1)//2)%12
    hour = STEMS[(2*(day%10)+branch)%10] + BRANCHES[branch]
    head = (day-day%5)%12
    if head in (0,3,6,9):
        yuan = 0
    elif head in (2,5,8,11):
        yuan = 1
    else:
        yuan = 2
    ju = TERMS[term][yuan]
    board = qimen.rotating(1 if ju>0 else -1,abs(ju),hour)
    empty = ''.join(BRANCHES[(board['xun_index']+i)%12] for i in (10,11))
    return {'原问时':local.isoformat(),'当地盘时':clock.isoformat(),'节气':term,
            '交节北京时间':solar_term.getSolar().toYmdHms(),'日柱':ganzhi(day),'时柱':hour,
            '元':'上中下'[yuan],'局':ju,'时空':empty,'盘面':board}


def ziwei_chart(local, corrected, sex):
    clock = chart_clock(local,corrected)
    lunar = lunar_time(clock)
    month, day, year = lunar.getMonth(), lunar.getDay(), lunar.getYear()
    adjusted_month = (abs(month) + int(month<0 and day>15)-1)%12+1
    yg,yb = (year-4)%10,(year-4)%12
    hour = ((clock.hour+1)//2)%12
    ming,shen,ju,rows,palace_stem = ziwei.chart(yg,yb,adjusted_month,day,hour)
    direction = 1 if ((yg%2==0)==(sex=='男')) else -1
    limits = []
    for i in range(12):
        b = (ming+direction*i)%12
        limits.append({'起虚岁':ju+10*i,'限命':BRANCHES[b],'原宫干':STEMS[palace_stem(b)]})
    return {'原钟表时':local.isoformat(),'当地盘时':clock.isoformat(),'农历':[year,month,day],
            '安星月':adjusted_month,'命':BRANCHES[ming],'身':BRANCHES[shen],'局':ju,
            '十二宫':rows,'生年四化':ziwei.SIHUA_FX[STEMS[yg]],'大限':limits}


def branch_dates(start,end,branch):
    if end<start:
        raise ValueError('终点须不早于起点。')
    offset=(BRANCHES.index(branch)-cycle(start)%12)%12
    return [{'日期':(start+timedelta(days=i)).isoformat(),'日柱':ganzhi(cycle(start)+i)}
            for i in range(offset,(end-start).days+1,12)]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest='command',required=True)
    for name in ('qimen','ziwei'):
        sub=subs.add_parser(name)
        sub.add_argument('time',type=datetime.fromisoformat,help='带 UTC 偏移的当地钟表时')
        sub.add_argument('--chart-time',type=datetime.fromisoformat,help='校正后的当地日期时间')
        if name=='ziwei':
            sub.add_argument('--sex',required=True,choices=['男','女'])
    ds=subs.add_parser('dates',help='将已选定的地支映射到公历日')
    ds.add_argument('start',type=date.fromisoformat)
    ds.add_argument('end',type=date.fromisoformat)
    ds.add_argument('branch',choices=list(BRANCHES))
    args=parser.parse_args()
    try:
        if args.command=='qimen':
            result=qimen_chart(args.time,args.chart_time)
        elif args.command=='ziwei':
            result=ziwei_chart(args.time,args.chart_time,args.sex)
        else:
            result=branch_dates(args.start,args.end,args.branch)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
