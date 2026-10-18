# -*- coding: utf-8 -*-
"""예시 보고서를 만든다. 가상의 커피 브랜드 A사이고, 회사와 숫자는 모두 가상이다.

    python3 examples/build_report.py              # examples/out/sample-report.docx
    python3 examples/build_report.py --overwrite  # 이미 있으면 덮어쓴다

먼저 도표와 캡처를 만든다.
    node tools/render.mjs examples/exhibits.json --out examples/out
    python3 tools/captures.py examples/exhibits.json --src examples --out examples/out

본문 숫자는 exhibits.json 에서 다시 계산해 확인한다(숫자를 지어내지 않는다).
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import report_docx as rd  # noqa: E402

OUT = os.path.join(HERE, 'out')
SOURCE = '출처: A사 주문 데이터베이스, 결제 완료 기준 (가상 데이터)'


def fig(name):
    path = os.path.join(OUT, name + '.png')
    if not os.path.exists(path):
        sys.exit(f'그림이 없습니다: {path}\n먼저 render.mjs 와 captures.py 를 돌려 주세요.')
    return path


def check_numbers():
    """본문에 쓰는 숫자를 설정 파일에서 다시 계산한다. 어긋나면 멈춘다."""
    spec = json.load(open(os.path.join(HERE, 'exhibits.json'), encoding='utf-8'))
    c = {x['id']: x for x in spec['charts']}
    now, before = (s['values'] for s in c['fig1-channel-orders']['series'])
    mix = c['fig2-monthly-mix']['series']
    inq = c['fig4-inquiries']['series'][0]['values']
    monthly_totals = [sum(s['values'][i] for s in mix) for i in range(6)]
    facts = {
        '2025 합계': sum(before), '2026 합계': sum(now),
        '정기구독 증가': now[3] - before[3], '자사몰 증가': now[0] - before[0], '배달앱 감소': before[1] - now[1],
        '도표2 월평균': sum(monthly_totals) / 6, '6월 합계': monthly_totals[5],
        '6월 정기구독과 재구매': mix[0]['values'][5] + mix[1]['values'][5],
        '문의 합계': sum(inq), '배송 관련 문의': sum(inq[:3]),
    }
    expect = {
        '2025 합계': 4830, '2026 합계': 5430, '정기구독 증가': 340, '자사몰 증가': 340, '배달앱 감소': 130,
        '도표2 월평균': 5430, '6월 합계': 5780, '6월 정기구독과 재구매': 4170, '문의 합계': 1075, '배송 관련 문의': 834,
    }
    wrong = {k: (facts[k], v) for k, v in expect.items() if facts[k] != v}
    if wrong:
        sys.exit(f'본문 숫자와 설정 파일이 다릅니다: {wrong}')


def build(path, overwrite):
    doc = rd.new_document(title='A사 온라인 주문 채널 점검 보고서', author='보고서 예시')
    rd.cover(doc, 'A사 온라인 주문 채널 점검 보고서', author='보고서 예시', date='2026년 7월 3일')
    rd.source_line(doc, '이 보고서의 회사와 숫자는 모두 가상입니다. 작성 방식을 보여 주는 예시입니다.')

    rd.h1(doc, '핵심 요약')
    rd.body(doc, '온라인 주문은 자사몰 정기구독을 중심으로 키워야 합니다. '
                 '2026년 상반기 주문 기록과 고객 문의가 같은 쪽을 가리킵니다.')
    rd.numbered(doc, [
        ('정기구독이 가장 빠르게 늡니다. ', '월평균 주문이 420건에서 760건으로 81% 늘었습니다.'),
        ('자사몰 고객이 다시 삽니다. ', '6월 재구매율은 자사몰 46%, 배달앱 19%입니다.'),
        ('배송이 약점입니다. ', '상반기 고객 문의 1,075건 가운데 78%(834건)가 배송 과정에서 생겼습니다.'),
    ])

    rd.spacer(doc)
    rd.h1(doc, '1. 배경과 핵심 질문')
    rd.body(doc, 'A사는 원두를 자사몰, 배달앱, 오픈마켓에서 팝니다. 2026년 상반기 전체 주문은 늘었지만, '
                 '가장 큰 채널인 배달앱 주문은 줄었습니다. 이 보고서는 한 가지 질문에 답합니다. '
                 '어느 채널에 힘을 모아야 합니까.')

    rd.spacer(doc)
    rd.h1(doc, '2. 채널별 주문: 정기구독이 가장 빠르게 늘었습니다')
    rd.exhibit_title(doc, '도표 1.', '채널별 월평균 주문 수', '(단위: 건)')
    rd.exhibit_img(doc, fig('fig1-channel-orders'), 165)
    rd.source_line(doc, SOURCE + '. 2025년과 2026년 1~6월')
    rd.spacer(doc)
    rd.body(doc, '전체 월평균 주문은 4,830건에서 5,430건으로 12% 늘었습니다. 늘어난 600건은 정기구독과 '
                 '자사몰에서 340건씩 나왔고, 배달앱은 130건 줄었습니다.')
    rd.body(doc, '배달앱이 줄고 자사몰과 정기구독이 늘었으므로, 일부 고객이 배달앱에서 자사몰로 옮겼을 가능성이 있습니다(추정). '
                 '수수료가 없는 채널로 옮겨 가는 흐름이라 A사에는 좋은 변화입니다. '
                 '자사몰 첫 화면에 정기구독 상품을 올려 이 흐름을 키웁니다.')

    rd.spacer(doc)
    rd.h1(doc, '3. 재구매: 자사몰 고객이 두 배 넘게 다시 삽니다')
    rd.exhibit_title(doc, '도표 2.', '월별 주문 구성', '(단위: 건)')
    rd.exhibit_img(doc, fig('fig2-monthly-mix'), 165)
    rd.source_line(doc, SOURCE + '. 2026년 1~6월')
    rd.spacer(doc)
    rd.body(doc, '6월 주문 5,780건 가운데 정기구독과 재구매가 4,170건(72%)입니다. '
                 '신규 주문은 1월 1,800건에서 6월 1,610건으로 조금씩 줄었습니다.')
    rd.spacer(doc)
    rd.exhibit_title(doc, '도표 3.', '채널별 재구매율', '(단위: %)')
    rd.exhibit_img(doc, fig('fig3-repurchase-rate'), 165)
    rd.source_line(doc, SOURCE + '. 그달 주문한 고객 가운데 앞서 주문한 적이 있는 고객 비율')
    rd.spacer(doc)
    rd.body(doc, '자사몰 재구매율은 1월 38%에서 6월 46%로 올랐고, 배달앱은 19~22%에 머물렀습니다. '
                 '고객을 다시 데려오는 힘은 자사몰이 두 배 넘게 큽니다. '
                 '신규 고객은 배달앱에서 만나되, 두 번째 주문은 자사몰로 옮기게 해야 합니다.')

    rd.spacer(doc)
    rd.h1(doc, '4. 고객 문의: 배송 과정이 가장 큰 약점입니다')
    rd.exhibit_title(doc, '도표 4.', '유형별 고객 문의 수', '(단위: 건)')
    rd.exhibit_img(doc, fig('fig4-inquiries'), 165)
    rd.source_line(doc, '출처: A사 고객센터 문의 기록, 2026년 1~6월 (가상 데이터). 주황 막대는 배송 과정에서 생긴 문의입니다')
    rd.spacer(doc)
    rd.body(doc, '상반기 문의 1,075건 가운데 배송 지연, 원두 신선도, 포장 파손이 834건(78%)입니다. '
                 '셋 다 배송 과정에서 생깁니다. 구매 후기에도 같은 불만이 보입니다(도표 5). '
                 '정기구독은 정해진 날 도착해야 하는 상품이므로, 구독을 키우기 전에 배송부터 고쳐야 합니다.')
    rd.spacer(doc)
    rd.exhibit_title(doc, '도표 5.', '자사몰 구매 후기 화면')
    rd.exhibit_img(doc, fig('cap1-product-reviews'), 170)
    rd.source_line(doc, '출처: A사 자사몰 상품 화면 (2026년 6월 22일 캡처, 예시 화면). '
                        '주황 테두리는 배송 지연을 말한 후기입니다.')

    rd.spacer(doc)
    rd.h1(doc, '5. 제안')
    rd.body(doc, '세 가지를 이 순서로 제안합니다. 앞의 일이 끝나야 뒤의 일이 효과를 냅니다.')
    rd.numbered(doc, [
        ('배송 계약을 다시 봅니다. ', '지연과 파손 기준을 계약에 넣고, 기준을 넘으면 업체를 바꿉니다.'),
        ('자사몰 첫 화면을 바꿉니다. ', '정기구독 상품을 첫 화면 맨 위에 올립니다.'),
        ('배달앱 고객을 자사몰로 옮깁니다. ', '배달앱 주문 상자에 자사몰 첫 구독 쿠폰을 넣습니다.'),
    ])
    rd.spacer(doc)
    rd.exhibit_title(doc, '표 1.', '채널별 요약')
    rd.data_table(
        doc, ['채널', '월평균 주문 (건)', '6월 재구매율', '제안'],
        [['자사몰', '1,580', '46%', '첫 화면에 정기구독'],
         ['배달앱', '2,180', '19%', '자사몰로 옮기기'],
         ['오픈마켓', '910', '확인 필요', '지금대로 유지'],
         ['정기구독', '760', '해당 없음', '배송을 고친 뒤 키우기'],
         ['합계', '5,430', '', '']],
        widths=[30, 32, 30, 58], aligns=['left', 'right', 'right', 'left'], bold_rows=[4],
        note='오픈마켓은 고객 정보를 받지 못해 재구매율을 셀 수 없습니다.')

    rd.h1(doc, '부록 A. 보조 자료', page_break=True)
    rd.exhibit_title(doc, '도표 A1.', '자사몰 방문 경로', '(단위: %)')
    rd.exhibit_img(doc, fig('fig5-traffic-sources'), 165)
    rd.source_line(doc, '출처: A사 자사몰 방문 기록, 2026년 1~6월 (가상 데이터)')
    rd.spacer(doc)
    rd.exhibit_title(doc, '도표 A2.', '지역별 정기구독 신청 수', '(단위: 건)')
    rd.exhibit_img(doc, fig('fig6-region-panels'), 150)
    rd.source_line(doc, SOURCE + '. 2025년과 2026년 1~2분기')

    return rd.save(doc, path, overwrite=overwrite)


def main():
    ap = argparse.ArgumentParser(description='예시 보고서 만들기')
    ap.add_argument('--out', default=os.path.join(OUT, 'sample-report.docx'))
    ap.add_argument('--overwrite', action='store_true', help='이미 있는 파일을 덮어쓴다')
    a = ap.parse_args()
    check_numbers()
    print(build(a.out, a.overwrite))


if __name__ == '__main__':
    main()
