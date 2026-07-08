#!/usr/bin/env node
/**
 * Mock real-name verification (实名认证) server.
 *
 * Industry-standard three-part shape (Feishu QR login / Alipay certify /
 * Stripe Identity): create session -> poll status -> terminal state.
 *
 * Endpoints:
 *   GET  /healthz                              liveness probe
 *   POST /v1/verifications                     create a verification session
 *   GET  /v1/verifications/{id}                poll session status
 *   GET  /v1/customers/me/verification-status  account-level status
 *   GET  /verify/{id}                          H5 page the phone opens (marks "scanned")
 *   POST /verify/{id}/decision                 H5 page submits approve / reject
 *
 * Session states: pending -> scanned -> approved | rejected; pending-only
 * sessions expire after QR_TTL_SECONDS (scanned sessions never expire).
 *
 * Env:
 *   HUAWEICLOUD_ONBOARDING_MOCK_PORT        default 3923
 *   HUAWEICLOUD_ONBOARDING_QR_TTL_SECONDS   default 180
 */
'use strict';

const http = require('node:http');
const os = require('node:os');
const crypto = require('node:crypto');

const PORT = Number(process.env.HUAWEICLOUD_ONBOARDING_MOCK_PORT || 3923);
const QR_TTL_SECONDS = Number(process.env.HUAWEICLOUD_ONBOARDING_QR_TTL_SECONDS || 180);

/** @type {Map<string, object>} */
const sessions = new Map();
const account = { verified: false, verified_at: null, method: null };

function lanIp() {
  const nets = os.networkInterfaces();
  for (const name of Object.keys(nets)) {
    for (const net of nets[name] || []) {
      if (net.family === 'IPv4' && !net.internal) return net.address;
    }
  }
  return '127.0.0.1';
}
const HOST_IP = lanIp();

function nowIso() {
  return new Date().toISOString();
}

/** Lazily flip a stale pending session to expired (scanned never expires). */
function withExpiry(session) {
  if (session.status === 'pending' && Date.now() > Date.parse(session.expires_at)) {
    session.status = 'expired';
  }
  return session;
}

function publicView(session) {
  const s = withExpiry(session);
  return {
    verification_id: s.verification_id,
    status: s.status,
    created_at: s.created_at,
    expires_at: s.expires_at,
    scanned_at: s.scanned_at,
    completed_at: s.completed_at,
    reason: s.reason,
    verify_url: s.verify_url,
  };
}

function sendJson(res, code, body) {
  const data = JSON.stringify(body, null, 2);
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(data);
}

function sendHtml(res, code, html) {
  res.writeHead(code, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(html);
}

function notFound(res) {
  sendJson(res, 404, { error_code: 'ONBOARD.0404', error_msg: 'resource not found' });
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', (chunk) => {
      raw += chunk;
      if (raw.length > 65536) reject(new Error('body too large'));
    });
    req.on('end', () => resolve(raw));
    req.on('error', reject);
  });
}

function page(title, bodyHtml) {
  return `<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title}</title>
<style>
  body{margin:0;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
       background:#f5f6f8;display:flex;justify-content:center;align-items:center;min-height:100vh}
  .card{background:#fff;border-radius:16px;box-shadow:0 4px 24px rgba(0,0,0,.08);
        padding:32px 28px;max-width:340px;width:88%;text-align:center}
  h1{font-size:20px;margin:0 0 6px;color:#1a1a1a}
  .sub{color:#8a8f99;font-size:13px;margin-bottom:24px}
  .mock{display:inline-block;background:#fff3e0;color:#b26a00;border-radius:6px;
        font-size:11px;padding:2px 8px;margin-bottom:16px}
  button{width:100%;border:0;border-radius:10px;padding:14px 0;font-size:16px;
         cursor:pointer;margin-top:10px}
  .approve{background:#c7000b;color:#fff}
  .reject{background:#eceef1;color:#5c6370}
  .state{font-size:40px;margin-bottom:12px}
</style></head><body><div class="card">${bodyHtml}</div>
</body></html>`;
}

function verifyPage(session) {
  const s = withExpiry(session);
  if (s.status === 'expired') {
    return page('二维码已失效', `<div class="state">&#9203;</div><h1>二维码已失效</h1>
      <div class="sub">请回到终端重新生成一张二维码</div>`);
  }
  if (s.status === 'approved' || s.status === 'rejected') {
    const ok = s.status === 'approved';
    return page('认证已完成', `<div class="state">${ok ? '&#9989;' : '&#10060;'}</div>
      <h1>${ok ? '实名认证已通过' : '认证已拒绝'}</h1>
      <div class="sub">本次会话已结束，可关闭此页面</div>`);
  }
  // pending / scanned -> mark scanned and show the decision buttons
  if (s.status === 'pending') {
    s.status = 'scanned';
    s.scanned_at = nowIso();
  }
  return page('华为云实名认证（Mock）', `
    <div class="mock">MOCK 演示环境 · 不采集任何真实身份信息</div>
    <h1>华为云实名认证</h1>
    <div class="sub">会话 ${s.verification_id.slice(0, 8)}… · 请确认本次实名认证</div>
    <button class="approve" onclick="decide('approve')">通过认证</button>
    <button class="reject" onclick="decide('reject')">拒绝</button>
    <script>
      function decide(action){
        fetch('/verify/${s.verification_id}/decision',{method:'POST',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({action:action})})
        .then(function(){location.reload()})
        .catch(function(){alert('提交失败，请重试')});
      }
    </script>`);
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const path = url.pathname;

  try {
    if (req.method === 'GET' && path === '/healthz') {
      return sendJson(res, 200, { ok: true, service: 'onboarding-mock', host_ip: HOST_IP });
    }

    if (req.method === 'POST' && path === '/v1/verifications') {
      if (account.verified) {
        return sendJson(res, 409, {
          error_code: 'ONBOARD.0409',
          error_msg: 'account already real-name verified',
          verified_at: account.verified_at,
        });
      }
      const id = crypto.randomUUID();
      const created = Date.now();
      const session = {
        verification_id: id,
        status: 'pending',
        created_at: new Date(created).toISOString(),
        expires_at: new Date(created + QR_TTL_SECONDS * 1000).toISOString(),
        scanned_at: null,
        completed_at: null,
        reason: null,
        verify_url: `http://${HOST_IP}:${PORT}/verify/${id}`,
      };
      sessions.set(id, session);
      return sendJson(res, 201, publicView(session));
    }

    let m = path.match(/^\/v1\/verifications\/([0-9a-f-]{36})$/);
    if (req.method === 'GET' && m) {
      const session = sessions.get(m[1]);
      if (!session) return notFound(res);
      return sendJson(res, 200, publicView(session));
    }

    if (req.method === 'GET' && path === '/v1/customers/me/verification-status') {
      return sendJson(res, 200, { ...account });
    }

    m = path.match(/^\/verify\/([0-9a-f-]{36})$/);
    if (req.method === 'GET' && m) {
      const session = sessions.get(m[1]);
      if (!session) return sendHtml(res, 404, page('无效链接', '<h1>无效的认证链接</h1>'));
      return sendHtml(res, 200, verifyPage(session));
    }

    m = path.match(/^\/verify\/([0-9a-f-]{36})\/decision$/);
    if (req.method === 'POST' && m) {
      const session = sessions.get(m[1]);
      if (!session) return notFound(res);
      withExpiry(session);
      if (session.status !== 'scanned' && session.status !== 'pending') {
        return sendJson(res, 409, {
          error_code: 'ONBOARD.0410',
          error_msg: `session is ${session.status}, decision not allowed`,
        });
      }
      let action;
      try {
        action = JSON.parse((await readBody(req)) || '{}').action;
      } catch {
        return sendJson(res, 400, { error_code: 'ONBOARD.0400', error_msg: 'invalid JSON body' });
      }
      if (action !== 'approve' && action !== 'reject') {
        return sendJson(res, 400, {
          error_code: 'ONBOARD.0400',
          error_msg: 'action must be "approve" or "reject"',
        });
      }
      session.status = action === 'approve' ? 'approved' : 'rejected';
      session.completed_at = nowIso();
      if (action === 'reject') session.reason = 'user rejected on phone';
      if (action === 'approve') {
        account.verified = true;
        account.verified_at = session.completed_at;
        account.method = 'qr_mock';
      }
      return sendJson(res, 200, publicView(session));
    }

    return notFound(res);
  } catch (err) {
    return sendJson(res, 500, { error_code: 'ONBOARD.0500', error_msg: String(err.message || err) });
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log('[onboarding-mock] listening on:');
  console.log(`  local : http://127.0.0.1:${PORT}`);
  console.log(`  lan   : http://${HOST_IP}:${PORT}   <- QR codes point here`);
  console.log(`  qr ttl: ${QR_TTL_SECONDS}s (pending only; scanned sessions never expire)`);
});
