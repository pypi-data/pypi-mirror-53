# Delete All Photos From Google Photos

Turns out it's impossible to delete all of your Google Photos, without manually
selecting photos, page per page, until they are all gone. This app does the
paging and selecting for you. Simply log in and it will start driving from
there!

## Setup ##

1. `pip3 install delete-all-google-photos`

2. To get the latest from time to time, update your version:
`pip3 install --upgrade delete-all-google-photos`

3. Chromedriver should be fetched automatically. But if you run into issues,
try this:
```
# Mac:
brew tap homebrew/cask
brew cask install chromedriver

# Ubuntu/Debian:
# See also: https://askubuntu.com/questions/539498/where-does-chromedriver-install-to
sudo apt-get install chromium-chromedriver
```
