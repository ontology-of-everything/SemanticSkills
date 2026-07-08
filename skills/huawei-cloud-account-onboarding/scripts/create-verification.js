#!/usr/bin/env node
/**
 * Create a real-name verification session and render its QR code in the
 * terminal (colored frame, high-contrast black/white modules for scannability).
 *
 * Usage: node create-verification.js
 * Env:   HUAWEICLOUD_ONBOARDING_BASE_URL  default http://127.0.0.1:3923
 *
 * Stdout ends with a machine-readable line for the orchestrating agent:
 *   VERIFICATION_ID=<uuid>
 */
'use strict';

const QRCode = require('qrcode');

const BASE_URL = process.env.HUAWEICLOUD_ONBOARDING_BASE_URL || 'http://127.0.0.1:3923';

const CYAN = '\x1b[36m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';
const RESET = '\x1b[0m';

/**
 * Render the QR matrix with half-block characters: each printed char covers
 * two module rows (fg = top, bg = bottom). Modules stay pure black-on-white
 * for contrast; only the frame and captions are colored.
 */
function renderQr(text) {
  const qr = QRCode.create(text, { errorCorrectionLevel: 'M' });
  const size = qr.modules.size;
  const data = qr.modules.data;
  const QUIET = 2;
  const total = size + QUIET * 2;
  const dark = (row, col) => {
    const r = row - QUIET;
    const c = col - QUIET;
    if (r < 0 || c < 0 || r >= size || c >= size) return false;
    return data[r * size + c] === 1;
  };

  const FG_BLACK = '\x1b[30m';
  const FG_WHITE = '\x1b[97m';
  const BG_BLACK = '\x1b[40m';
  const BG_WHITE = '\x1b[107m';

  const lines = [];
  for (let row = 0; row < total; row += 2) {
    let line = '';
    for (let col = 0; col < total; col += 1) {
      const top = dark(row, col);
      const bottom = row + 1 < total ? dark(row + 1, col) : false;
      line += (top ? FG_BLACK : FG_WHITE) + (bottom ? BG_BLACK : BG_WHITE) + '\u2580';
    }
    lines.push(line + RESET);
  }

  const width = total;
  const bar = '\u2500'.repeat(width + 2);
  console.log(`${CYAN}\u250c${bar}\u2510${RESET}`);
  for (const line of lines) {
    console.log(`${CYAN}\u2502${RESET} ${line} ${CYAN}\u2502${RESET}`);
  }
  console.log(`${CYAN}\u2514${bar}\u2518${RESET}`);
}

async function main() {
  const res = await fetch(`${BASE_URL}/v1/verifications`, { method: 'POST' });
  const body = await res.json();

  if (res.status === 409) {
    console.log(`${BOLD}账号已完成实名认证${RESET}（${body.verified_at || '时间未知'}），无需重复认证。`);
    console.log('ALREADY_VERIFIED=1');
    return;
  }
  if (!res.ok) {
    console.error(`创建认证会话失败：HTTP ${res.status} ${JSON.stringify(body)}`);
    process.exit(1);
  }

  const ttlSeconds = Math.round((Date.parse(body.expires_at) - Date.parse(body.created_at)) / 1000);

  console.log('');
  console.log(`${CYAN}${BOLD}  华为云实名认证（Mock 演示）${RESET}`);
  console.log(`${DIM}  请用手机（与本机同一 WiFi）扫描下方二维码${RESET}`);
  console.log('');
  renderQr(body.verify_url);
  console.log('');
  console.log(`  ${DIM}链接:${RESET} ${body.verify_url}`);
  console.log(`  ${DIM}有效期:${RESET} ${ttlSeconds}s（扫码后不再过期）`);
  console.log('');
  console.log(`VERIFICATION_ID=${body.verification_id}`);
}

main().catch((err) => {
  console.error(`无法连接 mock 服务（${BASE_URL}）：${err.message}`);
  console.error('请先启动：node scripts/mock-server.js');
  process.exit(1);
});
