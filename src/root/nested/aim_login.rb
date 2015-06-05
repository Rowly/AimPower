require 'rubygems'
require 'selenium-webdriver'

client = Selenium::WebDriver::Remote::Http::Default.new
client.timeout = 300

@driver = Selenium::WebDriver.for(:remote, :http_client => client)
@wait = Selenium::WebDriver::Wait.new(:timeout => 60)

@driver.navigate.to "http://10.10.10.10/"


def wait_for_element(locator)
  element = @wait.until { @driver.find_element(locator) }
  @wait.until { element.displayed? }
  return element
end

element = wait_for_element(:css => "#username")
element.send_keys "admin"

element = wait_for_element(:css => "#password")
element.send_keys "password"

element = wait_for_element(:css => "#login")
element.click

wait_for_element(:link_text => "DASHBOARD")


@driver.quit