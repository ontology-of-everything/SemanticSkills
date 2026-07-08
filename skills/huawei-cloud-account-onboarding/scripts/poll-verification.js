#!/usr/bin/env node
/**
 * Poll a verification session every POLL_INTERVAL seconds until it reaches a
 * terminal state, printing status transitions along the way.
 *
 * Usage: node poll-verification.js <verification_id>
 * Env:   HUAWEICLOUD_ONBOARDING_BASE_URL              default http://127.0.0.1:3923
 *        HUAWEICLOUD_ONBOARDING_POLL_INTERVAL_SECONDS default 3
 *        HUAWEICLOUD_ONBOARDING_POLL_TIMEOUT_SECONDS  default 600 (safety cap)
 *
 * Exit codes: 0 approved · 2 rejected · 3 expired · 4 poll timeout / error
 */
'use strict';

const BASE_URL = process.env.HUAWEICLOUD_ONBOARDING_BASE_URL || 'http://127.0.0.1:3923';
const INTERVAL = Number(process.env.HUAWEICLOUD_ONBOARDING_POLL_INTERVAL_SECONDS || 3);
const TIMEOUT = Number(process.env.HUAWEICLOUD_ONBOARDING_POLL_TIMEOUT_SECONDS || 600);

const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RED = '\x1b[31m';
const CYAN = '\x1b[36m';
const DIM = '\x1b[2m';
const RESET = '\x1b[0m';

const id = process.argv[2];
if (!id) {
  console.error('usage: node poll-verification.js <verification_id>');
  process.exit(4);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const deadline = Date.now() + TIMEOUT * 1000;
  let lastStatus = null;

  while (Date.now() < deadline) {
    let body;
    try {
      const res = await fetch(`${BASE_URL}/v1/verifications/${id}`);
      body = await res.json();
      if (!res.ok) {
        console.error(`${RED}查询失败：HTTP ${res.status} ${JSON.stringify(body)}${RESET}`);
        process.exit(4);
      }
    } catch (err) {
      console.error(`${RED}无法连接 mock 服务（${BASE_URL}）：${err.message}${RESET}`);
      process.exit(4);
    }

    if (body.status !== lastStatus) {
      lastStatus = body.status;
      const ts = new Date().toLocaleTimeString('zh-CN', { hour12: false });
      switch (body.status) {
        case 'pending':
          console.log(`${DIM}[${ts}]${RESET} ${CYAN}等待扫码…${RESET}`);
          break;
        case 'scanned':
          console.log(`${DIM}[${ts}]${RESET} ${YELLOW}已扫码，请在手机上完成认证${RESET}`);
          break;
        case 'approved':
          console.log(`${DIM}[${ts}]${RESET} ${GREEN}实名认证已通过${RESET}`);
          console.log('RESULT=approved');
          process.exit(0);
          break;
        case 'rejected':
          console.log(`${DIM}[${ts}]${RESET} ${RED}认证被拒绝${RESET}${body.reason ? `（${body.reason}）` : ''}`);
          console.log('RESULT=rejected');
          process.exit(2);
          break;
        case 'expired':
          console.log(`${DIM}[${ts}]${RESET} ${RED}二维码已失效，请重新生成${RESET}`);
          console.log('RESULT=expired');
          process.exit(3);
          break;
        default:
          console.log(`${DIM}[${ts}]${RESET} 未知状态：${body.status}`);
      }
    }

    await sleep(INTERVAL * 1000);
  }

  console.error(`${RED}轮询超过安全上限 ${TIMEOUT}s，停止。${RESET}`);
  console.log('RESULT=poll_timeout');
  process.exit(4);
}

main();
