# What FinOps Taught Me About AI Governance

*I built an AI pipeline. My FinOps instincts fired the whole time. Here's what transferred — and where I hit the edge.*

---

I didn't set out to think about AI governance.

I set out to build a document processing pipeline. Ten phases, $6.90, a working product. But somewhere around Phase 6 — when I was setting rate limits before flipping a live API switch — I realized I was doing something that had a name outside of FinOps.

I was governing an AI system.

Not formally. Not with a framework. But the instincts were the same ones I use in my day job: who owns this, what can go wrong, how do we detect it when it does, and who pays when it breaks.

That's when I started mapping the overlap.

---

## The FinOps Instincts That Fired Immediately

**Rate limiting before go-live.**

Before I flipped `CONFIG.SIMULATE` to `false`, I set a usage plan: 5 requests/second, burst of 10, 100 requests/day. In FinOps terms, that's a spending guardrail. In AI governance terms, that's access control and abuse prevention. Same instinct, different vocabulary.

The FinOps framing: don't expose a live API without a cost ceiling.
The governance framing: don't deploy an AI capability without usage boundaries.

They're the same decision.

**Tagging and attribution from day one.**

Every AWS resource in DocFlow has `Project`, `CostCenter`, `Environment`, and `ManagedBy` tags before a single line of processing logic runs. I also built a Lambda that audits tag compliance every Monday and emails me a report.

In FinOps, tagging is how you answer "what did this cost and who owns it?" In AI governance, asset classification is how you answer "what AI systems do we have, who's responsible for them, and what risk tier do they sit in?" The infrastructure is identical. The taxonomy is different.

**Documented limitations over scope creep.**

Phase 4: PyPDF2 preprocessing worked perfectly. Textract still rejected the same three PDFs. The real fix — `pdf2image` and `poppler` — would take another 1-2 hours. I stopped. Documented the limitation, defined the remediation path, shipped at 80%.

In FinOps, that's a deliberate trade-off with documented reasoning. In AI governance, that's a known limitation register — exactly what NIST AI RMF asks for under Measure 2.5: "The AI system to be deployed...and its components are evaluated..." with known failure modes documented.

I didn't know the framework name at the time. I just knew you don't ship without writing down what you know doesn't work.

**Cost visibility as an accountability mechanism.**

I have a cost tracker for every phase of this project. Not because the numbers were large — $6.90 total — but because cost data is evidence. It creates accountability. It makes decisions traceable.

AI governance requires the same thing, applied to model outputs. Who made this decision? On what basis? What was the confidence score? DocFlow stores every processed document in DynamoDB with `extractionConfidence`, `processedAt`, `status`, and the full extracted data. That's an audit trail. It exists because I knew someone would eventually need to answer for a result — even if that someone is just me.

---

## Where the FinOps Vocabulary Runs Out

**Hallucination has no FinOps equivalent.**

Cost anomalies are detectable — you set a threshold, you get an alert, you investigate. Model hallucinations are structurally different. A confident wrong answer looks exactly like a confident right answer. Textract returned `extraction_confidence: 94.74%` on a document. That confidence score reflects pattern matching quality, not factual accuracy. If the invoice said $31,794.54 and Textract extracted $31,794.54, great. If the invoice was fraudulent and Textract extracted it faithfully, that's a different problem — and the confidence score doesn't help you find it.

FinOps has no analogue for this. Cost data is objective. Model outputs aren't.

**Bias doesn't show up in a cost report.**

Comprehend's sentiment analysis on all 150 test documents came back `NEUTRAL`. That's a valid statistical outcome for invoice processing. But if I were processing loan applications, performance reviews, or customer support tickets, sentiment skewing neutral across a diverse dataset would be worth interrogating. Is the model actually neutral, or is it trained on data that systematically under-represents certain populations?

FinOps teaches you to ask "is this normal?" when you see a flat line. It doesn't teach you how to identify what normal should look like for a model trained on potentially biased data.

**Explainability is a new requirement.**

When DocFlow extracts "Invoice Number: INV-2025-9308" with 89% confidence, I can trace exactly how it got there — Textract's block analysis, the KEY_VALUE_SET structure, the relationship parsing. That's explainable. But Comprehend's entity detection is a black box. I know what it returned. I don't know why it classified "Acme Corporation Metro Business Services" as a single organization entity instead of two.

For invoice processing, that ambiguity is acceptable. For a hiring decision or a credit assessment, it's not. NIST AI RMF's Explain function exists precisely because "it worked" is not a sufficient answer when the system affects people's lives.

**Data provenance is a gap I didn't close.**

Where did the training data for Textract and Comprehend come from? What languages, document types, and demographics are represented? What's the error rate by document complexity? AWS publishes some of this — but I didn't audit it before deploying. In a FinOps engagement, I'd never deploy a vendor solution without reviewing the contract, the SLA, and the pricing model. I deployed two AI services without equivalent scrutiny of their training data and known failure modes.

That's a gap. And it's one that AI governance frameworks are specifically designed to surface.

---

## The NIST AI RMF Through a FinOps Lens

The NIST AI RMF organizes AI risk management into four functions: **Govern, Map, Measure, Manage.** Here's how they map to what I already know:

**Govern** — establish accountability, policies, and culture around AI risk. FinOps equivalent: organizational FinOps practice, tagging governance, RACI for cloud costs. I have this instinct. Applying it to AI means defining who owns model outputs, not just who owns the AWS bill.

**Map** — identify and categorize AI risks in context. FinOps equivalent: cost attribution, tagging taxonomy, identifying which workloads drive which costs. I'm fluent here. The new skill is risk taxonomy: categorizing by harm type, affected population, and deployment context rather than by service and cost center.

**Measure** — analyze and assess identified risks. FinOps equivalent: cost anomaly detection, benchmark analysis, variance reporting. The FinOps muscle is strong. The new application is measuring model performance, bias, drift, and confidence calibration — not just whether the bill is higher than last month.

**Manage** — prioritize and address risks. FinOps equivalent: optimization recommendations, rightsizing, commitment coverage decisions. This one transfers almost directly. The discipline of "here's the risk, here's the trade-off, here's the recommended action" is identical. The subject matter is different.

---

## What This Means for the Practitioner Pivot

I'm a FinOps practitioner transitioning into AI/ML engineering. AI governance wasn't the plan. But building DocFlow made it obvious that the two disciplines are closer than the job descriptions suggest.

The practitioners best positioned for AI governance aren't the pure ML engineers who think about model architecture, or the pure compliance officers who think about policy checklists. They're the people who can hold both: technical enough to understand what the system is actually doing, governance-minded enough to ask who's accountable when it doesn't.

FinOps builds exactly that muscle. It puts you in conversations with engineers, finance, and leadership simultaneously. It trains you to translate between "here's what the system does" and "here's who owns the consequences."

That's the bridge. And it's wider than I expected.

---

*DocFlow's full governance assessment is a companion piece to this article — mapping every control against the NIST AI RMF and documenting what's in place, what's missing, and what an enterprise deployment would require.*

*Follow along on [Substack](https://carlandrainthecloud.substack.com) or [LinkedIn](https://linkedin.com/in/carlandra-williams).*
