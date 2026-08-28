# conftest.py
import os
import json
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Local development ke liye — CI me .env nahi hoti, silently skip
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _load_user_data():
    """USER_DATA secret ko padho aur parse karo."""
    raw = os.environ.get("USER_DATA")

    if not raw:
        pytest.exit(
            "USER_DATA env variable set nahi hai.\n"
            "CI: workflow ke 'env:' block me add karo.\n"
            "Local: .env file me daalo.",
            returncode=1,
        )

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pytest.exit(
            "USER_DATA valid JSON nahi hai. "
            "Expected: {\"username\": \"...\", \"password\": \"...\"}",
            returncode=1,
        )


@pytest.fixture(scope="session")
def config():
    """Saara config ek jagah."""
    user = _load_user_data()

    return {
        "base_url": os.environ["BASE_URL"],
        "username": user["username"],
        "password": user["password"],
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
        "timeout": int(os.getenv("TIMEOUT", "30")),
    }


@pytest.fixture(scope="session", autouse=True)
def log_environment(config):
    """Run ke start me batao kya chal raha hai — password kabhi nahi."""
    print(f"\n{'='*50}")
    print(f"Base URL   : {config['base_url']}")
    print(f"Username   : {config['username']}")
    print(f"Password   : {'set' if config['password'] else 'MISSING'}")
    print(f"Headless   : {config['headless']}")
    print(f"{'='*50}\n")


@pytest.fixture
def driver(config):
    opts = Options()
    if config["headless"]:
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=opts)
    drv.implicitly_wait(config["timeout"])
    yield drv
    drv.quit()