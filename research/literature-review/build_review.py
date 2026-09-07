import json

with open('results.json') as f:
    data = json.load(f)

lines = ['# BRCAness / HRD / BRCAlike 文献检索报告\n', '**检索范围:** 2023-2026年（最近3年）\n**来源:** OpenAlex, PubMed, Crossref, Europe PMC\n**检索词:** BRCAness HRD\n\n---\n']

valid = []
for r in data.get('data', []):
    title = r.get('title')
    year = r.get('year')
    doi = r.get('doi')
    if title and year and doi:
        try:
            y = int(year)
            if 2023 <= y <= 2026:
                valid.append(r)
        except:
            pass

valid.sort(key=lambda x: x.get('citationCount', 0), reverse=True)

by_year = {}
for r in valid:
    y = str(r['year'])
    by_year.setdefault(y, []).append(r)

for y in sorted(by_year.keys(), reverse=True):
    lines.append('\n## ' + y + '年\n')
    for r in by_year[y]:
        doi = r.get('doi', 'N/A')
        title = r.get('title', '')
        authors = r.get('authors', [])
        venue = r.get('venue', 'N/A')
        cites = r.get('citationCount', 0)
        abstract = r.get('abstract', '')[:300]
        if authors:
            first3 = ', '.join(authors[:3])
            et_al = ' et al.' if len(authors) > 3 else ''
            author_str = first3 + et_al
        else:
            author_str = 'Unknown'
        lines.append('**' + title + '**\n')
        lines.append('- **作者:** ' + author_str + '\n')
        lines.append('- **期刊:** ' + str(venue) + ' (' + y + ')\n')
        lines.append('- **DOI:** ' + str(doi) + '\n')
        lines.append('- **引用:** ' + str(cites) + '次\n')
        if abstract:
            lines.append('- **摘要:** ' + abstract + '...\n')
        lines.append('\n---\n')

with open('review.md', 'w') as f:
    f.write('\n'.join(lines))

print('review.md written with', len(lines), 'lines,', len(valid), 'papers')
