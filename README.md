# EbayAutomation
This project contains automated UI tests for eBay using Python, Pytest, and Playwright.

## How to Run
Follow these steps to set up and run the project on your machine.

### Prerequisites
Before running the project, make sure the following are installed:
- Python 3.10 or higher
- pip
- Allure CLI (optional, for viewing reports locally)

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

**View Allure report locally** (Bash)
`allure serve allure-results`

#### Configuration & Reporting
The project uses **pytest.ini** for default configurations:
- **Logging:** You can view logs while the test is running, displaying logs starting at the info level.
- **Allure Report:** Test results are saved in `allure-results/` and can be viewed using Allure locally or via CI

**Customization:**
All default configurations can be overridden via the command line.
For example:
- Override Allure results directory: (PowerShell)  
`$env:ENVIRONMENT="prod"; pytest tests/ --alluredir=my-results`

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
- The automation assumes that all filtered products are valid for purchase; products that cannot be added to the cart will cause the test to fail

## Limitations
- Duplicate results are not handled
- The automation does not bypass anti-bot mechanisms
- In case of login failure, the flow continues as a guest