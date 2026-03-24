# Ship What Works, Document What Doesn't: Building a Serverless Document Pipeline on AWS

---

My partner used to own three businesses at the same time.

Not three locations of the same business — three different businesses. And for all three, he maintained the invoicing manually. Spreadsheets, paper trails, hours of work every month that existed purely because no one had built him a better option.

That's the small and medium business reality that gets skipped in most AI conversations. The use cases you see covered are enterprise — Fortune 500 workflows, large-scale data pipelines, six-figure implementations. SMBs are left figuring it out on their own, usually with tools that weren't designed for them or price points that don't make sense at their scale.

I wanted to build something that made sense for a business like his.

An AI document processor: upload an invoice or receipt, get back structured data automatically. No manual entry. No spreadsheets. Thirty seconds instead of three minutes, at $0.034 per document instead of $1.25 in staff time.

The other honest reason I built this: I had just passed my AWS AI Practitioner exam, I had barely-basic Python skills, and I wanted to know if I could build something real — not follow a tutorial, but actually build something — using what I knew and AI as a thought partner from conception to production. That challenge was half the point.

---

## What I built

A fully serverless AWS pipeline:

- **S3** — three buckets for uploads, processed results, and the frontend
- **Lambda** — three functions handling document processing, upload, and results retrieval
- **Textract** — OCR, key-value pair extraction, table analysis
- **Comprehend** — entity detection, sentiment analysis, key phrase extraction
- **API Gateway** — REST endpoints with rate limiting
- **EventBridge + SNS** — automated weekly tag compliance audits
- **Frontend** — drag-and-drop UI with real-time pipeline visualization

[architecture diagram screenshot]

Upload a document through the UI. It lands in S3, triggers the processor Lambda, runs through Textract and Comprehend, and the results come back as structured JSON. Names, dates, amounts, entities, sentiment — all of it extracted and organized automatically.

---

## The tagging side quest I almost skipped

Before I wrote a single line of processing logic, I set up resource tagging. Every AWS resource in this project gets `Project`, `CostCenter`, `Environment`, and `ManagedBy` tags from day one.

I want to be honest about this: even as a FinOps professional, I almost let it slide. It felt like overhead at the start of a project, not a priority.

I'm glad I didn't skip it. And I took it one step further — I built a Lambda function that runs every Monday, scans all my resources for missing tags, and sends me an email report. I also wrote `fix-tags.sh`, a script that applies the standard tag set to any resource ARN in a single command.

AWS Config does the same compliance scanning for about $1/month. My version cost $0.00 and forced me to actually build the Lambda, EventBridge schedule, and SNS notification by hand. I learned more from that side quest than I expected to.

The practical lesson: tagging is the kind of thing that's easy to do at the start and painful to retrofit later. A FinOps professional who lets their own projects go untagged doesn't have much credibility recommending tagging governance to anyone else. The automation made sure I wouldn't.

---

## Where I hit a wall I didn't see coming

Textract testing went well — until it didn't.

I tested against fifteen documents: invoices and receipts of varying complexity. Twelve processed perfectly. Three threw this:

```
UnsupportedDocumentException: Request has unsupported document format
```

Valid PDFs. Readable in any viewer. Textract just wouldn't touch them.

The obvious fix was a preprocessing step — normalize the PDFs before sending them to Textract. I built a Lambda layer with PyPDF2 to do exactly that. This was new territory for me; I'd never built a Lambda layer before. The process taught me things I didn't expect: Python version matching between your local environment and your Lambda runtime matters more than you'd think, and there are some AWS limitations that don't need workarounds — they just need a note in the dev log.

The preprocessing pipeline worked exactly as designed.

```
PDF has 2 page(s), normalizing...
Normalization complete: 3758 → 3283 bytes
Starting Textract analysis...
Textract error: UnsupportedDocumentException
```

Textract still rejected them.

PyPDF2 had done everything right. The files were smaller, cleaner, properly restructured. The problem was deeper than normalization — these PDFs were fundamentally incompatible with Textract regardless of what I did to them upstream. The real fix would require `pdf2image` and `poppler`: render each page as a JPEG image, then send the image to Textract instead. Textract handles images reliably every time.

That's another 1-2 hours of work, another layer to build and maintain, more complexity in the pipeline.

I went into the weeds on this one. I sat with the problem longer than I should have, kept looking for a cleaner solution, kept thinking there had to be something I was missing. There wasn't. The fix I'd found was the fix. I just didn't love it.

Eventually I stopped.

End of week deadline. Twelve of fifteen documents processing successfully. Clear root cause documented. Clear remediation path defined. The preprocessing foundation I'd built was the right architectural starting point — exactly what a production team would build before adding image conversion fallbacks. The 20% failure case had a name, a root cause, and a next step.

Here's the thing about testing: not every test has to come back 100% to be a passing score. Eighty percent with a documented path to a hundred is an honest result. Chasing the last twenty percent past your deadline, for a learning project, isn't engineering discipline. It's getting stuck in the weeds.

Ship what works. Document what doesn't.

---

## Rate limiting before the live switch

Building the frontend was straightforward — drag-and-drop upload, real-time pipeline visualization, result cards. What was interesting was the `CONFIG.SIMULATE` flag I built into it.

Before wiring the frontend to a real API, I ran it in simulation mode: realistic mock data, fake processing delays, the same results the real pipeline would return. This let me build, test, and demo the full experience without making a single real Textract call.

The flag would stay on until two things were done: the API was live, and rate limiting was in place.

That second condition is the FinOps instinct. I had set myself a cost ceiling for this project. An open API endpoint with no guardrails is an invitation to a runaway bill — whether from a mistake, a test gone long, or someone else hitting the URL. Before I flipped the switch, I set up a usage plan: 5 requests per second, burst of 10, hard cap of 100 requests per day. Worst case, that's $0.32/day in Textract costs.

Then I flipped the flag, redeployed the frontend, and ran a curl test.

Clean JSON back. 94.74% extraction confidence on the first real document. It worked.

---

## The batch test, and the fine print I should have read

With the live API running, I ran all 150 mock documents through the pipeline at once.

```
BATCH TEST COMPLETE
Total:   150
Passed:  150 (100.0%)
Failed:  0
Errors:  0
Avg Confidence: 80.88%
```

Then the email arrived from AWS.

> Your account has exceeded 85% of the usage limit for AmazonTextract — 100 Pages for AnalyzeDocTables.

I had hit the free tier ceiling for Textract's table analysis feature in a single afternoon. The overage: $3.55.

This one's on me. I chose to test 150 documents at once and I didn't read the free tier limits carefully enough before I did it. The table analysis feature — `AnalyzeDocTables` — has a separate 100-page monthly limit that I ran straight through.

The rate limiting I'd set up protects against per-second abuse. It doesn't protect against monthly free tier consumption. Those are different problems with different solutions. I had the right guardrail for the wrong scenario.

Total project cost: $5.90. I'm not bothered by it — $3.55 of that came from proving the pipeline works at real scale, which is exactly what the test was for. But I'd have preferred to know it was coming.

Read the fine print on the free tier before you run a batch test.

---

## What actually made this possible

I want to be direct about something: I could not have built this without AI as a thought partner.

Not because the technology is too hard, but because the gap between "I passed an exam" and "I can build this from scratch" is real, and AI closed a lot of that gap for me. Architecture questions, Python I didn't know how to write, debugging errors I'd never seen before, cost modeling, documentation — I used AI at every stage, and I used it openly.

That's not a shortcut. That's the actual skill set I'm building: knowing what to build, knowing how to ask the right questions to build it, and knowing when the answer you got is wrong. The judgment layer doesn't go away because AI is in the loop. It becomes more important.

The AI Practitioner exam gave me the vocabulary. Prompt engineering gave me the methodology. Building this project gave me the evidence.

---

*Code is on [GitHub](https://github.com/theDovelyDev/theprojectfolder/tree/main/IDR_pipeline). Dev log, architecture diagrams, and cost tracker are all in the repo.*

*Next: Budget Research Agent — a LangGraph agent with a real-time cost tracker and a human-in-the-loop budget interrupt. Because the same pattern that controls $0.05 controls $50,000.*

*Follow along on [Substack](https://carlandrainthecloud.substack.com) or [LinkedIn](https://linkedin.com/in/carlandra-williams).*
