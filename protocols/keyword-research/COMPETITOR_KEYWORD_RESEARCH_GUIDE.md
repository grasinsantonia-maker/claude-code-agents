# Competitor Keyword Research Guide - Hebrew Market
## Complete Methodology for Comprehensive Keyword Discovery

**Version:** 1.0
**Created:** 2026-01-12
**Author:** Nadav Digital
**Validated:** SE Ranking API (Israel Source)

---

## Overview

This guide documents the complete process for conducting comprehensive keyword research by analyzing competitors, including ALL Hebrew grammatical variations (singular, plural, construct state, feminine forms).

### Key Learnings (Mistakes to Avoid)

1. **NEVER assume you have all variations** - Hebrew has 5+ forms per root word
2. **Always verify against SE Ranking API** - Don't trust cached/old data
3. **Run multiple search waves** - Each wave discovers keywords missed by previous
4. **Include compound keywords** - Root + modifier combinations have high volume
5. **Don't stop at singular/plural** - Construct state (סמיכות) often has high volume

---

## Quick Start Command

```bash
# Run the complete keyword research pipeline
python3 /Users/antoniasepulvedagrasins/scripts/competitor_keyword_research.py \
    --client "CLIENT_NAME" \
    --competitors "domain1.co.il,domain2.co.il,domain3.co.il" \
    --output "/path/to/output.html"
```

---

## Step-by-Step Process

### Step 1: Define Competitors (8 recommended)

```python
competitors = [
    "competitor1.co.il",
    "competitor2.co.il",
    "competitor3.co.il",
    "competitor4.co.il",
    "competitor5.co.il",
    "competitor6.co.il",
    "competitor7.co.il",
    "competitor8.co.il"
]
```

### Step 2: Pull Competitor Keywords via SE Ranking API

```python
import requests

# SE Ranking Domain Keywords API
API_KEY = "YOUR_SE_RANKING_PROJECT_API_KEY"  # 52adfc67e785be54defc2ece910c69965513bbf9
BASE_URL = "https://api.seranking.com/v1"

def get_competitor_keywords(domain):
    """Get all keywords a domain ranks for in Israel"""
    url = f"{BASE_URL}/domain/keywords"
    params = {
        "source": "il",
        "domain": domain,
        "type": "organic"
    }
    headers = {"Authorization": f"Token {API_KEY}"}

    response = requests.get(url, params=params, headers=headers, timeout=60)
    if response.status_code == 200:
        return response.json()
    return []

# Collect from all competitors
all_keywords = []
for domain in competitors:
    keywords = get_competitor_keywords(domain)
    all_keywords.extend(keywords)
```

### Step 3: Hebrew Variation Patterns (CRITICAL)

**This is where most mistakes happen. Hebrew has multiple grammatical forms:**

| Form | Hebrew Name | Pattern | Example (מסנן) |
|------|-------------|---------|----------------|
| Singular | יחיד | Base | מסנן |
| Plural Masculine | רבים זכר | -ים | מסננים |
| Plural Feminine | רבים נקבה | -ות | מסננות |
| Construct State | סמיכות | -י | מסנני |
| Feminine Singular | יחיד נקבה | -ת/-ה | מסננת |

**Root Words to Check for Each Category:**

```python
root_variations = {
    # Water Filtration
    'מסנן': ['מסנן', 'מסננים', 'מסנני', 'מסננות', 'מסננת'],
    'פילטר': ['פילטר', 'פילטרים', 'פילטרי', 'פילטרות'],
    'סינון': ['סינון', 'סינונים', 'סינוני'],

    # Sinks
    'כיור': ['כיור', 'כיורים', 'כיורי', 'כיורות'],

    # Faucets
    'ברז': ['ברז', 'ברזים', 'ברזי', 'ברזות', 'ברזת'],
    'מתז': ['מתז', 'מתזים', 'מתזי', 'מתזות'],
    'מערבל': ['מערבל', 'מערבלים', 'מערבלי'],

    # Water Bars
    'בר מים': ['בר מים', 'ברי מים', 'בר המים'],
    'מיני בר': ['מיני בר', 'מיניבר', 'מיני ברים'],
    'מתקן מים': ['מתקן מים', 'מתקני מים', 'מתקנים'],
    'קולר': ['קולר', 'קולרים', 'קולרי'],
    'מצנן': ['מצנן', 'מצננים', 'מצנני', 'מצננת'],

    # Garbage Disposal
    'טוחן': ['טוחן', 'טוחנים', 'טוחני', 'טוחנת'],
    'מטחנה': ['מטחנה', 'מטחנות', 'מטחנת'],

    # Water Softener
    'מרכך': ['מרכך', 'מרככים', 'מרככי', 'מרככת'],

    # Osmosis
    'אוסמוזה': ['אוסמוזה', 'אוסמוזות'],
    'ממברנה': ['ממברנה', 'ממברנות', 'ממברני'],

    # Heating
    'דוד': ['דוד', 'דודים', 'דודי'],
    'מחמם': ['מחמם', 'מחממים', 'מחממי', 'מחממת'],
    'קומקום': ['קומקום', 'קומקומים', 'קומקומי'],

    # Plumbing
    'צינור': ['צינור', 'צינורות', 'צינורי'],
    'חיבור': ['חיבור', 'חיבורים', 'חיבורי'],
    'אטם': ['אטם', 'אטמים', 'אטמי'],
    'שסתום': ['שסתום', 'שסתומים', 'שסתומי'],
    'משאבה': ['משאבה', 'משאבות', 'משאבי'],
}
```

### Step 4: Verify Keywords via SE Ranking Data API

```python
# SE Ranking Data API (Different from Project API!)
DATA_API_KEY = "71d577cb-14f4-fb22-3d50-1ed2919458f6"
API_URL = "https://api.seranking.com/v1/keywords/export?source=il"

def verify_keywords(keywords_list):
    """Verify search volume for keywords via SE Ranking API"""
    headers = {
        "Authorization": f"Token {DATA_API_KEY}",
        "Content-Type": "application/json"
    }

    verified = []
    # Process in batches of 50
    for i in range(0, len(keywords_list), 50):
        batch = keywords_list[i:i+50]

        response = requests.post(
            API_URL,
            headers=headers,
            json={"keywords": batch},
            timeout=60
        )

        # Note: API returns 201 on success, not 200!
        if response.status_code == 201:
            results = response.json()
            for item in results:
                if item.get('volume', 0) > 0:
                    verified.append(item)

        time.sleep(0.5)  # Rate limiting

    return verified
```

### Step 5: Multi-Wave Search Strategy

**Wave 1: Basic Variations**
- All singular/plural forms of root words
- Returns ~50-100 new keywords

**Wave 2: Compound Keywords**
```python
compound_modifiers = [
    'מים', 'מטבח', 'אמבטיה', 'שירותים', 'בית', 'ביתי',
    'חשמלי', 'מקצועי', 'קטן', 'גדול', 'נירוסטה', 'תעשייתי'
]

# Generate: "מסנן מים", "מסנן ביתי", "מסנני מטבח", etc.
for root in root_words:
    for mod in compound_modifiers:
        variations.append(f"{root} {mod}")
        variations.append(f"{root} ל{mod}")
```

**Wave 3: Category Expansion**
```python
# Discover related high-volume categories
expansion_keywords = [
    # Bathroom (discovered ארון אמבטיה = 18,100!)
    'ארון אמבטיה', 'ארונות אמבטיה', 'מקלחון', 'מקלחונים',
    'אסלה', 'אסלות', 'אמבטיה', 'אמבטיות',

    # Kitchen
    'ארון מטבח', 'ארונות מטבח', 'משטח', 'משטחים',

    # Installation/Service
    'אינסטלציה', 'אינסטלטור', 'תיקון', 'התקנה',
]
```

**Wave 4: Brand Variations**
```python
brands = ['תמי 4', 'תמי4', 'מי עדן', 'גרואה', 'grohe', 'אלקטרה']
products = ['מסנן', 'פילטר', 'ברז', 'בר מים']

for brand in brands:
    for product in products:
        variations.append(f"{brand} {product}")
```

**Wave 5: Final Sweep**
- Check for any remaining high-volume related keywords
- Verify all data against API one final time

### Step 6: Categorization

```python
def categorize_keyword(keyword):
    """Categorize keyword into appropriate bucket"""
    kw = keyword.lower()

    categories = {
        'סינון מים': ['מסנן', 'פילטר', 'סינון', 'סנן', 'טיהור'],
        'כיורים': ['כיור'],
        'ברז ומתזים': ['ברז', 'מתז', 'grohe', 'גרואה', 'מזלף', 'מערבל'],
        'בר מים': ['בר מים', 'מיני בר', 'קולר', 'מצנן', 'מתקן מים'],
        'טוחן אשפה': ['טוחן', 'מטחנ', 'מגרס'],
        'מרכך מים': ['מרכך', 'ריכוך'],
        'אוסמוזה הפוכה': ['אוסמוזה', 'ממברנ'],
        'מערכות קירור/חימום': ['דוד', 'מחמם', 'קומקום', 'חימום', 'בויילר'],
        'מותגים ויצרנים': ['תמי', 'מי עדן', 'שטראוס', 'אלקטרה'],
        'אביזרים ותחזוקה': ['צינור', 'חיבור', 'אטם', 'שסתום', 'משאב', 'צנרת'],
    }

    for category, patterns in categories.items():
        if any(p in kw for p in patterns):
            return category

    return 'אחר'
```

### Step 7: Long-tail Classification

```python
def is_long_tail(keyword):
    """Keywords with 3+ words are long-tail"""
    return len(keyword.split()) >= 3
```

### Step 8: Generate HTML Report

```python
# See full template in /Users/antoniasepulvedagrasins/TEMPLATES/KEYWORD_RESEARCH_TEMPLATE.html
```

---

## API Reference

### SE Ranking Project API
- **Purpose**: Get keywords domains rank for
- **Key**: `52adfc67e785be54defc2ece910c69965513bbf9`
- **Endpoint**: `GET https://api.seranking.com/v1/domain/keywords?source=il&domain={domain}&type=organic`

### SE Ranking Data API
- **Purpose**: Verify keyword search volumes
- **Key**: `71d577cb-14f4-fb22-3d50-1ed2919458f6`
- **Endpoint**: `POST https://api.seranking.com/v1/keywords/export?source=il`
- **Body**: `{"keywords": ["keyword1", "keyword2", ...]}`
- **Note**: Returns status `201` on success (not 200!)

---

## Validation Checklist

Before delivering report, verify:

- [ ] All keywords verified against SE Ranking API
- [ ] Top 30 keywords have 100% match with API
- [ ] All Hebrew variations included (יחיד, רבים, סמיכות)
- [ ] No duplicate keywords
- [ ] Categories properly assigned
- [ ] Long-tail/Short-tail correctly classified
- [ ] HTML report renders correctly
- [ ] Search/filter functionality works

---

## Expected Results

| Metric | Minimum | Good | Excellent |
|--------|---------|------|-----------|
| Keywords | 1,500+ | 2,000+ | 2,500+ |
| Volume | 300,000+ | 500,000+ | 700,000+ |
| Categories | 8+ | 10+ | 12+ |
| Accuracy | 95%+ | 98%+ | 100% |

---

## File Locations

| File | Purpose |
|------|---------|
| `/Users/antoniasepulvedagrasins/laguna_keywords_categorized.json` | Example database |
| `/Users/antoniasepulvedagrasins/LAGUNA_competitor_keyword_research.html` | Example report |
| `/Users/antoniasepulvedagrasins/TEMPLATES/KEYWORD_RESEARCH_TEMPLATE.html` | HTML template |

---

## Troubleshooting

### API Returns Empty Results
- Check API key is correct
- Verify `source=il` parameter
- Check domain spelling

### Missing High-Volume Keywords
- Run additional search waves
- Check ALL Hebrew variations
- Include brand + product combinations
- Don't forget construct state (-י)

### Duplicate Keywords
```python
# Deduplicate by lowercase
existing = set(kw.lower() for kw in keywords)
```

### Wrong Category Assignment
- Update categorization patterns
- Check for overlapping patterns
- Most specific pattern should match first

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-12 | Initial guide based on LAGUNA project |

---

**Remember: Always be skeptical about your data. Verify everything against the API. Run multiple search waves. Include ALL Hebrew variations.**
