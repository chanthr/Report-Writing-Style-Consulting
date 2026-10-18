---
name: consulting-report
description: 컨설팅 보고서 방식으로 한국어 보고서, 제안서, 성과 보고서를 쓰고 Word 문서로 만든다. 피라미드 구조(결론 먼저, MECE, SCQA 도입부), 데이터마다 해석과 판단과 액션, 건조한 비즈니스 문체, 주황과 회색의 절제된 도표와 표와 캡처, 정해진 Word 레이아웃을 한 흐름으로 다룬다. "보고서 써 줘", "보고서 구조 잡아 줘", "결론이 안 보여", "도표 만들어 줘", "보고서 그래프", "docx 로 만들어 줘", "컨설팅 보고서처럼", "write a consulting-style report", "make report charts" 같은 요청에 쓴다. 문장 어투만 고치는 일도 2-style.md 로 처리한다.
---

# 컨설팅 보고서 작성

결론 하나를 맨 위에 두고, 데이터로 받치고, 절제된 도표와 정해진 레이아웃으로 Word 문서를 만듭니다.
이 파일이 있는 폴더를 아래에서 `$SKILL`이라고 부릅니다.

## 규칙 문서

작업 단계에 맞는 문서를 먼저 끝까지 읽습니다.

| 문서 | 다루는 것 | 읽는 때 |
| --- | --- | --- |
| [`rules/1-structure.md`](rules/1-structure.md) | 피라미드, SCQA, 데이터 블록, 레벨링, 본문과 부록 | 골격을 잡을 때, 초안 흐름을 고칠 때 |
| [`rules/2-style.md`](rules/2-style.md) | 한국어 비즈니스 문체 15개 규칙 | 문장을 쓰거나 다듬을 때 |
| [`rules/3-exhibits.md`](rules/3-exhibits.md) | 도표, 표, 캡처의 문법과 도구 | 그림이 필요할 때 |
| [`rules/4-document.md`](rules/4-document.md) | Word 조립, 레이아웃, 사람이 고친 문서에 덧붙이기 | 문서를 만들거나 고칠 때 |
| [`rules/5-checklist.md`](rules/5-checklist.md) | 제출 전 점검 | 넘기기 전에 |

## 절대 원칙

1. **골격부터 합의합니다.** 결론, 핵심 근거, 세부 근거의 글 트리를 먼저 보여 주고 확인받은 뒤 본문을 씁니다.
2. **숫자를 지어내지 않습니다.** 모든 수치는 받은 원자료에서 옵니다. 없는 값은 "확인 필요"로 비웁니다. 추측은 "(추정)"으로 표시합니다.
3. **캡처 내용을 고치지 않습니다.** 자르기와 테두리만 합니다.
4. **사람이 고친 문서를 덮어쓰지 않습니다.** 이미 있는 docx는 정본입니다. 다시 만들 때는 다른 이름으로 저장하고, 무엇이 달라지는지 먼저 알립니다.
5. **도구를 복사하지 않습니다.** 도표는 `$SKILL/tools/render.mjs`, 캡처는 `$SKILL/tools/captures.py`, 문서는 `$SKILL/tools/report_docx.py`를 그대로 씁니다. 보고서 폴더에는 설정 파일과 빌드 스크립트만 둡니다.
6. **장식하지 않습니다.** 둥근 카드, 칩, 그림자, 아이콘, 여러 색 점을 쓰지 않습니다.

## 흐름

### 1) 재료 확인

무엇을 결정하려는 보고서인지, 독자가 누구인지, 숫자와 캡처가 어디서 오는지 확인합니다.
빠진 것은 한 번에 모아 묻고, 항목마다 왜 필요한지 한 줄을 붙입니다. 핵심 정보 없이 쓰기 시작하지 않습니다.

### 2) 골격

`rules/1-structure.md`로 핵심 질문과 결론을 정하고 피라미드를 세웁니다. 글 트리로 보여 주고 확인받습니다.

### 3) 본문

장마다 데이터, 해석, 판단, 액션으로 씁니다. 문장은 `rules/2-style.md`를 따릅니다.

### 4) 시각자료

`rules/3-exhibits.md` 3.3 표에서 도표 종류를 고르고, 보고서 폴더의 `build/data.json`에 적어 그립니다.

```bash
node $SKILL/tools/render.mjs build/data.json --out 시각자료
python3 $SKILL/tools/captures.py build/data.json --src 캡처원본 --out 시각자료
```

결과 PNG를 직접 열어 숫자, 글자 크기, 테두리 위치를 확인합니다.

### 5) 문서 조립

`build/build_docx.py`에서 `report_docx`를 가져다 씁니다(`rules/4-document.md`). 결과는 새 이름으로 저장합니다.

### 6) 점검

`rules/5-checklist.md`를 차례로 확인하고, 확인한 것과 못 한 것을 나눠 보고합니다.
쪽 나눔은 Word에서 봐야 정확합니다. LibreOffice로만 봤다면 그렇게 적습니다.

## 보고서 작업 폴더

| 위치 | 내용 |
| --- | --- |
| `build/data.json` | 도표 수치(`charts`)와 캡처 설정(`captures`). 맨 위 `_출처`에 출처와 세는 기준 |
| `build/build_docx.py` | 문서 조립 스크립트 |
| `캡처원본/` | 받은 캡처 원본 |
| `시각자료/` | 만든 PNG |

## 처음 한 번

도표나 문서를 처음 만들 때 `$SKILL/node_modules`가 없거나 `python3 -c "import docx, PIL"`이 실패하면, 사용자에게 아래 명령을 보여 주고 허락을 받아 실행합니다.

```bash
cd $SKILL
npm install                       # 도표용 Playwright
npx playwright install chromium   # 도표를 그릴 브라우저
pip install -r requirements.txt   # Pillow, python-docx
```

`npx skills add`로 설치했다면 `$SKILL`은 보통 `~/.claude/skills/consulting-report`나 프로젝트의 `.claude/skills/consulting-report`입니다.

본보기는 `$SKILL/examples/`에 있습니다. 가상의 커피 브랜드 A사 보고서이고, 회사와 숫자는 모두 가상입니다.
