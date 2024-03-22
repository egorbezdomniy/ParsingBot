from selenium import webdriver


# настройки при которых открывается окно браузера
def default_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--use-gl=desktop')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-features=UseOzonePlatform')
    options.add_argument('--ozone-platform=wayland')
    options.add_argument('--mute-audio')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-infobars')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--no-sandbox')
    options.add_argument('--no-zygote')
    options.add_argument('--log-level=3')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-breakpad')
    options.add_argument("--page-load-strategy=none")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Убираем видимость того что мы ботик
    return options


# нерабочие настройки в фоновом режиме
def headless_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--use-gl=desktop')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-features=UseOzonePlatform')
    options.add_argument('--ozone-platform=wayland')
    options.add_argument('--mute-audio')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-infobars')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--no-sandbox')
    options.add_argument('--no-zygote')
    options.add_argument('--log-level=3')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-breakpad')
    options.add_argument('--headless')  # Без запуска браузера
    options.add_argument("--disable-blink-features")
    options.add_argument("--page-load-strategy=none")
    options.add_argument(
        f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # беспалевный юзерагент
    options.add_argument("--disable-blink-features=AutomationControlled")  # Убираем видимость того что мы ботик
    return options
