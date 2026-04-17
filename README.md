# EbayAutomation
This project contains automated UI tests for eBay using Python, Pytest, and Playwright.

## How to Run
Follow these steps to set up and run the project on your machine.

### Prerequisites
Before running the project, make sure the following are installed:
- Python 3.10 or higher
- pip
- Playwright browser binaries

Check Python version: (Bash)
`python --version`

### Installation
- **Clone the repository:** (Bash) 
```
git clone https://github.com/rotem131/EbayAutomation.git
cd EbayAutomation
```
- **Install dependencies:** (Bash)
`pip install -r requirements.txt`

- **Install Playwright browsers:** (Bash)
`playwright install`

### Execution
**Run all tests** (PowerShell)
`$env:ENVIRONMENT="prod"; pytest tests/`

#### Configuration & Reporting
The project uses **pytest.ini** for default configurations:
- **Logging:** You can view logs while the test is running, displaying logs starting at the info level.
- **HTML Report:** A report named `report-local.html` is automatically generated after each run

**Customization:**
All default configurations can be overridden via the command line.
For example:
- Change report name: (Powershell)
`$env:ENVIRONMENT="prod"; pytest tests/ --html=new-report.html`

## Project Architecture
The project is built using the **Page Object Model (POM)** design pattern,
which separates test logic from page interactions.

### Structure
- **pages/** – page classes with UI actions  
- **tests/** – test scenarios  
- **utils/** – helper functions (e.g., extracting prices, item quantity, reading JSON files)  
- **data/** – test data  
- **config/** – configuration files  
- **constants/** – shared constant values  
- **conftest.py** – defines shared fixtures used by tests (e.g., loading environment variables, test data, and page objects)  
- **requirements.txt** – project dependencies  
- **.env.example** – example environment variables  

## Assumptions
- Prices are handled in Israeli currency (ILS)
- A price filter is available on the website

## Limitations
- Duplicate results are not handled
- The automation does not bypass anti-bot mechanisms
- In case of login failure, the flow continues as a guest