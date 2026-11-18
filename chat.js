/* Hỏi đáp (chatbox) — POST /api/chat {q, history:[{role,content}]}
   1. Tìm trong dữ liệu web (data.json: tag/bản vẽ; tech.json: công nghệ + giáo trình; vendor.json: tài liệu vendor)
      bằng chấm điểm từ khóa (bỏ dấu tiếng Việt) + khớp tên tag.
   2. Đưa các đoạn tìm được cho mô hình ngôn ngữ trả lời, có trích nguồn [n]:
      - secret ANTHROPIC_API_KEY (Claude, model theo biến CHAT_MODEL, mặc định claude-sonnet-5-5), nếu không có thì
      - Workers AI (binding AI trong wrangler.jsonc, model CHAT_AI_MODEL), nếu không có nữa thì
      - chỉ trả danh sách kết quả tìm được.
   Giới hạn mỗi tài khoản CHAT_LIMIT câu/ngày (mặc định 150), đếm ở KV "chat:<user>:<ngày>". */

const AI_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast";
let CORPUS = null;

const fold = (s) =>
  String(s ?? "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/g, "d");
const nk = (s) => String(s ?? "").toUpperCase().replace(/[^A-Z0-9/]/g, "");
const STOP = new Set(("la cua va cac cho voi trong nao gi bao nhieu the nhu thi co khong duoc mot nhung de den tu tai o " +
  "may hay xin cho biet ve ra vao hoi giup minh ban toi cai nay do nhe a ah the_nao what is the of and").split(" "));
const toks = (s) => fold(s).split(/[^a-z0-9]+/).filter((w) => w && (w.length > 1 || /\d/.test(w)) && !STOP.has(w));

function flat(x, out = []) {
  if (x == null) return out;
  if (typeof x === "string") out.push(x);
  else if (Array.isArray(x)) x.forEach((y) => flat(y, out));
  else if (typeof x === "object") Object.values(x).forEach((y) => flat(y, out));
  return out;
}

async function getJSON(env, origin, p) {
  const r = await env.ASSETS.fetch(new Request(origin + p));
  if (!r.ok) throw new Error("Không đọc được " + p);
  return r.json();
}

async function loadCorpus(env, origin) {
  if (CORPUS) return CORPUS;
  const [D, T, V] = await Promise.all([
    getJSON(env, origin, "/data/data.json"),
    getJSON(env, origin, "/data/tech.json").catch(() => null),
    getJSON(env, origin, "/data/vendor.json").catch(() => null),
  ]);
  const unitName = Object.fromEntries(D.units.map((u) => [u.code, u.name]));
  const items = [];
  const add = (kind, title, text, ref, keys = []) => items.push({ kind, title, text: text.slice(0, 2500), ref, keys });
  const KIND = { line: "Đường ống", equipment: "Thiết bị", valve: "Van" };
  for (const t of D.tags) {
    const sh = [...new Set(t.o.map((o) => o[0]))].slice(0, 6).map((i) => D.sheets[i]);
    const units = [...new Set(sh.flatMap((s) => [s.unit, ...(s.also || [])]))];
    const txt = `${KIND[t.k] || t.k} ${t.t}: ${t.d || ""}${t.p ? `; thuộc thiết bị ${t.p}` : ""}${t.n ? `; ghi chú: ${t.n}` : ""}. ` +
      `Unit ${units.map((u) => `${u} (${unitName[u] || ""})`).join(", ")}. Bản vẽ: ${sh.map((s) => `${s.dwg} ${s.title}`).join("; ")}` +
      (t.a ? `. Tên khác: ${t.a.join(", ")}` : "");
    add("tag", t.t, txt, { type: "tag", t: t.t }, [t.t, ...(t.a || [])]);
    if (t.p) items[items.length - 1].pk = nk(t.p);
  }
  for (const s of D.sheets)
    add("sheet", `${s.dwg} ${s.title}`, `Bản vẽ ${s.kind} ${s.dwg} – ${s.title}, Unit ${s.unit} (${unitName[s.unit] || ""}).`, { type: "sheet", dwg: s.dwg }, [s.dwg]);
  for (const u of D.units) add("unit", `Unit ${u.code}`, `Unit ${u.code}: ${u.name}`, { type: "unit", u: u.code }, []);
  if (T) {
    for (const [u, e] of Object.entries(T.units || {})) {
      add("tech", e.t, `${e.t}. ${e.intro || ""}`, { type: "unit", u, tab: "tech" }, []);
      (e.s || []).forEach((sec) => add("tech", `${e.t} – ${sec.h || ""}`, `${sec.h || ""}: ${flat(sec.ul || sec.p || sec).join(" ")}`, { type: "unit", u, tab: "tech" }, []));
    }
    const seen = new Set();
    for (const [k, e] of Object.entries(T.tags || {})) {
      const sig = e.t + (e.intro || "").slice(0, 80);
      if (seen.has(sig)) continue;
      seen.add(sig);
      const body = [e.intro || "", ...(e.s || []).map((s) => `${s.h || ""}: ${flat(s.ul || s.p || s).join(" ")}`)].join(" ");
      add("tech", `${k} – ${e.t}`, `Công nghệ ${k} (${e.t}): ${body}`, { type: "tech", t: k }, [k]);
    }
    for (const [k, g] of Object.entries(T.gt || {})) {
      const head = `Giáo trình ${g.no} – ${g.t} (cương vị ${g.cv || ""}, Unit ${(g.units || []).join(", ")})`;
      add("gt", head, `${head}. ${flat(g.sum).join(" ")} Điểm chính: ${flat(g.key).join(" ")}`, { type: "gt", u: (g.units || [])[0], p: g.f }, [g.no]);
      (g.sec || []).forEach((s) => add("gt", `${g.no} – ${s.h || ""}`, `${head}. ${s.h || ""}: ${flat(s.ul || s).join(" ")}`, { type: "gt", u: (g.units || [])[0], p: g.f }, []));
      (g.toc || []).forEach((c) => c[3] && add("gt", `${g.no} – ${c[1]} (tr. ${c[2]})`, `${head}, mục "${c[1]}" trang ${c[2]}`, { type: "doc", p: c[3] }, []));
      if (g.q && g.q.length) add("gt", `${g.no} – Câu hỏi ôn tập`, `${head}. Câu hỏi ôn tập: ${g.q.join(" | ")}`, { type: "gt", u: (g.units || [])[0], p: g.f }, []);
    }
  }
  if (V) {
    const byDoc = new Map();
    for (const [tag, ids] of Object.entries(V.tags || {})) for (const i of ids) (byDoc.get(i) || byDoc.set(i, []).get(i)).push(tag);
    V.docs.forEach((d, i) => {
      const tags = byDoc.get(i) || [];
      add("doc", d.t, `Tài liệu vendor "${d.t}"${d.no ? ` số ${d.no}` : ""}, nhóm ${d.g || ""}${d.src ? `, nguồn ${d.src}` : ""}. Thiết bị: ${tags.slice(0, 12).join(", ")}. File: ${d.p}`,
        { type: "doc", p: d.p }, tags.slice(0, 20));
    });
  }
  // chỉ mục từ khóa
  const df = new Map();
  for (const it of items) {
    it.tk = new Set(toks(it.title + " " + it.text));
    it.nk = it.keys.filter(Boolean).map(nk);
    for (const w of it.tk) df.set(w, (df.get(w) || 0) + 1);
  }
  CORPUS = { items, df, N: items.length, updated: D.updated };
  return CORPUS;
}

function search(C, q, limit = 28) {
  const qt = [...new Set(toks(q))];
  // tên tag trong câu hỏi: chuỗi có chữ số, ví dụ 30-P-2001A, PSV-37503, 10B8001
  const tagq = (q.toUpperCase().match(/[A-Z0-9][A-Z0-9/".\-]*\d[A-Z0-9/"\-]*/g) || []).map(nk).filter((s) => s.length >= 4);
  const scored = [];
  for (const it of C.items) {
    let s = 0;
    for (const w of qt) if (it.tk.has(w)) s += Math.log(1 + C.N / (C.df.get(w) || 1));
    const W = { tag: 40, tech: 34, sheet: 30, gt: 10, doc: 9, unit: 10 }[it.kind] || 10;
    for (const t of tagq) {
      let best = 0;
      for (const k of it.nk) {
        if (k === t) best = Math.max(best, W);
        else if (k.startsWith(t) && /^[A-Z]?$/.test(k.slice(t.length))) best = Math.max(best, W * 0.7); // 30-P-2001 → 30-P-2001A
        else if (t.startsWith(k) && k.length >= 6 && /^[A-Z/]/.test(t.slice(k.length))) best = Math.max(best, W * 0.6); // hỏi 30-P-2001A → đoạn 30-P-2001
        else if (t.length >= 6 && k.includes(t)) best = Math.max(best, W * 0.3);
      }
      if (it.pk && it.pk === t) best = Math.max(best, 8); // van/thiết bị con của tag được hỏi
      if (!best && t.length >= 5 && nk(it.text).includes(t)) best = 5;
      s += best;
    }
    if (s > 0) {
      if (it.kind === "tech" || it.kind === "gt") s *= 1.25;
      scored.push([s, it]);
    }
  }
  scored.sort((a, b) => b[0] - a[0]);
  const out = [], seenTitle = new Set(), perKind = {};
  const cap = { tag: 14, doc: 10, sheet: 6, gt: 10, tech: 10, unit: 3 };
  for (const [s, it] of scored) {
    if (seenTitle.has(it.title) || (perKind[it.kind] || 0) >= (cap[it.kind] || 8)) continue;
    seenTitle.add(it.title);
    perKind[it.kind] = (perKind[it.kind] || 0) + 1;
    out.push(it);
    if (out.length >= limit) break;
  }
  return out;
}

const SYSTEM = `Bạn là trợ lý tra cứu của Xưởng Phụ Trợ, Nhà máy Đạm Phú Mỹ. Người hỏi là kỹ sư/vận hành viên.
Chỉ trả lời dựa trên các đoạn TÀI LIỆU được cung cấp (danh mục tag/bản vẽ P&ID, mô tả công nghệ, giáo trình cương vị, danh mục tài liệu vendor).
- Trả lời bằng tiếng Việt, ngắn gọn, đúng trọng tâm; dùng gạch đầu dòng khi liệt kê.
- Ghi nguồn bằng số trong ngoặc vuông ngay sau ý, ví dụ [2] hoặc [1][4]. Chỉ dùng số có trong danh sách tài liệu.
- Viết đúng tên tag như trong tài liệu (ví dụ 30-P-2001A, 1801-1/4-B1-01).
- Nếu tài liệu không có thông tin để trả lời, nói rõ là chưa tìm thấy trong dữ liệu của web và gợi ý cách hỏi/tìm khác. Không bịa số liệu.
- Đây là thông tin tham khảo; với thao tác vận hành, nhắc người dùng làm theo quy trình vận hành hiện hành.`;

async function callLLM(env, msgs) {
  if (env.ANTHROPIC_API_KEY) {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "content-type": "application/json", "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model: env.CHAT_MODEL || "claude-sonnet-5-5", max_tokens: 1500, system: SYSTEM, messages: msgs }),
    });
    const j = await r.json();
    if (!r.ok) throw new Error((j.error && j.error.message) || "Lỗi gọi Claude API");
    return { text: (j.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n"), engine: "claude" };
  }
  if (env.AI) {
    const r = await env.AI.run(env.CHAT_AI_MODEL || AI_MODEL, { messages: [{ role: "system", content: SYSTEM }, ...msgs], max_tokens: 1200 });
    return { text: r.response || "", engine: "workers-ai" };
  }
  return null;
}

export async function handleChat(req, env, me, url) {
  if (req.method !== "POST") return Response.json({ error: "Chỉ hỗ trợ POST" }, { status: 405 });
  let body;
  try { body = await req.json(); } catch { return Response.json({ error: "Dữ liệu không hợp lệ" }, { status: 400 }); }
  const q = String(body.q || "").trim().slice(0, 600);
  if (!q) return Response.json({ error: "Chưa có câu hỏi" }, { status: 400 });
  const hist = (Array.isArray(body.history) ? body.history : []).slice(-6)
    .filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .map((m) => ({ role: m.role, content: m.content.slice(0, 1500) }));

  // giới hạn số câu hỏi mỗi ngày
  const day = new Date(Date.now() + 7 * 3600e3).toISOString().slice(0, 10);
  const ck = `chat:${me.u}:${day}`, lim = +(env.CHAT_LIMIT || 150);
  const used = +((await env.EDITS.get(ck)) || 0);
  if (used >= lim) return Response.json({ error: `Bạn đã hỏi ${lim} câu hôm nay, hãy thử lại vào ngày mai.` }, { status: 429 });
  await env.EDITS.put(ck, String(used + 1), { expirationTtl: 2 * 86400 });

  const C = await loadCorpus(env, url.origin);
  const lastUser = [...hist].reverse().find((m) => m.role === "user");
  let hits = search(C, q);
  if (hits.length < 6 && lastUser) hits = [...hits, ...search(C, lastUser.content + " " + q, 12).filter((h) => !hits.includes(h))].slice(0, 28);
  const sources = hits.map((h, i) => ({ n: i + 1, label: h.title, kind: h.kind, ref: h.ref }));
  let budget = 16000;
  const ctx = [];
  for (const [i, h] of hits.entries()) {
    const s = `[${i + 1}] (${h.kind}) ${h.title}\n${h.text}`;
    if (budget - s.length < 0) break;
    budget -= s.length;
    ctx.push(s);
  }
  const prompt = `TÀI LIỆU (dữ liệu web cập nhật ${C.updated}):\n${ctx.join("\n\n") || "(không tìm thấy đoạn nào khớp)"}\n\nCÂU HỎI: ${q}`;
  let ans = null, err = null;
  try { ans = await callLLM(env, [...hist, { role: "user", content: prompt }]); } catch (e) { err = String(e.message || e); }
  if (!ans) {
    const text = hits.length
      ? (err ? `Không gọi được mô hình trả lời (${err}). ` : "Chưa bật mô hình trả lời, ") + "đây là các kết quả tìm được trong dữ liệu:\n" +
        hits.slice(0, 10).map((h, i) => `- ${h.title} [${i + 1}]`).join("\n")
      : "Chưa tìm thấy thông tin phù hợp trong dữ liệu của web. Hãy thử ghi tên tag (ví dụ 30-P-2001A) hoặc từ khóa khác.";
    return Response.json({ answer: text, sources, engine: "search" });
  }
  return Response.json({ answer: ans.text.trim(), sources, engine: ans.engine });
}
