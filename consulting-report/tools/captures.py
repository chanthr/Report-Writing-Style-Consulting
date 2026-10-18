# -*- coding: utf-8 -*-
"""화면 캡처를 보고서용으로 가공한다.

하는 일은 세 가지뿐이다. 사진 내용은 손대지 않는다.
  1. 빈 여백을 잘라 낸다(crop).
  2. 보여 줄 자리에 주황 실선 테두리를 얹는다(marks).
  3. 흰 사진이 흰 종이에 묻히지 않게 바깥에 회색 실선을 두른다.

실행: python3 tools/captures.py <설정.json> [--src <원본 폴더>] [--out <결과 폴더>]
결과: <결과 폴더>/<id>.png   (원본 픽셀 그대로, 확대와 축소 없음)
      --src, --out 을 안 주면 설정 파일이 있는 폴더.

설정 파일의 "captures" 항목 한 개:
  { "id": "캡처_상품_후기", "file": "원본.png", "crop": [x, y, w, h], "marks": [[x, y, w, h], ...] }
  crop 과 marks 는 원본 사진의 픽셀 좌표다. marks 는 없어도 된다.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw

ORANGE = (220, 82, 24)      # #dc5218, 도표의 주황과 같은 색
FRAME = (204, 208, 213)     # #ccd0d5
MARK_W = 3                  # 테두리 굵기(원본 픽셀)


def process(c, src, out):
    path = os.path.join(src, c["file"])
    if not os.path.exists(path):
        print(f"[멈춤] 원본이 없습니다: {path}")
        return False
    im = Image.open(path).convert("RGB")
    cx, cy, cw, ch = c.get("crop") or [0, 0, im.width, im.height]
    cw, ch = min(cw, im.width - cx), min(ch, im.height - cy)
    img = im.crop((cx, cy, cx + cw, cy + ch))
    d = ImageDraw.Draw(img)
    for x, y, w, h in c.get("marks", []):
        if x < cx or y < cy or x + w > cx + cw or y + h > cy + ch:
            print(f"[주의] {c['id']}: 테두리 {[x, y, w, h]} 가 자른 범위를 벗어납니다")
        d.rectangle((x - cx, y - cy, x - cx + w, y - cy + h), outline=ORANGE, width=MARK_W)
    d.rectangle((0, 0, img.width - 1, img.height - 1), outline=FRAME, width=1)
    img.save(os.path.join(out, f"{c['id']}.png"))
    print(f"{c['id']}.png  {img.width}x{img.height}")
    return True


def main():
    ap = argparse.ArgumentParser(description="캡처를 자르고 주황 테두리를 얹는다")
    ap.add_argument("spec")
    ap.add_argument("--src")
    ap.add_argument("--out")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.spec))
    src, out = a.src or base, a.out or base
    caps = json.load(open(a.spec, encoding="utf-8")).get("captures", [])
    if not caps:
        print("captures 항목이 없어 만들 캡처가 없습니다.")
        return 0
    os.makedirs(out, exist_ok=True)
    ok = [process(c, src, out) for c in caps]
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
