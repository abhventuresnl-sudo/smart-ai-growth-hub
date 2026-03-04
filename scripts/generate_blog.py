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