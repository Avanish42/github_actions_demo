# YAML Practice — Basic se GitHub Actions tak

Har exercise apne aap likho, phir solution se compare karo.
Solutions sabse neeche hain — pehle mat dekho.

---

## Setup: validator banao

Ye script har exercise ke baad chalao. Ye tumhe batayega ki YAML valid
hai ya nahi, aur parse hone ke baad Python me kya structure bana.

**`check.py`**

```python
import sys, json, yaml

path = sys.argv[1]
try:
    with open(path) as f:
        data = yaml.safe_load(f)
    print("VALID\n")
    print(json.dumps(data, indent=2, default=str))
except yaml.YAMLError as e:
    print("INVALID")
    print(e)
```

```bash
pip install pyyaml
python check.py exercise1.yml
```

JSON output dekhna zaroori hai. Wahi batata hai ki YAML ne tumhari value
ko **string** samjha, **number** samjha, ya **boolean** — jo aksar
surprise hota hai.

---

# LEVEL 1 — Pure YAML

## Ex 1.1 — Apna profile

Banao `profile.yml`. Isme ho:

- `name` (string)
- `experience_years` (number)
- `is_remote` (boolean)
- `manager` (null)
- `skills` (list of 4 strings)
- `location` — nested map jisme `city` aur `country`

**Check:** JSON output me `experience_years` quotes ke bina number dikhna
chahiye, aur `manager` `null` hona chahiye.

---

## Ex 1.2 — Nested list of maps

`team.yml` banao — 3 log, har ek ke paas:

- `name`
- `role`
- `skills` (list)
- `active` (boolean)

Ek naam **flow style** me list likho (`[a, b, c]`), baaki block style me.

**Check:** Top level ek list honi chahiye, dict nahi.

---

## Ex 1.3 — Multi-line strings

`scripts.yml` banao jisme 3 keys hon:

- `setup` — 3 alag shell commands, `|` use karke
- `description` — 3 lines jo ek paragraph me judni chahiye, `>` use karke
- `sql` — ek SQL query jisme indentation preserve ho

**Check:** JSON output me `setup` me `\n` dikhne chahiye, `description` me nahi.

---

## Ex 1.4 — Traps se bacho

`tricky.yml` banao. Ye saari values **string** ke roop me aani chahiye:

| Key | Value |
|---|---|
| `country` | NO |
| `version` | 3.10 |
| `port_code` | 0755 |
| `meeting` | 12:30 |
| `answer` | yes |
| `sha` | 1e10 |

**Check:** JSON me saari values quotes me honi chahiye. Ek bhi bina quotes
ke dikhi to woh galat parse hui hai.

---

## Ex 1.5 — Anchors

`environments.yml` banao. Ek anchor `&defaults` jisme `retries: 3`,
`timeout: 30`, `region: us-east-1`. Phir 3 environments (`dev`, `qa`,
`prod`) jo usko merge karein — `prod` me `timeout` 60 override ho.

**Check:** JSON me teeno env me poori values dikhni chahiye.

---

# LEVEL 2 — Bug dhundo

Har file me kuch galat hai. Pehle **bina chalaye** batao kya galat hai,
phir `check.py` se verify karo.

## Bug 1
```yaml
name: My Workflow
on: push
jobs:
  test:
	runs-on: ubuntu-latest
    steps:
      - run: pytest
```

## Bug 2
```yaml
services:
  - name: api
    port: 8080
   - name: worker
     port: 8081
```

## Bug 3
```yaml
config:
  python-version: 3.10
  enabled: yes
  path: C:\Users\test
```
(Ye parse ho jaayega — batao **values galat kaise** parse hui.)

## Bug 4
```yaml
steps:
  run: echo "first"
  run: echo "second"
```

## Bug 5
```yaml
build:
  script: >
    mkdir reports
    pytest tests/
    echo done
```
(Parse hoga — batao **runtime pe kya tootega**.)

---

# LEVEL 3 — GitHub Actions

Ek naya repo banao (`yaml-practice`) aur har exercise ko actually chalao.
YAML valid hona kaafi nahi — green run milna chahiye.

## Ex 3.1 — Hello World

`.github/workflows/hello.yml`

- Sirf manual trigger
- Ek job `greet`, ubuntu pe
- Do steps: apna naam echo karo, aur date print karo

**Goal:** Actions tab me "Run workflow" button dikhe aur green ho.

---

## Ex 3.2 — Inputs

`hello.yml` me add karo:

- Input `your_name` (string, required, default "Avanish")
- Input `greeting` (choice: Hello / Namaste / Hi)
- Steps me dono use karo

**Goal:** Run karte time do fields wala form dikhe.

---

## Ex 3.3 — Multiple triggers

`.github/workflows/triggers.yml`

- `push` sirf `main` pe, `.md` files ignore
- `schedule` — roz 10:00 AM IST (UTC me convert karo!)
- `workflow_dispatch`
- Ek step jo print kare kis trigger se chala (`github.event_name`)

**Goal:** Push karke verify karo. Cron ka UTC calculation khud karo.

---

## Ex 3.4 — Do jobs, dependency

`.github/workflows/two-jobs.yml`

- Job `build` — ek output `version` set kare (`$GITHUB_OUTPUT` me)
- Job `deploy` — `needs: build`, us version ko print kare
- `deploy` sirf `main` branch pe chale (`if:`)

**Goal:** Actions tab me dono jobs sequential dikhein, arrow ke saath.

---

## Ex 3.5 — Matrix

`.github/workflows/matrix.yml`

- Python 3.10, 3.11, 3.12 pe chale
- `fail-fast: false`
- Har run me `python --version` print ho

**Goal:** 3 parallel jobs dikhein.

---

## Ex 3.6 — Secrets aur variables

- Repo me ek variable `APP_NAME` aur ek secret `MY_TOKEN` banao
- Workflow me dono print karne ki koshish karo
- Ek step jo check kare `MY_TOKEN` set hai ya nahi (value dikhaye bina)

**Goal:** Dekho ki variable plain dikhta hai aur secret `***` ban jaata hai.

---

## Ex 3.7 — Artifact

- Ek step jo `output/result.txt` file banaye (date + run number likhe)
- Us file ko artifact ki tarah upload karo
- `if: always()` lagao
- Run ke baad artifact download karke verify karo

---

## Ex 3.8 — Fail aur recover

- Step 1: `exit 1` (deliberately fail)
- Step 2: `if: failure()` — "step 1 failed" print kare
- Step 3: `if: always()` — hamesha chale
- Step 4: normal (chalna nahi chahiye)

**Goal:** Samjho ki conditions kaise behave karti hain.

---

# Final challenge

Ek workflow banao jo sab combine kare:

- 3 triggers (push, schedule, manual with 2 inputs)
- `concurrency` block
- Environment selection input se
- Job 1: config validate kare (missing var pe fail ho)
- Job 2: `needs` job 1, matrix pe test chalaye
- Artifact upload `if: always()`
- Job summary me markdown table

Bina neeche wale solutions dekhe likho. Ye tumhare asli
pytest-selenium workflow ka mini version hai.

---
---

# SOLUTIONS

## 1.1
```yaml
name: Avanish
experience_years: 12
is_remote: true
manager: null
skills:
  - Python
  - PySpark
  - Snowflake
  - Airflow
location:
  city: Greater Noida
  country: India
```

## 1.2
```yaml
- name: Avanish
  role: Principal Data Engineer
  skills: [Python, PySpark, Snowflake]
  active: true

- name: Priya
  role: Backend Engineer
  skills:
    - Java
    - Kafka
  active: true

- name: Rahul
  role: QA Engineer
  skills:
    - Selenium
    - pytest
  active: false
```

## 1.3
```yaml
setup: |
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

description: >
  Ye teen lines me likha gaya hai
  par parse hone ke baad ek hi
  line banega.

sql: |
  SELECT
      customer_id,
      SUM(amount) AS total
  FROM orders
  GROUP BY customer_id
```

## 1.4
```yaml
country: "NO"
version: "3.10"
port_code: "0755"
meeting: "12:30"
answer: "yes"
sha: "1e10"
```
Bina quotes ke: `NO` → false, `3.10` → 3.1, `0755` → 493 (octal),
`12:30` → 750 (base-60), `yes` → true, `1e10` → 10000000000.0

## 1.5
```yaml
defaults: &defaults
  retries: 3
  timeout: 30
  region: us-east-1

dev:
  <<: *defaults
  url: https://dev.app.com

qa:
  <<: *defaults
  url: https://qa.app.com

prod:
  <<: *defaults
  url: https://app.com
  timeout: 60
```

## Bugs
1. **Tab character** `runs-on` se pehle. YAML me tab illegal hai.
2. **Inconsistent indent** — doosra `- name` 3 space pe hai, pehla 2 pe.
3. `3.10` → float `3.1`, `yes` → `true`, `C:\Users\test` → `\U` invalid
   escape (double quotes me hota to error deta). Teeno quote karo.
4. **Duplicate key `run`** — `steps` list honi chahiye, `- ` chahiye.
5. `>` newlines ko space bana deta hai → `mkdir reports pytest tests/ echo done`
   ek hi command ban jaayegi. `|` use karo.

## 3.1
```yaml
name: Hello World

on: workflow_dispatch

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Say hello
        run: echo "Hello, Avanish!"

      - name: Show date
        run: date
```

## 3.2
```yaml
name: Hello World

on:
  workflow_dispatch:
    inputs:
      your_name:
        description: 'Aapka naam'
        type: string
        default: Avanish
        required: true
      greeting:
        description: 'Greeting style'
        type: choice
        options: [Hello, Namaste, Hi]
        default: Namaste
        required: true

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ inputs.greeting }}, ${{ inputs.your_name }}!"
```

## 3.3
```yaml
name: Trigger Demo

on:
  push:
    branches: [main]
    paths-ignore: ['**.md']
  schedule:
    - cron: "30 4 * * *"      # 04:30 UTC = 10:00 AM IST
  workflow_dispatch:

jobs:
  show:
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo "Trigger : ${{ github.event_name }}"
          echo "Branch  : ${{ github.ref_name }}"
          echo "Actor   : ${{ github.actor }}"
```

## 3.4
```yaml
name: Two Jobs

on: workflow_dispatch

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.set.outputs.version }}
    steps:
      - id: set
        run: echo "version=1.0.${{ github.run_number }}" >> $GITHUB_OUTPUT
      - run: echo "Built version 1.0.${{ github.run_number }}"

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying ${{ needs.build.outputs.version }}"
```

## 3.5
```yaml
name: Matrix Demo

on: workflow_dispatch

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: python --version
```

## 3.6
```yaml
name: Secrets Demo

on: workflow_dispatch

jobs:
  show:
    runs-on: ubuntu-latest
    steps:
      - name: Variable (plain dikhega)
        run: |
          echo "APP_NAME: ${{ vars.APP_NAME }}"

      - name: Secret (masked)
        run: |
          echo "Masked  : $MY_TOKEN"
          echo "Set?    : ${{ secrets.MY_TOKEN != '' }}"
          echo "Length  : ${#MY_TOKEN}"
        env:
          MY_TOKEN: ${{ secrets.MY_TOKEN }}
```

## 3.7
```yaml
name: Artifact Demo

on: workflow_dispatch

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Create file
        run: |
          mkdir -p output
          echo "Run  : ${{ github.run_number }}" >  output/result.txt
          echo "Date : $(date -u)"               >> output/result.txt

      - name: Upload
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: my-output
          path: output/
```

## 3.8
```yaml
name: Conditions Demo

on: workflow_dispatch

jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      - name: This fails
        run: exit 1

      - name: Runs on failure
        if: failure()
        run: echo "Step 1 fail ho gaya"

      - name: Always runs
        if: always()
        run: echo "Main hamesha chalta hoon"

      - name: Never runs
        run: echo "Ye kabhi nahi chalega"
```

Job overall **failed** dikhega — sahi hai. `if: failure()` step chalne
ka matlab ye nahi ki failure "handle" ho gaya.
