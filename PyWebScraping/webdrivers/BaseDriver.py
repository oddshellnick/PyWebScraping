import typing
from time import sleep
from subprocess import Popen
from random import choice, random
from selenium.webdriver.common.by import By
from PyWebScraping.utilities import WindowRect
from selenium.webdriver import ActionChains, Keys
from PyWindowsCMD.taskkill.parameters import TaskKillTypes
from selenium.webdriver.remote.webelement import WebElement
from PyWebRequests.user_agents import generate_random_user_agent
from PyWindowsCMD.taskkill import (
	ProcessID,
	taskkill_windows
)
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from PyWindowsCMD.netstat import (
	get_localhost_busy_ports,
	get_localhost_minimum_free_port,
	get_localhost_processes_with_pids
)


class EmptyWebDriver:
	"""
    Provides a simplified interface for interacting with a web driver.

    Attributes:
        base_implicitly_wait (int): The base implicit wait time in seconds.
        base_page_load_timeout (int): The base page load timeout in seconds.
        driver (webdriver): The underlying webdriver instance (initialized to None).

    :Usage:
        driver = EmptyWebDriver(implicitly_wait=10, page_load_timeout=30)
    """
	
	def __init__(self, implicitly_wait: int = 5, page_load_timeout: int = 5):
		"""
        Initializes an instance of the EmptyWebDriver class.

        Args:
            implicitly_wait (int): The base implicit wait time in seconds.
            page_load_timeout (int): The base page load timeout in seconds.
        """
		self.base_implicitly_wait = implicitly_wait
		self.base_page_load_timeout = page_load_timeout
		self.driver = None
	
	def switch_to_window(self, window: typing.Optional[typing.Union[str, int]] = None):
		"""
        Switches focus to the specified window.

        Args:
            window (typing.Optional[typing.Union[str, int]]): The name, index, or handle of the window to switch to. If None, switches to the current window. Defaults to None.

        :Usage:
            driver.switch_to_window("window_name")
            driver.switch_to_window(1)  # Switch to the second window
            driver.switch_to_window() # Stays at current window
        """
		if isinstance(window, str):
			self.driver.switch_to.window(window)
		elif isinstance(window, int):
			self.driver.switch_to.window(self.driver.window_handles[window])
		else:
			self.driver.switch_to.window(self.driver.current_window_handle)
	
	def close_window(self, window: typing.Optional[typing.Union[str, int]] = None):
		"""
        Closes the specified window.

        Args:
            window (typing.Optional[typing.Union[str, int]]): The name, index, or handle of the window to close. If None, closes the current window. Defaults to None.
        """
		if window is not None:
			switch_to_new_window = window == self.driver.current_window_handle
		
			self.switch_to_window(window)
			self.driver.close()
		
			if switch_to_new_window and len(self.driver.window_handles) > 0:
				self.switch_to_window(-1)
	
	def close_all_windows(self):
		"""
        Closes all open windows.
        """
		for window in self.driver.window_handles:
			self.close_window(window)
	
	def update_times(
			self,
			temp_implicitly_wait: typing.Optional[int] = None,
			temp_page_load_timeout: typing.Optional[int] = None
	):
		"""
        Updates the implicit wait and page load timeout.

        Args:
            temp_implicitly_wait (typing.Optional[int]): Temporary implicit wait time. Defaults to None.
            temp_page_load_timeout (typing.Optional[int]): Temporary page load timeout. Defaults to None.
        """
		if temp_implicitly_wait:
			implicitly_wait = temp_implicitly_wait + random()
		else:
			implicitly_wait = self.base_implicitly_wait + random()
		
		if temp_page_load_timeout:
			page_load_timeout = temp_page_load_timeout + random()
		else:
			page_load_timeout = self.base_page_load_timeout + random()
		
		self.driver.implicitly_wait(implicitly_wait)
		self.driver.set_page_load_timeout(page_load_timeout)
	
	def find_inner_web_element(
			self,
			parent_element: WebElement,
			by: By,
			value: str,
			temp_implicitly_wait: typing.Optional[int] = None,
			temp_page_load_timeout: typing.Optional[int] = None,
	) -> WebElement:
		"""
        Finds a single web element within another element.

        Args:
            parent_element (WebElement): The parent web element.
            by (By): Locator strategy.
            value (str): Locator value.
            temp_implicitly_wait (typing.Optional[int]): Temporary implicit wait time. Defaults to None.
            temp_page_load_timeout (typing.Optional[int]): Temporary page load timeout. Defaults to None.

        Returns:
            WebElement: The found web element.
        """
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		return parent_element.find_element(by, value)
	
	def find_inner_web_elements(
			self,
			parent_element: WebElement,
			by: By,
			value: str,
			temp_implicitly_wait: typing.Optional[int] = None,
			temp_page_load_timeout: typing.Optional[int] = None,
	) -> list[WebElement]:
		"""
        Finds multiple web elements within another element.

        Args:
            parent_element (WebElement): The parent web element.
            by (By): Locator strategy.
            value (str): Locator value.
            temp_implicitly_wait (typing.Optional[int]): Temporary implicit wait time. Defaults to None.
            temp_page_load_timeout (typing.Optional[int]): Temporary page load timeout. Defaults to None.

        Returns:
            list[WebElement]: A list of found web elements.
        """
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		return parent_element.find_elements(by, value)
	
	def find_web_elements(
			self,
			by: By,
			value: str,
			temp_implicitly_wait: typing.Optional[int] = None,
			temp_page_load_timeout: typing.Optional[int] = None
	) -> list[WebElement]:
		"""
        Finds multiple web elements.

        Args:
            by (By): Locator strategy.
            value (str): Locator value.
            temp_implicitly_wait (typing.Optional[int]): Temporary implicit wait time. Defaults to None.
            temp_page_load_timeout (typing.Optional[int]): Temporary page load timeout. Defaults to None.

        Returns:
            list[WebElement]: A list of found web elements.

        :Usage:
            elements = driver.find_elements(By.CLASS_NAME, "foo")
        """
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		return self.driver.find_elements(by, value)
	
	def get_current_url(self) -> str:
		"""
        Gets the current URL.

        Returns:
            str: The current URL.
        """
		current_url = self.driver.current_url
		return current_url
	
	def get_page_html(self) -> str:
		"""
        Gets the current page source

        Returns:
            str: The page source.
        """
		return self.driver.page_source
	
	def get_rect(self) -> WindowRect:
		"""
        Gets the window rectangle.

        Returns:
            WindowRect: The window rectangle.

        """
		window_rect = self.driver.get_window_rect()
		
		return WindowRect(
				window_rect["x"],
				window_rect["y"],
				window_rect["width"],
				window_rect["height"]
		)
	
	def get_windows_names(self) -> list[str]:
		"""
        Gets the handles of all open windows.

        Returns:
           list[str]:  A list of window handles.
        """
		windows_names = self.driver.window_handles
		return windows_names
	
	def hover_element(self, element: WebElement):
		"""
        Hovers the mouse over an element.

        Args:
            element (WebElement): The element to hover over.
        """
		ActionChains(self.driver).move_to_element(element).perform()
	
	def execute_js_script(self, script: str, *args):
		"""
        Executes a JavaScript script.

        Args:
            script (str): The JavaScript to execute.
            *args: Arguments to pass to the script.
        """
		self.driver.execute_script(script, *args)
	
	def open_new_tab(self, link: str = ""):
		"""
        Opens a new tab with the given URL.

        Args:
            link (str): URL to open in the new tab. Defaults to "".
        """
		self.execute_js_script('window.open("%s");' % link)
	
	def refresh_webdriver(self):
		"""
        Refreshes the current page.
        """
		self.driver.refresh()
	
	def scroll_by_amount(self, x: int = 0, y: int = 0):
		"""
        Scrolls the viewport by a specified amount.

        Args:
            x (int): Horizontal scroll amount. Defaults to 0.
            y (int): Vertical scroll amount. Defaults to 0.
        """
		ActionChains(self.driver).scroll_by_amount(x, y).perform()
	
	def find_web_element(
			self,
			by: By,
			value: str,
			temp_implicitly_wait: typing.Optional[int] = None,
			temp_page_load_timeout: typing.Optional[int] = None
	) -> WebElement:
		"""
        Finds a single web element.

        Args:
            by (By): Locator strategy.
            value (str): Locator value.
            temp_implicitly_wait (typing.Optional[int]): Temporary implicit wait time. Defaults to None.
            temp_page_load_timeout (typing.Optional[int]): Temporary page load timeout. Defaults to None.

        Returns:
            WebElement: The found web element.

        :Usage:
            element = driver.find_element(By.ID, "foo")
        """
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		return self.driver.find_element(by, value)
	
	def scroll_down_of_element(self, by: By, value: str):
		"""
        Scrolls down within a specific element.

        Args:
            by (By): Locator Strategy.
            value (str): Locator Value.
        """
		self.find_web_element(by, value).send_keys(Keys.PAGE_DOWN)
	
	def scroll_from_origin(self, origin: ScrollOrigin, x: int = 0, y: int = 0):
		"""
        Scrolls from a specific origin by a specified amount.

        Args:
            origin (ScrollOrigin): The scroll origin.
            x (int): Horizontal scroll amount. Defaults to 0.
            y (int): Vertical scroll amount. Defaults to 0.

        Raises:
            MoveTargetOutOfBoundsException: If the origin with offset is outside the viewport.
        """
		ActionChains(self.driver).scroll_from_origin(origin, x, y).perform()
	
	def scroll_to_element(self, element: WebElement):
		"""
        Scrolls an element into view.

        Args:
            element (WebElement): The element to scroll into view.
        """
		ActionChains(self.driver).scroll_to_element(element).perform()
	
	def scroll_up_of_element(self, by: By, value: str):
		"""
        Scrolls up within a specific element.

        Args:
            by (By): Locator strategy.
            value (str): Locator value.
        """
		self.find_web_element(by, value).send_keys(Keys.PAGE_UP)
	
	def search_url(
			self,
			url: str,
			temp_implicitly_wait: typing.Optional[int] = None,
			temp_page_load_timeout: typing.Optional[int] = None
	):
		"""
        Opens a URL in the current browser session.

        Args:
            url (str): The URL to open.
            temp_implicitly_wait (typing.Optional[int]): Temporary implicit wait time. Defaults to None.
            temp_page_load_timeout (typing.Optional[int]): Temporary page load timeout. Defaults to None.
        """
		self.update_times(temp_implicitly_wait, temp_page_load_timeout)
		self.driver.get(url)
	
	def stop_browser_loading(self):
		"""
        Stops the current page loading.
        """
		self.execute_js_script("window.stop();")


class BrowserOptionsManager:
	"""
    Manages browser options for Selenium webdriver.

    Attributes:
        options: The browser options object.
        debugging_port_command (str): Command-line argument for setting the debugging port.
        user_agent_command (str): Command-line argument for setting the user agent.
        proxy_command (str): Command-line argument for setting the proxy.
        debugging_port (typing.Optional[int]): The debugging port number. Defaults to None.
        user_agent (typing.Optional[list[str]]): The user agent string as a list of parts. Defaults to None.
        proxy (typing.Optional[typing.Union[str, list[str]]]): The proxy server address or a list of addresses. Defaults to None.

    :Usage:
        options_manager = BrowserOptionsManager(
                debugging_port_command="--remote-debugging-port=%s",
                user_agent_command="--user-agent=%s",
                proxy_command="--proxy-server=%s",
                debugging_port=9222,
                proxy="127.0.0.1:8080"
        )
    """
	
	def __init__(
			self,
			debugging_port_command: str,
			user_agent_command: str,
			proxy_command: str,
			debugging_port: typing.Optional[int] = None,
			user_agent: typing.Optional[list[str]] = None,
			proxy: typing.Optional[typing.Union[str, list[str]]] = None,
	):
		"""
        Initializes the BrowserOptionsManager.

        Args:
            debugging_port_command (str): Command-line argument for setting the debugging port.
            user_agent_command (str): Command-line argument for setting the user agent.
            proxy_command (str): Command-line argument for setting the proxy.
            debugging_port (typing.Optional[int]): The debugging port number. Defaults to None.
            user_agent (typing.Optional[list[str]]): The user agent string as a list. Defaults to None.
            proxy (typing.Optional[typing.Union[str, list[str]]]): The proxy server address or a list of addresses. Defaults to None.
        """
		self.options = self.renew_webdriver_options()
		self.debugging_port_command = debugging_port_command
		self.user_agent_command = user_agent_command
		self.proxy_command = proxy_command
		self.debugging_port = None
		self.user_agent = None
		self.proxy = None
		
		self.set_debugger_address(debugging_port)
		
		self.hide_automation()
		
		self.set_proxy(proxy)
		
		self.set_user_agent(user_agent)
	
	def set_user_agent(self, user_agent: typing.Optional[list[str]] = None):
		"""
        Sets the user agent for the browser.

        Args:
            user_agent (typing.Optional[list[str]]): The user agent string as a list. If None, a default user agent is used. Defaults to None.
        """
		if user_agent is not None:
			self.user_agent = user_agent
		else:
			self.user_agent = [generate_random_user_agent()]
		
		self.options.add_argument(self.user_agent_command % " ".join(self.user_agent))
	
	def set_proxy(self, proxy: typing.Optional[typing.Union[str, list[str]]] = None):
		"""
        Sets the proxy server for the browser.

        Args:
            proxy (typing.Optional[typing.Union[str, list[str]]]): The proxy server address, or a list of addresses. If a list is provided, a random proxy is chosen. Defaults to None.
        """
		self.proxy = proxy
		
		if self.proxy is not None:
			if isinstance(self.proxy, str):
				self.options.add_argument(self.proxy_command % self.proxy)
			else:
				self.options.add_argument(self.proxy_command % choice(self.proxy))
	
	def hide_automation(self):
		"""
        Hides browser automation flags (currently a placeholder).
        """
		pass
	
	def set_debugger_address(self, debugging_port: typing.Optional[int]):
		"""
        Sets the debugger address for the browser.

        Args:
            debugging_port (typing.Optional[int]): The debugging port number.
        """
		self.debugging_port = debugging_port
		
		if self.debugging_port is not None:
			self.options.debugger_address = self.debugging_port_command % self.debugging_port
	
	def renew_webdriver_options(self) -> None:
		"""
        Creates and returns a new browser options object (currently a placeholder).

        Returns:
             None: The new browser options object.
        """
		return None


class BrowserStartArgs:
	"""
    Manages the command-line arguments for starting a web browser.

    Attributes:
        start_command (str): The assembled start command.
        browser_file_name (str): Path to the browser executable.
        debugging_port_command_line (str): Command-line argument for the debugging port.
        webdriver_dir_command_line (str): Command-line argument for the webdriver directory.
        headless_mode_command_line (str): Command-line argument for headless mode.
        mute_audio_command_line (str): Command-line argument for muting audio.
        debugging_port (int): The debugging port number. Defaults to None.
        webdriver_dir (str): The webdriver directory. Defaults to None.
        headless_mode (bool): Whether to run in headless mode. Defaults to False.
        mute_audio (bool): Whether to mute audio. Defaults to False.

    :Usage:
        start_args = BrowserStartArgs(
                browser_file_name="chrome.exe",
                debugging_port_command_line="--remote-debugging-port=%s",
                webdriver_dir_command_line="--webdriver-dir=%s",
                headless_mode_command_line="--headless",
                mute_audio_command_line="--mute-audio"
        )
    """
	
	start_command = ""
	
	def __init__(
			self,
			browser_file_name: str,
			debugging_port_command_line: str,
			webdriver_dir_command_line: str,
			headless_mode_command_line: str,
			mute_audio_command_line: str,
			webdriver_dir: typing.Optional[str] = None,
			debugging_port: typing.Optional[int] = None,
			headless_mode: bool = False,
			mute_audio: bool = False,
	):
		"""
        Initializes BrowserStartArgs with browser settings.

        Args:
            browser_file_name (str): Path to the browser executable.
            debugging_port_command_line (str): Command-line argument for the debugging port.
            webdriver_dir_command_line (str): Command-line argument for the webdriver directory.
            headless_mode_command_line (str): Command-line argument for headless mode.
            mute_audio_command_line (str): Command-line argument for muting audio.
            webdriver_dir (typing.Optional[str]): The webdriver directory. Defaults to None.
            debugging_port (typing.Optional[int]): The debugging port number. Defaults to None.
            headless_mode (bool): Whether to run in headless mode. Defaults to False.
            mute_audio (bool): Whether to mute audio. Defaults to False.
        """
		self.browser_file_name = browser_file_name
		self.debugging_port_command_line = debugging_port_command_line
		self.webdriver_dir_command_line = webdriver_dir_command_line
		self.headless_mode_command_line = headless_mode_command_line
		self.mute_audio_command_line = mute_audio_command_line
		self.debugging_port = debugging_port
		self.webdriver_dir = webdriver_dir
		self.headless_mode = headless_mode
		self.mute_audio = mute_audio
		
		self.update_command()
	
	def update_command(self):
		"""
        Assembles the browser start command based on the current settings.
        """
		start_args = [self.browser_file_name]
		
		if self.debugging_port is not None:
			start_args.append(self.debugging_port_command_line % self.debugging_port)
		
		if self.webdriver_dir is not None:
			start_args.append(self.webdriver_dir_command_line % self.webdriver_dir)
		
		if self.headless_mode:
			start_args.append(self.headless_mode_command_line)
		
		if self.mute_audio is not None:
			start_args.append(self.mute_audio_command_line)
		
		self.start_command = " ".join(start_args)
	
	def clear_command(self):
		"""
        Clears the start command and resets the settings to default values.
        """
		self.debugging_port = None
		self.webdriver_dir = None
		self.headless_mode = False
		self.mute_audio = False
		
		self.update_command()
	
	def set_debugging_port(self, debugging_port: typing.Optional[int] = None):
		"""
        Sets the debugging port.

        Args:
            debugging_port (typing.Optional[int]): The debugging port number. Defaults to None.
        """
		self.debugging_port = debugging_port
		
		self.update_command()
	
	def set_headless_mode(self, headless_mode: bool = False):
		"""
        Sets headless mode.

        Args:
            headless_mode (bool): Whether to enable headless mode. Defaults to False.
        """
		self.headless_mode = headless_mode
		
		self.update_command()
	
	def set_mute_audio(self, mute_audio: bool = False):
		"""
        Sets whether to mute audio.

        Args:
            mute_audio (bool): Whether to mute audio. Defaults to False.
        """
		self.mute_audio = mute_audio
		
		self.update_command()
	
	def set_webdriver_dir(self, webdriver_dir: typing.Optional[str] = None):
		"""
        Sets the webdriver directory.

        Args:
            webdriver_dir (typing.Optional[str]): The webdriver directory path. Defaults to None.
        """
		self.webdriver_dir = webdriver_dir
		
		self.update_command()


class BrowserWebDriver(EmptyWebDriver):
	"""
    Manages a Selenium webdriver instance, including starting, stopping, and restarting the browser.

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
        webdriver_start_args (BrowserStartArgs): Manages browser start-up arguments.
        webdriver_options_manager (BrowserOptionsManager): Manages browser options.
        debugging_port (typing.Optional[int]): The debugging port number. Defaults to None.
        webdriver_dir (typing.Optional[str]): The webdriver directory.  Defaults to None.
        headless_mode (bool): Whether to run in headless mode. Defaults to False.
        mute_audio (bool): Whether to mute audio. Defaults to False.
        user_agent (typing.Optional[list[str]]): The user agent. Defaults to None.
        proxy (typing.Optional[typing.Union[str, list[str]]]) : The proxy server(s). Defaults to None.
        window_rect (WindowRect):  The browser window rectangle.
        webdriver_is_active (bool):  Indicates if the webdriver is currently active.
        webdriver_service (Service | None): The webdriver service. Defaults to None.
        webdriver_options (Options | None): The webdriver options. Defaults to None.

    :Usage:
        webdriver = BrowserWebDriver(...)
        webdriver.start_webdriver(...)
    """
	
	def __init__(
			self,
			browser_file_name: str,
			bsa_debugging_port_command_line: str,
			bsa_webdriver_dir_command_line: str,
			bsa_headless_mode_command_line: str,
			bsa_mute_audio_command_line: str,
			bom_debugging_port_command: str,
			bom_user_agent_command: str,
			bom_proxy_command: str,
			webdriver_path: str,
			webdriver_start_args: typing.Optional[BrowserStartArgs] = None,
			webdriver_options_manager: typing.Optional[BrowserOptionsManager] = None,
			implicitly_wait: int = 5,
			page_load_timeout: int = 5,
			window_rect: WindowRect = WindowRect(),
	):
		"""
        Initializes a new instance of the BrowserWebDriver class.

        Args:
            browser_file_name (str): Path to the browser executable.
            bsa_debugging_port_command_line (str): BrowserStartArgs command-line argument for debugging port.
            bsa_webdriver_dir_command_line (str): BrowserStartArgs command-line argument for webdriver directory.
            bsa_headless_mode_command_line (str): BrowserStartArgs command-line argument for headless mode.
            bsa_mute_audio_command_line (str): BrowserStartArgs command-line argument for muting audio.
            bom_debugging_port_command (str): BrowserOptionsManager command for debugging port.
            bom_user_agent_command (str): BrowserOptionsManager command for user agent.
            bom_proxy_command (str): BrowserOptionsManager command for proxy.
            webdriver_path (str): Path to the webdriver executable.
            webdriver_start_args (typing.Optional[BrowserStartArgs]): Manages browser start-up arguments. Defaults to None.
            webdriver_options_manager (typing.Optional[BrowserOptionsManager]): Manages browser options. Defaults to None.
            implicitly_wait (int): Implicit wait time in seconds. Defaults to 5.
            page_load_timeout (int): Page load timeout in seconds. Defaults to 5.
            window_rect (WindowRect): Initial browser window rectangle. Defaults to WindowRect().
        """
		super().__init__(implicitly_wait, page_load_timeout)
		
		self.browser_file_name = browser_file_name
		self.bsa_debugging_port_command_line = bsa_debugging_port_command_line
		self.bsa_webdriver_dir_command_line = bsa_webdriver_dir_command_line
		self.bsa_headless_mode_command_line = bsa_headless_mode_command_line
		self.bsa_mute_audio_command_line = bsa_mute_audio_command_line
		self.bom_debugging_port_command = bom_debugging_port_command
		self.bom_user_agent_command = bom_user_agent_command
		self.bom_proxy_command = bom_proxy_command
		self.webdriver_path = webdriver_path
		
		if webdriver_start_args is not None:
			self.webdriver_start_args = webdriver_start_args
		else:
			self.webdriver_start_args = BrowserStartArgs(
					self.browser_file_name,
					self.bsa_debugging_port_command_line,
					self.bsa_webdriver_dir_command_line,
					self.bsa_headless_mode_command_line,
					self.bsa_mute_audio_command_line,
			)
		
		if webdriver_options_manager is not None:
			self.webdriver_options_manager = webdriver_options_manager
		else:
			self.webdriver_options_manager = BrowserOptionsManager(
					self.bom_debugging_port_command,
					self.bom_user_agent_command,
					self.bom_proxy_command
			)
		
		self.webdriver_dir, self.headless_mode, self.mute_audio = (
				self.webdriver_start_args.webdriver_dir,
				self.webdriver_start_args.headless_mode,
				self.webdriver_start_args.mute_audio,
		)
		
		self.user_agent, self.proxy = self.webdriver_options_manager.user_agent, self.webdriver_options_manager.proxy
		
		if (
				self.webdriver_options_manager.debugging_port is not None
				and self.webdriver_start_args.debugging_port is not None
		):
			self.debugging_port = self.webdriver_options_manager.debugging_port
		elif self.webdriver_options_manager.debugging_port is not None:
			self.debugging_port = self.webdriver_options_manager.debugging_port
			self.webdriver_start_args.set_debugging_port(self.debugging_port)
		elif self.webdriver_start_args.debugging_port is not None:
			self.debugging_port = self.webdriver_start_args.debugging_port
			self.webdriver_options_manager.set_debugger_address(self.debugging_port)
		else:
			self.debugging_port = None
		
		self.window_rect = window_rect
		self.webdriver_is_active = False
		self.webdriver_service, self.webdriver_options = None, None
	
	def create_driver(self):
		"""
        Creates the webdriver instance (placeholder).
        """
		pass
	
	def renew_bas_and_bom(self):
		"""
        Renews BrowserStartArgs and BrowserOptionsManager (placeholder).
        """
		pass
	
	def check_webdriver_active(self):
		"""
        Checks if the webdriver is currently active.

        Returns:
            bool: True if the webdriver is active, False otherwise.
        """
		if self.debugging_port is not None and self.debugging_port in get_localhost_busy_ports():
			return True
		else:
			return False
	
	def start_webdriver(
			self,
			debugging_port: typing.Optional[int] = None,
			webdriver_dir: typing.Optional[str] = None,
			headless_mode: typing.Optional[bool] = None,
			mute_audio: typing.Optional[bool] = None,
			proxy: typing.Optional[typing.Union[str, list[str]]] = None,
			user_agent: typing.Optional[list[str]] = None,
			window_rect: typing.Optional[WindowRect] = None,
	):
		"""
        Starts the webdriver.

        Args:
            debugging_port (typing.Optional[int]): The debugging port. Defaults to None.
            webdriver_dir (typing.Optional[str]): The webdriver directory. Defaults to None.
            headless_mode (typing.Optional[bool]): Whether to run in headless mode. Defaults to None.
            mute_audio (typing.Optional[bool]): Whether to mute audio. Defaults to None.
            proxy (typing.Optional[typing.Union[str, list[str]]]): The proxy server(s). Defaults to None.
            user_agent (typing.Optional[list[str]]): The user agent. Defaults to None.
            window_rect (typing.Optional[WindowRect]): The browser window size and position. Defaults to None.
        """
		if self.driver is None:
			if webdriver_dir is not None:
				self.webdriver_dir = webdriver_dir
		
			if debugging_port is not None:
				self.debugging_port = get_localhost_minimum_free_port(debugging_port)
			elif self.debugging_port is None:
				self.debugging_port = get_localhost_minimum_free_port()
		
			if headless_mode is not None:
				self.headless_mode = headless_mode
		
			if headless_mode is not None:
				self.mute_audio = mute_audio
		
			if user_agent is not None:
				self.user_agent = user_agent
		
			if proxy is not None:
				self.proxy = proxy
		
			if window_rect is not None:
				self.window_rect = window_rect
		
			self.webdriver_is_active = self.check_webdriver_active()
		
			if not self.webdriver_is_active:
				self.renew_bas_and_bom()
		
				Popen(self.webdriver_start_args.start_command, shell=True)
		
				while not self.webdriver_is_active:
					self.webdriver_is_active = self.check_webdriver_active()
		
				self.create_driver()
			else:
				self.webdriver_start_args.set_debugging_port(self.debugging_port)
				self.webdriver_options_manager.set_debugger_address(self.debugging_port)
		
				self.create_driver()
	
	def close_webdriver(self):
		"""
        Closes the webdriver and associated browser process.
        """
		for pid, ports in get_localhost_processes_with_pids().items():
			if self.debugging_port in ports:
				taskkill_windows(
						taskkill_type=TaskKillTypes.forcefully_terminate,
						selectors=ProcessID(pid)
				)
		
				while self.webdriver_is_active:
					self.webdriver_is_active = self.check_webdriver_active()
		
				sleep(1)
				break
		
		self.webdriver_service = None
		self.webdriver_options = None
		self.driver = None
	
	def restart_webdriver(
			self,
			debugging_port: typing.Optional[int] = None,
			webdriver_dir: typing.Optional[str] = None,
			headless_mode: typing.Optional[bool] = None,
			mute_audio: typing.Optional[bool] = None,
			proxy: typing.Optional[typing.Union[str, list[str]]] = None,
			user_agent: typing.Optional[list[str]] = None,
			window_rect: typing.Optional[WindowRect] = None,
	):
		"""
        Restarts the webdriver with given options.

        Args:
            debugging_port (typing.Optional[int]): The debugging port. Defaults to None.
            webdriver_dir (typing.Optional[str]): The webdriver directory. Defaults to None.
            headless_mode (typing.Optional[bool]): Run in headless mode. Defaults to None.
            mute_audio (typing.Optional[bool]): Whether to mute audio. Defaults to None.
            proxy (typing.Optional[typing.Union[str, list[str]]]): The proxy server. Defaults to None.
            user_agent (typing.Optional[list[str]]): The user agent. Defaults to None.
            window_rect (typing.Optional[WindowRect]): The desired window size and position. Defaults to None.
        """
		self.close_webdriver()
		self.start_webdriver(
				debugging_port,
				webdriver_dir,
				headless_mode,
				mute_audio,
				proxy,
				user_agent,
				window_rect
		)
	
	def change_proxy(self, proxy: str | list[str]):
		"""
        Changes the proxy settings and restarts the webdriver.

        Args:
            proxy (str | list[str]): The new proxy server or list of servers.
        """
		self.webdriver_options_manager.set_proxy(proxy)
		self.restart_webdriver()
	
	def get_vars_for_remote(self):
		"""
        Gets variables needed to create a remote webdriver connection.

        Returns:
            tuple[str, str]: A tuple containing the command executor URL and the session ID.
        """
		return self.driver.command_executor._url, self.driver.session_id
