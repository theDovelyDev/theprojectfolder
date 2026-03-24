/* ============================================================
   DocFlow — app.js
   Phase 6: Live API wired
   Phase 10: Dashboard link added to result cards
   ============================================================ */

// ─────────────────────────────────────────────────────────────
// CONFIG
// ─────────────────────────────────────────────────────────────
const CONFIG = {
  API_ENDPOINT: 'https://0r8p6ap199.execute-api.us-east-1.amazonaws.com/prod',
  UPLOAD_BUCKET: "doc-processing-demo-uploads-848747536965",
  FRONTEND_BUCKET: "doc-processing-demo-frontend-848747536965",
  AWS_REGION: "us-east-1",
  COST_PER_DOC: 0.034,
  SIMULATE: false,
};

// ─────────────────────────────────────────────────────────────
// STATE
// ─────────────────────────────────────────────────────────────
const state = {
  files: [],
  totalDocs: 0,
  totalTime: 0,
  successCount: 0,
  totalCost: 0,
};

// ─────────────────────────────────────────────────────────────
// DOM REFS
// ─────────────────────────────────────────────────────────────
const uploadBox = document.getElementById("uploadBox");
const fileInput = document.getElementById("fileInput");
const fileQueue = document.getElementById("fileQueue");
const processBtn = document.getElementById("processBtn");
const btnCount = document.getElementById("btnCount");
const processingSection = document.getElementById("processingSection");
const processingStatus = document.getElementById("processingStatus");
const ringProgress = document.getElementById("ringProgress");
const ringLabel = document.getElementById("ringLabel");
const resultsSection = document.getElementById("resultsSection");
const resultsContainer = document.getElementById("resultsContainer");
const clearBtn = document.getElementById("clearBtn");
const statusBadge = document.getElementById("statusBadge");

const statDocs = document.getElementById("statDocs");
const statTime = document.getElementById("statTime");
const statRate = document.getElementById("statRate");
const statCost = document.getElementById("statCost");

// ─────────────────────────────────────────────────────────────
// UPLOAD BOX — drag & drop + click
// ─────────────────────────────────────────────────────────────
uploadBox.addEventListener("click", () => fileInput.click());
uploadBox.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") fileInput.click();
});

fileInput.addEventListener("change", (e) => {
  addFiles(Array.from(e.target.files));
  fileInput.value = "";
});

uploadBox.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadBox.classList.add("drag-over");
});

uploadBox.addEventListener("dragleave", (e) => {
  if (!uploadBox.contains(e.relatedTarget)) {
    uploadBox.classList.remove("drag-over");
  }
});

uploadBox.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadBox.classList.remove("drag-over");
  const dropped = Array.from(e.dataTransfer.files).filter(isValidFile);
  addFiles(dropped);
});

function isValidFile(file) {
  const allowed = ["application/pdf", "image/jpeg", "image/jpg", "image/png"];
  return allowed.includes(file.type) && file.size <= 10 * 1024 * 1024;
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function fileIcon(file) {
  if (file.type === "application/pdf") return "📄";
  if (file.type.startsWith("image/")) return "🖼️";
  return "📎";
}

function addFiles(newFiles) {
  newFiles.forEach((file) => {
    const exists = state.files.some(
      (f) => f.name === file.name && f.size === file.size
    );
    if (!exists && isValidFile(file)) state.files.push(file);
  });
  renderFileQueue();
}

function renderFileQueue() {
  fileQueue.innerHTML = "";
  state.files.forEach((file, i) => {
    const item = document.createElement("div");
    item.className = "file-item";
    item.innerHTML = `
      <span class="file-item-icon">${fileIcon(file)}</span>
      <div class="file-item-info">
        <div class="file-item-name">${file.name}</div>
        <div class="file-item-meta">${formatBytes(file.size)} · ${file.type.split("/")[1].toUpperCase()}</div>
      </div>
      <button class="file-item-remove" data-index="${i}" title="Remove">✕</button>
    `;
    fileQueue.appendChild(item);
  });

  fileQueue.querySelectorAll(".file-item-remove").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const idx = parseInt(e.currentTarget.dataset.index);
      state.files.splice(idx, 1);
      renderFileQueue();
    });
  });

  processBtn.disabled = state.files.length === 0;
  btnCount.textContent = state.files.length > 0 ? `${state.files.length}` : "";
}

// ─────────────────────────────────────────────────────────────
// PROCESS BUTTON
// ─────────────────────────────────────────────────────────────
processBtn.addEventListener("click", async () => {
  if (state.files.length === 0) return;

  const filesToProcess = [...state.files];
  state.files = [];
  renderFileQueue();

  showProcessing();

  const startTime = Date.now();
  const results = [];

  for (let i = 0; i < filesToProcess.length; i++) {
    const file = filesToProcess[i];
    const progress = Math.round(((i + 0.5) / filesToProcess.length) * 100);
    setRingProgress(progress);

    try {
      let result;
      if (CONFIG.SIMULATE) {
        result = await simulatePipeline(file, i);
      } else {
        result = await runRealPipeline(file);
      }
      results.push(result);
      if (result.success) state.successCount++;
    } catch (err) {
      results.push({ file, success: false, error: err.message });
    }
  }

  const elapsed = Date.now() - startTime;
  state.totalDocs += filesToProcess.length;
  state.totalTime += elapsed;
  state.totalCost += filesToProcess.length * CONFIG.COST_PER_DOC;

  setRingProgress(100);
  await sleep(400);

  hideProcessing();
  showResults(results, elapsed, filesToProcess.length);
  updateStats();
});

// ─────────────────────────────────────────────────────────────
// PIPELINE — REAL (Phase 6)
// ─────────────────────────────────────────────────────────────
async function runRealPipeline(file) {
  setStageActive("step-upload");
  processingStatus.textContent = "Uploading to S3...";

  // Step 1: encode file as base64 and POST to /upload
  const base64 = await fileToBase64(file);
  const uploadResp = await fetch(`${CONFIG.API_ENDPOINT}/upload`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      fileName: file.name,
      fileContent: base64,
      contentType: file.type,
    }),
  });
  if (!uploadResp.ok) throw new Error(`Upload failed: ${uploadResp.status}`);
  const { documentId, s3Key } = await uploadResp.json();
  setStageComplete("step-upload");

  // Step 2: poll /results?documentId= until processing completes
  setStageActive("step-textract");
  processingStatus.textContent = "Textract OCR in progress…";

  for (let attempt = 0; attempt < 20; attempt++) {
    await sleep(3000);

    if (attempt === 3) {
      setStageComplete("step-textract");
      setStageActive("step-comprehend");
      processingStatus.textContent = "Comprehend NLP running…";
    }

    const resultResp = await fetch(
      `${CONFIG.API_ENDPOINT}/results?documentId=${documentId}`
    );

    if (resultResp.status === 404) continue; // still processing

    if (!resultResp.ok) throw new Error(`Results fetch failed: ${resultResp.status}`);

    const data = await resultResp.json();

    if (data.status === "success") {
      setStageComplete("step-comprehend");
      setStageActive("step-store");
      processingStatus.textContent = "Storing results…";
      await sleep(400);
      setStageComplete("step-store");

      return {
        file,
        success: true,
        documentId,
        s3Key,
        textract: {
          documentType: "DOCUMENT",
          fields: data.extraction?.key_value_pairs || {},
          confidence: `${data.extraction?.extraction_confidence || 0}%`,
          pages: data.extraction?.page_count || 1,
        },
        comprehend: {
          sentiment: data.analysis?.sentiment?.overall || "NEUTRAL",
          confidence: Math.round(
            (data.analysis?.sentiment?.scores?.[
              data.analysis?.sentiment?.overall
            ] || 0) * 100
          ),
          entities: (data.analysis?.entities || []).map((e) => ({
            type: e.type,
            text: e.text,
          })),
          keyPhrases: (data.analysis?.key_phrases || []).map((p) => p.text),
        },
      };
    }

    if (data.status === "failed") {
      return { file, success: false, error: data.error || "Processing failed" };
    }
  }

  throw new Error("Timed out waiting for processing results");
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result.split(",")[1]);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

// ─────────────────────────────────────────────────────────────
// PIPELINE — SIMULATED (Phase 5 — kept for reference/testing)
// ─────────────────────────────────────────────────────────────
async function simulatePipeline(file, index) {
  const stages = [
    { id: "step-upload", label: "Uploading to S3...", ms: 600 + rand(400) },
    { id: "step-textract", label: "Textract OCR in progress…", ms: 900 + rand(600) },
    { id: "step-comprehend", label: "Comprehend NLP running…", ms: 700 + rand(400) },
    { id: "step-store", label: "Storing results to S3…", ms: 300 + rand(200) },
  ];

  for (const stage of stages) {
    setStageActive(stage.id);
    processingStatus.textContent = stage.label;
    await sleep(stage.ms);
    setStageComplete(stage.id);
  }

  const isPdf = file.type === "application/pdf";
  const isComplexPdf = isPdf && index % 5 === 4;

  if (isComplexPdf) {
    return {
      file,
      success: false,
      error: "UnsupportedDocumentException — complex PDF encoding. Known limitation: requires pdf2image + poppler fallback.",
    };
  }

  return {
    file,
    success: true,
    documentId: `doc-${Date.now()}-${index}`,
    s3Key: `processed/${file.name.replace(/\s/g, "_")}.json`,
    textract: generateMockTextract(file),
    comprehend: generateMockComprehend(),
  };
}

// ─────────────────────────────────────────────────────────────
// MOCK DATA GENERATORS
// ─────────────────────────────────────────────────────────────
function generateMockTextract(file) {
  const docTypes = ["INVOICE", "RECEIPT", "FORM", "CONTRACT"];
  const type = docTypes[Math.floor(Math.random() * docTypes.length)];

  if (type === "INVOICE")
    return {
      documentType: "INVOICE",
      fields: {
        "Invoice Number": `INV-2024-${3000 + Math.floor(Math.random() * 999)}`,
        Date: randomDate(),
        Vendor: randomVendor(),
        "Amount Due": `$${(Math.random() * 4000 + 200).toFixed(2)}`,
        "Due Date": randomDate(30),
        "PO Number": `PO-${Math.floor(Math.random() * 9000) + 1000}`,
      },
      confidence: (92 + Math.random() * 7).toFixed(1) + "%",
      pages: 1 + Math.floor(Math.random() * 3),
    };

  if (type === "RECEIPT")
    return {
      documentType: "RECEIPT",
      fields: {
        Merchant: randomVendor(),
        "Transaction Date": randomDate(),
        Total: `$${(Math.random() * 300 + 10).toFixed(2)}`,
        Tax: `$${(Math.random() * 25 + 1).toFixed(2)}`,
        "Payment Method": ["VISA ****4821", "MC ****2290", "AMEX ****0063"][
          Math.floor(Math.random() * 3)
        ],
      },
      confidence: (90 + Math.random() * 9).toFixed(1) + "%",
      pages: 1,
    };

  return {
    documentType: type,
    fields: {
      "Document ID": `DOC-${Date.now()}`,
      "Date Created": randomDate(),
      Pages: `${1 + Math.floor(Math.random() * 6)}`,
    },
    confidence: (88 + Math.random() * 10).toFixed(1) + "%",
    pages: 1 + Math.floor(Math.random() * 5),
  };
}

function generateMockComprehend() {
  const sentiments = ["POSITIVE", "NEUTRAL", "NEGATIVE", "MIXED"];
  const sentiment = sentiments[Math.floor(Math.random() * sentiments.length)];
  const confidence = (75 + Math.random() * 24).toFixed(0);
  return {
    sentiment,
    confidence: parseInt(confidence),
    entities: randomEntities(),
    keyPhrases: randomKeyPhrases(),
  };
}

function randomEntities() {
  const names = ["Acme Corp", "GlobalTech Inc", "Smith & Associates", "Patel Consulting"];
  const orgs = ["Finance Dept", "Procurement", "Accounts Payable"];
  const locs = ["New York, NY", "San Francisco, CA", "Chicago, IL"];
  return [
    { type: "ORGANIZATION", text: names[Math.floor(Math.random() * names.length)] },
    { type: "ORGANIZATION", text: orgs[Math.floor(Math.random() * orgs.length)] },
    { type: "LOCATION", text: locs[Math.floor(Math.random() * locs.length)] },
    { type: "DATE", text: randomDate() },
  ];
}

function randomKeyPhrases() {
  const pool = [
    "payment terms", "net 30", "accounts payable", "invoice total",
    "tax exempt", "purchase order", "vendor code", "billing address", "due date",
  ];
  return pool.sort(() => Math.random() - 0.5).slice(0, 4);
}

function randomVendor() {
  const v = [
    "Acme Supplies Co.", "TechVendor Inc.", "Consolidated Services",
    "Pacific Materials LLC", "Northeast Distributors",
  ];
  return v[Math.floor(Math.random() * v.length)];
}

function randomDate(offsetDays = 0) {
  const d = new Date();
  d.setDate(d.getDate() - Math.floor(Math.random() * 60) + offsetDays);
  return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
}

function rand(n) { return Math.floor(Math.random() * n); }
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

// ─────────────────────────────────────────────────────────────
// RESULTS — render cards
// ─────────────────────────────────────────────────────────────
function showResults(results, elapsedMs, count) {
  resultsSection.style.display = "block";
  resultsContainer.innerHTML = "";

  results.forEach((result) => {
    const card = document.createElement("div");
    card.className = "result-card";

    const badgeClass = result.success ? "success" : "error";
    const badgeLabel = result.success ? "✓ Processed" : "✗ Failed";

    card.innerHTML = `
      <div class="result-card-header">
        <span class="result-card-icon">${fileIcon(result.file)}</span>
        <span class="result-card-title">${result.file.name}</span>
        <span class="result-card-badge ${badgeClass}">${badgeLabel}</span>
      </div>
    `;

    if (result.success) {
      const t = result.textract;
      const c = result.comprehend;
      const sentimentClass = c.sentiment.toLowerCase();

      const fieldsHtml = Object.entries(t.fields)
        .map(([k, v]) => `
          <div class="result-row">
            <span class="result-key">${k}</span>
            <span class="result-val">${v}</span>
          </div>`)
        .join("");

      const tagsHtml = c.keyPhrases.map((p) => `<span class="tag">${p}</span>`).join("");
      const entitiesHtml = c.entities.map((e) => `<span class="tag">${e.text}</span>`).join("");

      const body = document.createElement("div");
      body.className = "result-card-body";
      body.innerHTML = `
        <div class="result-row">
          <span class="result-key">Document Type</span>
          <span class="result-val">${t.documentType}</span>
        </div>
        <div class="result-row">
          <span class="result-key">OCR Confidence</span>
          <span class="result-val">${t.confidence} · ${t.pages} page${t.pages !== 1 ? "s" : ""}</span>
        </div>
        ${fieldsHtml}
        <div class="result-row">
          <span class="result-key">S3 Key</span>
          <span class="result-val mono">${result.s3Key}</span>
        </div>
        <div class="result-row">
          <span class="result-key">Sentiment</span>
          <span class="result-val">
            <div class="sentiment-bar">
              <span class="sentiment-label ${sentimentClass}">${c.sentiment}</span>
              <div class="sentiment-track">
                <div class="sentiment-fill ${sentimentClass}" style="width:${c.confidence}%"></div>
              </div>
              <span class="result-key">${c.confidence}%</span>
            </div>
          </span>
        </div>
        <div class="result-row">
          <span class="result-key">Entities</span>
          <span class="result-val"><div class="tag-list">${entitiesHtml}</div></span>
        </div>
        <div class="result-row">
          <span class="result-key">Key Phrases</span>
          <span class="result-val"><div class="tag-list">${tagsHtml}</div></span>
        </div>
        <div class="result-row" style="padding-top: 8px; border-top: 1px solid var(--border); margin-top: 4px;">
          <span class="result-key">Output</span>
          <span class="result-val">
            <a href="dashboard.html" style="
              display: inline-flex;
              align-items: center;
              gap: 6px;
              font-family: var(--font-mono);
              font-size: 0.78rem;
              color: var(--accent);
              text-decoration: none;
              border: 1px solid rgba(0,229,160,0.3);
              background: var(--accent-dim);
              border-radius: 8px;
              padding: 6px 14px;
              transition: opacity 0.2s ease;
            " onmouseover="this.style.opacity=0.8" onmouseout="this.style.opacity=1">
              View in Dashboard →
            </a>
          </span>
        </div>
      `;
      card.appendChild(body);
    } else {
      const err = document.createElement("div");
      err.className = "result-error";
      err.innerHTML = `
        <span class="result-key">Could not process this document.</span>
        <div class="error-msg">${result.error}</div>
      `;
      card.appendChild(err);
    }

    resultsContainer.appendChild(card);
  });
}

// ─────────────────────────────────────────────────────────────
// UI STATE MANAGEMENT
// ─────────────────────────────────────────────────────────────
function showProcessing() {
  document.querySelector(".upload-section").style.display = "none";
  processingSection.style.display = "block";
  resultsSection.style.display = "none";
  statusBadge.querySelector("span:last-child").textContent = "Processing…";
  statusBadge.classList.add("processing");
  setRingProgress(0);
  resetSteps();
}

function hideProcessing() {
  processingSection.style.display = "none";
  statusBadge.querySelector("span:last-child").textContent = "Pipeline Ready";
  statusBadge.classList.remove("processing");
}

// ─────────────────────────────────────────────────────────────
// CLEAR / RESET
// ─────────────────────────────────────────────────────────────
clearBtn.addEventListener("click", () => {
  resultsSection.style.display = "none";
  document.querySelector(".upload-section").style.display = "block";
  state.files = [];
  renderFileQueue();
});

// ─────────────────────────────────────────────────────────────
// STATS
// ─────────────────────────────────────────────────────────────
function updateStats() {
  statDocs.textContent = state.totalDocs;
  const avgMs = state.totalDocs > 0 ? state.totalTime / state.totalDocs : 0;
  statTime.textContent = state.totalDocs > 0 ? `${(avgMs / 1000).toFixed(1)}s` : "—";
  statRate.textContent = state.totalDocs > 0
    ? `${Math.round((state.successCount / state.totalDocs) * 100)}%`
    : "—";
  statCost.textContent = `$${state.totalCost.toFixed(3)}`;
}

// ─────────────────────────────────────────────────────────────
// PROGRESS RING
// ─────────────────────────────────────────────────────────────
function setRingProgress(pct) {
  const circumference = 163.4;
  const offset = circumference - (pct / 100) * circumference;
  ringProgress.style.strokeDashoffset = offset;
  ringLabel.textContent = `${pct}%`;
}

// ─────────────────────────────────────────────────────────────
// PIPELINE STEP INDICATORS
// ─────────────────────────────────────────────────────────────
const stepIds = ["step-upload", "step-textract", "step-comprehend", "step-store"];

function resetSteps() {
  stepIds.forEach((id) => {
    const el = document.getElementById(id);
    el.classList.remove("active", "done");
  });
}

function setStageActive(id) {
  const idx = stepIds.indexOf(id);
  stepIds.slice(0, idx).forEach((prev) => {
    document.getElementById(prev).classList.remove("active");
    document.getElementById(prev).classList.add("done");
  });
  document.getElementById(id).classList.add("active");
}

function setStageComplete(id) {
  const el = document.getElementById(id);
  el.classList.remove("active");
  el.classList.add("done");
}

// ─────────────────────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────────────────────
renderFileQueue();