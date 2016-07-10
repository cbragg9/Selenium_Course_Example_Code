import pytest
from selenium import webdriver
import os
import config


def pytest_addoption(parser):
    parser.addoption("--baseurl",
                     action="store",
                     default="http://the-internet.herokuapp.com",
                     help="base URL for the application under test")
    parser.addoption("--host",
                     action="store",
                     default="saucelabs",
                     help="where to run your tests: localhost or saucelabs")
    parser.addoption("--browser",
                     action="store",
                     default="internet explorer",
                     help="the name of the browser you want to test with")
    parser.addoption("--browserversion",
                     action="store",
                     default="10.0",
                     help="the browser version you want to test with")
    parser.addoption("--platform",
                     action="store",
                     default="Windows 7",
                     help="the operating system to run your tests on (saucelabs only)")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    grab the test outcome and store the result
    add the result for each phase of a call ("setup", "call", and "teardown")
    as an attribute to the request.node object in a fixture
    e.g.,
        request.node.result_call.failed
        request.node.result_call.passed
    """
    outcome = yield
    result = outcome.get_result()
    setattr(item, "result_" + result.when, result)


@pytest.fixture(scope="function")
def driver(request):
    config.baseurl = request.config.getoption("--baseurl")
    config.host = request.config.getoption("--host").lower()
    config.browser = request.config.getoption("--browser").lower()
    config.browserversion = request.config.getoption("--browserversion").lower()
    config.platform = request.config.getoption("--platform").lower()

    if config.host == "saucelabs":
        desired_caps = {}
        desired_caps["browserName"] = config.browser
        desired_caps["version"] = config.browserversion
        desired_caps["platform"] = config.platform
        desired_caps["name"] = request.cls.__name__ + "." + request.function.__name__
        credentials = os.environ["SAUCE_USERNAME"] + ":" + os.environ["SAUCE_ACCESS_KEY"]
        url = "http://" + credentials + "@ondemand.saucelabs.com:80/wd/hub"
        _driver = webdriver.Remote(url, desired_caps)
    if config.host == "localhost":
        if config.browser == "firefox":
            _driver = webdriver.Firefox()
        elif config.browser == "chrome":
            chromedriver = os.getcwd() + "/vendor/chromedriver"
            _driver = webdriver.Chrome(chromedriver)

    def quit():
        try:
            if config.host == "saucelabs":
                if request.node.result_call.failed:
                    _driver.execute_script("sauce:job-result=failed")
                    raise AssertionError("http://saucelabs.com/beta/tests/" + _driver.session_id)
                elif request.node.result_call.passed:
                    _driver.execute_script("sauce:job-result=passed")
        finally:
            _driver.quit()

    request.addfinalizer(quit)
    return _driver
