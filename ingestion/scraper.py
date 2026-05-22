import requests
from fake_useragent import UserAgent
from storage.local import load_csv, save_html
from loguru import logger
from config.settings import LOG_DIR, CONFIG_DIR, BRONZE_HTML_DIR

path_to_log_file = LOG_DIR / "bronze_html.log"
logger.add(path_to_log_file)


def create_session():
    s = requests.Session()
    ua = UserAgent(browsers=["Chrome", "Edge", "Firefox"])
    s.headers.update(
        {
            "User-Agent": ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://etrain.info/",
        }
    )
    return s


def fetch(request_session: requests.Session, train_no: str, train_name: str, time="1y"):

    safe_train_name = train_name.strip().replace(" ", "-")
    output_path = BRONZE_HTML_DIR / f"{safe_train_name}-{train_no}.html"
    url = f"https://etrain.info/train/{safe_train_name}-{train_no}/history?d={time}"
    try:
        response = request_session.get(url, allow_redirects=True, timeout=15)
        response.raise_for_status()
        save_html(output_path, response.text)
        logger.info(f"Saved HTMLFetched {url} status={response.status_code}")

    except requests.exceptions.HTTPError as err:
        logger.warning(f"HTTP ERROR {safe_train_name} {train_no} {url}{err}")
    except requests.exceptions.RequestException as err:
        logger.warning(f"Request error {safe_train_name} {train_no} {url}{err}")


if __name__ == "__main__":
    train_config_path = CONFIG_DIR / "trains.csv"
    session = create_session()
    df = load_csv(train_config_path)
    train_no = df.loc[0, "number"]  # type: ignore
    train_name = df.loc[0, "name"]  # type: ignore

    fetch(session, train_no, train_name)  # type: ignore
