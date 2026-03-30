"""Update all work-detail.html links in work.html to point to correct project pages."""
import re

WORK_HTML = "c:/Users/sohum/Studio GSA/shed-template/work.html"

with open(WORK_HTML, "r", encoding="utf-8") as f:
    content = f.read()

# Featured grid projects (ordered as they appear)
# Map: comment/alt text -> slug
FEATURED_SLUGS = [
    # comment pattern -> slug
    ("Luton Airport", "luton-airport"),
    ("Lotte Dongtang", "lotte-dongtang"),
    ("Ulu Cliffhouse", "ulu-cliffhouse"),
    ("Russell & Bromley", "russell-bromley"),
    ("Shakti", "shakti"),
    ("Jollibee", "jollibee"),
    ("Meat Liquor", "meat-liquor"),
    ("Angel Square", "angel-square"),
    ("Harrods Toy Kingdom", "harrods-toy-kingdom"),
    ("Spencer Hart", "spencer-hart"),
    ("Bounce Battersea", "bounce-battersea"),
    ("Level Shoe District", "level-shoe-district"),
    ("Birdies Crazy Golf", "birdies-crazy-golf"),
    ("Barbour", "barbour"),
    ("Commodity", "commodity"),
]

# Index items (ordered as they appear in HTML)
INDEX_SLUGS = [
    ("Angel Square", "angel-square"),
    ("Barbour", "barbour"),
    ("B_Fit", "b-fit"),
    ("Birdies Crazy Golf", "birdies-crazy-golf"),
    ("Bite", "bite"),
    ("Bounce Battersea", "bounce-battersea"),
    ("Bunkers", "bunkers"),
    ("Cha Cha Teng", "cha-cha-teng"),
    ("Commodity", "commodity"),
    ("The Counter House", "counter-house"),
    ("Etat Libre", "etat-libre"),
    ("Freuds", "freuds"),
    ("Harrods Toy Kingdom", "harrods-toy-kingdom"),
    ("Jollibee", "jollibee"),
    ("Kudos", "kudos"),
    ("Level Shoe District", "level-shoe-district"),
    ("Lotte Dongtang", "lotte-dongtang"),
    ("Margaret Dabbs", "margaret-dabbs"),
    ("Meat Liquor", "meat-liquor"),
    ("Optimo", "optimo"),
    ("Oree", "oree"),
    ("Pass on Plastic", "pass-on-plastic"),
    ("Peter Reed", "peter-reed"),
    ("Queens Skate", "queens-skate"),
    ("Russell & Bromley", "russell-bromley"),
    ("Shakti", "shakti"),
    ("Spencer Hart", "spencer-hart"),
    ("The Brewery", "the-brewery"),
    ("The Office Group", "the-office-group"),
    ("Thomas Goode", "thomas-goode"),
    ("Turnbull & Asser", "turnbull-asser"),
    ("Ulu Cliffhouse", "ulu-cliffhouse"),
    ("Vertu", "vertu"),
    ("William & Son", "william-son"),
    ("Luton Airport", "luton-airport"),
]

# Next Up section (3 cards at bottom)
NEXT_UP_SLUGS = [
    ("Harrods", "harrods-toy-kingdom"),  # "Harrods" in Next Up -> Harrods Toy Kingdom
    ("Meat Liquor", "meat-liquor"),
    ("Jollibee", "jollibee"),
]

# Strategy: Replace work-detail.html links one at a time by finding them in context
# We'll process the file line by line and replace based on position

lines = content.split('\n')
result_lines = []

# Track which featured/index project we're on
featured_idx = 0
index_idx = 0
nextup_idx = 0
in_featured = False
in_index = False
in_nextup = False

for i, line in enumerate(lines):
    # Detect sections
    if '===== WORK GRID =====' in line or 'id="featuredView"' in line:
        in_featured = True
        in_index = False
        in_nextup = False
    elif 'id="indexView"' in line:
        in_featured = False
        in_index = True
        in_nextup = False
    elif 'class="next-up"' in line and 'next-up--dark' not in line:
        in_featured = False
        in_index = False
        in_nextup = True
    elif '===== FOOTER =====' in line:
        in_featured = False
        in_index = False
        in_nextup = False

    # Replace work-detail.html links based on context
    if 'href="work-detail.html"' in line:
        if in_featured and featured_idx < len(FEATURED_SLUGS):
            slug = FEATURED_SLUGS[featured_idx][1]
            line = line.replace('href="work-detail.html"', f'href="work/{slug}.html"')
            featured_idx += 1
        elif in_index and index_idx < len(INDEX_SLUGS):
            slug = INDEX_SLUGS[index_idx][1]
            line = line.replace('href="work-detail.html"', f'href="work/{slug}.html"')
            index_idx += 1
        elif in_nextup and nextup_idx < len(NEXT_UP_SLUGS):
            slug = NEXT_UP_SLUGS[nextup_idx][1]
            line = line.replace('href="work-detail.html"', f'href="work/{slug}.html"')
            nextup_idx += 1

    result_lines.append(line)

new_content = '\n'.join(result_lines)

with open(WORK_HTML, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Updated {featured_idx} featured links, {index_idx} index links, {nextup_idx} next-up links")
print(f"Total: {featured_idx + index_idx + nextup_idx} links updated")

# Verify no work-detail.html links remain
remaining = new_content.count('href="work-detail.html"')
print(f"Remaining work-detail.html links: {remaining}")
