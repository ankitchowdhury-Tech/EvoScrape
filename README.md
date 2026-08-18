\# EvoScrape 🤖



AI-Assisted Self-Healing Web Scraper



\## 📌 About



EvoScrape is an AI-assisted web scraper that can automatically recover when a website changes its HTML structure or CSS selectors.



Traditional web scrapers can break when a website changes something like:



```text

\[data-testid="price"]

```



to:



```text

.product-price

```



EvoScrape detects the broken selector, analyzes the current webpage, finds possible replacement elements, scores them, validates the best candidate, saves the new selector, and continues scraping.



\## ✨ Features



\* 🔎 Live webpage inspection

\* 🎯 CSS selector validation

\* 🧠 Intelligent candidate scoring

\* 🔧 Automatic selector healing

\* 🧪 Replacement selector validation

\* 💾 Automatic selector updates

\* 📊 Healing confidence scores

\* 📝 Healing history logs

\* 📦 Product data extraction

\* 🚀 One-command execution



\## 🧠 How EvoScrape Works



```text

Saved Selector

&#x20;     │

&#x20;     ▼

Check Selector

&#x20;     │

&#x20;     ├── ✅ Works ───────► Extract Data

&#x20;     │

&#x20;     └── ❌ Failed

&#x20;           │

&#x20;           ▼

&#x20;    Discover Candidates

&#x20;           │

&#x20;           ▼

&#x20;     Score Candidates

&#x20;           │

&#x20;           ▼

&#x20;      Best Candidate

&#x20;           │

&#x20;           ▼

&#x20;    Validate Selector

&#x20;           │

&#x20;           ▼

&#x20;     Save New Selector

&#x20;           │

&#x20;           ▼

&#x20;      Extract Data

```



\## 🏗️ Project Structure



```text

EvoScrape/

│

├── run.py

├── demo.py

├── README.md

│

├── ai/

│   ├── \_\_init\_\_.py

│   ├── auto\_heal.py

│   ├── healer.py

│   ├── scorer.py

│   └── validator.py

│

├── config/

│   ├── selectors.json

│   └── healing\_log.json

│

└── website/

&#x20;   ├── index.html

&#x20;   └── index\_backup.html

```



\## ⚙️ Technologies Used



\* Python

\* Playwright

\* BeautifulSoup

\* HTML

\* CSS Selectors

\* JSON

\* PowerShell



\## 📦 Requirements



Python 3.10 or newer.



Install the required packages:



```bash

pip install playwright beautifulsoup4

```



Install the Playwright browser:



```bash

playwright install chromium

```



\## 🚀 Running EvoScrape



\### Step 1 — Start the test website



Open a PowerShell terminal inside the EvoScrape folder and run:



```powershell

python -m http.server 8000 --directory website

```



Keep this terminal running.



\### Step 2 — Open another PowerShell



Go to the project folder:



```powershell

cd C:\\Users\\rick\\Desktop\\EvoScrape

```



Activate the virtual environment:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### Step 3 — Run EvoScrape



```powershell

python .\\run.py

```



\## 🧪 Self-Healing Demo



The project contains a simulated website redesign.



\### Original selector



```text

\[data-testid="price"]

```



\### New selector



```text

.product-price

```



When the old selector stops working, EvoScrape detects the failure.



It discovers candidates such as:



```text

.product

.product-price

```



The candidate scorer evaluates them.



Example:



```text

Candidate:

{'tag': 'div',

&#x20;'text': '₹49,999',

&#x20;'data-testid': None,

&#x20;'id': None,

&#x20;'class': \['product-price']}



Score: 85



Reasons:

\- exact value match

\- price-like value

\- price-related class

```



The system chooses:



```text

.product-price

```



It then validates the selector and saves it automatically.



\## 📊 Example Output



```text

================================

&#x20;       EVOSCRAPE AI

================================



🔧 Checking scraper health...



🔎 Checking saved selector:

\[data-testid="price"]



❌ Selector failed.

Reason: Selector found no elements



🔧 AUTO-HEAL ACTIVATED



🔎 Candidates discovered:



Candidate:

{'tag': 'div', 'text': '₹49,999',

&#x20;'data-testid': None,

&#x20;'id': None,

&#x20;'class': \['product-price']}



Score: 85



🏆 BEST REPLACEMENT

Element : div

Value   : ₹49,999

Selector: .product-price

Score   : 85



🧪 Validating replacement selector...



❤️ AUTO-HEAL SUCCESSFUL

Old: \[data-testid="price"]

New: .product-price



💾 Selector saved!

File: config/selectors.json



📊 Healing report saved!

File: config/healing\_log.json



🚀 Starting extraction...



================================

&#x20;      EVOSCRAPE RESULT

================================



📦 Product : Gaming Laptop

💰 Price   : ₹49,999

⭐ Rating  : 4.5



🔎 Selector : .product-price



✅ SCRAPING COMPLETE

```



\## 📊 Healing Log



Every successful healing operation can be recorded in:



```text

config/healing\_log.json

```



Example:



```json

{

&#x20;   "field": "price",

&#x20;   "old\_selector": "\[data-testid=\\"price\\"]",

&#x20;   "new\_selector": ".product-price",

&#x20;   "confidence": 0.85,

&#x20;   "reasons": \[

&#x20;       "exact value match",

&#x20;       "price-like value",

&#x20;       "price-related class"

&#x20;   ],

&#x20;   "status": "healed"

}

```





\## 🎯 Why EvoScrape?



Traditional scrapers often depend on fixed selectors.



For example:



```html

<span data-testid="price">₹49,999</span>

```



If a website redesign changes the element to:



```html

<div class="product-price">₹49,999</div>

```



the original selector may stop working.



EvoScrape attempts to recover automatically instead of requiring the developer to manually update the scraper.



\## 🔮 Future Improvements



Future versions could include:



\* 🤖 LLM-powered element reasoning

\* 🧠 More advanced semantic matching

\* 🔄 Automatic retries

\* 📄 Multiple-page scraping

\* 📦 CSV and JSON exports

\* 🖼️ Screenshot-based element detection

\* 🎯 Multiple-field healing

\* 🌐 Support for more complex websites

\* 📊 Web dashboard for healing history

\* 📈 Advanced confidence thresholds



\## 🎓 Educational Purpose



EvoScrape is an educational project exploring how AI-assisted systems can make web automation more resilient to website changes.



The current version uses deterministic scoring and validation rather than relying on an external AI API.



\## 📜 License



This project is intended for educational and experimental purposes.



