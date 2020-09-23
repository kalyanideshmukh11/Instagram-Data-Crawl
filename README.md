## Install
1. Make sure you have Chrome browser installed.
2. Download [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) and put it into bin folder: `./inscrawler/bin/`
3. Install Selenium: `pip3 install -r requirements.txt`
4. Create secret.txt file into `./inscrawler/`. First line of secret.txt should be Instagram username and second line should be password.

## Crawler
### Usage
```
positional arguments:
  mode
    options: [posts_full, profile, hashtag]

optional arguments:
  -n NUMBER, --number NUMBER
                        number of returned posts
  -u USERNAME, --username USERNAME
                        instagram's username
  -t TAG, --tag TAG     instagram's tag name

```


### Get User Details

1. Create `pending.json` file at the root folder
2. Add the list of usernames you want to fetch details for into the pending.json file
3. Create `visited.json` file at the root folder
4. Add list of usernames for which you don't want to fetch the details or add empty list
5. Run using `python crawler.py profile`
6. User details will be added into the file `users.json`. 
7. Crawler will update the list in `pending.json` using usernames from followers and following list
