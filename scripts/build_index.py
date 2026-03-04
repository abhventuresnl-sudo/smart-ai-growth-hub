from pathlib import Path

from datetime import datetime



BASE_URL = "https://abhventuresnl-sudo.github.io/smart-ai-growth-hub/site/"



site_dir = Path("site")

posts = sorted([p for p in site_dir.glob("*.html") if p.name != "index.html"])



def title_from_filename(name: str) -> str:

    # nette titel van slug

    return name.replace(".html", "").replace("-", " ").title()



# index.html

items = "\n".join([f'<li><a href="{p.name}">{title_from_filename(p.name)}</a></li>' for p in posts])



index_html = f"""<!doctype html>

<html lang="en">

<head>

  <meta charset="utf-8">

  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>Smart AI Growth Hub</title>

  <link rel="stylesheet" href="style.css">

</head>

<body>

  <main class="container">

    <header class="hero">

      <h1>Smart AI Growth Hub</h1>

      <p>AI tools, ecommerce automation and growth guides.</p>

    </header>



    <section class="card">

      <h2>Latest posts</h2>

      <ul class="postlist">

        {items}

      </ul>

    </section>

  </main>

</body>

</html>

"""

(site_dir / "index.html").write_text(index_html, encoding="utf-8")



# sitemap.xml

today = datetime.utcnow().strftime("%Y-%m-%d")

urls = "\n".join([f"  <url><loc>{BASE_URL}{p.name}</loc><lastmod>{today}</lastmod></url>" for p in posts])



sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

  <url><loc>{BASE_URL}</loc><lastmod>{today}</lastmod></url>

{urls}

</urlset>

"""

(site_dir / "sitemap.xml").write_text(sitemap, encoding="utf-8")



print(f"Built index.html and sitemap.xml for {len(posts)} posts")