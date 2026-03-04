from pathlib import Path



blog_folder = Path("outputs/blog_html")

pin_output = Path("outputs/pinterest_csv")



pin_output.mkdir(exist_ok=True)



csv_file = pin_output / "pins.csv"



for blog in blog_folder.glob("*.html"):



    title = blog.stem.replace("-", " ")



    print(f"Generating pins for {title}")



    pin_title = f"{title} - Must Know Guide"



    pin_description = f"""

Discover the best tips about {title}.

Learn how to use AI tools, automation and smart strategies to grow faster.

"""



    pin_titles = [
    f"{title} - Must Know Guide",
    f"{title} - Best Tools Explained",
    f"Top Tips About {title}",
    f"{title} For Beginners",
    f"How {title} Can Grow Your Business"
]

with open(csv_file, "a", encoding="utf-8") as f:
    for pin_title in pin_titles:
        url = f"abhventuresnl-sudo.github.io/smart-ai-growth-hub/{blog.name}"
        f.write(f"{pin_title},{pin_description},{blog.name}\n")