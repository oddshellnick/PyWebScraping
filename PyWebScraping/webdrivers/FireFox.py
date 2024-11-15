from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from PyWebScraping.utilities import WindowRect
from PyWebScraping.webdrivers.BaseDriver import (
    BrowserOptionsManager,
    BrowserStartArgs,
    BrowserWebDriver,
    EmptyWebDriver,
)


class FirefoxOptionsManager(BrowserOptionsManager):
    """
    Manages Firefox webdriver options.

    Attributes:
        options (Options): The Firefox options object.
        debugging_port_command (str): Command-line argument for setting the debugging port.
        user_agent_command (str): Command-line argument for setting the user agent.
        proxy_command (str): Command-line argument for setting the proxy.
        debugging_port (int | None): The debugging port number. Defaults to None.
        user_agent (list[str] | None): The user agent string as a list of parts. Defaults to None.
        proxy (str | list[str] | None): The proxy server address or a list of addresses. Defaults to None.

    :Usage:
        options_manager = FirefoxOptionsManager(debugging_port=9222, user_agent="MyUserAgent", proxy="127.0.0.1:8080")
        options_manager.hide_automation()
    """

    def __init__(
        self,
        debugging_port: int | None = None,
        user_agent: list[str] | None = None,
        proxy: str | list[str] | None = None,
    ):
        """
        Initializes FirefoxOptionsManager.

        Args:
            debugging_port (int | None): Port for remote debugging. Defaults to None.
            user_agent (list[str] | None): User agent string or list of strings. Defaults to None.
            proxy (str | list[str] | None): Proxy server address or list of addresses. Defaults to None.

        :Usage:
            options_manager = FirefoxOptionsManager(debugging_port=9222, user_agent=["My","User","Agent"], proxy="127.0.0.1:8080")
        """
        super().__init__("127.0.0.1:%d", "user-agent=%s", "--proxy-server=%s", debugging_port, user_agent, proxy)

    def hide_automation(self):
        """
        Adds arguments to hide automation features.
        These arguments may not have the desired effect in Firefox.

        :Usage:
            options_manager = FirefoxOptionsManager()
            options_manager.hide_automation()
        """
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--no-first-run")
        self.options.add_argument("--no-service-autorun")
        self.options.add_argument("--password-store=basic")

    def renew_webdriver_options(self):
        """
        Creates and returns a new Options object.

        Returns:
            Options: A new Selenium Firefox options object.

        :Usage:
            options_manager = FirefoxOptionsManager()
            new_options = options_manager.renew_webdriver_options()
        """
        return Options()


class FirefoxStartArgs(BrowserStartArgs):
    """
    Manages Firefox webdriver startup arguments.

    Attributes:
        start_command (str): The assembled start command.
        browser_file_name (str): Path to the browser executable.
        debugging_port_command_line (str): Command-line argument for the debugging port.
        webdriver_dir_command_line (str): Command-line argument for the webdriver directory.
        headless_mode_command_line (str): Command-line argument for headless mode.
        mute_audio_command_line (str): Command-line argument for muting audio.
        debugging_port (int | None): The debugging port number. Defaults to None.
        webdriver_dir (str | None): The webdriver directory. Defaults to None.
        headless_mode (bool): Whether to run in headless mode. Defaults to False.
        mute_audio (bool): Whether to mute audio. Defaults to False.

    :Usage:
        start_args = FirefoxStartArgs(webdriver_dir="/path/to/webdriver", debugging_port=9222, headless_mode=True)
    """

    def __init__(
        self,
        webdriver_dir: str | None = None,
        debugging_port: int | None = None,
        headless_mode: bool = False,
        mute_audio: bool = False,
    ):
        """
        Initializes FirefoxStartArgs.

        Args:
            webdriver_dir (str | None): Directory of the webdriver executable (profile directory). Defaults to None.
            debugging_port (int | None): Port for remote debugging. Defaults to None.
            headless_mode (bool): Run Firefox in headless mode. Defaults to False.
            mute_audio (bool): Intended to mute audio, but likely has no effect in Firefox. Defaults to False.

        :Usage:
            start_args = FirefoxStartArgs(webdriver_dir="/path/to/profile", debugging_port=9222, headless_mode = True)
        """
        super().__init__(
            "firefox.exe",
            "--remote-debugging-port %d",
            '--profile "%s"',
            "--headless",
            "--mute-audio",
            webdriver_dir,
            debugging_port,
            headless_mode,
            mute_audio,
        )


class FirefoxWebDriver(BrowserWebDriver):
    """
    Controls a Firefox webdriver instance.

    Attributes:
        browser_file_name (str): Path to the browser executable.
        bsa_debugging_port_command_line (str): BrowserStartArgs command-line argument for debugging port.
        bsa_webdriver_dir_command_line (str): BrowserStartArgs command-line argument for webdriver directory.
        bsa_headless_mode_command_line (str): BrowserStartArgs command-line argument for headless mode.
        bsa_mute_audio_command_line (str): BrowserStartArgs command-line argument for muting audio.
        bom_debugging_port_command (str): BrowserOptionsManager command for debugging port.
        bom_user_agent_command (str): BrowserOptionsManager command for user agent.
        bom_proxy_command (str): BrowserOptionsManager command for proxy.
        webdriver_path (str): Path to the webdriver executable.
        webdriver_start_args (FirefoxStartArgs): Manages browser start-up arguments.
        webdriver_options_manager (FirefoxOptionsManager): Manages browser options.
        debugging_port (int | None): The debugging port number. Defaults to None.
        webdriver_dir (str | None): The webdriver directory.  Defaults to None.
        headless_mode (bool): Whether to run in headless mode. Defaults to False.
        mute_audio (bool): Whether to mute audio. Defaults to False.
        user_agent (list[str] | None): The user agent. Defaults to None.
        proxy (str | list[str] | None) : The proxy server(s). Defaults to None.
        window_rect (WindowRect):  The browser window rectangle.
        webdriver_is_active (bool):  Indicates if the webdriver is currently active.
        webdriver_service (Service | None): The webdriver service. Defaults to None.
        webdriver_options (Options | None): The webdriver options. Defaults to None.

    :Usage:
        webdriver = FirefoxWebDriver(webdriver_path="/path/to/geckodriver")
        webdriver.create_driver()
        webdriver.driver.get("https://www.example.com")
    """

    def __init__(
        self,
        webdriver_path: str,
        webdriver_start_args: FirefoxStartArgs = FirefoxStartArgs(),
        webdriver_options_manager: FirefoxOptionsManager = FirefoxOptionsManager(),
        implicitly_wait: int = 5,
        page_load_timeout: int = 5,
        window_rect: WindowRect = WindowRect(),
    ):
        """
        Initializes FirefoxWebDriver.

        Args:
            webdriver_path (str): Path to the geckodriver executable.
            webdriver_start_args (FirefoxStartArgs): Startup arguments for Firefox.
            webdriver_options_manager (FirefoxOptionsManager): Options manager for Firefox.
            implicitly_wait (int): Implicit wait time in seconds.
            page_load_timeout (int): Page load timeout in seconds.
            window_rect (WindowRect): Window rectangle for setting window position and size.

        :Usage:
            webdriver = FirefoxWebDriver(webdriver_path="/path/to/geckodriver", webdriver_start_args=FirefoxStartArgs(webdriver_dir="path/to/profile", debugging_port=9222))
        """
        super().__init__(
            "firefox.exe",
            "--remote-debugging-port %d",
            '--profile "%s"',
            "--headless",
            "--mute-audio",
            "127.0.0.1:%d",
            "user-agent=%s",
            "--proxy-server=%s",
            webdriver_path,
            webdriver_start_args,
            webdriver_options_manager,
            implicitly_wait,
            page_load_timeout,
            window_rect,
        )

    def create_driver(self):
        """
        Creates the Firefox webdriver instance.

        :Usage:
            webdriver = FirefoxWebDriver(webdriver_path="/path/to/geckodriver")
            webdriver.create_driver()
        """
        self.webdriver_service = Service(executable_path=self.webdriver_path)
        self.webdriver_options = self.webdriver_options_manager.options

        self.driver = webdriver.Firefox(options=self.webdriver_options, service=self.webdriver_service)

        self.driver.set_window_position(x=self.window_rect.x, y=self.window_rect.y)
        self.driver.set_window_size(width=self.window_rect.width, height=self.window_rect.height)

        self.driver.implicitly_wait(self.base_implicitly_wait)
        self.driver.set_page_load_timeout(self.base_page_load_timeout)

    def renew_bas_and_bom(self):
        """
        Renews the BrowserStartArgs and BrowserOptionsManager.

        :Usage:
           webdriver = FirefoxWebDriver(webdriver_path="/path/to/geckodriver")
           webdriver.renew_bas_and_bom()
        """
        self.webdriver_start_args = FirefoxStartArgs(
            self.webdriver_dir, self.debugging_port, self.headless_mode, self.mute_audio
        )
        self.webdriver_options_manager = FirefoxOptionsManager(self.debugging_port, self.user_agent, self.proxy)


class FirefoxRemoteWebDriver(EmptyWebDriver):
    """
    Controls a remote Firefox webdriver instance.

    Attributes:
        base_implicitly_wait (int): The base implicit wait time in seconds.
        base_page_load_timeout (int): The base page load timeout in seconds.
        driver (webdriver.Remote | None): The remote webdriver instance. Defaults to None.
        command_executor (str): The address of the remote webdriver server.
        session_id (str): The session ID of the remote webdriver.
        webdriver_options_manager (FirefoxOptionsManager): The options manager for the webdriver.

    :Usage:
         remote_webdriver = FirefoxRemoteWebDriver(command_executor="http://127.0.0.1:4444", session_id="some_session_id")
         remote_webdriver.create_driver()
    """

    def __init__(
        self,
        command_executor: str,
        session_id: str,
        webdriver_options_manager: FirefoxOptionsManager = FirefoxOptionsManager(),
        implicitly_wait: int = 5,
        page_load_timeout: int = 5,
    ):
        """
        Initializes FirefoxRemoteWebDriver.

        Args:
            command_executor (str): The address of the remote webdriver server.
            session_id (str): The ID of the existing webdriver session.
            webdriver_options_manager (FirefoxOptionsManager): Options manager for Firefox. Defaults to FirefoxOptionsManager().
            implicitly_wait (int): Implicit wait time in seconds. Defaults to 5.
            page_load_timeout (int): Page load timeout in seconds. Defaults to 5.

        :Usage:
            remote_webdriver = FirefoxRemoteWebDriver(command_executor="http://127.0.0.1:4444", session_id="some_session_id")
        """
        super().__init__(implicitly_wait, page_load_timeout)

        self.command_executor = command_executor
        self.session_id = session_id
        self.webdriver_options_manager = webdriver_options_manager
        self.driver = None

    def create_driver(self, command_executor: str | None = None, session_id: str | None = None):
        """
        Creates the remote Firefox webdriver instance.

        Args:
            command_executor (str | None): The address of the remote webdriver server. Defaults to None.
            session_id (str | None): The ID of the existing webdriver session. Defaults to None.

        :Usage:
            remote_webdriver = FirefoxRemoteWebDriver(command_executor="http://127.0.0.1:4444", session_id="some_session_id")
            remote_webdriver.create_driver()
            # or to reconnect to a different session
            remote_webdriver.create_driver(session_id="another_session_id")
        """
        if command_executor is not None:
            self.command_executor = command_executor

        if session_id is not None:
            self.session_id = session_id

        self.driver = webdriver.Remote(
            command_executor=self.command_executor, options=self.webdriver_options_manager.options
        )

        self.close_window()
        self.driver.session_id = self.session_id
        self.switch_to_window()

        self.driver.implicitly_wait(self.base_implicitly_wait)
        self.driver.set_page_load_timeout(self.base_page_load_timeout)
