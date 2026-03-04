# Smart AI Growth Hub — Weekly Operating System

This document describes the repeatable process for producing 5 blog posts per week using the AI Content Pipeline. Follow this system consistently and the site will grow steadily without requiring you to work on it every day.

---

## The Weekly Rhythm

| Day | Task | Time Required |
|-----|------|--------------|
| **Monday** | Add new keywords, run generator | 30–45 min |
| **Tuesday** | QA review of generated posts | 60–90 min |
| **Wednesday** | Upload to Drive, trigger Blogger publishing | 20 min |
| **Thursday** | Pinterest scheduling via Make.com or Tailwind | 20 min |
| **Friday** | Review analytics, update tracking sheet | 20 min |
| **Weekend** | Optional: research next week's keywords | 30 min |

**Total active time per week: approximately 3–4 hours**

---

## Step 1 (Monday): Add New Keywords and Run the Generator

### Adding New Keywords

1. Open `keywords/keywords.csv` in Excel or Google Sheets
2. Add new rows at the bottom with the following:
   - **Keyword**: your target keyword (be specific — think about what your reader is actually searching for)
   - **Status**: `NEW`
   - **CreatedAt**: today's date (YYYY-MM-DD format)
   - Leave all other columns blank — the generator fills them in

**Keyword quality checklist before adding:**
- [ ] Is it a question or topic a Shopify/ecommerce beginner would search for?
- [ ] Does it have clear commercial or informational intent?
- [ ] Is it specific enough to produce a focused post? ("best free AI tools for writing product descriptions" is better than "AI tools")
- [ ] Is it relevant to Smart AI Growth Hub's niche (AI + ecommerce for beginners)?

**Recommended keyword sources:**
- Google Search autocomplete (type your seed topic, note the suggestions)
- Answer The Public or AlsoAsked for question-format keywords
- Reddit communities like r/shopify, r/ecommerce, r/dropship
- Your own search history — what did you Google when starting your store?

### Running the Generator

**Windows users:** Double-click `scripts/run.bat`

Or from a terminal:
```
cd path\to\smart-ai-growth-hub
python scripts\generate_content.py
```

The generator will:
1. Find all rows with `Status=NEW`
2. Generate blog HTML and Pinterest CSVs
3. Update the CSV with `Status=GENERATED` and fill in all metadata fields
4. Write a timestamped log file to `outputs/logs/`

If the script finishes without error, you are ready for QA.

---

## Step 2 (Tuesday): QA Review

This is your human quality check before anything goes live. AI-generated content is a strong first draft — not a finished product. The QA step protects your reputation and ensures your content actually helps readers.

### QA Checklist (per post)

Open each `.html` file from `outputs/blog_html/` in a web browser (drag and drop the file into Chrome or Edge).

**Content accuracy:**
- [ ] Does the post accurately describe the topic?
- [ ] Are tool names, features, and prices mentioned plausibly correct? *(Check current pricing on each tool's website — AI content can drift)*
- [ ] Are there any factual errors or misleading statements?
- [ ] Does the post avoid medical, legal, or financial claims?

**Tone and quality:**
- [ ] Does it sound human and helpful — not robotic or repetitive?
- [ ] Is the intro engaging enough that a beginner would keep reading?
- [ ] Are the CTAs (calls to action) clear and appropriate?
- [ ] Does the affiliate disclosure appear near the top?

**SEO check:**
- [ ] Is the main keyword present in the H1 title?
- [ ] Does the meta description (in the `<meta name="description">` tag) stay under 155 characters?
- [ ] Are there natural internal link placeholders (`<!-- INTERNAL_LINKS -->`) ready to fill in?

**Affiliate links:**
- [ ] Are the affiliate block placeholders (`<!-- AFFILIATE_LINK:SHOPIFY -->` etc.) in the right places?
- [ ] Replace placeholders with real affiliate links before publishing. Do this either in the HTML file directly or in Blogger's editor after the draft is created.

**After passing QA:**
- Edit the HTML file directly if small fixes are needed
- For major rewrites, edit the file and note the changes in the log
- Mark a post as "QA PASS" in your notes if it needs no changes

---

## Step 3 (Wednesday): Upload to Drive and Publish to Blogger

### Upload to Google Drive

1. Open Google Drive in your browser
2. Navigate to your `Smart AI Growth Hub` Drive folder
3. Upload (or sync) the contents of `outputs/blog_html/` to the `blog_html` subfolder in Drive
4. Upload the updated `keywords/keywords.csv` to Drive and confirm it's synced as a Google Sheet

**If using Google Drive for Desktop (sync):** The files will upload automatically. Just confirm they appear in Drive before proceeding.

### Trigger Make.com Scenario A

1. Log into Make.com
2. Open **Scenario A: Publish to Blogger**
3. Click **Run Once** to process the current batch of GENERATED posts
4. Watch the execution log — confirm each post created a Blogger draft
5. Check your Blogger dashboard to confirm the drafts appear

**After successful run:**
- The Google Sheet will update to `Status=PUBLISHED` with the Blogger post URL
- Review the Blogger draft for any formatting issues (images, tables, code blocks)
- Replace affiliate link placeholders in Blogger's HTML editor with real links
- Set the post to **Published** manually after your final review (or configure Make to publish directly — not just draft — once you are confident in the process)

---

## Step 4 (Thursday): Schedule Pinterest Pins

### Prepare Pin Images (15 minutes)

Pinterest is a visual platform — text-only pins do not perform well. Before scheduling:

1. Open Canva (canva.com) — the free plan is sufficient
2. Create a **Pinterest Pin** (1000×1500px) for each post
3. Use the post's SEO title as the pin text overlay
4. Save and download the images as PNG or JPG

**Time-saving tip:** Create a reusable Canva template with your brand colours and font. Each week, just swap the title text and export.

### Schedule Pins via Make.com Scenario B

1. Upload your pin images to the Drive folder `outputs/pin_images/` (create this folder)
2. In Make.com, open **Scenario B: Schedule Pinterest**
3. Run Once or let it run on its scheduled time
4. Confirm pins appear in your Pinterest scheduled queue or Tailwind queue

### Manual Pinterest Scheduling (Alternative)

If Make.com automation is not yet set up for Pinterest:
1. Open the `outputs/pinterest_csv/{slug}_pins.csv` file for each post
2. Use the Title and Description from the CSV to manually create pins in Pinterest
3. Schedule 2–3 pins per post across different boards and times
4. Use Tailwind's SmartSchedule feature to automatically pick optimal posting times

---

## Step 5 (Friday): Analytics Review

### What to Check (15–20 minutes)

**Blogger/Google:**
- Are recent posts indexed? (Search `site:yourblog.blogspot.com` in Google)
- Which posts are getting the most views in Blogger's stats?
- Any comments or questions to respond to?

**Pinterest:**
- Which pins are getting the most impressions and clicks?
- Any pins performing unusually well? (Create more pins for that post)

**Google Search Console (recommended setup):**
- Add your Blogger site to Google Search Console (it's free)
- Check which keywords you are starting to rank for
- Look for pages with high impressions but low clicks — these need better titles or meta descriptions

### Tracking Updates

In your keywords tracker (Google Sheet or CSV):
- Note which posts are live
- Add a rough view count or impression count in a notes column
- Flag any posts that need updating based on performance

---

## Batch Operations

### Running the Generator for Multiple Keywords at Once

The generator is designed to handle batches. Add as many `Status=NEW` rows as you want and run the script once. It processes all new rows in a single run.

**Recommended batch size:** 5–10 keywords per run. Larger batches work fine but take longer to QA.

### Re-generating a Post

If you want to regenerate a post (e.g., after adding a new keyword profile):
1. Open `keywords/keywords.csv`
2. Find the row for the keyword
3. Change `Status` from `GENERATED` back to `NEW`
4. Delete the existing HTML file from `outputs/blog_html/`
5. Run the generator again

The script will not overwrite files for rows where `Status` is not `NEW` — this is intentional to protect content you've already reviewed.

---

## Expanding the Keyword Database

The generator script (`scripts/generate_content.py`) contains a `KEYWORD_PROFILES` dictionary with detailed profiles for the 5 starter keywords. As you add new keywords, you have two options:

**Option A: Add a profile to the script (recommended for important keywords)**
1. Open `scripts/generate_content.py`
2. Copy an existing profile block in `KEYWORD_PROFILES`
3. Add your new keyword as the key (lowercase) and fill in the profile fields
4. The generated post will be high quality and on-topic

**Option B: Let the fallback handle it**
For any keyword without a profile, the generator creates a generic post structure. This works but produces less targeted content. Always review fallback posts carefully during QA.

---

## Common Issues and Fixes

| Issue | Likely Cause | Fix |
|-------|-------------|-----|
| Script says "No Python found" | Python not installed or not on PATH | Download Python from python.org, check "Add to PATH" during install |
| Post HTML file not found in Drive | Upload did not complete | Re-upload `outputs/` folder to Drive |
| Make scenario skips rows | Filter condition wrong | Check that `Status` column name matches exactly and filter value is `GENERATED` |
| Blogger draft has broken formatting | HTML file has encoding issues | Open HTML in browser first to check, then copy clean content into Blogger |
| Pinterest pin has no image | Image URL not set | Manually add a Canva image URL or upload image directly in Pinterest |
| CSV has extra blank rows | Excel added trailing rows | Open CSV in Notepad and delete blank lines at the bottom |

---

## Monthly Review (30 minutes)

Once per month, take a step back and review the system as a whole:

1. **Content audit:** Are the posts on your site current and accurate? AI tools update frequently — verify pricing and features mentioned in older posts every 2–3 months.
2. **Keyword performance:** Which keywords from your tracker are ranking? Double down on related keywords in those categories.
3. **Affiliate link audit:** Are all affiliate links working? Broken links mean lost revenue.
4. **Process improvements:** Is there a step in the weekly system that feels slow or manual? Note it and look for a way to automate it.
5. **Backup:** Download a copy of your keywords CSV and outputs folder to a local backup location.

---

## Goal: 5 Posts Per Week

To consistently hit 5 posts per week:

- Add 5–10 new keywords every Monday (a buffer in case some fail QA)
- Keep your Canva pin template ready so image creation is fast
- Run the generator on a fixed schedule so it becomes automatic
- Use the QA checklist consistently — don't skip it, even when the AI output looks good

**After 12 weeks at this pace:** 60 posts live, Pinterest pins active, and real search data to guide your content strategy.

---

*This operating system is designed to be simple and sustainable. Adjust the schedule and batch sizes to match your available time. A consistent 2-hour week beats an inconsistent 10-hour week.*
