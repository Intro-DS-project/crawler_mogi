# Installation

### Dependencies
Requires Python 3.8+ or later

```bash
pip install Scrapy
```

### Run
in root directory of project

```bash
scrapy crawl mogi -o output.json
```

or use Docker
```bash
docker build -t mogi .
docker run --name mogi_c1 mogi
```