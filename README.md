# twisearch
Program to download tweets containing a given hashtag and store the results in a csv file

## Setup
Tested on Python3.8 and Python3.9
* Clone this repository
  ```
  $ git clone https://github.com/vikctar/twisearch.git
  ```
* Setup a virtual environment and install requirements
  ```
  $ python3 -m venv env
  ```
  ```
  $ source env/bin/activate
  ```
  ```
  $ pip install -r requirements.txt
  ```
* Create a Twitter developer account by following steps found at [Twitter Developer Portal](https://developer.twitter.com/en/apply-for-access)
* After having successfully set up a Twitter developer account, create an app and obtain an *API KEY* and an *API SECRET*
* Paste the API KEY and SECRET in the .env file
* With the virtual environment active, run the program
  ```
  $ python app.py hashtag
  ```
  Replace *hashtag* with your desired search tag.
* In case you run the program without supplying a hashtag, a default hashtag is set inside the program.