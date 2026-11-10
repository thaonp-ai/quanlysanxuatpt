// Lưu các chỉnh sửa tag của web tra cứu P&ID vào Cloudflare KV.
// GET  /api/edits  -> { edits: {key: {...}}, log: [...] }
// POST /api/edits  -> body { key, patch | reset:true, by } ; trả về trạng thái mới
// Nếu đặt secret EDIT_PASSWORD, POST phải gửi header x-edit-key trùng mã đó.

const KINDS = new Set(["line", "equipment", "valve"]);
const MAX_LOG = 5000;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

function clean(s, max) {
  return typeof s === "string" ? s.replace(/[\u0000-\u001f]/g, " ").trim().slice(0, max) : undefined;
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

async function load(env) {
  return (await env.EDITS.get("state", "json")) || { edits: {}, log: [] };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/api/edits") return env.ASSETS.fetch(request);

    if (request.method === "GET") return json(await load(env));
    if (request.method !== "POST") return json({ error: "Phương thức không hỗ trợ" }, 405);

    if (env.EDIT_PASSWORD && request.headers.get("x-edit-key") !== env.EDIT_PASSWORD) {
      return json({ error: "Cần mã sửa đúng để lưu thay đổi" }, 401);
    }
    let body;
    try { body = await request.json(); } catch { return json({ error: "Dữ liệu gửi lên không đọc được" }, 400); }
    const key = clean(body.key, 200);
    if (!key || !/^(o|n):/.test(key)) return json({ error: "Thiếu mã tag" }, 400);

    const by = clean(request.headers.get("cf-access-authenticated-user-email"), 120) || clean(body.by, 60) || "Không rõ";
    const at = new Date().toISOString();
    const state = await load(env);
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
  },
};
