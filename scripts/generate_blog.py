import csv

from pathlib import Path



keywords_file = "keywords/keywords.csv"

output_folder = Path("site")



output_folder.mkdir(exist_ok=True)



with open(keywords_file, encoding="utf-8") as f:

    reader = csv.reader(f)



    for row in reader:

        keyword = row[0]



        print(f"Generating blog for: {keyword}")



        title = keyword.title()



        blog_content = f"""

<html>

<head>

<title>{title}</title>

</head>



<body>



<h1>{title}</h1>



<p>This guide explains everything you need to know about {keyword}.</p>



<h2>Why {keyword} matters</h2>



<p>AI tools and automation are transforming how businesses operate. Learning about {keyword} can help you stay ahead.</p>



<h2>Best tools</h2>



<ul>

<li>Tool 1</li>

<li>Tool 2</li>

<li>Tool 3</li>

</ul>



<p>Using the right tools can dramatically improve productivity and growth.</p>



</body>

</html>

"""



        file = output_folder / f"{keyword.replace(' ','-')}.html"



        with open(file, "w", encoding="utf-8") as out:

            out.write(blog_content)

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

from pathlib import Path

site_folder = Path("site")
index_file = site_folder / "index.html"

blog_links = ""

for blog in site_folder.glob("*.html"):
    if blog.name != "index.html":
        title = blog.stem.replace("-", " ").title()
        blog_links += f'<li><a href="{blog.name}">{title}</a></li>\n'

index_content = f"""
<html>
<head>
<link rel="stylesheet" href="style.css">
<title>Smart AI Growth Hub</title>
</head>

<body>

<h1>Smart AI Growth Hub</h1>
<p>AI tools, ecommerce automation and growth guides.</p>

<h2>Latest Guides</h2>

<ul>
{blog_links}
</ul>

</body>
</html>
"""

index_file.write_text(index_content)