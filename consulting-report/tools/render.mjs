/* 도표 설정(JSON)을 읽어 보고서용 도표를 PNG 로 저장한다.
 *
 * 실행: node tools/render.mjs <설정.json> [--out <폴더>]
 * 결과: <폴더>/<도표 id>.png  (3배 해상도, 흰 바탕). --out 을 안 주면 설정 파일이 있는 폴더.
 * 설정 형식은 rules/3-exhibits.md. 설정 파일에 "charts" 가 없으면 아무것도 만들지 않는다.
 *
 * 처음 한 번: 이 스킬 폴더에서 npm install, npx playwright install chromium
 * 크로미움을 못 띄우면 설치된 Google Chrome 으로 다시 시도한다.
 */
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

const here = path.dirname(fileURLToPath(import.meta.url));

const args = process.argv.slice(2);
const specPath = args.find((a) => !a.startsWith("--"));
if (!specPath) {
  console.error("사용법: node tools/render.mjs <설정.json> [--out <폴더>]");
  process.exit(2);
}
const outIdx = args.indexOf("--out");
const specAbs = path.resolve(specPath);
const outDir = path.resolve(outIdx >= 0 ? args[outIdx + 1] : path.dirname(specAbs));
const spec = JSON.parse(fs.readFileSync(specAbs, "utf8"));
if (!Array.isArray(spec.charts) || spec.charts.length === 0) {
  console.log("charts 항목이 없어 만들 도표가 없습니다.");
  process.exit(0);
}
const ids = spec.charts.map((c) => c.id);
const dup = ids.filter((id, i) => !id || ids.indexOf(id) !== i);
if (dup.length) {
  console.error("도표 id 가 비었거나 겹칩니다:", dup);
  process.exit(2);
}

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch {
  console.error("Playwright 가 없습니다. 이 스킬 폴더에서 npm install 을 먼저 돌려 주세요.");
  process.exit(1);
}

async function launch() {
  try {
    return await chromium.launch();
  } catch (first) {
    try {
      return await chromium.launch({ channel: "chrome" });
    } catch {
      console.error("크로미움을 띄우지 못했습니다. npx playwright install chromium 을 돌려 주세요.");
      throw first;
    }
  }
}

const browser = await launch();
const page = await browser.newPage({ viewport: { width: (spec.width || 680) + 80, height: 900 }, deviceScaleFactor: 3 });
const errors = [];
page.on("pageerror", (e) => errors.push(String(e)));
await page.addInitScript((d) => { window.SPEC = d; }, spec);
await page.goto(pathToFileURL(path.join(here, "chart.html")).href, { waitUntil: "load" });
await page.waitForFunction(() => window.CHARTS_READY === true || window.CHARTS_ERROR, null, { timeout: 30000 }).catch(() => {});
const drawError = await page.evaluate(() => window.CHARTS_ERROR || (window.CHARTS_READY ? null : "30초 안에 그리기를 마치지 못했습니다"));
if (drawError) errors.push(drawError);
if (errors.length) {
  console.error("도표를 그리다 오류가 났습니다:", errors);
  await browser.close();
  process.exit(1);
}
const fontOk = await page.evaluate(() => document.fonts.check('500 13px "Rep"'));
if (!fontOk) console.warn("경고: Freesentation 글꼴을 읽지 못해 시스템 글꼴로 그렸습니다(fonts/ 폴더를 확인해 주세요)");

fs.mkdirSync(outDir, { recursive: true });
for (const fig of await page.locator(".fig").all()) {
  const id = await fig.getAttribute("id");
  await fig.screenshot({ path: path.join(outDir, `${id}.png`) });
  const box = await fig.boundingBox();
  console.log(`${id}.png  ${Math.round(box.width)}x${Math.round(box.height)} (화면 px)`);
}
await browser.close();
