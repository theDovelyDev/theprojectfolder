/* ============================================================
   DocFlow — app.js
   Phase 5: Frontend logic with simulated pipeline
   Phase 6 TODO markers clearly indicate API wiring points
   ============================================================ */

// ─────────────────────────────────────────────────────────────
// CONFIG — update these in Phase 6 when API Gateway is live
// ─────────────────────────────────────────────────────────────
const CONFIG = {
  // Phase 6: replace with your API Gateway URL
  // e.g. https://abc123.execute-api.us-east-1.amazonaws.com/prod
  API_ENDPOINT: null,

  // Your frontend + uploads bucket names (fill in your ACCOUNT_ID)
  UPLOAD_BUCKET: "doc-processing-demo-uploads-ACCOUNT_ID",
  FRONTEND_BUCKET: "doc-processing-demo-frontend-ACCOUNT_ID",
  AWS_REGION: "us-east-1",

  // Cost estimate per document ($0.034 based on Phase 3 actuals)
  COST_PER_DOC: 0.034,

  // Phase 5: simulate processing (set false in Phase 6 when real API is wired)
  SIMULATE: true,
};

// ─────────────────────────────────────────────────────────────
// STATE
// ─────────────────────────────────────────────────────────────
const state = {
  files: [], // File objects queued for processing
  totalDocs: 0,
  totalTime: 0, // ms
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

// Stats
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
  fileInput.value = ""; // reset so same file can be re-added
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
    // Deduplicate by name + size
    const exists = state.files.some(
      (f) => f.name === file.name && f.size === file.size,
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

  // Remove buttons
  fileQueue.querySelectorAll(".file-item-remove").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const idx = parseInt(e.currentTarget.dataset.index);
      state.files.splice(idx, 1);
      renderFileQueue();
    });
  });

  // Process button state
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
        // ── PHASE 6 TODO ──────────────────────────────────
        // Replace simulatePipeline with real API calls:
        // 1. Get presigned URL from POST /upload
        // 2. PUT file bytes to presigned URL (direct to S3)
        // 3. Poll GET /results/{documentId} until done
        // result = await runRealPipeline(file);
        // ─────────────────────────────────────────────────
        result = await simulatePipeline(file, i);
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
// PIPELINE — SIMULATED (Phase 5)
// Mimics the real pipeline stages with realistic timing
// ─────────────────────────────────────────────────────────────
async function simulatePipeline(file, index) {
  const stages = [
    { id: "step-upload", label: "Uploading to S3...", ms: 600 + rand(400) },
    {
      id: "step-textract",
      label: "Textract OCR in progress…",
      ms: 900 + rand(600),
    },
    {
      id: "step-comprehend",
      label: "Comprehend NLP running…",
      ms: 700 + rand(400),
    },
    { id: "step-store", label: "Storing results to S3…", ms: 300 + rand(200) },
  ];

  for (const stage of stages) {
    setStageActive(stage.id);
    processingStatus.textContent = stage.label;
    await sleep(stage.ms);
    setStageComplete(stage.id);
  }

  // 80% success rate — matches Phase 3/4 actuals
  const isPdf = file.type === "application/pdf";
  const isComplexPdf = isPdf && index % 5 === 4; // simulate the known 20% failure

  if (isComplexPdf) {
    return {
      file,
      success: false,
      error:
        "UnsupportedDocumentException — complex PDF encoding. Known limitation: requires pdf2image + poppler fallback (Phase 4 remediation path).",
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
// PIPELINE — REAL (Phase 6 implementation)
// ─────────────────────────────────────────────────────────────

/* ── PHASE 6 TODO ──────────────────────────────────────────
   Uncomment and implement when API Gateway is deployed.

async function runRealPipeline(file) {
    // Step 1: Request a presigned URL from your upload Lambda
    //
    // WHY presigned URLs?
    // The browser can't hold AWS credentials safely. Instead, your
    // Lambda generates a temporary signed URL that lets the browser
    // PUT the file directly to S3 — no credentials exposed client-side.
    //
    const uploadResp = await fetch(`${CONFIG.API_ENDPOINT}/upload`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fileName: file.name, fileType: file.type }),
    });
    if (!uploadResp.ok) throw new Error(`Upload request failed: ${uploadResp.status}`);
    const { presignedUrl, documentId } = await uploadResp.json();

    // Step 2: PUT the file directly to S3 via presigned URL
    const s3Resp = await fetch(presignedUrl, {
        method: 'PUT',
        headers: { 'Content-Type': file.type },
        body: file,
    });
    if (!s3Resp.ok) throw new Error(`S3 upload failed: ${s3Resp.status}`);

    // Step 3: Poll GET /results/{documentId} until Lambda finishes
    //
    // WHY polling?
    // Textract + Comprehend take seconds to run. The browser can't
    // hold a connection open that long reliably. Instead, we ask
    // "is it done yet?" every 2 seconds. WebSockets/EventBridge would
    // be the production upgrade, but polling is simple and correct here.
    //
    for (let attempt = 0; attempt < 20; attempt++) {
        await sleep(2000);
        const resultResp = await fetch(`${CONFIG.API_ENDPOINT}/results/${documentId}`);
        if (!resultResp.ok) continue;
        const data = await resultResp.json();
        if (data.status === 'complete') return { file, success: true, ...data };
        if (data.status === 'failed')   return { file, success: false, error: data.error };
    }
    throw new Error('Timed out waiting for processing results');
}
─────────────────────────────────────────────────────────── */

// ─────────────────────────────────────────────────────────────
// MOCK DATA GENERATORS (realistic Phase 5 simulation)
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
  const entities = randomEntities();
  const keyPhrases = randomKeyPhrases();

  return { sentiment, confidence: parseInt(confidence), entities, keyPhrases };
}

function randomEntities() {
  const names = [
    "Acme Corp",
    "GlobalTech Inc",
    "Smith & Associates",
    "Patel Consulting",
  ];
  const orgs = ["Finance Dept", "Procurement", "Accounts Payable"];
  const locs = ["New York, NY", "San Francisco, CA", "Chicago, IL"];
  return [
    {
      type: "ORGANIZATION",
      text: names[Math.floor(Math.random() * names.length)],
    },
    {
      type: "ORGANIZATION",
      text: orgs[Math.floor(Math.random() * orgs.length)],
    },
    { type: "LOCATION", text: locs[Math.floor(Math.random() * locs.length)] },
    { type: "DATE", text: randomDate() },
  ];
}

function randomKeyPhrases() {
  const pool = [
    "payment terms",
    "net 30",
    "accounts payable",
    "invoice total",
    "tax exempt",
    "purchase order",
    "vendor code",
    "billing address",
    "due date",
  ];
  return pool.sort(() => Math.random() - 0.5).slice(0, 4);
}

function randomVendor() {
  const v = [
    "Acme Supplies Co.",
    "TechVendor Inc.",
    "Consolidated Services",
    "Pacific Materials LLC",
    "Northeast Distributors",
  ];
  return v[Math.floor(Math.random() * v.length)];
}

function randomDate(offsetDays = 0) {
  const d = new Date();
  d.setDate(d.getDate() - Math.floor(Math.random() * 60) + offsetDays);
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function rand(n) {
  return Math.floor(Math.random() * n);
}
function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
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
        .map(
          ([k, v]) => `
                    <div class="result-row">
                        <span class="result-key">${k}</span>
                        <span class="result-val">${v}</span>
                    </div>`,
        )
        .join("");

      const tagsHtml = c.keyPhrases
        .map((p) => `<span class="tag">${p}</span>`)
        .join("");
      const entitiesHtml = c.entities
        .map((e) => `<span class="tag">${e.text}</span>`)
        .join("");

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
  statTime.textContent =
    state.totalDocs > 0 ? `${(avgMs / 1000).toFixed(1)}s` : "—";

  statRate.textContent =
    state.totalDocs > 0
      ? `${Math.round((state.successCount / state.totalDocs) * 100)}%`
      : "—";

  statCost.textContent = `$${state.totalCost.toFixed(3)}`;
}

// ─────────────────────────────────────────────────────────────
// PROGRESS RING
// ─────────────────────────────────────────────────────────────
function setRingProgress(pct) {
  const circumference = 163.4; // 2π × r=26
  const offset = circumference - (pct / 100) * circumference;
  ringProgress.style.strokeDashoffset = offset;
  ringLabel.textContent = `${pct}%`;
}

// ─────────────────────────────────────────────────────────────
// PIPELINE STEP INDICATORS
// ─────────────────────────────────────────────────────────────
const stepIds = [
  "step-upload",
  "step-textract",
  "step-comprehend",
  "step-store",
];

function resetSteps() {
  stepIds.forEach((id) => {
    const el = document.getElementById(id);
    el.classList.remove("active", "done");
  });
}

function setStageActive(id) {
  // Mark previous steps done
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
