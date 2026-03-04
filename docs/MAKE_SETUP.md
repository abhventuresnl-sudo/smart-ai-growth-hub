# Make.com Setup Guide — Smart AI Growth Hub Content Pipeline

This guide walks you through building two Make.com automation scenarios that connect your content pipeline outputs to Blogger and Pinterest. No prior Make.com experience is required.

---

## Prerequisites

Before building scenarios in Make.com, complete the following:

- [ ] Run `scripts/run.bat` at least once so `keywords/keywords.csv` has rows with `Status=GENERATED`
- [ ] Upload the entire `outputs/` folder to Google Drive (keep the same subfolder structure)
- [ ] Share `keywords/keywords.csv` as a Google Sheet OR upload it and convert it to Sheets format
- [ ] Connect your Google account, Blogger account, and Pinterest account to Make.com

### Google Sheet Column Reference

Your tracker sheet must have these exact column names (case-sensitive):

| Column | What It Contains |
|--------|-----------------|
| `Keyword` | The original keyword |
| `Status` | NEW / GENERATED / PUBLISHED / ERROR |
| `SEOTitle` | The optimised blog post title |
| `Slug` | The kebab-case URL slug |
| `HTMLFile` | Relative path to the HTML file (e.g. `outputs/blog_html/slug.html`) |
| `MetaDescription` | ≤155 character meta description |
| `PinterestTitles` | 10 pin titles separated by ` | ` |
| `PinterestDescriptions` | 10 pin descriptions separated by ` | ` |
| `PublishedURL` | Filled in after publishing (blank initially) |
| `CreatedAt` | Date the keyword was added |
| `UpdatedAt` | Date last updated by the pipeline |

---

## Scenario A: Publish Blog Posts to Blogger as Draft

### Overview

```
Google Sheets Watch Rows (Status=GENERATED)
    → Google Drive Get File (HTML content)
    → Blogger Create Post (title + HTML body)
    → Google Sheets Update Row (Status=PUBLISHED + URL)
```

### Step-by-Step Setup

#### Module 1: Google Sheets — Watch Rows

1. In Make.com, click **Create a new scenario**
2. Search for and add the **Google Sheets** module
3. Choose the action: **Watch Rows**
4. Connect your Google account if not already connected
5. Select your spreadsheet and the sheet containing your keyword tracker
6. Set **Row with headers** to match row 1 of your sheet
7. Set **Limit** to `5` (one batch of posts per run)

**Filter on this module:**
- Click the filter icon (wrench) after the module
- Add condition: `Status` **equals (text)** `GENERATED`
- This ensures only ready-to-publish posts are picked up

#### Module 2: Google Drive — Get a File

1. Add the **Google Drive** module
2. Choose action: **Get a File**
3. For **File ID**, use the dynamic value from Module 1:
   - Map the `HTMLFile` column value to a Google Drive file search
   - **Alternative:** Use **Google Drive — Search Files** module first, searching by name using the `Slug` value, then pipe the File ID result into **Get a File**
4. Set **Convert to text** to `Yes` (so you get the HTML string, not a binary blob)

**Recommended approach for finding the file:**

Instead of Module 2 alone, use a two-step approach:
- **Module 2a: Google Drive — Search Files**
  - Query: `name = '{{Slug}}.html'` (using the Slug value from Module 1)
  - Folder: your `outputs/blog_html/` Drive folder ID
- **Module 2b: Google Drive — Get a File**
  - File ID: map from Module 2a results (first result's ID)

#### Module 3: Blogger — Create Post

1. Add the **Blogger** module
2. Choose action: **Create a Post**
3. Connect your Blogger account
4. Select your blog from the dropdown
5. Map the fields:
   - **Title** → `SEOTitle` (from Module 1)
   - **Content** → file content (text) from Module 2b
   - **Status** → `DRAFT` (recommended — review before publishing live)
   - **Labels/Tags** → optionally add static tags like `AI Tools`, `Shopify`, `Ecommerce`

#### Module 4: Google Sheets — Update a Row

1. Add the **Google Sheets** module
2. Choose action: **Update a Row**
3. Select the same spreadsheet and sheet
4. Set **Row Number** → map from Module 1 (the row number of the watched row)
5. Map the columns to update:
   - `Status` → `PUBLISHED`
   - `PublishedURL` → URL returned by Module 3 (Blogger's post URL field)
   - `UpdatedAt` → `{{now}}` (Make.com's current date/time function)

### Error Handling for Scenario A

Add an **Error Handler** route on Module 3 (Blogger Create Post):

1. Right-click Module 3 → **Add error handler**
2. Choose **Resume** or **Break** based on your preference
3. Add a **Google Sheets Update Row** in the error path:
   - `Status` → `ERROR`
   - `UpdatedAt` → `{{now}}`
   - Optionally add an `ErrorMessage` column and map Make's error message text there

**Recommended filter on Scenario A trigger:**
- Run this scenario **on a schedule**: every Monday, Wednesday, Friday at 9:00 AM
- Or trigger manually when you have new GENERATED posts ready

---

## Scenario B: Schedule Pinterest Pins

### Overview

```
Google Sheets Watch Rows (Status=PUBLISHED)
    → Split PinterestTitles and PinterestDescriptions (Text Parser or Iterator)
    → Pinterest Create Pin (or Tailwind Schedule Pin)
    → Google Sheets Update Row (UpdatedAt)
```

### Step-by-Step Setup

#### Module 1: Google Sheets — Watch Rows

1. Add **Google Sheets — Watch Rows**
2. Same spreadsheet and sheet as Scenario A
3. **Filter:** `Status` **equals (text)** `PUBLISHED`
4. Set **Limit** to `5` rows per run

#### Module 2: Tools — Text Parser (Split the pin data)

The `PinterestTitles` and `PinterestDescriptions` columns contain 10 values separated by ` | `.

**Option A — Parse directly in Make:**
1. Add **Tools — Text Parser** module
2. Set **Pattern** to split on ` | ` (pipe with spaces)
3. Input: the `PinterestTitles` value from Module 1
4. Repeat for `PinterestDescriptions`

**Option B — Use an Iterator (simpler):**
1. Add a **Tools — Set Variable** module
2. Split the string using Make's built-in `split(PinterestTitles; " | ")` formula
3. Add an **Iterator** module and iterate over the resulting array
4. The Iterator will emit one pin title per cycle

#### Module 3a: Pinterest — Create Pin (Direct Pinterest API)

If you are connecting directly to Pinterest via Make:

1. Add **Pinterest — Create Pin** (or search for the HTTP module if Pinterest is not natively available)
2. Map the fields:
   - **Title** → current pin title from the Iterator
   - **Description** → current pin description from the Iterator
   - **Link** → `PublishedURL` from Module 1 (the live Blogger post URL)
   - **Board** → select your target Pinterest board from the dropdown
   - **Media** → you will need to supply an image URL; use a placeholder image URL for now and replace with real pin images later

**Note on Pinterest scheduling:** The Pinterest API via Make.com supports creating pins but scheduling to a specific time requires a Tailwind integration or manual scheduling within Pinterest.

#### Module 3b: Tailwind — Schedule Pin (Recommended for scheduling)

If you are using Tailwind for Pinterest scheduling:

1. Add an **HTTP — Make a Request** module (Tailwind has a REST API)
2. Method: `POST`
3. URL: `https://www.tailwindapp.com/api/1/post/` (verify current endpoint in Tailwind docs)
4. Headers: `Authorization: Bearer {{YOUR_TAILWIND_API_TOKEN}}`
5. Body (JSON):
   ```json
   {
     "postUrl": "{{PublishedURL}}",
     "imageUrl": "{{IMAGE_URL_PLACEHOLDER}}",
     "notes": "{{current_pin_description}}",
     "scheduledTime": "{{addDays(now; 1)}}"
   }
   ```
6. Replace `IMAGE_URL_PLACEHOLDER` with an actual image URL (from your Drive or Canva exports)

**Tailwind vs Direct Pinterest:**

| | Direct Pinterest | Tailwind |
|---|---|---|
| **Scheduling** | Limited (publish now only) | Full scheduling calendar |
| **Batch pinning** | API rate limits apply | Managed queue |
| **Analytics** | Pinterest native | Enhanced Tailwind analytics |
| **Cost** | Free (Make operations cost) | Tailwind subscription required |
| **Best for** | Testing / simple workflows | Consistent weekly scheduling |

#### Module 4: Google Sheets — Update a Row

1. Add **Google Sheets — Update a Row**
2. Same sheet, same row number from Module 1
3. Map:
   - `UpdatedAt` → `{{now}}`
   - Optionally add a `PinsScheduled` column and set it to `YES`

### Error Handling for Scenario B

1. Right-click the Pinterest/Tailwind module → **Add error handler**
2. In the error path, add **Google Sheets — Update Row**:
   - `Status` → `ERROR`
   - `UpdatedAt` → `{{now}}`
3. Optionally send yourself an **Email** or **Slack** notification on failure

---

## Using the Pinterest CSV Files Instead of the Sheet

If you prefer to read pin data from the CSV files generated in `outputs/pinterest_csv/` rather than the Google Sheet columns:

1. Upload `outputs/pinterest_csv/` to a Google Drive folder
2. In Scenario B, replace Module 2 with:
   - **Google Drive — Search Files**: find `{{Slug}}_pins.csv`
   - **Google Drive — Get a File**: get the CSV content as text
   - **CSV — Parse CSV**: parse the text into rows
   - **Iterator**: iterate over the rows (each row = one pin)
3. Map `Title`, `Description`, and `URL` columns directly to your Pinterest module

This approach is more flexible and keeps pin data as standalone files, which is useful if you edit pin content manually before scheduling.

---

## Recommended Make.com Scenario Settings

| Setting | Scenario A (Blogger) | Scenario B (Pinterest) |
|---------|---------------------|----------------------|
| **Schedule** | Mon/Wed/Fri 9:00 AM | Daily 10:00 AM |
| **Max rows per run** | 3–5 | 5–10 |
| **Error notifications** | Email on error | Email on error |
| **Scenario status** | Active | Active |

---

## Connecting Your Accounts in Make.com

1. Go to **Make.com → Connections**
2. Add connections for:
   - **Google** (covers Sheets, Drive, Blogger)
   - **Pinterest** (if using direct API)
3. For Tailwind, use the **HTTP module** with your API token (no native Make integration as of 2026)

---

## Testing Your Scenarios

1. **Run Scenario A once manually** (click the Run Once button in Make)
2. Check that a DRAFT post appears in your Blogger dashboard
3. Check that the Google Sheet row updated to `Status=PUBLISHED`
4. Then test Scenario B with the same row
5. Confirm a pin was created or scheduled

Only activate the automatic schedule after a successful manual test run.
