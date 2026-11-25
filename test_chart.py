import unittest
from datetime import date, datetime
from chart import branch_dates, qimen_chart, ziwei_chart


class CalendarTests(unittest.TestCase):
    def test_published_table_tennis_chart(self):
        chart = qimen_chart(datetime.fromisoformat('1995-05-07T20:00:00+08:00'))
        self.assertEqual((chart['日柱'], chart['时柱'], chart['局']), ('戊戌', '壬戌', 4))
        board = chart['盘面']
        self.assertEqual((board['chief_star'], board['chief_to'], board['chief_door_to']), ('天英', 8, 8))
        self.assertEqual(board['doors'][8], '景')
        self.assertIn('壬', board['sky'][7])

    def test_solar_term_boundary(self):
        corrected = datetime.fromisoformat('2026-11-22T15:12:00')
        for time, expected in [('15:15', '立冬'), ('15:30', '小雪')]:
            with self.subTest(time=time):
                instant = datetime.fromisoformat(f'2026-11-22T{time}:00+08:00')
                self.assertEqual(qimen_chart(instant, corrected)['节气'], expected)

    def test_late_zi(self):
        before = qimen_chart(datetime.fromisoformat('2000-01-06T23:10:00+08:00'))
        after = qimen_chart(datetime.fromisoformat('2000-01-07T00:10:00+08:00'))
        self.assertEqual((before['日柱'], before['时柱']), (after['日柱'], after['时柱']))

    def test_new_year_and_transformations(self):
        chart = ziwei_chart(datetime.fromisoformat('2000-02-05T12:00:00+08:00'), None, '女')
        self.assertEqual(chart['农历'], [2000, 1, 1])
        self.assertEqual(chart['生年四化'], ['太阳', '武曲', '太阴', '天同'])
        self.assertEqual(len(chart['十二宫']), 12)
        self.assertEqual(len({period['限命'] for period in chart['大限']}), 12)

    def test_branch_dates_include_both_ends(self):
        days = branch_dates(date(2000, 1, 7), date(2000, 1, 19), '子')
        self.assertEqual([day['日期'] for day in days], ['2000-01-07', '2000-01-19'])
