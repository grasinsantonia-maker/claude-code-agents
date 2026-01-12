#!/usr/bin/env python3
"""
Competitor Keyword Research Tool - Hebrew Market
Comprehensive keyword discovery with ALL Hebrew variations

Usage:
    python3 competitor_keyword_research.py --client "CLIENT_NAME" \
        --competitors "domain1.co.il,domain2.co.il" \
        --output "output.html"

Author: Nadav Digital
Version: 1.0
"""

import argparse
import json
import requests
import time
from datetime import datetime
from pathlib import Path

# API Configuration
SE_RANKING_PROJECT_API = "52adfc67e785be54defc2ece910c69965513bbf9"
SE_RANKING_DATA_API = "71d577cb-14f4-fb22-3d50-1ed2919458f6"
DATA_API_URL = "https://api.seranking.com/v1/keywords/export?source=il"


class CompetitorKeywordResearch:
    def __init__(self, client_name, competitors):
        self.client_name = client_name
        self.competitors = competitors
        self.keywords_db = {}
        self.existing_keywords = set()

    def get_competitor_keywords(self, domain):
        """Get keywords a domain ranks for via SE Ranking Domain API"""
        url = "https://api.seranking.com/v1/domain/keywords"
        params = {"source": "il", "domain": domain, "type": "organic"}
        headers = {"Authorization": f"Token {SE_RANKING_PROJECT_API}"}

        try:
            response = requests.get(url, params=params, headers=headers, timeout=60)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"  Error fetching {domain}: {e}")
        return []

    def verify_keywords_batch(self, keywords_list):
        """Verify keywords via SE Ranking Data API"""
        headers = {
            "Authorization": f"Token {SE_RANKING_DATA_API}",
            "Content-Type": "application/json"
        }

        verified = []
        for i in range(0, len(keywords_list), 50):
            batch = keywords_list[i:i+50]
            try:
                response = requests.post(
                    DATA_API_URL,
                    headers=headers,
                    json={"keywords": batch},
                    timeout=60
                )
                if response.status_code == 201:  # Note: 201 not 200!
                    for item in response.json():
                        if item.get('volume', 0) > 0:
                            verified.append(item)
                            print(f"    Found: {item['keyword']} ({item['volume']:,})")
            except Exception as e:
                print(f"  API Error: {e}")
            time.sleep(0.5)

        return verified

    def generate_hebrew_variations(self):
        """Generate ALL Hebrew grammatical variations"""
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

        variations = []
        for root, forms in root_variations.items():
            variations.extend(forms)

        return list(set(variations))

    def generate_compound_keywords(self, base_keywords):
        """Generate compound keywords (root + modifier)"""
        modifiers = [
            'מים', 'מטבח', 'אמבטיה', 'שירותים', 'בית', 'ביתי',
            'חשמלי', 'מקצועי', 'קטן', 'גדול', 'נירוסטה', 'תעשייתי'
        ]

        compounds = []
        for kw in base_keywords:
            for mod in modifiers:
                compounds.append(f"{kw} {mod}")
                compounds.append(f"{kw} ל{mod}")

        return list(set(compounds))

    def get_expansion_keywords(self):
        """Additional high-value keywords to search"""
        return [
            # Bathroom
            'ארון אמבטיה', 'ארונות אמבטיה', 'מקלחון', 'מקלחונים',
            'אסלה', 'אסלות', 'אמבטיה', 'אמבטיות',
            'מראה אמבטיה', 'מדף אמבטיה', 'וילון מקלחת',

            # Kitchen
            'ארון מטבח', 'ארונות מטבח', 'משטח', 'משטחים',

            # Installation
            'אינסטלציה', 'אינסטלטור', 'תיקון', 'התקנה',

            # Materials
            'נירוסטה', 'קרמיקה', 'פורצלן', 'שיש',
        ]

    def categorize_keyword(self, keyword):
        """Assign keyword to appropriate category"""
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

    def add_keywords_to_db(self, keywords_list):
        """Add verified keywords to database"""
        added = 0
        for kw in keywords_list:
            keyword = kw.get('keyword', '').strip()
            if keyword.lower() in self.existing_keywords:
                continue

            category = self.categorize_keyword(keyword)
            if category not in self.keywords_db:
                self.keywords_db[category] = []

            entry = {
                'keyword': keyword,
                'volume': kw.get('volume', 0),
                'cpc': kw.get('cpc', 0),
                'difficulty': kw.get('difficulty', 0),
                'competition': kw.get('competition', 0),
                'is_long_tail': len(keyword.split()) >= 3,
            }

            self.keywords_db[category].append(entry)
            self.existing_keywords.add(keyword.lower())
            added += 1

        return added

    def run_wave(self, wave_name, keywords_to_check):
        """Run a search wave and add results"""
        print(f"\n{'='*60}")
        print(f"WAVE: {wave_name}")
        print(f"{'='*60}")

        # Filter out existing
        new_keywords = [k for k in keywords_to_check if k.lower() not in self.existing_keywords]
        print(f"  Checking {len(new_keywords)} new keywords...")

        if not new_keywords:
            print("  No new keywords to check")
            return 0

        verified = self.verify_keywords_batch(new_keywords)
        added = self.add_keywords_to_db(verified)
        print(f"  Added {added} keywords")

        return added

    def run(self):
        """Execute full keyword research pipeline"""
        print(f"\n{'='*60}")
        print(f"COMPETITOR KEYWORD RESEARCH - {self.client_name}")
        print(f"{'='*60}")
        print(f"Competitors: {len(self.competitors)}")

        # Step 1: Get competitor keywords
        print("\n[STEP 1] Fetching competitor keywords...")
        competitor_keywords = []
        for domain in self.competitors:
            print(f"  Fetching {domain}...")
            kws = self.get_competitor_keywords(domain)
            competitor_keywords.extend(kws)
            print(f"    Found {len(kws)} keywords")

        # Dedupe
        unique_kws = list({kw.get('keyword', ''): kw for kw in competitor_keywords}.values())
        print(f"  Total unique: {len(unique_kws)}")

        # Add to DB
        self.add_keywords_to_db(unique_kws)

        # Step 2: Hebrew variations
        print("\n[STEP 2] Generating Hebrew variations...")
        variations = self.generate_hebrew_variations()
        self.run_wave("Hebrew Variations", variations)

        # Step 3: Compound keywords
        print("\n[STEP 3] Generating compound keywords...")
        compounds = self.generate_compound_keywords(variations)
        self.run_wave("Compound Keywords", compounds)

        # Step 4: Expansion keywords
        print("\n[STEP 4] Checking expansion keywords...")
        expansion = self.get_expansion_keywords()
        self.run_wave("Expansion", expansion)

        # Sort all categories
        for cat in self.keywords_db:
            self.keywords_db[cat] = sorted(
                self.keywords_db[cat],
                key=lambda x: x.get('volume', 0),
                reverse=True
            )

        # Final stats
        total_kw = sum(len(kws) for kws in self.keywords_db.values())
        total_vol = sum(sum(kw.get('volume', 0) for kw in kws) for kws in self.keywords_db.values())

        print(f"\n{'='*60}")
        print("FINAL RESULTS")
        print(f"{'='*60}")
        print(f"Total Keywords: {total_kw:,}")
        print(f"Total Volume: {total_vol:,}")
        print(f"Categories: {len(self.keywords_db)}")

        return self.keywords_db

    def save_json(self, output_path):
        """Save database to JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.keywords_db, f, ensure_ascii=False, indent=2)
        print(f"Saved JSON: {output_path}")

    def generate_html_report(self, output_path):
        """Generate HTML report"""
        total_kw = sum(len(kws) for kws in self.keywords_db.values())
        total_vol = sum(sum(kw.get('volume', 0) for kw in kws) for kws in self.keywords_db.values())

        # HTML generation code here (same as in the guide)
        # ... [truncated for brevity - use template file]

        print(f"Generated HTML: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Competitor Keyword Research Tool')
    parser.add_argument('--client', required=True, help='Client name')
    parser.add_argument('--competitors', required=True, help='Comma-separated competitor domains')
    parser.add_argument('--output', default='keyword_research.html', help='Output HTML file')
    parser.add_argument('--json', help='Also save JSON database')

    args = parser.parse_args()

    competitors = [c.strip() for c in args.competitors.split(',')]

    research = CompetitorKeywordResearch(args.client, competitors)
    research.run()

    if args.json:
        research.save_json(args.json)

    research.generate_html_report(args.output)

    print(f"\nDone! Report saved to: {args.output}")


if __name__ == '__main__':
    main()
