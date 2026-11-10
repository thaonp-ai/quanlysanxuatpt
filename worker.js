// Web tra cứu P&ID Xưởng Phụ Trợ: đăng nhập + phục vụ web/ + API chỉnh sửa tag.
//
// Đăng nhập
//   - Mọi trang và file (kể cả ảnh bản vẽ, data.json) chỉ mở được sau khi đăng nhập.
//   - Tài khoản quản trị dựng sẵn: tên "admin", mật khẩu = secret ADMIN_PASSWORD đặt trên Cloudflare.
//     Đổi secret này là đăng xuất phiên admin cũ.
//   - Admin tạo/sửa/khóa/xóa tài khoản ở trang /account. Quyền: admin (quản lý tài khoản + sửa tag),
//     editor (sửa tag), viewer (chỉ xem).
//   - Tài khoản lưu trong KV (khóa "auth:users"), mật khẩu băm PBKDF2-SHA256.
//   - Phiên đăng nhập: cookie ký HMAC (khóa SESSION_SECRET nếu có, nếu không tự tạo và lưu ở KV "auth:secret").
//
// API
//   GET  /api/me                 -> { u, name, role }
//   GET  /api/edits              -> { edits, log }
//   POST /api/edits              -> { key, patch | reset:true }  (editor, admin)
//   POST /api/password           -> { old, new }                 (tài khoản tự đổi mật khẩu)
//   GET  /api/users              -> [ { u, name, role, disabled, created, updated } ]   (admin)
//   POST /api/users              -> { action:"save", u, name, role, password?, disabled? } | { action:"delete", u }  (admin)

const KINDS = new Set(["line", "equipment", "valve"]);
const ROLES = { admin: "Quản trị", editor: "Được sửa tag", viewer: "Chỉ xem" };
const MAX_LOG = 5000;
const COOKIE = "pid_session";
const SESSION_DAYS = 30;
const PBKDF2_ITER = 100000;
const MAX_FAIL = 8;
const enc = new TextEncoder();

/* ---------------- helpers ---------------- */
function json(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra },
  });
}
function html(body, status = 200, extra = {}) {
  return new Response(body, {
    status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-frame-options": "DENY",
      "referrer-policy": "same-origin",
      ...extra,
    },
  });
}
function clean(s, max) {
  return typeof s === "string" ? s.replace(/[\u0000-\u001f]/g, " ").trim().slice(0, max) : undefined;
}
function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
const unhex = (s) => new Uint8Array(s.match(/../g).map((h) => parseInt(h, 16)));
const b64u = (s) => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const unb64u = (s) => decodeURIComponent(escape(atob(s.replace(/-/g, "+").replace(/_/g, "/"))));
function safeEq(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}
function cookies(req) {
  const out = {};
  (req.headers.get("cookie") || "").split(/;\s*/).forEach((p) => {
    const i = p.indexOf("=");
    if (i > 0) out[p.slice(0, i)] = p.slice(i + 1);
  });
  return out;
}
function safeNext(n) {
  return typeof n === "string" && n.startsWith("/") && !n.startsWith("//") && !n.startsWith("/login") ? n : "/";
}

/* ---------------- crypto ---------------- */
async function hashPassword(pw, saltHex) {
  const salt = saltHex ? unhex(saltHex) : crypto.getRandomValues(new Uint8Array(16));
  const key = await crypto.subtle.importKey("raw", enc.encode(pw), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt, iterations: PBKDF2_ITER }, key, 256);
  return { salt: hex(salt), hash: hex(bits) };
}
async function sha(s) {
  return hex(await crypto.subtle.digest("SHA-256", enc.encode(s)));
}
let _hmac = null;
async function hmacKey(env) {
  if (_hmac) return _hmac;
  let secret = env.SESSION_SECRET || (await env.EDITS.get("auth:secret"));
  if (!secret) {
    secret = hex(crypto.getRandomValues(new Uint8Array(32)));
    await env.EDITS.put("auth:secret", secret);
  }
  _hmac = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return _hmac;
}
async function sign(env, payload) {
  const body = b64u(JSON.stringify(payload));
  const sig = hex(await crypto.subtle.sign("HMAC", await hmacKey(env), enc.encode(body)));
  return body + "." + sig;
}
async function unsign(env, token) {
  if (!token || !token.includes(".")) return null;
  const [body, sig] = token.split(".");
  const want = hex(await crypto.subtle.sign("HMAC", await hmacKey(env), enc.encode(body)));
  if (!safeEq(sig, want)) return null;
  try { return JSON.parse(unb64u(body)); } catch { return null; }
}

/* ---------------- users ---------------- */
let _users = null, _usersAt = 0;
async function loadUsers(env, fresh = false) {
  if (!fresh && _users && Date.now() - _usersAt < 30000) return _users;
  _users = (await env.EDITS.get("auth:users", "json")) || {};
  _usersAt = Date.now();
  return _users;
}
async function saveUsers(env, users) {
  await env.EDITS.put("auth:users", JSON.stringify(users));
  _users = users;
  _usersAt = Date.now();
}
async function builtinAdminVersion(env) {
  return env.ADMIN_PASSWORD ? (await sha("v1:" + env.ADMIN_PASSWORD)).slice(0, 12) : null;
}
async function currentUser(req, env) {
  const tok = cookies(req)[COOKIE];
  const p = await unsign(env, tok);
  if (!p || !p.u || !(p.exp > Date.now())) return null;
  if (p.u === "admin") {
    const v = await builtinAdminVersion(env);
    return v && p.v === v ? { u: "admin", name: "admin", role: "admin", builtin: true } : null;
  }
  const rec = (await loadUsers(env))[p.u];
  if (!rec || rec.disabled || rec.v !== p.v) return null;
  return { u: p.u, name: rec.name || p.u, role: rec.role };
}
function sessionCookie(token, remember) {
  const age = remember ? `; Max-Age=${SESSION_DAYS * 86400}` : "";
  return `${COOKIE}=${token}; Path=/; HttpOnly; Secure; SameSite=Lax${age}`;
}
function publicUser(u, r) {
  return { u, name: r.name || u, role: r.role, disabled: !!r.disabled, created: r.created, updated: r.updated };
}

/* ---------------- pages ---------------- */
const FONTS = `<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">`;
const BASE_CSS = `
:root{--paper:#f3f5f6;--sheet:#fff;--ink:#15222e;--muted:#5b6a76;--rule:#d5dce1;--line:#0f6e8c;--line-soft:#e1eef2;--mark:#e39b12;--err:#b4432f;--err-soft:#f8e6e2;--ok:#2f7d4f;
--f-disp:"Barlow Condensed","Arial Narrow",system-ui,sans-serif;--f-body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Consolas,monospace;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#0f161c;--sheet:#151f27;--ink:#e3eaef;--muted:#93a3ae;--rule:#2a3843;--line:#4fb3d1;--line-soft:#173039;--mark:#f0b13a;--err:#ec8a74;--err-soft:#3a1f1a;--ok:#6cc890;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#0f161c;--sheet:#151f27;--ink:#e3eaef;--muted:#93a3ae;--rule:#2a3843;--line:#4fb3d1;--line-soft:#173039;--mark:#f0b13a;--err:#ec8a74;--err-soft:#3a1f1a;--ok:#6cc890;color-scheme:dark}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0}
body{background:var(--paper);color:var(--ink);font-family:var(--f-body);font-size:14px;line-height:1.45;min-height:100vh}
button,input,select{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--line);outline-offset:2px}
label{display:flex;flex-direction:column;gap:5px;font-size:12.5px;font-weight:500;color:var(--muted)}
input[type=text],input[type=password],select{font-size:15px;padding:9px 11px;border:1.5px solid var(--rule);border-radius:6px;background:var(--paper);color:var(--ink);width:100%;min-width:0}
input:focus,select:focus{border-color:var(--line);outline:none}
.btn{border:1px solid var(--rule);background:var(--sheet);border-radius:6px;padding:8px 14px;font-size:13.5px;font-weight:500;cursor:pointer}
.btn.primary{background:var(--ink);color:var(--sheet);border-color:var(--ink)}
.btn.danger{color:var(--err)}
.btn:disabled{opacity:.55;cursor:default}
.err{background:var(--err-soft);color:var(--err);border-radius:6px;padding:8px 11px;font-size:13px}
.ok{color:var(--ok);font-size:13px}
.brand{font-family:var(--f-disp);font-weight:700;font-size:22px;letter-spacing:.02em;text-transform:uppercase;line-height:1.05}
.eyebrow{font-family:var(--f-disp);font-weight:600;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
`;

function loginPage({ next = "/", error = "", user = "", setup = false }) {
  return `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Đăng nhập · P&amp;ID Xưởng Phụ Trợ</title>${FONTS}<style>${BASE_CSS}
body{display:grid;place-items:center;padding:24px max(16px,env(safe-area-inset-left,0px)) 24px max(16px,env(safe-area-inset-right,0px));
  background-color:var(--paper);background-image:linear-gradient(var(--rule) 1px,transparent 1px),linear-gradient(90deg,var(--rule) 1px,transparent 1px);background-size:32px 32px;background-position:-1px -1px}
.card{width:100%;max-width:380px;background:var(--sheet);border:1px solid var(--rule);border-radius:10px;overflow:hidden;box-shadow:0 12px 40px rgba(15,30,45,.12)}
.card header{padding:22px 24px 16px;border-bottom:1px solid var(--rule);display:flex;flex-direction:column;gap:6px}
.card header span{font-size:12.5px;color:var(--muted)}
form{padding:20px 24px 24px;display:flex;flex-direction:column;gap:14px}
.chk{flex-direction:row;align-items:center;gap:8px;font-weight:400;color:var(--ink);font-size:13px}
.btn.primary{padding:11px 14px;font-size:15px}
label[for=pw]{margin-bottom:-9px}
.pwbox{position:relative;display:flex}
.pwbox input{padding-right:64px}
.eye{position:absolute;right:5px;top:50%;transform:translateY(-50%);border:0;background:none;color:var(--line);font-size:13px;font-weight:600;padding:6px 9px;border-radius:5px;cursor:pointer}
.eye:hover{background:var(--line-soft)}
.foot{padding:12px 24px;border-top:1px solid var(--rule);font-size:12px;color:var(--muted);background:var(--paper)}
.titleblock{display:grid;grid-template-columns:auto 1fr;font-family:var(--f-mono);font-size:10.5px;color:var(--muted);border-top:1px solid var(--rule)}
.titleblock div{padding:5px 10px;border-right:1px solid var(--rule)}
.titleblock div:last-child{border-right:0}
</style></head><body>
<main class="card">
  <header><div class="eyebrow">Nhà máy Đạm Phú Mỹ</div><div class="brand">P&amp;ID · PFD Xưởng Phụ Trợ</div><span>Tra cứu đường ống, thiết bị, van trên bản vẽ</span></header>
  ${setup ? `<div style="padding:20px 24px" class="err">Web chưa có tài khoản quản trị. Người quản lý cần đặt secret <b>ADMIN_PASSWORD</b> trên Cloudflare (Workers &amp; Pages → quanlysanxuatpt → Settings → Variables and Secrets), rồi đăng nhập với tên <b>admin</b>.</div>` : ""}
  <form method="post" action="/login" autocomplete="on">
    <input type="hidden" name="next" value="${esc(next)}">
    <label>Tên đăng nhập<input type="text" name="u" value="${esc(user)}" autocomplete="username" autocapitalize="none" spellcheck="false" required ${user ? "" : "autofocus"}></label>
    <label for="pw">Mật khẩu</label>
    <div class="pwbox"><input type="password" id="pw" name="p" autocomplete="current-password" required ${user ? "autofocus" : ""}><button type="button" class="eye" id="eye" aria-pressed="false" aria-controls="pw">Hiện</button></div>
    <label class="chk"><input type="checkbox" name="remember" value="1" checked> Giữ đăng nhập trên máy này (${SESSION_DAYS} ngày)</label>
    ${error ? `<div class="err" role="alert">${esc(error)}</div>` : ""}
    <button class="btn primary" type="submit">Đăng nhập</button>
  </form>
  <script>
  (function(){var b=document.getElementById("eye"),i=document.getElementById("pw");
    b.onclick=function(){var show=i.type==="password";i.type=show?"text":"password";b.textContent=show?"Ẩn":"Hiện";b.setAttribute("aria-pressed",show);i.focus();};
    i.form.addEventListener("submit",function(){i.type="password";});})();
  </script>
  <div class="foot">Chưa có tài khoản hoặc quên mật khẩu? Liên hệ người quản lý web để được cấp lại.</div>
</main>
</body></html>`;
}

function accountPage() {
  return `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Tài khoản · P&amp;ID Xưởng Phụ Trợ</title>${FONTS}<style>${BASE_CSS}
.top{background:var(--sheet);border-bottom:1px solid var(--rule);padding-block:10px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;gap:10px 16px;align-items:center;flex-wrap:wrap}
.top a.back{color:var(--line);text-decoration:none;font-weight:500}
.top .me{margin-left:auto;font-size:13px;color:var(--muted)}
.wrap{max-width:980px;margin:0 auto;padding-block:20px 40px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:20px}
section{background:var(--sheet);border:1px solid var(--rule);border-radius:10px;padding:18px 20px;display:flex;flex-direction:column;gap:14px;min-width:0}
h2{margin:0;font-family:var(--f-disp);font-weight:700;font-size:20px;letter-spacing:.03em;text-transform:uppercase}
.hint{margin:0;color:var(--muted);font-size:13px;max-width:70ch}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;align-items:end}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.tbl{overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:640px;font-size:13.5px}
th{text-align:left;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600;padding:8px 10px;border-bottom:1.5px solid var(--rule)}
td{padding:9px 10px;border-bottom:1px solid var(--rule);vertical-align:middle}
td.u{font-family:var(--f-mono);font-weight:500}
tr.off td{color:var(--muted)}
.pill{display:inline-block;font-size:11.5px;padding:2px 8px;border-radius:999px;border:1px solid var(--rule)}
.pill.admin{border-color:var(--mark);color:var(--ink)}
.pill.off{background:var(--err-soft);color:var(--err);border-color:transparent}
td .btn{padding:5px 10px;font-size:12.5px}
.scrim{position:fixed;inset:0;background:rgba(10,18,26,.45);display:grid;place-items:center;padding:16px;z-index:20}
.dlg{background:var(--sheet);border-radius:10px;border:1px solid var(--rule);width:100%;max-width:440px;padding:20px;display:flex;flex-direction:column;gap:12px;max-height:calc(100vh - 32px);overflow:auto}
.dlg h3{margin:0;font-family:var(--f-disp);font-size:20px;text-transform:uppercase;letter-spacing:.03em}
.chk{flex-direction:row;align-items:center;gap:8px;font-weight:400;color:var(--ink);font-size:13px}
.acts{display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap}
.acts .left{margin-right:auto}
</style></head><body>
<div class="top"><a class="back" href="/">← Về trang tra cứu</a><span class="brand" style="font-size:18px">Tài khoản</span><span class="me" id="me"></span><form method="post" action="/logout" style="margin:0"><button class="btn">Đăng xuất</button></form></div>
<div class="wrap">
  <section id="pwSec">
    <h2>Đổi mật khẩu</h2>
    <form id="pwForm" class="grid" autocomplete="on">
      <input type="text" name="username" id="pwUser" autocomplete="username" hidden>
      <label>Mật khẩu hiện tại<input type="password" id="pwOld" autocomplete="current-password" required></label>
      <label>Mật khẩu mới (ít nhất 8 ký tự)<input type="password" id="pwNew" autocomplete="new-password" minlength="8" required></label>
      <label>Nhập lại mật khẩu mới<input type="password" id="pwNew2" autocomplete="new-password" minlength="8" required></label>
      <div class="row"><label class="chk"><input type="checkbox" id="pwShow"> Hiện mật khẩu</label><button class="btn primary" type="submit">Lưu mật khẩu</button><span id="pwMsg"></span></div>
    </form>
  </section>
  <section id="usersSec" hidden>
    <div class="row" style="justify-content:space-between"><h2>Quản lý tài khoản</h2><button class="btn primary" id="btnNew">+ Thêm tài khoản</button></div>
    <p class="hint"><b>Chỉ xem</b>: tra cứu, xuất Excel. <b>Được sửa tag</b>: thêm vào đó sửa tên, ẩn, thêm tag trên bản vẽ. <b>Quản trị</b>: thêm vào đó quản lý tài khoản. Khi khóa tài khoản, đổi quyền hoặc đặt lại mật khẩu, người đó bị đăng xuất trong vòng khoảng 30 giây.</p>
    <div class="tbl"><table><thead><tr><th>Tên đăng nhập</th><th>Họ tên</th><th>Quyền</th><th>Trạng thái</th><th>Cập nhật</th><th></th></tr></thead><tbody id="tbody"><tr><td colspan="6">Đang tải…</td></tr></tbody></table></div>
  </section>
</div>
<div class="scrim" id="scrim" hidden>
  <form class="dlg" id="uForm" role="dialog" aria-modal="true" aria-labelledby="uTitle" autocomplete="off">
    <h3 id="uTitle">Thêm tài khoản</h3>
    <label>Tên đăng nhập (chữ thường, số, . _ -)<input type="text" id="uU" autocapitalize="none" spellcheck="false" required pattern="[a-z0-9._\\-]{3,32}"></label>
    <label>Họ tên (hiện trong lịch sử chỉnh sửa)<input type="text" id="uName" required></label>
    <label>Quyền<select id="uRole"><option value="viewer">Chỉ xem</option><option value="editor">Được sửa tag</option><option value="admin">Quản trị</option></select></label>
    <label><span id="uPwLbl">Mật khẩu (ít nhất 8 ký tự)</span><input type="text" id="uPw" autocomplete="new-password" spellcheck="false"></label>
    <div class="row"><button type="button" class="btn" id="uGen">Tạo mật khẩu ngẫu nhiên</button></div>
    <label class="chk"><input type="checkbox" id="uOff"> Khóa tài khoản (không cho đăng nhập)</label>
    <div class="err" id="uErr" hidden></div>
    <div class="acts"><button type="button" class="btn danger left" id="uDel" hidden>Xóa tài khoản</button><button type="button" class="btn" id="uCancel">Hủy</button><button class="btn primary" type="submit" id="uSave">Lưu</button></div>
  </form>
</div>
<script>
const $=id=>document.getElementById(id);
const ROLES=${JSON.stringify(ROLES)};
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const fmt=iso=>iso?new Date(iso).toLocaleString("vi-VN",{hour12:false}):"";
async function call(url,body){const r=await fetch(url,body?{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(body)}:{cache:"no-store"});
  if(r.status===401){location.href="/login?next=/account";throw new Error("Phiên đăng nhập đã hết");}
  const j=await r.json().catch(()=>({}));if(!r.ok)throw new Error(j.error||("Lỗi "+r.status));return j;}
let ME=null,USERS=[],cur=null;
(async()=>{
  ME=await call("/api/me");
  $("me").textContent=ME.name+" · "+ROLES[ME.role];$("pwUser").value=ME.u;
  if(ME.builtin){$("pwSec").innerHTML='<h2>Đổi mật khẩu</h2><p class="hint">Đây là tài khoản quản trị dựng sẵn. Mật khẩu của nó là secret <b>ADMIN_PASSWORD</b> trên Cloudflare; đổi secret đó để đổi mật khẩu. Nên tạo cho mình một tài khoản quản trị riêng ở bên dưới để dùng hằng ngày.</p>';}
  if(ME.role==="admin"){$("usersSec").hidden=false;load();}
})();
async function load(){USERS=await call("/api/users");render();}
function render(){
  $("tbody").innerHTML=USERS.length?USERS.map((u,i)=>'<tr class="'+(u.disabled?"off":"")+'"><td class="u">'+esc(u.u)+'</td><td>'+esc(u.name)+'</td><td><span class="pill '+u.role+'">'+ROLES[u.role]+'</span></td><td>'+(u.disabled?'<span class="pill off">Đã khóa</span>':"Hoạt động")+'</td><td>'+esc(fmt(u.updated||u.created))+'</td><td><button class="btn" data-i="'+i+'">Sửa</button></td></tr>').join(""):'<tr><td colspan="6">Chưa có tài khoản nào. Bấm “+ Thêm tài khoản”.</td></tr>';
  $("tbody").querySelectorAll("button[data-i]").forEach(b=>b.onclick=()=>open(USERS[b.dataset.i]));
}
function gen(){const a="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789";const r=crypto.getRandomValues(new Uint32Array(12));return [...r].map(x=>a[x%a.length]).join("");}
function open(u){cur=u||null;$("uTitle").textContent=u?"Sửa tài khoản":"Thêm tài khoản";$("uU").value=u?u.u:"";$("uU").readOnly=!!u;$("uName").value=u?u.name:"";$("uRole").value=u?u.role:"viewer";
  $("uPw").value=u?"":gen();$("uPw").required=!u;$("uPwLbl").textContent=u?"Đặt lại mật khẩu (để trống nếu không đổi)":"Mật khẩu (ít nhất 8 ký tự)";
  $("uOff").checked=!!(u&&u.disabled);$("uDel").hidden=!u||u.u===ME.u;$("uErr").hidden=true;$("scrim").hidden=false;setTimeout(()=>(u?$("uName"):$("uU")).focus(),30);}
function close(){$("scrim").hidden=true;}
$("btnNew").onclick=()=>open(null);$("uCancel").onclick=close;$("uGen").onclick=()=>{$("uPw").value=gen();};
$("scrim").addEventListener("click",e=>{if(e.target===$("scrim"))close();});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!$("scrim").hidden)close();});
function showErr(m){$("uErr").textContent=m;$("uErr").hidden=false;}
$("uForm").addEventListener("submit",async e=>{e.preventDefault();
  const body={action:"save",u:$("uU").value.trim().toLowerCase(),name:$("uName").value.trim(),role:$("uRole").value,disabled:$("uOff").checked};
  if($("uPw").value)body.password=$("uPw").value;
  $("uSave").disabled=true;
  try{USERS=await call("/api/users",body);render();close();
    if(body.password){alertBox("Đã lưu. Gửi cho người dùng: tên đăng nhập "+body.u+", mật khẩu "+body.password);} }
  catch(err){showErr(err.message);}finally{$("uSave").disabled=false;}
});
let delArm=0;
$("uDel").onclick=async()=>{if(Date.now()-delArm>4000){delArm=Date.now();$("uDel").textContent="Bấm lần nữa để xóa";setTimeout(()=>$("uDel").textContent="Xóa tài khoản",4000);return;}
  try{USERS=await call("/api/users",{action:"delete",u:cur.u});render();close();}catch(err){showErr(err.message);}};
function alertBox(msg){const s=document.createElement("section");s.innerHTML='<div class="row" style="justify-content:space-between"><b class="ok">'+esc(msg)+'</b><span class="row"><button class="btn">Chép</button><button class="btn">Đóng</button></span></div>';
  const [cp,cl]=s.querySelectorAll("button");cp.onclick=()=>navigator.clipboard.writeText(msg.replace(/^Đã lưu\\. /,"")).then(()=>cp.textContent="Đã chép",()=>{});cl.onclick=()=>s.remove();
  $("usersSec").before(s);}
$("pwShow")&&($("pwShow").onchange=e=>["pwOld","pwNew","pwNew2"].forEach(id=>$(id).type=e.target.checked?"text":"password"));
$("pwForm").addEventListener("submit",async e=>{e.preventDefault();const m=$("pwMsg");m.className="";
  if($("pwNew").value!==$("pwNew2").value){m.className="err";m.textContent="Hai lần nhập mật khẩu mới không khớp.";return;}
  try{await call("/api/password",{old:$("pwOld").value,new:$("pwNew").value});m.className="ok";m.textContent="Đã đổi mật khẩu.";e.target.reset();}
  catch(err){m.className="err";m.textContent=err.message;}});
</script>
</body></html>`;
}

/* ---------------- handlers ---------------- */
async function handleLogin(req, env, url) {
  const users = await loadUsers(env, true);
  const setup = !env.ADMIN_PASSWORD && !Object.keys(users).length;
  if (req.method === "GET") {
    if (await currentUser(req, env)) return Response.redirect(url.origin + safeNext(url.searchParams.get("next")), 302);
    return html(loginPage({ next: safeNext(url.searchParams.get("next")), setup }));
  }
  if (req.method !== "POST") return html("", 405);
  const f = await req.formData();
  const u = (clean(f.get("u"), 40) || "").toLowerCase();
  const p = typeof f.get("p") === "string" ? f.get("p") : "";
  const next = safeNext(f.get("next"));
  const remember = f.get("remember") === "1";
  const fail = (msg) => html(loginPage({ next, error: msg, user: u, setup }), 401);
  if (!u || !p) return fail("Nhập tên đăng nhập và mật khẩu.");

  const fkey = "auth:fail:" + u + ":" + (req.headers.get("cf-connecting-ip") || "");
  const fails = parseInt((await env.EDITS.get(fkey)) || "0", 10);
  if (fails >= MAX_FAIL) return fail("Nhập sai quá nhiều lần. Thử lại sau 15 phút.");

  let payload = null;
  if (u === "admin") {
    if (env.ADMIN_PASSWORD && safeEq(await sha(p), await sha(env.ADMIN_PASSWORD))) payload = { u, v: await builtinAdminVersion(env) };
  } else {
    const rec = users[u];
    if (rec && !rec.disabled && safeEq((await hashPassword(p, rec.salt)).hash, rec.hash)) payload = { u, v: rec.v };
    else if (rec && rec.disabled) return fail("Tài khoản này đã bị khóa. Liên hệ người quản lý web.");
  }
  if (!payload) {
    await env.EDITS.put(fkey, String(fails + 1), { expirationTtl: 900 });
    return fail("Sai tên đăng nhập hoặc mật khẩu.");
  }
  if (fails) await env.EDITS.delete(fkey);
  payload.exp = Date.now() + SESSION_DAYS * 86400000;
  const token = await sign(env, payload);
  return new Response(null, { status: 303, headers: { location: next, "set-cookie": sessionCookie(token, remember), "cache-control": "no-store" } });
}

async function handleEdits(req, env, me) {
  if (req.method === "GET") return json((await env.EDITS.get("state", "json")) || { edits: {}, log: [] });
  if (req.method !== "POST") return json({ error: "Phương thức không hỗ trợ" }, 405);
  if (me.role === "viewer") return json({ error: "Tài khoản của bạn chỉ có quyền xem. Liên hệ người quản lý để được cấp quyền sửa." }, 403);
  let body;
  try { body = await req.json(); } catch { return json({ error: "Dữ liệu gửi lên không đọc được" }, 400); }
  const key = clean(body.key, 200);
  if (!key || !/^(o|n):/.test(key)) return json({ error: "Thiếu mã tag" }, 400);

  const by = me.name;
  const at = new Date().toISOString();
  const state = (await env.EDITS.get("state", "json")) || { edits: {}, log: [] };
  const prev = state.edits[key];
  let action, patch = {};
  try {
    if (body.reset) {
      if (!prev) return json(state);
      delete state.edits[key];
      action = "Khôi phục bản gốc";
    } else {
      patch = sanitizePatch(body.patch || {}, key.startsWith("n:"));
      if (key.startsWith("n:") && !prev && (!patch.t || !patch.o)) throw new Error("Tag mới cần tên và vị trí");
      state.edits[key] = { ...(prev || {}), ...patch, by, at };
      action = !prev && key.startsWith("n:") ? "Thêm tag" : patch.del === true ? "Ẩn tag" : patch.del === false && prev && prev.del ? "Hiện lại tag" : "Sửa";
    }
  } catch (e) {
    return json({ error: e.message }, 400);
  }
  state.log.unshift({
    at, by, key, action,
    from: prev ? { t: prev.t, k: prev.k, note: prev.note, del: prev.del } : null,
    to: body.reset ? null : { t: patch.t, k: patch.k, note: patch.note, del: patch.del },
  });
  if (state.log.length > MAX_LOG) state.log.length = MAX_LOG;
  await env.EDITS.put("state", JSON.stringify(state));
  return json(state);
}

function sanitizePatch(p, isNew) {
  const out = {};
  if (p.t !== undefined) { const t = clean(p.t, 80); if (!t) throw new Error("Tên tag không được để trống"); out.t = t; }
  if (p.k !== undefined) { if (!KINDS.has(p.k)) throw new Error("Loại không hợp lệ"); out.k = p.k; }
  if (p.note !== undefined) out.note = clean(p.note, 500) || "";
  if (p.del !== undefined) out.del = !!p.del;
  if (isNew && p.o !== undefined) {
    if (!Array.isArray(p.o) || !p.o.length || p.o.length > 20) throw new Error("Vị trí không hợp lệ");
    out.o = p.o.map((o) => {
      if (!Array.isArray(o) || o.length !== 5 || typeof o[0] !== "string") throw new Error("Vị trí không hợp lệ");
      const n = o.slice(1).map(Number);
      if (n.some((v) => !(v >= 0 && v <= 1))) throw new Error("Vị trí không hợp lệ");
      return [o[0].slice(0, 80), ...n.map((v) => Math.round(v * 1e4) / 1e4)];
    });
  }
  return out;
}

async function handleUsers(req, env, me) {
  if (me.role !== "admin") return json({ error: "Chỉ quản trị viên mới quản lý tài khoản" }, 403);
  const list = (users) => Object.entries(users).map(([u, r]) => publicUser(u, r)).sort((a, b) => a.u.localeCompare(b.u));
  if (req.method === "GET") return json(list(await loadUsers(env, true)));
  if (req.method !== "POST") return json({ error: "Phương thức không hỗ trợ" }, 405);
  let b;
  try { b = await req.json(); } catch { return json({ error: "Dữ liệu gửi lên không đọc được" }, 400); }
  const users = { ...(await loadUsers(env, true)) };
  const u = (clean(b.u, 40) || "").toLowerCase();
  const now = new Date().toISOString();
  if (b.action === "delete") {
    if (!users[u]) return json({ error: "Không có tài khoản này" }, 404);
    if (u === me.u) return json({ error: "Không thể tự xóa tài khoản đang dùng" }, 400);
    delete users[u];
    await saveUsers(env, users);
    return json(list(users));
  }
  if (b.action !== "save") return json({ error: "Thao tác không hợp lệ" }, 400);
  if (!/^[a-z0-9._-]{3,32}$/.test(u)) return json({ error: "Tên đăng nhập 3–32 ký tự, chỉ gồm chữ thường không dấu, số, dấu . _ -" }, 400);
  if (u === "admin") return json({ error: "Tên “admin” dành cho tài khoản quản trị dựng sẵn, hãy chọn tên khác" }, 400);
  if (!ROLES[b.role]) return json({ error: "Quyền không hợp lệ" }, 400);
  const name = clean(b.name, 60);
  if (!name) return json({ error: "Nhập họ tên" }, 400);
  const prev = users[u];
  if (!prev && !b.password) return json({ error: "Tài khoản mới cần mật khẩu" }, 400);
  if (b.password !== undefined && (typeof b.password !== "string" || b.password.length < 8 || b.password.length > 200)) return json({ error: "Mật khẩu cần ít nhất 8 ký tự" }, 400);
  if (u === me.u && (b.role !== "admin" || b.disabled)) return json({ error: "Không thể tự hạ quyền hoặc khóa tài khoản đang dùng" }, 400);
  const rec = { ...(prev || { created: now }), name, role: b.role, disabled: !!b.disabled, updated: now };
  // đổi mật khẩu, quyền hoặc khóa -> đăng xuất các phiên cũ của tài khoản này
  if (b.password) Object.assign(rec, await hashPassword(b.password));
  if (!prev || b.password || prev.role !== rec.role || !!prev.disabled !== rec.disabled) rec.v = hex(crypto.getRandomValues(new Uint8Array(6)));
  users[u] = rec;
  await saveUsers(env, users);
  return json(list(users));
}

async function handlePassword(req, env, me) {
  if (req.method !== "POST") return json({ error: "Phương thức không hỗ trợ" }, 405);
  if (me.builtin) return json({ error: "Mật khẩu tài khoản admin dựng sẵn là secret ADMIN_PASSWORD trên Cloudflare" }, 400);
  let b;
  try { b = await req.json(); } catch { return json({ error: "Dữ liệu gửi lên không đọc được" }, 400); }
  const users = { ...(await loadUsers(env, true)) };
  const rec = users[me.u];
  if (!rec || typeof b.old !== "string" || !safeEq((await hashPassword(b.old, rec.salt)).hash, rec.hash)) return json({ error: "Mật khẩu hiện tại không đúng" }, 400);
  if (typeof b.new !== "string" || b.new.length < 8 || b.new.length > 200) return json({ error: "Mật khẩu mới cần ít nhất 8 ký tự" }, 400);
  users[me.u] = { ...rec, ...(await hashPassword(b.new)), updated: new Date().toISOString() };
  // giữ nguyên v để phiên đang dùng không bị đăng xuất
  await saveUsers(env, users);
  return json({ ok: true });
}

/* ---------------- router ---------------- */
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const path = url.pathname;

    // chặn POST từ trang web khác (CSRF)
    if (req.method === "POST") {
      const origin = req.headers.get("origin");
      if (origin && origin !== url.origin) return json({ error: "Yêu cầu không hợp lệ" }, 403);
    }

    if (path === "/login") return handleLogin(req, env, url);
    if (path === "/logout") {
      return new Response(null, { status: 303, headers: { location: "/login", "set-cookie": `${COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`, "cache-control": "no-store" } });
    }

    const me = await currentUser(req, env);
    if (!me) {
      if (path.startsWith("/api/")) return json({ error: "Cần đăng nhập" }, 401);
      const accept = req.headers.get("accept") || "";
      if (req.method === "GET" && (accept.includes("text/html") || path === "/" || path.endsWith(".html"))) {
        return Response.redirect(url.origin + "/login?next=" + encodeURIComponent(path + url.search), 302);
      }
      return new Response("Cần đăng nhập", { status: 401, headers: { "cache-control": "no-store" } });
    }

    if (path === "/api/me") return json(me);
    if (path === "/api/edits") return handleEdits(req, env, me);
    if (path === "/api/users") return handleUsers(req, env, me);
    if (path === "/api/password") return handlePassword(req, env, me);
    if (path.startsWith("/api/")) return json({ error: "Không có API này" }, 404);
    if (path === "/account") return html(accountPage());

    const res = await env.ASSETS.fetch(req);
    // nội dung sau đăng nhập: không cho bộ nhớ đệm dùng chung lưu lại
    const out = new Response(res.body, res);
    const cc = out.headers.get("cache-control") || "";
    out.headers.set("cache-control", cc.includes("max-age") ? cc.replace(/public/g, "private") : "private, no-cache");
    out.headers.append("vary", "Cookie");
    return out;
  },
};
