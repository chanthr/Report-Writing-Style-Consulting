# 4. Word 문서 조립

보고서는 빌드 스크립트 하나로 Word 문서(docx)를 만듭니다. 서식은 [`tools/report_docx.py`](../tools/report_docx.py)에 기본값으로 들어 있습니다.
서식 함수를 보고서마다 복사하지 않습니다. 필요한 것이 없으면 이 모듈을 넓힙니다.

## 4.1 빌드 스크립트

```python
import sys; sys.path.insert(0, "<스킬 폴더>/tools")
import report_docx as rd

doc = rd.new_document(title="A사 온라인 주문 채널 점검")
rd.cover(doc, "A사 온라인 주문 채널 점검", author="작성자 이름", date="2026년 7월 3일")
rd.h1(doc, "핵심 요약")
rd.body(doc, "온라인 주문은 정기구독에 집중해야 합니다.")
rd.spacer(doc)
rd.exhibit_title(doc, "도표 1.", "채널별 월평균 주문 수", "(단위: 건)")
rd.exhibit_img(doc, "시각자료/도표1_채널별주문.png", 165)
rd.source_line(doc, "출처: A사 주문 데이터베이스 (2026년 1~6월)")
rd.data_table(doc, ["채널", "월평균 주문"], [["자사몰", "1,580"]], widths=[120, 50], aligns=["left", "right"])
rd.save(doc, "보고서.docx")
```

전체 본보기는 [`examples/build_report.py`](../examples/build_report.py)입니다.

## 4.2 함수

| 함수 | 하는 일 |
| --- | --- |
| `new_document(title, author)` | A4, 좌우 여백 20mm, 위아래 18mm, 기본 글꼴 |
| `cover(doc, title, author, date)` | 표지. 제목 한 줄과 작성자, 작성일 |
| `h1(doc, text, page_break=False)` | 대제목. 14pt 남색 굵게, 아래 실선 |
| `h2(doc, text)` | 소제목. 12pt 파란색 굵게 |
| `body(doc, parts, bold_quotes=False)` | 본문 문단. 글이나 `[(글, 굵게)]` 목록. `bold_quotes=True`면 작은따옴표로 묶은 말을 굵게 씁니다 |
| `numbered(doc, items)` | 번호 목록. `[(굵은 머리말, 나머지 글)]` |
| `spacer(doc)` | 빈 줄 하나 |
| `exhibit_title(doc, label, title, unit)` | 도표와 표 위 제목 줄 |
| `exhibit_img(doc, path, width_mm)` | 그림. 가운데 정렬, 아래 출처 줄과 같은 쪽에 둡니다 |
| `source_line(doc, text)` | 출처 줄. 10pt 회색 |
| `note_line(doc, text)` | 표 주석. `* `로 시작합니다 |
| `placeholder(doc, text)` | 나중에 사람이 그림을 넣을 빈 상자 |
| `data_table(doc, header, rows, widths, aligns, vmerge, bold_rows, note)` | 회색 머리줄 표. `widths`는 열 비율이고 합이 본문 폭에 맞춰집니다. `note`를 주면 표 아래 주석을 표와 같은 쪽에 붙입니다 |
| `save(doc, path, overwrite=False)` | 저장. 이미 있는 파일은 덮어쓰지 않습니다 |

## 4.3 레이아웃 기본값

| 항목 | 값 |
| --- | --- |
| 용지와 여백 | A4, 좌우 20mm, 위아래 18mm |
| 글꼴 | Freesentation. 바꾸려면 환경변수 `REPORT_FONT` |
| 표지 | 띠 없이 제목 한 줄(가운데, 20pt 굵게). 아래 오른쪽에 `작성자:`, `작성일:` (12pt 굵게) |
| 대제목 | 14pt 남색 굵게, 아래 실선 |
| 소제목 | 12pt 파란색 굵게 |
| 본문 | 12pt, 줄 간격 1.35, 양쪽 정렬 |
| 표, 도표 제목 | 12pt |
| 출처, 주석 | 10pt 회색. 표 주석은 `* `로 시작합니다 |
| 그림 폭 | 캡처는 본문 폭 가득(170mm), 도표는 165mm. 가운데 정렬 |

docx는 글꼴 파일을 담지 않습니다. 문서를 여는 컴퓨터에 Freesentation이 없으면 다른 글꼴로 보입니다. 받는 사람에게는 PDF로 보내거나, 스킬의 `fonts/`를 설치해 두게 합니다.

## 4.4 빈 줄을 넣는 자리

블록 사이는 문단 간격 대신 빈 줄(`rd.spacer(doc)`)로 띄웁니다.

1. 제목(대제목, 소제목) 앞. 바로 위가 제목이거나 쪽의 맨 위면 넣지 않습니다.
2. 표의 앞과 뒤.
3. 도표 설명 문단과 다음 블록 사이.

도표 제목, 그림, 출처 줄 사이에는 넣지 않습니다.

## 4.5 사람이 고친 문서가 정본입니다

사람이 Word에서 고친 docx가 있으면 그 파일이 정본입니다. 빌드를 다시 돌려 덮어쓰지 않습니다(`rd.save`가 막습니다).
검증용으로 다시 만들 때는 늘 다른 이름이나 임시 폴더에 저장합니다.

정본에 내용을 더할 때는 정본을 열어, 그 안의 문단과 그림과 표 줄을 본떠 끼워 넣습니다. 서식이 본뜬 블록에서 따라오므로 사람이 바꾼 글자 크기, 간격, 그림 폭이 그대로 남습니다.

```python
from docx import Document
doc = Document("정본.docx")
t = rd.find_par(doc, "도표 4.")                      # 본뜰 도표 제목
src = t.getnext().getnext()                          # 그 도표의 출처 줄
new_t = rd.clone_after(src, t)                       # 출처 줄 뒤에 제목 복제
rd.add_parts(new_t, [("도표 5. ", False), ("새 제목", True)], clear=True)
img = rd.clone_after(new_t, t.getnext())             # 그림 문단 복제
rd.swap_image(doc, img, "시각자료/새도표.png")         # 폭은 원래 그림, 높이는 새 비율
rd.append_row(rd.table_after(rd.find_par(doc, "표 2.")), ["6월", "1,640", "46%"])
rd.replace_in(rd.find_par(doc, "2. 분석:"), "4개", "5개")
rd.save(doc, "정본_v2.docx")
```

| 함수 | 하는 일 |
| --- | --- |
| `find_par(doc, startswith)` | 그 글로 시작하는 첫 문단 |
| `table_after(p)` | 문단 뒤에 나오는 첫 표 |
| `clone_after(anchor, template)` | 문단이나 표를 복제해 anchor 바로 뒤에 넣습니다 |
| `add_parts(p, parts, clear)` | 문단 글을 씁니다. 글자 서식은 그 문단의 첫 글자를 본뜹니다 |
| `set_run_texts(p, texts)` | 글자 묶음마다 글만 바꿉니다. 표 제목처럼 서식이 나뉜 문단에 씁니다 |
| `replace_in(p, old, new)` | 문단 안 글을 바꿉니다. 없으면 멈춥니다 |
| `swap_image(doc, p, path)` | 그림 문단의 그림을 바꿉니다 |
| `append_row(tbl, values)` | 표 끝에 줄을 더합니다. 마지막 줄을 본뜹니다 |
| `table_like(anchor, template, header, rows, widths)` | 정본 표 서식을 본떠 열 수가 다른 새 표를 만듭니다 |

1. 도표 번호를 밀 때는 새 도표를 넣기 전에 옛 번호부터 바꿉니다.
2. 사람이 쓴 문장은 숫자만 바꿉니다. 새로 쓴 문장은 따로 알립니다.
3. 본문의 캡처를 부록으로 옮길 때는 복제하지 않고 문단 요소를 그대로 옮깁니다(lxml `addnext`는 요소를 옮깁니다). 도표 제목, 그림, 출처 줄, 해설 문단을 한 묶음으로 옮기고, 부록 대제목에는 `page_break_before`를 겁니다. 옮긴 뒤 모든 도표 제목과 그림 문단에 `keep_with_next`를 다시 겁니다.
4. 사람이 문서를 고쳤다고 하면, 고치기 전에 원래 판과 대조부터 합니다. 원래 판을 임시 폴더에 다시 만들고 두 문서의 문단, 표, 그림 크기를 한 줄씩 비교합니다.

## 4.6 함정

| 함정 | 대응 |
| --- | --- |
| 빌드를 다시 돌려 Word에서 고친 내용을 덮어씀 | `rd.save`는 이미 있는 파일을 덮어쓰지 않습니다. 다른 이름으로 저장합니다 |
| 쪽 나눔이 미리보기와 다름 | LibreOffice 변환본은 Word와 쪽 나눔이 다릅니다. 마지막 확인은 Word에서 합니다 |
| 숫자와 한글 사이가 벌어져 보임 | Word의 자동 간격 기능입니다(예: "10 월 25 일"). 문서 오류가 아닙니다 |
| 받는 사람 화면에서 글꼴이 바뀜 | docx는 글꼴을 담지 않습니다. PDF로 보내거나 글꼴을 설치하게 합니다 |
| 제목과 그림이 다른 쪽으로 갈라짐 | 도표 제목과 그림 문단에 `keep_with_next`가 있는지 봅니다. `exhibit_title`, `exhibit_img`는 기본으로 겁니다 |
