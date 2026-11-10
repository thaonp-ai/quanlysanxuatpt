/* Trang /account: nhập nhiều tài khoản từ file Excel (.xlsx) hoặc .csv.
   Dùng các hàm của trang: $, call, esc, gen, render, ROLES, USERS (biến toàn cục của script chính). */
(function () {
  const ROLE_OF = { viewer: "Chỉ xem", editor: "Được sửa tag", admin: "Quản trị" };
  const strip = (s) => String(s ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toLowerCase().replace(/\s+/g, " ").trim();
  const hex = (b) => [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("");
  let ROWS = [], RESULT = null;

  function headerMap(row) {
    const m = {};
    row.forEach((c, i) => {
      const h = strip(c);
      if (!h) return;
      if (m.u == null && /(dang nhap|username|user name|^user$|tai khoan|login)/.test(h)) m.u = i;
      else if (m.pw == null && /(mat khau|password|^pass)/.test(h)) m.pw = i;
      else if (m.role == null && /(quyen|role|vai tro)/.test(h)) m.role = i;
      else if (m.name == null && /(ho ten|ho va ten|^ten$|name|nhan vien|nguoi dung)/.test(h)) m.name = i;
    });
    return m.u != null ? m : null;
  }
  function roleOf(v) {
    const s = strip(v);
    if (!s) return "viewer";
    if (/(quan tri|admin)/.test(s)) return "admin";
    if (/(sua|edit)/.test(s)) return "editor";
    if (/(xem|view|doc)/.test(s)) return "viewer";
    return null;
  }

  function parse(rows) {
    let start = 0, map = { u: 0, name: 1, role: 2, pw: 3 };
    for (let i = 0; i < Math.min(rows.length, 6); i++) {
      const m = headerMap(rows[i]);
      if (m) { map = m; start = i + 1; break; }
    }
    const have = new Set((typeof USERS !== "undefined" ? USERS : []).map((x) => x.u));
    const seen = new Set();
    const out = [];
    rows.slice(start).forEach((r, k) => {
      const get = (key) => (map[key] == null ? "" : String(r[map[key]] ?? "").trim());
      const u = get("u").toLowerCase(), name = get("name"), roleRaw = get("role"), pw = get("pw");
      if (!u && !name && !pw) return; // dòng trống
      const role = roleOf(roleRaw);
      const it = { line: start + k + 1, u, name: name || u, role, pw, auto: !pw, st: "ok", why: "" };
      if (!u) { it.st = "bad"; it.why = "Thiếu tên đăng nhập"; }
      else if (!/^[a-z0-9._-]{3,32}$/.test(u)) { it.st = "bad"; it.why = "Tên đăng nhập 3–32 ký tự: chữ thường không dấu, số, . _ -"; }
      else if (u === "admin") { it.st = "bad"; it.why = "Tên “admin” không dùng được"; }
      else if (seen.has(u)) { it.st = "bad"; it.why = "Trùng với dòng phía trên"; }
      else if (have.has(u)) { it.st = "skip"; it.why = "Đã có, bỏ qua"; }
      else if (!role) { it.st = "bad"; it.why = "Quyền “" + roleRaw + "” không rõ (Chỉ xem / Được sửa tag / Quản trị)"; }
      else if (pw && pw.length < 8) { it.st = "bad"; it.why = "Mật khẩu cần ít nhất 8 ký tự"; }
      if (u) seen.add(u);
      if (it.auto) it.pw = gen();
      out.push(it);
    });
    return out;
  }

  function showPreview() {
    const ok = ROWS.filter((r) => r.st === "ok").length, bad = ROWS.filter((r) => r.st === "bad").length, skip = ROWS.filter((r) => r.st === "skip").length;
    $("impPrev").innerHTML = ROWS.length
      ? '<table><thead><tr><th>Dòng</th><th>Tên đăng nhập</th><th>Họ tên</th><th>Quyền</th><th>Mật khẩu</th><th>Kiểm tra</th></tr></thead><tbody>' +
        ROWS.map((r) => '<tr class="' + (r.st === "ok" ? "" : r.st) + '"><td>' + r.line + '</td><td class="u">' + esc(r.u) + "</td><td>" + esc(r.name) + "</td><td>" + (r.role ? ROLE_OF[r.role] : "?") + "</td><td>" + (r.auto ? "<i>tự tạo</i>" : "đã nhập") + '</td><td class="st">' + (r.st === "ok" ? "Sẵn sàng" : esc(r.why)) + "</td></tr>").join("") +
        "</tbody></table>"
      : '<p class="hint">Không thấy dòng dữ liệu nào trong file.</p>';
    $("impProg").textContent = ROWS.length ? ok + " sẵn sàng" + (skip ? " · " + skip + " đã có" : "") + (bad ? " · " + bad + " lỗi (sửa trong file rồi chọn lại)" : "") : "";
    $("impGo").textContent = "Tạo " + ok + " tài khoản";
    $("impGo").disabled = !ok;
    $("impGo").hidden = false;
  }

  async function pbkdf2(pw) {
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveBits"]);
    const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt, iterations: 100000 }, key, 256);
    return { salt: hex(salt), hash: hex(bits) };
  }

  function download(blob, name) {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
  }

  function openImp() {
    ROWS = []; RESULT = null;
    $("impPrev").innerHTML = ""; $("impErr").hidden = true; $("impFile").textContent = ""; $("impProg").textContent = "";
    $("impGo").disabled = true; $("impGo").hidden = false; $("impGo").textContent = "Tạo tài khoản";
    $("impFileIn").value = "";
    $("impGo").onclick = goCreate;
    $("impScrim").hidden = false;
  }
  function closeImp() { $("impScrim").hidden = true; }

  $("btnImp").onclick = openImp;
  $("impCancel").onclick = closeImp;
  $("impScrim").addEventListener("click", (e) => { if (e.target === $("impScrim")) closeImp(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !$("impScrim").hidden) closeImp(); });

  $("impTpl").onclick = () => {
    download(XL([{ name: "Tai khoan", widths: [20, 28, 16, 18], rows: [
      ["Tên đăng nhập", "Họ tên", "Quyền", "Mật khẩu"],
      ["nguyen.van.a", "Nguyễn Văn A", "Chỉ xem", ""],
      ["tran.thi.b", "Trần Thị B", "Được sửa tag", ""],
      ["le.van.c", "Lê Văn C", "Quản trị", "MatKhau@2026"],
    ] }]), "Mau-nhap-tai-khoan.xlsx");
  };

  $("impFileIn").onchange = async (e) => {
    const f = e.target.files[0];
    if (!f) return;
    $("impErr").hidden = true; $("impFile").textContent = f.name;
    try {
      ROWS = parse(await XLREAD(f));
      showPreview();
    } catch (err) {
      ROWS = []; $("impPrev").innerHTML = ""; $("impGo").disabled = true;
      $("impErr").textContent = err.message || "Không đọc được file"; $("impErr").hidden = false;
    }
  };

  const goCreate = async () => {
    const todo = ROWS.filter((r) => r.st === "ok");
    if (!todo.length) return;
    $("impGo").disabled = true; $("impErr").hidden = true;
    try {
      const items = [];
      for (let i = 0; i < todo.length; i++) {
        $("impProg").textContent = "Đang mã hóa mật khẩu " + (i + 1) + "/" + todo.length + "…";
        items.push({ u: todo[i].u, name: todo[i].name, role: todo[i].role, ...(await pbkdf2(todo[i].pw)) });
      }
      $("impProg").textContent = "Đang lưu…";
      const res = await call("/api/users", { action: "bulk", items });
      USERS = res.users; render();
      const made = new Set(res.created), why = Object.fromEntries(res.skipped.map((s) => [s.u, s.reason]));
      RESULT = todo.map((r) => ({ ...r, done: made.has(r.u), why: why[r.u] || "" }));
      $("impPrev").innerHTML = '<table><thead><tr><th>Tên đăng nhập</th><th>Họ tên</th><th>Quyền</th><th>Mật khẩu</th><th>Kết quả</th></tr></thead><tbody>' +
        RESULT.map((r) => '<tr class="' + (r.done ? "" : "bad") + '"><td class="u">' + esc(r.u) + "</td><td>" + esc(r.name) + "</td><td>" + ROLE_OF[r.role] + '</td><td class="u">' + (r.done ? esc(r.pw) : "") + "</td><td>" + (r.done ? "Đã tạo" : esc(r.why)) + "</td></tr>").join("") +
        "</tbody></table>";
      $("impProg").innerHTML = '<b class="ok">Đã tạo ' + res.created.length + " tài khoản.</b> Tải danh sách mật khẩu để gửi cho từng người.";
      $("impGo").textContent = "Tải danh sách mật khẩu (Excel)";
      $("impGo").disabled = !res.created.length;
      $("impGo").onclick = () => download(XL([{ name: "Tai khoan moi", widths: [20, 28, 16, 18], rows: [
        ["Tên đăng nhập", "Họ tên", "Quyền", "Mật khẩu"],
        ...RESULT.filter((r) => r.done).map((r) => [r.u, r.name, ROLE_OF[r.role], r.pw]),
      ] }]), "Tai-khoan-moi_" + new Date().toISOString().slice(0, 10) + ".xlsx");
    } catch (err) {
      $("impErr").textContent = err.message || "Không lưu được"; $("impErr").hidden = false;
      $("impGo").disabled = false; $("impProg").textContent = "";
    }
  };
  $("impGo").onclick = goCreate;
})();
