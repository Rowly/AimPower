require 'selenium-webdriver'
require 'headless'

headless = Headless.new
headless.start

@driver = Selenium::WebDriver.for :firefox
@wait = Selenium::WebDriver::Wait.new(:timeout => 60)

@driver.navigate.to "http://10.10.l0.10/"

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

element = wait_for_element(:link_text => "Updates")
element.click

element = wait_for_element(:link_text => "Reset Aim Configuration")
element.click

element = wait_for_element(:css => "#confirm_reset_link")
element.click

@driver.quit