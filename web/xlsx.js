/* Đọc/ghi Excel (.xlsx) không cần thư viện ngoài. Dùng ở trang /account. */
const XL=(()=>{
  const CRC=new Uint32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;CRC[n]=c>>>0;}
  const crc32=u=>{let c=0xFFFFFFFF;for(let i=0;i<u.length;i++)c=CRC[(c^u[i])&255]^(c>>>8);return(c^0xFFFFFFFF)>>>0;};
  const enc=new TextEncoder();
  function zip(files){
    const parts=[],central=[];let off=0;
    files.forEach(f=>{
      const name=enc.encode(f.name),data=enc.encode(f.data),crc=crc32(data);
      const h=new DataView(new ArrayBuffer(30));
      h.setUint32(0,0x04034b50,true);h.setUint16(4,20,true);h.setUint16(6,0x0800,true);h.setUint16(8,0,true);
      h.setUint32(14,crc,true);h.setUint32(18,data.length,true);h.setUint32(22,data.length,true);h.setUint16(26,name.length,true);
      parts.push(new Uint8Array(h.buffer),name,data);
      const c=new DataView(new ArrayBuffer(46));
      c.setUint32(0,0x02014b50,true);c.setUint16(4,20,true);c.setUint16(6,20,true);c.setUint16(8,0x0800,true);
      c.setUint32(16,crc,true);c.setUint32(20,data.length,true);c.setUint32(24,data.length,true);c.setUint16(28,name.length,true);c.setUint32(42,off,true);
      central.push(new Uint8Array(c.buffer),name);
      off+=30+name.length+data.length;
    });
    const csize=central.reduce((n,p)=>n+p.length,0);
    const e=new DataView(new ArrayBuffer(22));
    e.setUint32(0,0x06054b50,true);e.setUint16(8,files.length,true);e.setUint16(10,files.length,true);e.setUint32(12,csize,true);e.setUint32(16,off,true);
    return new Blob([...parts,...central,new Uint8Array(e.buffer)],{type:"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"});
  }
  const x=v=>String(v??"").replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g,"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const col=i=>{let s="";i++;while(i){const m=(i-1)%26;s=String.fromCharCode(65+m)+s;i=Math.floor((i-1)/26);}return s;};
  function sheetXml(rows,widths){
    const last=col(Math.max(1,rows[0].length)-1)+Math.max(1,rows.length);
    const cols=`<cols>${widths.map((w,i)=>`<col min="${i+1}" max="${i+1}" width="${w}" customWidth="1"/>`).join("")}</cols>`;
    const data=rows.map((r,ri)=>`<row r="${ri+1}">${r.map((v,ci)=>{const ref=col(ci)+(ri+1),st=ri===0?' s="1"':"";
      return typeof v==="number"?`<c r="${ref}"${st}><v>${v}</v></c>`:`<c r="${ref}"${st} t="inlineStr"><is><t xml:space="preserve">${x(v)}</t></is></c>`;}).join("")}</row>`).join("");
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>${cols}<sheetData>${data}</sheetData><autoFilter ref="A1:${last}"/></worksheet>`;
  }
  return function(sheets){
    const files=[
      {name:"[Content_Types].xml",data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>${sheets.map((_,i)=>`<Override PartName="/xl/worksheets/sheet${i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join("")}</Types>`},
      {name:"_rels/.rels",data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`},
      {name:"xl/workbook.xml",data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>${sheets.map((s,i)=>`<sheet name="${x(s.name)}" sheetId="${i+1}" r:id="rId${i+1}"/>`).join("")}</sheets><definedNames>${sheets.map((s,i)=>`<definedName name="_xlnm._FilterDatabase" localSheetId="${i}" hidden="1">'${x(s.name)}'!$A$1:$${col(Math.max(1,s.rows[0].length)-1)}$${Math.max(1,s.rows.length)}</definedName>`).join("")}</definedNames></workbook>`},
      {name:"xl/_rels/workbook.xml.rels",data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${sheets.map((_,i)=>`<Relationship Id="rId${i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i+1}.xml"/>`).join("")}<Relationship Id="rId${sheets.length+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`},
      {name:"xl/styles.xml",data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF15222E"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>`},
      ...sheets.map((s,i)=>({name:`xl/worksheets/sheet${i+1}.xml`,data:sheetXml(s.rows,s.widths)}))
    ];
    return zip(files);
  };
})();

/* ---- .xlsx / .csv reader: first sheet -> array of rows (strings) ---- */
const XLREAD=(()=>{
  const dec=new TextDecoder();
  async function inflate(u8){
    const ds=new DecompressionStream("deflate-raw");
    return new Uint8Array(await new Response(new Blob([u8]).stream().pipeThrough(ds)).arrayBuffer());
  }
  async function unzip(buf){
    const u8=new Uint8Array(buf),dv=new DataView(buf);let e=-1;
    for(let i=u8.length-22;i>=Math.max(0,u8.length-65558);i--){if(dv.getUint32(i,true)===0x06054b50){e=i;break;}}
    if(e<0)throw new Error("File không phải Excel (.xlsx) hợp lệ");
    const n=dv.getUint16(e+10,true);let p=dv.getUint32(e+16,true);const out={};
    for(let k=0;k<n;k++){
      if(dv.getUint32(p,true)!==0x02014b50)break;
      const method=dv.getUint16(p+10,true),csize=dv.getUint32(p+20,true),nlen=dv.getUint16(p+28,true),elen=dv.getUint16(p+30,true),clen=dv.getUint16(p+32,true),off=dv.getUint32(p+42,true);
      const name=dec.decode(u8.subarray(p+46,p+46+nlen));p+=46+nlen+elen+clen;
      if(!/\.(xml|rels)$/i.test(name))continue;
      const start=off+30+dv.getUint16(off+26,true)+dv.getUint16(off+28,true),data=u8.subarray(start,start+csize);
      out[name]=dec.decode(method===8?await inflate(data):data);
    }
    return out;
  }
  const xml=s=>new DOMParser().parseFromString(s,"application/xml");
  const all=(d,t)=>[...d.getElementsByTagNameNS("*",t)];
  const text=el=>all(el,"t").map(t=>t.textContent).join("");
  const colIdx=ref=>{const m=/^[A-Z]+/.exec(ref||"");if(!m)return -1;let n=0;for(const ch of m[0])n=n*26+ch.charCodeAt(0)-64;return n-1;};
  async function xlsx(buf){
    const f=await unzip(buf);
    const wb=f["xl/workbook.xml"];if(!wb)throw new Error("File không phải Excel (.xlsx) hợp lệ");
    const first=all(xml(wb),"sheet")[0];
    const rid=first&&(first.getAttribute("r:id")||[...first.attributes].find(a=>a.localName==="id")?.value);
    let target="worksheets/sheet1.xml";
    if(f["xl/_rels/workbook.xml.rels"]){const r=all(xml(f["xl/_rels/workbook.xml.rels"]),"Relationship").find(r=>r.getAttribute("Id")===rid);if(r)target=r.getAttribute("Target");}
    const path=target.startsWith("/")?target.slice(1):"xl/"+target.replace(/^\.\//,"");
    const ss=f["xl/sharedStrings.xml"]?all(xml(f["xl/sharedStrings.xml"]),"si").map(text):[];
    const sh=f[path];if(!sh)throw new Error("Không đọc được trang tính đầu tiên");
    return all(xml(sh),"row").map(row=>{const r=[];all(row,"c").forEach((c,i)=>{
      let j=colIdx(c.getAttribute("r"));if(j<0)j=r.length;
      const t=c.getAttribute("t"),v=all(c,"v")[0];
      r[j]=t==="s"?(ss[+(v&&v.textContent)]??""):t==="inlineStr"?text(c):(v?v.textContent:"");});
      for(let k=0;k<r.length;k++)if(r[k]==null)r[k]="";return r;});
  }
  function csv(s){
    s=s.replace(/^﻿/,"");const sep=(s.split("\n")[0].match(/;/g)||[]).length>(s.split("\n")[0].match(/,/g)||[]).length?";":",";
    const rows=[];let row=[],cur="",q=false;
    for(let i=0;i<s.length;i++){const ch=s[i];
      if(q){if(ch==='"'){if(s[i+1]==='"'){cur+='"';i++;}else q=false;}else cur+=ch;}
      else if(ch==='"')q=true;else if(ch===sep){row.push(cur);cur="";}
      else if(ch==="\n"||ch==="\r"){if(ch==="\r"&&s[i+1]==="\n")i++;row.push(cur);rows.push(row);row=[];cur="";}
      else cur+=ch;}
    if(cur||row.length){row.push(cur);rows.push(row);}
    return rows;
  }
  return async function(file){
    const buf=await file.arrayBuffer();
    if(/\.csv$/i.test(file.name))return csv(dec.decode(buf));
    if(/\.xls$/i.test(file.name))throw new Error("File .xls (Excel cũ) chưa hỗ trợ. Mở bằng Excel rồi Lưu thành .xlsx");
    return xlsx(buf);
  };
})();
