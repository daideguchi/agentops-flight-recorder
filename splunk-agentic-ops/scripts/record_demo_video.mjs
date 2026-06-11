import { chromium } from 'playwright';
import { mkdir, rm, writeFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(scriptDir, '..');
const defaultOut = path.join(root, 'media', 'agentops-flight-recorder-demo-recording.mp4');
const outputPath = path.resolve(process.argv[2] || defaultOut);
const frameDir = path.join(root, 'media', '.recording_frames');
const dashboardPath = path.join(root, 'prototype', 'flight-recorder-dashboard.html');
const chromeExecutable =
  process.env.CHROME_EXECUTABLE ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

let frameIndex = 0;
const concatRows = [];

async function capture(page, seconds) {
  frameIndex += 1;
  const file = path.join(frameDir, `frame-${String(frameIndex).padStart(3, '0')}.png`);
  await page.screenshot({ path: file, fullPage: false });
  concatRows.push(`file '${file.replaceAll("'", "'\\''")}'`);
  concatRows.push(`duration ${seconds}`);
}

async function main() {
  await rm(frameDir, { recursive: true, force: true });
  await mkdir(frameDir, { recursive: true });
  await mkdir(path.dirname(outputPath), { recursive: true });

  const browser = await chromium.launch({
    headless: true,
    executablePath: chromeExecutable,
  });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();

  await page.goto(pathToFileURL(dashboardPath).href, { waitUntil: 'domcontentloaded' });
  await capture(page, 3.2);

  await page.locator('#demo-runner').scrollIntoViewIfNeeded();
  await capture(page, 3.4);

  await page.locator('[data-demo-filter="all"]').click();
  await capture(page, 3.6);

  await page.locator('[data-demo-filter="risk"]').click();
  await capture(page, 3.8);

  await page.locator('[data-demo-filter="approval"]').click();
  await capture(page, 3.8);

  await page.locator('[data-demo-spl]').click();
  await capture(page, 4.4);

  await page.locator('[data-demo-ai]').click();
  await capture(page, 7.2);

  await page.locator('.two-col').scrollIntoViewIfNeeded();
  await capture(page, 4.2);

  await page.locator('.spl-grid').scrollIntoViewIfNeeded();
  await capture(page, 4.2);

  await page.locator('.timeline').scrollIntoViewIfNeeded();
  await capture(page, 4.6);

  await page.locator('#demo-runner').scrollIntoViewIfNeeded();
  await capture(page, 4.6);

  await browser.close();

  const lastFrame = path.join(frameDir, `frame-${String(frameIndex).padStart(3, '0')}.png`);
  concatRows.push(`file '${lastFrame.replaceAll("'", "'\\''")}'`);
  await writeFile(path.join(frameDir, 'frames.txt'), `${concatRows.join('\n')}\n`, 'utf8');

  execFileSync(
    'ffmpeg',
    [
      '-y',
      '-f',
      'concat',
      '-safe',
      '0',
      '-i',
      path.join(frameDir, 'frames.txt'),
      '-vf',
      'fps=30,format=yuv420p',
      '-c:v',
      'libx264',
      '-preset',
      'veryfast',
      '-crf',
      '22',
      outputPath,
    ],
    { stdio: 'inherit' },
  );

  await rm(frameDir, { recursive: true, force: true });
  console.log(outputPath);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : String(error));
  process.exitCode = 1;
});
