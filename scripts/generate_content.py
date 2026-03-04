"""
Smart AI Growth Hub — AI Content Pipeline Generator
====================================================
Reads keywords/keywords.csv and generates:
  - SEO-optimised affiliate blog posts (HTML)
  - Pinterest pin metadata (CSV)
  - Updated keyword tracker CSV

Requirements: Python 3.8+ standard library only.
Run from the project root:  python scripts/generate_content.py
"""

import csv
import json
import os
import re
import sys
import logging
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths (resolved relative to this script's parent folder)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
KEYWORDS_CSV = BASE_DIR / "keywords" / "keywords.csv"
BLOG_HTML_DIR = BASE_DIR / "outputs" / "blog_html"
PINTEREST_CSV_DIR = BASE_DIR / "outputs" / "pinterest_csv"
LOGS_DIR = BASE_DIR / "outputs" / "logs"
AFFILIATE_LINKS_JSON = BASE_DIR / "config" / "affiliate_links.json"

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_filename = LOGS_DIR / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Affiliate links
# ---------------------------------------------------------------------------

# Maps uppercase HTML comment tags → lowercase keys in affiliate_links.json
TAG_TO_AFFILIATE_KEY = {
    "SHOPIFY": "shopify",
    "AI_COPY_TOOL": "jasper",
    "EMAIL_MARKETING_TOOL": "mailerlite",
    "CONVERTKIT": "convertkit",
    "CANVA": "canva",
}

TAG_DISPLAY_LABELS = {
    "SHOPIFY": "Start your free Shopify trial →",
    "AI_COPY_TOOL": "Try Jasper AI free →",
    "EMAIL_MARKETING_TOOL": "Try MailerLite free →",
    "CONVERTKIT": "Try ConvertKit free →",
    "CANVA": "Try Canva free →",
}


def load_affiliate_links() -> dict:
    """Return non-empty affiliate URLs from config/affiliate_links.json."""
    if not AFFILIATE_LINKS_JSON.exists():
        log.warning(f"affiliate_links.json not found at {AFFILIATE_LINKS_JSON}")
        return {}
    with open(AFFILIATE_LINKS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    loaded = {k: v for k, v in data.items() if v}
    log.info(f"Loaded {len(loaded)} affiliate link(s): {list(loaded.keys())}")
    return loaded


AFFILIATE_LINKS = load_affiliate_links()


def inject_affiliate_links(html: str) -> str:
    """Replace <!-- AFFILIATE_LINK:TAG --> placeholders with real anchor tags.

    Tags with no URL configured are silently removed (comment stripped).
    """
    def replace_tag(match):
        tag = match.group(1)
        key = TAG_TO_AFFILIATE_KEY.get(tag)
        if key:
            url = AFFILIATE_LINKS.get(key, "")
            if url:
                label = TAG_DISPLAY_LABELS.get(tag, f"Learn more →")
                return (
                    f'<p><a href="{url}" rel="nofollow sponsored" target="_blank">'
                    f'{label}</a></p>'
                )
        return ""  # drop the comment when no URL is configured

    return re.sub(r"<!-- AFFILIATE_LINK:([A-Z0-9_]+) -->", replace_tag, html)


# ---------------------------------------------------------------------------
# Keyword → content mapping
# ---------------------------------------------------------------------------

KEYWORD_PROFILES = {
    "best ai tools for shopify beginners 2026": {
        "template": "listicle",
        "seo_title": "7 Best AI Tools for Shopify Beginners in 2026 (Tested & Ranked)",
        "meta": "Discover the 7 best AI tools for Shopify beginners in 2026. Save time, grow faster, and automate your store — even with zero tech experience.",
        "topic": "best AI tools for Shopify beginners",
        "tools": [
            {"name": "Tidio AI", "use": "AI Customer Support", "price": "Free / $29/mo",
             "tag": "TIDIO", "pros": ["Easy to set up", "Works right out of the box", "Free plan available"],
             "cons": ["Limited customisation on free tier", "Can feel repetitive for complex queries"],
             "description": "Tidio is an AI-powered live chat and chatbot platform built with ecommerce in mind. It connects directly to your Shopify store and can automatically answer customer questions, track orders, and recover abandoned carts.",
             "best_for": "Beginners who want to automate customer support without hiring staff"},
            {"name": "Jasper AI", "use": "AI Copywriting", "price": "$49/mo",
             "tag": "AI_COPY_TOOL", "pros": ["Huge template library", "Shopify product description mode", "Beginner-friendly"],
             "cons": ["No free plan", "Can produce generic output without good prompts"],
             "description": "Jasper is one of the most popular AI writing tools available. For Shopify store owners, it excels at generating product descriptions, email campaigns, and ad copy in minutes rather than hours.",
             "best_for": "Store owners who struggle with writing and want to publish content consistently"},
            {"name": "Klaviyo AI", "use": "AI Email Marketing", "price": "Free up to 500 contacts",
             "tag": "EMAIL_MARKETING_TOOL", "pros": ["Deep Shopify integration", "AI subject line suggestions", "Predictive analytics"],
             "cons": ["Pricing scales fast as your list grows", "Learning curve for advanced flows"],
             "description": "Klaviyo is the email marketing platform of choice for serious Shopify sellers. Its AI features help you write better subject lines, predict when customers will buy again, and segment your audience automatically.",
             "best_for": "Store owners ready to build an email list and automate follow-ups"},
            {"name": "Replo", "use": "AI Landing Page Builder", "price": "$99/mo",
             "tag": "REPLO", "pros": ["Purpose-built for Shopify", "No coding needed", "AI section generation"],
             "cons": ["Higher price point", "Overkill for very small stores"],
             "description": "Replo lets you build high-converting landing pages and sales pages directly inside Shopify using drag-and-drop — no developer needed. The AI features help generate section copy and layout ideas.",
             "best_for": "Store owners running paid ads who need fast, professional landing pages"},
            {"name": "Ecomtent", "use": "AI Product Images & Content", "price": "$49/mo",
             "tag": "ECOMTENT", "pros": ["Generates lifestyle product images with AI", "Bulk content creation", "SEO descriptions included"],
             "cons": ["Newer tool — still evolving", "Image quality varies by product type"],
             "description": "Ecomtent uses AI to generate lifestyle product images and SEO-optimised content at scale. Instead of expensive photoshoots, you can create scroll-stopping visuals for your listings.",
             "best_for": "Dropshippers or store owners who need great product images without a photographer"},
        ],
        "alts": [
            {"name": "Zyro AI", "desc": "An affordable all-in-one website builder with built-in AI copywriting tools — good if you're still deciding on a platform."},
            {"name": "AutoDS", "desc": "An automation platform for dropshipping with AI-assisted product research and listing creation."},
            {"name": "ChatGPT (OpenAI)", "desc": "The versatile AI assistant you can use for product descriptions, email drafts, social captions, and more at a low monthly cost."},
        ],
        "faqs": [
            {"q": "Do I need technical skills to use AI tools with Shopify?", "a": "No. The tools in this list are specifically chosen because they are beginner-friendly. Most connect to Shopify with a simple install from the Shopify App Store, with no coding required."},
            {"q": "Are AI tools worth the cost for a new Shopify store?", "a": "It depends on the tool. We recommend starting with free plans or trials before committing. Many tools — like Klaviyo and Tidio — have genuinely useful free tiers that are plenty for a store just starting out."},
            {"q": "Can AI replace a professional copywriter for my store?", "a": "AI tools are excellent for producing first drafts quickly, but human review is still valuable — especially for brand voice, accuracy, and nuance. Think of AI as a very fast writing assistant, not a full replacement."},
            {"q": "Which AI tool should I start with as a complete beginner?", "a": "We recommend starting with Tidio (customer support) and Klaviyo (email) because both have strong free plans, connect directly to Shopify, and solve real pain points from day one."},
            {"q": "Will these AI tools work outside of Shopify?", "a": "Most of the tools listed — like Jasper and ChatGPT — work with any ecommerce platform. Klaviyo and Tidio also support WooCommerce, BigCommerce, and others. Replo is Shopify-specific."},
            {"q": "How quickly will I see results from using AI tools?", "a": "You can see results almost immediately for tasks like writing product descriptions or setting up a chatbot. For email marketing and SEO, results build over weeks and months as you grow your audience."},
        ],
        "intro": "Starting a Shopify store in 2026 without the right AI tools is like opening a restaurant without a kitchen — technically possible, but exhausting and slow. The good news? There are now beginner-friendly AI tools that can write your product descriptions, handle customer questions, send personalised emails, and even create product images — all without needing to hire anyone.",
        "conclusion": "The right AI tools can turn a one-person Shopify operation into something that punches well above its weight. Start small — pick one or two tools from this list that address your biggest pain point right now, whether that's customer support, content creation, or email marketing.",
        "cta": "Start your Shopify store today and put these AI tools to work from day one.",
    },

    "how to automate shopify with ai step by step": {
        "template": "howto",
        "seo_title": "How to Automate Your Shopify Store with AI (Step-by-Step for Beginners)",
        "meta": "Learn how to automate your Shopify store with AI step by step. Cut hours of manual work and grow your ecommerce business faster — beginner-friendly guide.",
        "topic": "automate Shopify with AI",
        "goal": "automate your Shopify store using AI tools",
        "steps": [
            {"title": "Map Out What You Want to Automate",
             "intro": "Before touching any tools, spend 15 minutes listing the repetitive tasks that eat your time every week. Common candidates for Shopify automation include answering customer questions, writing product descriptions, sending order follow-up emails, recovering abandoned carts, and updating inventory.",
             "actions": ["Open a spreadsheet or notepad and write down your top 5 time-consuming tasks", "Mark each task as: Customer-Facing, Content, or Operations", "Prioritise the tasks that happen most often and take the most time"],
             "tip": "Focus on automating tasks you currently do manually — not tasks you've never tried. Automation works best when you understand the process first.",
             "tag": "SHOPIFY"},
            {"title": "Set Up AI Customer Support with Tidio",
             "intro": "Customer questions are one of the biggest time drains for solo store owners. Tidio's AI can handle common questions — shipping times, return policy, order tracking — automatically, 24/7.",
             "actions": ["Go to the Shopify App Store and install Tidio", "Connect Tidio to your Shopify store and sync your product catalogue", "Enable the Lyro AI bot and set your business hours and fallback message"],
             "tip": "Write out your 10 most common customer questions and add them to Tidio's FAQ section during setup. The more context you give the AI, the better its responses will be.",
             "tag": "TIDIO"},
            {"title": "Automate Email Marketing with Klaviyo AI",
             "intro": "Email automation is where most Shopify stores leave money on the table. Klaviyo's AI can automatically send welcome emails, abandoned cart reminders, and post-purchase sequences — all personalised to each customer.",
             "actions": ["Install Klaviyo from the Shopify App Store and connect your store", "Enable the Abandoned Cart flow (pre-built templates are available)", "Turn on the Welcome Series and Post-Purchase follow-up sequences"],
             "tip": "Don't try to build every flow on day one. Start with Abandoned Cart — it typically recovers 5–15% of lost sales automatically.",
             "tag": "EMAIL_MARKETING_TOOL"},
            {"title": "Use AI to Generate Product Descriptions at Scale",
             "intro": "Writing unique, SEO-friendly product descriptions for every item in your store is time-consuming. AI writing tools like Jasper or even ChatGPT can produce a solid first draft in seconds.",
             "actions": ["Choose an AI writing tool (Jasper, ChatGPT, or similar)", "Create a prompt template that includes: product name, key features, target customer, and tone", "Generate descriptions in batches and paste into Shopify — always review before publishing"],
             "tip": "Include your brand voice in your prompt. For example: 'Write in a friendly, conversational tone for first-time ecommerce shoppers.'",
             "tag": "AI_COPY_TOOL"},
            {"title": "Connect It All with Make.com (Optional but Powerful)",
             "intro": "Once you have individual automations running, Make.com lets you connect them into full workflows. For example: when a new product is added to Shopify → automatically generate a description with AI → post to social media.",
             "actions": ["Create a free Make.com account at make.com", "Choose the Shopify module as your trigger (e.g. 'Watch New Products')", "Add actions to connect your AI tools and social platforms"],
             "tip": "Start with one simple scenario in Make before building complex multi-step workflows. A working simple automation beats a broken complex one.",
             "tag": "SHOPIFY"},
        ],
        "alts": [
            {"title": "Use Zapier Instead of Make.com", "desc": "Zapier is slightly easier for beginners but has fewer features on the free plan. Good option if you need something running quickly without a learning curve.", "best_for": "Absolute beginners who want simple two-step automations"},
            {"title": "Use Shopify Flow (Built-in)", "desc": "Shopify's own automation tool is available on paid plans. It handles inventory alerts, order tagging, and customer segmentation natively — no third-party tools needed.", "best_for": "Store owners who want automation without adding new software"},
            {"title": "Hire a VA + AI Combo", "desc": "If full automation feels overwhelming, a virtual assistant using AI tools can handle tasks at a fraction of the cost of a full employee.", "best_for": "Store owners who prefer human oversight but want to reduce workload"},
        ],
        "faqs": [
            {"q": "How much does it cost to automate a Shopify store with AI?", "a": "You can start for free with tools like Tidio, Klaviyo (up to 500 contacts), and Make.com (basic plan). A reasonable beginner budget for AI automation is $30–$100/month, which can save many hours of manual work each week."},
            {"q": "Do I need to know how to code to automate Shopify?", "a": "No coding is required. All the tools in this guide are designed for non-technical users. If you can drag, drop, and fill in a form, you can set up these automations."},
            {"q": "Will AI automation make my store feel impersonal?", "a": "Not if done correctly. Good AI automation is designed to feel personal — for example, Klaviyo sends emails with the customer's name and references their specific purchase. The goal is to scale personalisation, not remove it."},
            {"q": "How long does it take to set up these automations?", "a": "Most of the basic automations in this guide can be set up in an afternoon. The email flows in Klaviyo have pre-built templates that take under an hour to configure."},
            {"q": "What if an AI tool makes a mistake?", "a": "Always review AI-generated content before it goes live — especially product descriptions and email copy. For customer-facing chatbots, set a fallback to hand off to a human when the AI is unsure."},
            {"q": "Which automation should I set up first?", "a": "Start with Abandoned Cart emails in Klaviyo. It directly recovers revenue you're already losing, and it typically takes less than an hour to activate using Klaviyo's pre-built template."},
        ],
        "intro": "Imagine waking up to new orders processed, customer questions answered, and follow-up emails already sent — all while you were asleep. That's what AI automation can do for your Shopify store. And the best part? You don't need a developer or a big budget to get started.",
        "conclusion": "Shopify automation with AI is not just for big brands anymore. The tools have become affordable, beginner-friendly, and genuinely effective for solo store owners. The key is to start with one high-impact automation — like abandoned cart emails — get it working, then layer in more over time.",
        "cta": "Ready to save hours each week? Start your Shopify store and enable your first automation today.",
        "action_plan": ["Install Klaviyo and activate the Abandoned Cart flow", "Set up Tidio AI to handle your most common customer questions", "Use an AI writing tool to generate your next batch of product descriptions"],
        "requirements": [
            {"name": "Shopify Store", "purpose": "Your ecommerce platform", "cost": "From $39/month"},
            {"name": "Tidio Account", "purpose": "AI customer support chatbot", "cost": "Free plan available"},
            {"name": "Klaviyo Account", "purpose": "AI email marketing automation", "cost": "Free up to 500 contacts"},
            {"name": "Make.com Account", "purpose": "Connect tools into workflows", "cost": "Free plan available"},
        ],
        "time": "2–4 hours total",
        "budget": "$0–$50/month to start",
    },

    "best ai tools for dropshipping product research": {
        "template": "listicle",
        "seo_title": "6 Best AI Tools for Dropshipping Product Research in 2026",
        "meta": "Find winning dropshipping products faster with these AI-powered research tools. Tested for beginners — no guesswork, no wasted ad spend.",
        "topic": "best AI tools for dropshipping product research",
        "tools": [
            {"name": "AutoDS", "use": "All-in-One Dropshipping Automation", "price": "From $26.90/mo",
             "tag": "AUTODS", "pros": ["Product research database with millions of items", "AI-powered winning product detection", "Automated order fulfilment"],
             "cons": ["Learning curve for complete beginners", "Pricing can add up with add-ons"],
             "description": "AutoDS is a comprehensive dropshipping platform that uses AI to surface trending products, automate order processing, and track competitor pricing. Its product research database is one of the largest available.",
             "best_for": "Dropshippers who want an all-in-one platform rather than piecing together separate tools"},
            {"name": "Sell The Trend", "use": "AI Product Research & Store Builder", "price": "$39.97/mo",
             "tag": "SELLTHETREND", "pros": ["NEXUS AI identifies trending products early", "1-click Shopify import", "Competitor store spy tool"],
             "cons": ["No free plan", "Some data lags behind real-time trends"],
             "description": "Sell The Trend's NEXUS AI scans millions of products across AliExpress, Amazon, and major dropshipping stores to identify what's trending before it becomes saturated.",
             "best_for": "Dropshippers who want data-driven product decisions rather than guesswork"},
            {"name": "Zik Analytics", "use": "eBay & Shopify Product Research", "price": "From $29.99/mo",
             "tag": "ZIKANALYTICS", "pros": ["Strong eBay market data", "Competitor research tools", "Category trend analysis"],
             "cons": ["Best suited for eBay dropshipping", "Interface can feel dated"],
             "description": "Zik Analytics specialises in marketplace research, particularly for eBay. If you're doing multi-channel dropshipping or primarily selling on eBay, its data is valuable and specific.",
             "best_for": "eBay dropshippers or sellers who want multi-platform product research"},
            {"name": "Minea", "use": "Social Ad & Winning Product Spy Tool", "price": "From $49/mo",
             "tag": "MINEA", "pros": ["Tracks ads on Facebook, TikTok, Pinterest", "Product performance data", "Influencer marketing insights"],
             "cons": ["Higher price point", "Primarily useful for paid traffic strategies"],
             "description": "Minea monitors social media advertising to show you which products are actively being promoted and generating sales. If a product is running lots of ads, that's a strong signal it's profitable.",
             "best_for": "Dropshippers who run Facebook or TikTok ads and want validated product ideas"},
            {"name": "ChatGPT + Google Trends (Free combo)", "use": "Free AI-Assisted Research", "price": "Free / $20/mo",
             "tag": "CHATGPT", "pros": ["Incredibly versatile", "Niche research, trend analysis, product naming", "Low cost"],
             "cons": ["Requires more manual effort", "No ecommerce-specific database"],
             "description": "Don't overlook the free combo of ChatGPT and Google Trends. ChatGPT can help you brainstorm niches, analyse demand signals, and generate product angles, while Google Trends confirms seasonal and long-term demand patterns.",
             "best_for": "Complete beginners on a tight budget who want to do research intelligently without paid tools"},
        ],
        "alts": [
            {"name": "Niche Scraper", "desc": "A scraper-style tool that pulls winning products from AliExpress and Shopify stores. Good entry-level option."},
            {"name": "Dropship.io", "desc": "Newer product research platform with a clean interface and strong data on Shopify store performance."},
            {"name": "FindNiche", "desc": "Focuses on niche analysis and AliExpress product trends with a simple, beginner-friendly interface."},
        ],
        "faqs": [
            {"q": "How do AI tools help with dropshipping product research?", "a": "AI tools analyse massive amounts of sales data, social media trends, and competitor activity to surface products that are gaining popularity before they become saturated. This saves hours of manual research and reduces guesswork."},
            {"q": "Can I do dropshipping product research without paid tools?", "a": "Yes. The ChatGPT + Google Trends combo in this list is a legitimate starting point that costs little to nothing. Paid tools provide more data and automation, but aren't required to get started."},
            {"q": "What makes a good dropshipping product?", "a": "Good dropshipping products typically have: high perceived value vs. shipping cost, a wow factor, low availability in mainstream retail, a clear problem they solve, and manageable competition. AI tools help you find products that fit these criteria at scale."},
            {"q": "How do I know if a product is already saturated?", "a": "Check the number of competing ads on Facebook and TikTok (tools like Minea help here), look at how many Shopify stores are selling it, and examine review dates on AliExpress. If the market is crowded but not dominated, you can still enter with a unique angle."},
            {"q": "Is dropshipping still profitable in 2026?", "a": "Dropshipping remains viable but has evolved. The edge now comes from better product research, stronger branding, faster fulfilment, and smarter marketing — all areas where AI tools provide a real advantage."},
        ],
        "intro": "Finding the right product is the hardest part of dropshipping. Pick the wrong one and you lose money on ads and inventory before you make a single sale. Pick the right one and a simple store can generate consistent revenue with minimal overhead. AI-powered product research tools have changed the game — they analyse millions of products, track social trends, and surface winners before the market gets saturated.",
        "conclusion": "The best AI tools for dropshipping product research save you from expensive trial and error. Whether you're on a tight budget using the free ChatGPT + Google Trends combo or ready to invest in a dedicated platform like AutoDS or Sell The Trend, there's an option here that fits your stage.",
        "cta": "Start your dropshipping journey with Shopify — the platform all these tools are built to work with.",
    },

    "ai tools for ecommerce beginners under $50": {
        "template": "listicle",
        "seo_title": "Best AI Tools for Ecommerce Beginners Under $50/Month (2026 Edition)",
        "meta": "Build a profitable ecommerce store on a budget. These AI tools for beginners all cost under $50/month — and some are completely free.",
        "topic": "AI tools for ecommerce beginners under $50",
        "tools": [
            {"name": "Klaviyo (Free Plan)", "use": "Email Marketing Automation", "price": "Free up to 500 contacts",
             "tag": "EMAIL_MARKETING_TOOL", "pros": ["Generous free plan", "Pre-built automation flows", "Deep Shopify integration"],
             "cons": ["Pricing jumps significantly as your list grows", "Some advanced features require paid plan"],
             "description": "Klaviyo is the gold standard for ecommerce email marketing, and its free plan is genuinely useful for new stores. You get access to the core automation flows — including abandoned cart, welcome series, and post-purchase emails — that drive the majority of email revenue.",
             "best_for": "Any ecommerce beginner who wants to start building an email list and automating follow-ups from day one"},
            {"name": "Tidio (Free Plan)", "use": "AI Customer Support", "price": "Free / $29/mo upgrade",
             "tag": "TIDIO", "pros": ["Excellent free tier", "Handles common questions automatically", "Works on mobile"],
             "cons": ["Free plan limits on conversations", "AI responses need training to be accurate"],
             "description": "Tidio's free plan gives you a live chat widget and basic AI chatbot functionality. For a new store, it's often all you need to handle the most common customer questions without being glued to your inbox.",
             "best_for": "New store owners who want 24/7 customer support without hiring anyone"},
            {"name": "ChatGPT Plus", "use": "AI Writing & Research Assistant", "price": "$20/mo",
             "tag": "AI_COPY_TOOL", "pros": ["Extremely versatile", "Product descriptions, email copy, social posts", "Also great for business strategy questions"],
             "cons": ["Requires good prompts to get great output", "No native Shopify integration — copy and paste workflow"],
             "description": "At $20/month, ChatGPT Plus is one of the highest-value AI subscriptions for ecommerce beginners. Use it to write product descriptions, brainstorm marketing angles, draft email campaigns, and research your niche — all in one place.",
             "best_for": "Budget-conscious beginners who want a versatile AI tool that does many jobs well"},
            {"name": "Canva AI (Free/Pro)", "use": "AI Graphic Design for Store & Social", "price": "Free / $15/mo",
             "tag": "CANVA", "pros": ["AI image generation built in", "Huge template library", "One-click brand kit"],
             "cons": ["AI image quality varies", "Pro features require subscription"],
             "description": "Canva's AI features — including text-to-image generation and Magic Write — make it a powerful design tool for ecommerce beginners who don't have a graphic design background. Create product banners, Pinterest pins, and social media posts without hiring a designer.",
             "best_for": "Store owners who need professional-looking visuals without design skills or a big budget"},
            {"name": "Make.com (Free Plan)", "use": "No-Code Automation & Workflow Builder", "price": "Free / $9/mo",
             "tag": "MAKECOM", "pros": ["Free plan includes 1,000 operations/month", "Connects hundreds of apps", "Visual workflow builder"],
             "cons": ["Learning curve for beginners", "Complex scenarios can be tricky to troubleshoot"],
             "description": "Make.com lets you connect your apps into automated workflows without code. Use it to automatically pull new Shopify orders into a spreadsheet, post new products to social media, or connect your email tool to your store — all for free on the basic plan.",
             "best_for": "Store owners who want to eliminate repetitive manual tasks by connecting their apps together"},
        ],
        "alts": [
            {"name": "Mailchimp", "desc": "Another popular email marketing option with a free plan, though it's less ecommerce-focused than Klaviyo."},
            {"name": "Writesonic", "desc": "An AI writing tool with a lower price point than Jasper. Good for product descriptions and blog posts."},
            {"name": "Buffer (Free Plan)", "desc": "Schedule your social media posts for free across multiple platforms — pairs nicely with Canva for content creation."},
        ],
        "faqs": [
            {"q": "Can I build a profitable ecommerce store using only free tools?", "a": "Yes — especially in the early stages. Klaviyo, Tidio, Canva, and Make.com all have meaningful free plans. You can run an effective store on under $30/month using free tiers, then invest in paid plans as your revenue grows."},
            {"q": "Which tool should I buy first as a beginner?", "a": "If you're going to spend your first $20, spend it on ChatGPT Plus. Its versatility means it can help with writing, research, strategy, and more — covering multiple use cases with one subscription."},
            {"q": "Do I need all these tools or just a few?", "a": "Start with one or two tools that address your biggest current challenge. If customer support is eating your time, start with Tidio. If content is the bottleneck, start with ChatGPT. Add more tools as you grow."},
            {"q": "Are there hidden costs beyond the monthly subscription?", "a": "Watch out for usage-based pricing. Klaviyo charges based on contact list size, Make.com charges based on operations, and some tools charge per message or per request. Always read the pricing page carefully before signing up."},
            {"q": "What if my budget is literally $0?", "a": "You can still make progress. Use the free plans of Klaviyo, Tidio, Canva, and Make.com. Use the free version of ChatGPT (GPT-4o is available without a subscription as of 2026). It requires more manual effort but it works."},
        ],
        "intro": "You don't need a big budget to run a smart ecommerce store in 2026. Some of the most powerful AI tools available today have free plans or cost less than a Netflix subscription. Whether you're starting your first Shopify store or looking to work more efficiently without blowing your margins, this guide covers the best AI tools that cost under $50 per month — and some that cost nothing at all.",
        "conclusion": "Great AI tools are no longer reserved for big brands with big budgets. The tools in this guide give beginners access to automation, content creation, design, and customer support at a price that makes sense for a store in its early stages. Start free, prove the value, and upgrade when the return on investment is clear.",
        "cta": "Start your Shopify store today and pair it with the free tools in this list to hit the ground running.",
    },

    "how to start a shopify store using ai": {
        "template": "howto",
        "seo_title": "How to Start a Shopify Store Using AI (Beginner's Guide for 2026)",
        "meta": "Learn how to start a Shopify store using AI in 2026. This beginner's guide covers every step — from picking a niche to launching with AI-powered tools.",
        "topic": "start a Shopify store using AI",
        "goal": "launch your first Shopify store using AI to accelerate every step",
        "steps": [
            {"title": "Pick a Profitable Niche with AI Research",
             "intro": "The niche you choose determines everything — your audience, your products, your marketing, and your competition. AI tools make this research faster and more data-driven than ever before.",
             "actions": ["Open ChatGPT and ask: 'Suggest 10 profitable ecommerce niches for a beginner in 2026 with low competition and good margins'", "Cross-reference your top 3 ideas in Google Trends to check demand over time", "Use Sell The Trend or AutoDS to validate that products in your niche are actively selling"],
             "tip": "Pick a niche you're at least somewhat interested in — you'll be creating content and answering questions about it for months.",
             "tag": "SHOPIFY"},
            {"title": "Set Up Your Shopify Store",
             "intro": "Shopify is the most beginner-friendly ecommerce platform available and has the best ecosystem of AI tools. Setting up a basic store takes under an hour.",
             "actions": ["Sign up for a Shopify trial at shopify.com", "Choose a clean, fast theme from the Shopify Theme Store (the free Dawn theme is excellent for beginners)", "Set up your store name, currency, payment gateways (Shopify Payments or PayPal), and shipping zones"],
             "tip": "Don't spend weeks perfecting your store design before you have products or traffic. A clean, simple store that's live beats a beautiful store that's never launched.",
             "tag": "SHOPIFY"},
            {"title": "Find and Add Products Using AI",
             "intro": "Once your store is set up, you need products. AI tools can help you research winning products and write compelling descriptions at scale — cutting weeks of work down to hours.",
             "actions": ["Use AutoDS or Sell The Trend to identify 5–10 trending products in your niche", "Import product images from your supplier and use ChatGPT to generate unique, SEO-friendly product descriptions", "Review every AI-generated description before publishing — add your brand voice and check for accuracy"],
             "tip": "Don't list 100 products on day one. Start with 10–20 well-described, well-photographed products and expand from there.",
             "tag": "AI_COPY_TOOL"},
            {"title": "Set Up AI-Powered Customer Support",
             "intro": "Before your store gets traffic, set up a way to handle customer questions automatically. Tidio's AI chatbot can answer common questions about shipping, returns, and products around the clock.",
             "actions": ["Install Tidio from the Shopify App Store", "Set up answers to your top 10 expected customer questions", "Enable the Lyro AI assistant and connect it to your product catalogue"],
             "tip": "Write your FAQs and return policy before launching. These become the training data for your chatbot and reduce the questions you need to answer manually.",
             "tag": "TIDIO"},
            {"title": "Launch and Drive Traffic with AI-Assisted Marketing",
             "intro": "With your store ready, it's time to get visitors. AI tools can help you write ad copy, social media captions, Pinterest descriptions, and email campaigns faster than starting from scratch.",
             "actions": ["Install Klaviyo and set up your Welcome email and Abandoned Cart flows before your first sale", "Use Canva's AI tools to create product graphics for Pinterest and Instagram", "Write your first 3 blog posts using AI to help with SEO — focus on keywords your target customer is searching for"],
             "tip": "Pinterest is an underrated traffic source for ecommerce beginners. It's free, and pins can drive traffic for months after posting.",
             "tag": "EMAIL_MARKETING_TOOL"},
        ],
        "alts": [
            {"title": "Start with a Print-on-Demand Model", "desc": "Use Printful or Printify instead of dropshipping. You design products with AI tools like Midjourney, and they handle production and shipping.", "best_for": "Creative entrepreneurs who want to sell custom products without inventory risk"},
            {"title": "Start with Digital Products", "desc": "Use AI to create and sell digital downloads — printables, templates, guides — with zero inventory or shipping to manage.", "best_for": "People who want to test ecommerce with the lowest possible overhead"},
            {"title": "Start with a Niche Blog First", "desc": "Build an audience through a niche blog using AI-assisted content, then layer in ecommerce products once you have traffic.", "best_for": "People who enjoy content creation and want a built-in audience before launching a store"},
        ],
        "faqs": [
            {"q": "How much money do I need to start a Shopify store with AI?", "a": "You can get started for as little as $1 (Shopify's trial), $20 (ChatGPT Plus), and free tiers of Tidio and Klaviyo. A realistic starting budget including your first month of Shopify ($39) and a few tools is $80–$150."},
            {"q": "How long does it take to launch a Shopify store using AI?", "a": "With AI tools handling product descriptions, store copy, and initial content, a basic store can be ready to launch in 1–2 days of focused work. Don't let perfection delay your launch."},
            {"q": "Do I need to know how to code?", "a": "No. Shopify is designed for non-technical users, and the AI tools in this guide require no coding. The most technical thing you'll do is install apps from the Shopify App Store."},
            {"q": "What's the biggest mistake beginners make when starting a Shopify store?", "a": "Spending too long setting up and not enough time getting traffic. A good-enough store that's live and getting visitors will teach you more in a week than months of planning."},
            {"q": "Can AI write all my product descriptions and store copy?", "a": "AI can write excellent first drafts, but you should always review and personalise them. Add specific details about your products that only you know, and make sure the tone matches your brand."},
            {"q": "What AI tools are the most important when starting a Shopify store?", "a": "We'd prioritise: (1) ChatGPT for content and research, (2) Klaviyo for email automation, (3) Tidio for customer support. These three alone give you a significant advantage over a store without any AI tools."},
        ],
        "intro": "Starting a Shopify store has never been more accessible — but it can still feel overwhelming when you're staring at a blank store with no products, no traffic, and no idea where to begin. In 2026, AI tools change this equation entirely. They can help you choose a niche, write your store copy, generate product descriptions, handle customer questions, and even create your marketing materials — cutting weeks of work down to days.",
        "conclusion": "Starting a Shopify store with AI support in 2026 is genuinely achievable for beginners without technical skills or a big budget. The key is to take action: choose your niche, set up your store, add your first products, and launch — then improve based on what you learn from real customers.",
        "cta": "Start your Shopify free trial today and follow this guide step by step.",
        "action_plan": ["Start your Shopify trial and choose a clean theme", "Research your niche using ChatGPT and Google Trends", "Add your first 10 products with AI-generated descriptions"],
        "requirements": [
            {"name": "Shopify Account", "purpose": "Your ecommerce storefront", "cost": "From $39/month (free trial available)"},
            {"name": "ChatGPT Plus", "purpose": "AI writing, research, and strategy", "cost": "$20/month"},
            {"name": "Klaviyo Account", "purpose": "Email marketing automation", "cost": "Free up to 500 contacts"},
            {"name": "Tidio Account", "purpose": "AI customer support chatbot", "cost": "Free plan available"},
        ],
        "time": "1–2 days to launch",
        "budget": "$80–$150 for your first month",
    },
}

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert a string to a URL-friendly kebab-case slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def detect_template(keyword: str) -> str:
    """Infer the best template type from the keyword."""
    kw = keyword.lower()
    if kw.startswith("how to") or kw.startswith("how do"):
        return "howto"
    if any(word in kw for word in ["vs", "versus", "compare", "comparison", "or "]):
        return "comparison"
    return "listicle"


def build_faq_schema(faqs: list) -> str:
    """Build a JSON-LD FAQPage schema block."""
    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"],
            },
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }
    return json.dumps(schema, indent=2, ensure_ascii=False)


def generate_pinterest_titles(keyword: str, seo_title: str, topic: str) -> list:
    """Generate 10 Pinterest pin titles (<=100 chars each)."""
    base_phrases = [
        f"{seo_title[:90]}",
        f"How AI is changing ecommerce for beginners | {topic[:50]}",
        f"Save hours every week: {topic[:65]}",
        f"Beginner's guide to {topic[:70]}",
        f"{topic[:80]} — what actually works in 2026",
        f"Stop guessing: find the best {topic[:60]}",
        f"The only guide you need for {topic[:62]}",
        f"Smart tools for smart ecommerce: {topic[:55]}",
        f"Ecommerce on autopilot — {topic[:65]}",
        f"Start smarter: {topic[:77]}",
    ]
    # Truncate each to 100 chars safely
    return [t[:100] for t in base_phrases]


def generate_pinterest_descriptions(keyword: str, topic: str, meta: str) -> list:
    """Generate 10 Pinterest pin descriptions with natural keyword usage."""
    kws = [w for w in keyword.lower().split() if len(w) > 3][:5]
    kw_string = ", ".join(kws[:3])

    templates = [
        f"Discover the top resources for {topic}. Perfect for ecommerce beginners who want to save time and grow their Shopify store faster using AI. {meta}",
        f"If you're just starting out with {topic}, this guide breaks everything down step by step — no tech skills required. Includes real tool recommendations and beginner tips.",
        f"AI tools are transforming ecommerce. Here's everything a beginner needs to know about {topic} — from free options to paid upgrades that are worth the investment.",
        f"Looking for the best approach to {topic}? We tested the top options so you don't have to. Read the full breakdown on Smart AI Growth Hub.",
        f"Running an online store as a solo entrepreneur? Learn how {topic} can save you hours every week and help you compete with bigger brands.",
        f"This guide covers everything you need to know about {topic} — including what to avoid, what to prioritise, and how to get started on a budget.",
        f"Ecommerce beginners: here's your shortcut to {topic}. We cover the tools, the steps, and the tips that actually make a difference in 2026.",
        f"Want to work smarter, not harder? {topic.capitalize()} is one of the fastest ways to level up your Shopify store without hiring a team. See how inside.",
        f"From product research to customer support, AI is reshaping ecommerce for beginners. This post on {topic} is your starting point. Save it for later!",
        f"Smart AI Growth Hub breaks down {topic} for ecommerce beginners — with honest reviews, real pricing, and actionable next steps. No fluff.",
    ]
    return templates


def build_listicle_html(profile: dict, slug: str, keyword: str) -> str:
    """Generate a 2000+ word listicle blog post in clean HTML."""
    today = datetime.now().strftime("%B %d, %Y")
    tools = profile.get("tools", [])
    faqs = profile.get("faqs", [])
    alts = profile.get("alts", [])
    seo_title = profile["seo_title"]
    intro = profile["intro"]
    conclusion = profile["conclusion"]
    cta = profile["cta"]

    # Tool list items
    tool_rows = "\n".join(
        f"<tr><td><strong>{t['name']}</strong></td><td>{t['use']}</td><td>{t['price']}</td></tr>"
        for t in tools
    )

    tool_sections = ""
    for i, t in enumerate(tools, 1):
        pros_html = "\n".join(f"<li>{p}</li>" for p in t["pros"])
        cons_html = "\n".join(f"<li>{c}</li>" for c in t["cons"])
        tool_sections += f"""
<h3>{i}. {t['name']} &mdash; Best for {t['use']}</h3>
<p>{t['description']}</p>
<p><strong>What we like:</strong></p>
<ul>
{pros_html}
</ul>
<p><strong>What to watch out for:</strong></p>
<ul>
{cons_html}
</ul>
<p><strong>Who it&rsquo;s best for:</strong> {t['best_for']}</p>
<!-- AFFILIATE_LINK:{t['tag']} -->
<hr>
"""

    alt_items = "\n".join(f"<li><strong>{a['name']}</strong> &mdash; {a['desc']}</li>" for a in alts)

    faq_html = ""
    for faq in faqs:
        faq_html += f"<h3>{faq['q']}</h3>\n<p>{faq['a']}</p>\n"

    faq_schema = build_faq_schema(faqs)

    internal_links_placeholder = """<!-- INTERNAL_LINKS -->
<p><em>Related reading on Smart AI Growth Hub:</em></p>
<ul>
  <li><em>[INTERNAL_LINK_1_PLACEHOLDER]</em></li>
  <li><em>[INTERNAL_LINK_2_PLACEHOLDER]</em></li>
  <li><em>[INTERNAL_LINK_3_PLACEHOLDER]</em></li>
</ul>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{seo_title}</title>
  <meta name="description" content="{profile['meta']}">
</head>
<body>

<h1>{seo_title}</h1>

<p><em>Disclosure: This post contains affiliate links. If you purchase through our links, we may earn a commission at no extra cost to you. We only recommend tools we genuinely believe help ecommerce beginners.</em></p>

<hr>

<h2>Introduction</h2>
<p>{intro}</p>
<p>Whether you&rsquo;re just starting your first online store or looking to level up with automation, the right AI tools can make a real difference without a steep learning curve or a huge budget. In this guide, we&rsquo;ve tested and ranked the best options so you don&rsquo;t have to.</p>
<blockquote><strong>Note:</strong> AI tools and their pricing evolve quickly. Always check the tool&rsquo;s official website to confirm current plans and features before purchasing.</blockquote>

<h2>Table of Contents</h2>
<ol>
  <li><a href="#who-this-is-for">Who This Guide Is For</a></li>
  <li><a href="#quick-picks">Quick Recommendations</a></li>
  <li><a href="#deep-dives">Top Picks: Deep Dives</a></li>
  <li><a href="#alternatives">Alternatives Worth Considering</a></li>
  <li><a href="#faqs">Frequently Asked Questions</a></li>
  <li><a href="#conclusion">Conclusion</a></li>
</ol>

<h2 id="who-this-is-for">Who This Guide Is For</h2>
<p>This list is built for:</p>
<ul>
  <li><strong>New ecommerce store owners</strong> who are just getting started and don&rsquo;t want to waste money on the wrong tools</li>
  <li><strong>Shopify beginners</strong> who want AI to handle repetitive tasks like writing product descriptions or answering customer emails</li>
  <li><strong>Side hustlers and solopreneurs</strong> running a store without a team</li>
  <li><strong>Budget-conscious entrepreneurs</strong> who need maximum value per dollar</li>
</ul>
<p>If you&rsquo;re already running a 7-figure store with a full tech stack, some of these tools will still be useful &mdash; but this list is primarily written with beginners in mind.</p>

<h2 id="quick-picks">Quick Recommendations</h2>
<p>Here&rsquo;s a quick overview before we go deeper:</p>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;">
  <thead>
    <tr>
      <th>Tool</th>
      <th>Best For</th>
      <th>Starting Price</th>
    </tr>
  </thead>
  <tbody>
{tool_rows}
  </tbody>
</table>
<p><em>Prices are as of {today}. Verify current pricing on each tool&rsquo;s website.</em></p>

<!-- AFFILIATE_BLOCK:TOOL_STACK -->

<h2 id="deep-dives">Top Picks: Deep Dives</h2>
{tool_sections}

<h2 id="alternatives">Alternatives Worth Considering</h2>
<p>Not every tool will be the right fit. Here are a few other options worth exploring:</p>
<ul>
{alt_items}
</ul>

<!-- AFFILIATE_BLOCK:ALTERNATIVES -->

<hr>

{internal_links_placeholder}

<hr>

<h2 id="faqs">Frequently Asked Questions</h2>
{faq_html}

<h2 id="conclusion">Conclusion</h2>
<p>{conclusion}</p>
<p>The tools in this guide are all beginner-friendly, and most offer free trials so you can test before committing. Start with one tool, get comfortable, then layer in others as your store grows.</p>
<p><strong>Ready to get started?</strong> {cta}</p>

<!-- AFFILIATE_LINK:SHOPIFY -->
<!-- AFFILIATE_LINK:EMAIL_MARKETING_TOOL -->
<!-- AFFILIATE_LINK:AI_COPY_TOOL -->

<hr>
<p><em>Smart AI Growth Hub is a reader-supported site. We may earn commissions from qualifying purchases. This does not affect our editorial independence or the accuracy of our reviews.</em></p>

<script type="application/ld+json">
{faq_schema}
</script>

</body>
</html>"""


def build_howto_html(profile: dict, slug: str, keyword: str) -> str:
    """Generate a 2000+ word how-to blog post in clean HTML."""
    today = datetime.now().strftime("%B %d, %Y")
    steps = profile.get("steps", [])
    faqs = profile.get("faqs", [])
    alts = profile.get("alts", [])
    requirements = profile.get("requirements", [])
    seo_title = profile["seo_title"]
    intro = profile["intro"]
    conclusion = profile["conclusion"]
    cta = profile["cta"]
    goal = profile.get("goal", "achieve your goal")
    action_plan = profile.get("action_plan", [])
    time_est = profile.get("time", "a few hours")
    budget_est = profile.get("budget", "varies")

    req_rows = "\n".join(
        f"<tr><td><strong>{r['name']}</strong></td><td>{r['purpose']}</td><td>{r['cost']}</td></tr>"
        for r in requirements
    )

    step_sections = ""
    for i, step in enumerate(steps, 1):
        actions_html = "\n".join(f"<li>{a}</li>" for a in step["actions"])
        step_sections += f"""
<h3>Step {i}: {step['title']}</h3>
<p>{step['intro']}</p>
<p>Here&rsquo;s how to do it:</p>
<ol>
{actions_html}
</ol>
<p><strong>Pro tip:</strong> {step['tip']}</p>
<!-- AFFILIATE_LINK:{step['tag']} -->
<hr>
"""

    alt_sections = ""
    for alt in alts:
        alt_sections += f"""
<h3>{alt['title']}</h3>
<p>{alt['desc']}</p>
<p><strong>Best for:</strong> {alt['best_for']}</p>
"""

    faq_html = ""
    for faq in faqs:
        faq_html += f"<h3>{faq['q']}</h3>\n<p>{faq['a']}</p>\n"

    action_items = "\n".join(f"<li>{a}</li>" for a in action_plan)
    faq_schema = build_faq_schema(faqs)

    internal_links_placeholder = """<!-- INTERNAL_LINKS -->
<p><em>Related guides on Smart AI Growth Hub:</em></p>
<ul>
  <li><em>[INTERNAL_LINK_1_PLACEHOLDER]</em></li>
  <li><em>[INTERNAL_LINK_2_PLACEHOLDER]</em></li>
  <li><em>[INTERNAL_LINK_3_PLACEHOLDER]</em></li>
</ul>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{seo_title}</title>
  <meta name="description" content="{profile['meta']}">
</head>
<body>

<h1>{seo_title}</h1>

<p><em>Disclosure: This post contains affiliate links. If you purchase through our links, we may earn a commission at no extra cost to you. We only recommend tools we genuinely believe help ecommerce beginners.</em></p>

<hr>

<h2>Introduction</h2>
<p>{intro}</p>
<p>By the end of this guide, you&rsquo;ll know exactly how to {goal} &mdash; even if you have zero technical experience. We&rsquo;ll walk through each step with practical examples so you can follow along and implement immediately.</p>
<blockquote><strong>Heads up:</strong> The tools and platforms mentioned in this guide are subject to updates. Always verify current features and pricing on each tool&rsquo;s official website before making purchasing decisions.</blockquote>

<h2>Table of Contents</h2>
<ol>
  <li><a href="#who-this-is-for">Who This Guide Is For</a></li>
  <li><a href="#what-youll-need">What You&rsquo;ll Need</a></li>
  <li><a href="#step-by-step">Step-by-Step Instructions</a></li>
  <li><a href="#alternatives">Alternative Approaches</a></li>
  <li><a href="#faqs">Frequently Asked Questions</a></li>
  <li><a href="#next-steps">Next Steps</a></li>
</ol>

<h2 id="who-this-is-for">Who This Guide Is For</h2>
<p>This how-to guide is written for:</p>
<ul>
  <li><strong>Complete beginners</strong> who have never tried to {profile['topic']} before</li>
  <li><strong>Shopify store owners</strong> who want to work smarter, not harder</li>
  <li><strong>Busy entrepreneurs</strong> with limited time who need clear, actionable steps</li>
  <li><strong>Budget-conscious sellers</strong> who want results without hiring a developer</li>
</ul>
<p>You don&rsquo;t need coding skills, a big team, or a large budget to follow this guide. If you can use a spreadsheet and set up a free account, you can do this.</p>

<h2 id="what-youll-need">What You&rsquo;ll Need</h2>
<p>Before we get started, here&rsquo;s a quick checklist of what you&rsquo;ll need:</p>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%;">
  <thead>
    <tr>
      <th>Requirement</th>
      <th>Purpose</th>
      <th>Cost</th>
    </tr>
  </thead>
  <tbody>
{req_rows}
  </tbody>
</table>
<p><strong>Estimated total time:</strong> {time_est}</p>
<p><strong>Estimated budget:</strong> {budget_est}</p>

<!-- AFFILIATE_BLOCK:TOOL_STACK -->

<h2 id="step-by-step">Step-by-Step Instructions</h2>
{step_sections}

<h2 id="alternatives">Alternative Approaches</h2>
<p>The method above works great for most beginners, but here are some variations worth knowing:</p>
{alt_sections}

<!-- AFFILIATE_BLOCK:ALTERNATIVES -->

<hr>

{internal_links_placeholder}

<hr>

<h2 id="faqs">Frequently Asked Questions</h2>
{faq_html}

<h2 id="next-steps">Next Steps</h2>
<p>{conclusion}</p>
<p>You&rsquo;ve now got everything you need to {goal}. The most important thing is to start &mdash; even a simple setup today beats a perfect setup that never happens.</p>
<p><strong>Your action plan:</strong></p>
<ol>
{action_items}
</ol>
<p><strong>Ready to take the next step?</strong> {cta}</p>

<!-- AFFILIATE_LINK:SHOPIFY -->
<!-- AFFILIATE_LINK:EMAIL_MARKETING_TOOL -->
<!-- AFFILIATE_LINK:AI_COPY_TOOL -->

<hr>
<p><em>Smart AI Growth Hub is a reader-supported site. We may earn commissions from qualifying purchases. This does not affect our editorial independence or the accuracy of our guides.</em></p>

<script type="application/ld+json">
{faq_schema}
</script>

</body>
</html>"""


def generate_html(profile: dict, template_type: str, slug: str, keyword: str) -> str:
    """Dispatch to the correct HTML builder based on template type."""
    if template_type == "howto":
        return build_howto_html(profile, slug, keyword)
    else:
        # Both listicle and comparison use listicle builder for these keywords
        return build_listicle_html(profile, slug, keyword)


# ---------------------------------------------------------------------------
# CSV I/O
# ---------------------------------------------------------------------------

CSV_FIELDNAMES = [
    "Keyword", "Status", "SEOTitle", "Slug", "HTMLFile",
    "MetaDescription", "PinterestTitles", "PinterestDescriptions",
    "PublishedURL", "CreatedAt", "UpdatedAt",
]


def read_csv(path: Path) -> list:
    if not path.exists():
        log.error(f"Keywords CSV not found: {path}")
        sys.exit(1)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    log.info(f"Loaded {len(rows)} rows from {path}")
    return rows


def write_csv(path: Path, rows: list) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    log.info(f"Updated CSV written to {path}")


def write_pinterest_csv(path: Path, slug: str, titles: list, descriptions: list) -> None:
    url = f"https://example.com/{slug}"
    rows = []
    for i, (title, desc) in enumerate(zip(titles, descriptions)):
        rows.append({"Title": title, "Description": desc, "URL": url})
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Description", "URL"])
        writer.writeheader()
        writer.writerows(rows)
    log.info(f"Pinterest CSV written to {path}")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def process_row(row: dict) -> dict:
    """Process one keyword row. Returns the updated row dict."""
    keyword = row.get("Keyword", "").strip()
    status = row.get("Status", "").strip().upper()

    if status != "NEW":
        log.info(f"Skipping '{keyword}' (Status={status})")
        return row

    log.info(f"Processing: '{keyword}'")

    keyword_key = keyword.lower()
    profile = KEYWORD_PROFILES.get(keyword_key)

    if not profile:
        # Fallback: generate basic metadata for unknown keywords
        log.warning(f"No profile for '{keyword}' — generating generic content.")
        template_type = detect_template(keyword)
        seo_title = keyword.title() + " — Complete Beginner's Guide"
        slug = slugify(keyword)
        meta = f"Learn about {keyword.lower()}. Beginner-friendly guide with practical tips and tool recommendations."[:155]
        profile = {
            "template": template_type,
            "seo_title": seo_title,
            "meta": meta,
            "topic": keyword.lower(),
            "goal": keyword.lower(),
            "tools": [],
            "steps": [],
            "faqs": [],
            "alts": [],
            "requirements": [],
            "intro": f"This guide covers everything a beginner needs to know about {keyword.lower()}.",
            "conclusion": f"Now you have a solid foundation for {keyword.lower()}. Take action and start implementing today.",
            "cta": "Get started today with the resources mentioned in this guide.",
            "action_plan": ["Start with step one", "Review the tools mentioned", "Take action"],
            "time": "A few hours",
            "budget": "Varies",
        }
    else:
        template_type = profile["template"]
        seo_title = profile["seo_title"]
        slug = slugify(seo_title)
        meta = profile["meta"]

    # Ensure output directories exist
    BLOG_HTML_DIR.mkdir(parents=True, exist_ok=True)
    PINTEREST_CSV_DIR.mkdir(parents=True, exist_ok=True)

    # Generate HTML
    try:
        html_content = generate_html(profile, template_type, slug, keyword)
    except Exception as e:
        log.error(f"HTML generation failed for '{keyword}': {e}")
        row["Status"] = "ERROR"
        row["UpdatedAt"] = datetime.now().strftime("%Y-%m-%d")
        return row

    html_path = BLOG_HTML_DIR / f"{slug}.html"
    html_content = inject_affiliate_links(html_content)
    html_content = html_content.replace(" &mdash; ", ", ").replace("&mdash;", ",")
    html_content = html_content.replace(" \u2014 ", ", ").replace("\u2014", ",")
    html_path.write_text(html_content, encoding="utf-8")
    word_count = len(html_content.split())
    log.info(f"HTML saved to {html_path} (~{word_count} words in raw HTML)")

    # Generate Pinterest data
    pin_titles = generate_pinterest_titles(keyword, seo_title, profile.get("topic", keyword))
    pin_descs = generate_pinterest_descriptions(keyword, profile.get("topic", keyword), meta)

    pinterest_path = PINTEREST_CSV_DIR / f"{slug}_pins.csv"
    write_pinterest_csv(pinterest_path, slug, pin_titles, pin_descs)

    # Update row
    now = datetime.now().strftime("%Y-%m-%d")
    row["Status"] = "GENERATED"
    row["SEOTitle"] = seo_title
    row["Slug"] = slug
    row["HTMLFile"] = str(html_path.relative_to(BASE_DIR)).replace("\\", "/")
    row["MetaDescription"] = meta[:155]
    row["PinterestTitles"] = " | ".join(pin_titles)
    row["PinterestDescriptions"] = " | ".join(pin_descs)
    row["UpdatedAt"] = now

    log.info(f"Done: '{keyword}' → {slug}")
    return row


def main():
    log.info("=" * 60)
    log.info("Smart AI Growth Hub — Content Pipeline Generator")
    log.info(f"Run started: {datetime.now().isoformat()}")
    log.info("=" * 60)

    rows = read_csv(KEYWORDS_CSV)
    updated_rows = []
    new_count = 0
    generated_count = 0

    for row in rows:
        status = row.get("Status", "").strip().upper()
        if status == "NEW":
            new_count += 1

        updated_row = process_row(row)
        updated_rows.append(updated_row)

        if updated_row.get("Status") == "GENERATED":
            generated_count += 1

    write_csv(KEYWORDS_CSV, updated_rows)

    log.info("=" * 60)
    log.info(f"Run complete. Processed: {new_count} NEW | Generated: {generated_count}")
    log.info(f"Blog HTML   → {BLOG_HTML_DIR}")
    log.info(f"Pinterest   → {PINTEREST_CSV_DIR}")
    log.info(f"Log file    → {log_filename}")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
Write a detailed SEO blog post of 1200-2000 words.



Structure:

- Introduction

- Who this guide is for

- Quick recommendations

- Detailed breakdown of each tool

- Comparison table

- Alternatives

- FAQ

- Conclusion



Use clear headings (H2/H3) and short paragraphs.

Optimize for SEO but keep it natural and readable.


from pathlib import Path



site_folder = Path("site")



def generate_homepage():

    html_files = [f for f in site_folder.glob("*.html") if f.name != "index.html"]



    links = ""

    for file in html_files:

        title = file.stem.replace("-", " ").title()

        links += f'<li><a href="{file.name}">{title}</a></li>\n'



    index_html = f"""

<html>

<head>

<title>Smart AI Growth Hub</title>

<link rel="stylesheet" href="style.css">

</head>



<body>



<h1>Smart AI Growth Hub</h1>



<p>Guides about AI tools, ecommerce automation and side hustles.</p>



<h2>Latest Guides</h2>



<ul>

{links}

</ul>



</body>

</html>

"""



    with open(site_folder / "index.html", "w", encoding="utf-8") as f:

        f.write(index_html)



generate_homepage()