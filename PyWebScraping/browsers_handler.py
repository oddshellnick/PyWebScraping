import browsers


def get_installed_browsers():
	"""
    Gets a list of unique installed browsers using the 'browsers' module.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a unique installed browser
        and contains information like browser name, version, etc.  Returns an empty list if no browsers are found.

    :Usage:
        installed = get_installed_browsers()
        print(installed)  # Output will vary depending on the user's system.
    """
	installed_browsers = []
	
	for browser in browsers.browsers():
		if browser not in installed_browsers:
			installed_browsers.append(browser)
	
	return installed_browsers


def get_browser_version(browser_name: str):
	"""
    Gets the version of a specified browser.

    Args:
        browser_name (str): The display name of the browser (e.g., "Chrome", "Firefox").

    Returns:
        typing.Optional[str]: The version string of the browser if found, otherwise None.

    :Usage:
       version = get_browser_version("Chrome")
       print(version)  # Output will vary depending on the user's installed Chrome version or be None if not found
    """
	for browser in browsers.browsers():
		if browser["display_name"] == browser_name:
			return browser["version"]
	
	return None
