# InstaBot

InstaBot project is an automation for increasing followers.

InstaBot can:

- Like.
- Follow.
- Unfollow.
- Scroll "home" and "explore".
- Increase his databse based on another account's followers.

randomly so it won't get detected and blocked.

## Installation:

```python
pip install -r requirements.txt
```

also, download <a href="https://chromedriver.chromium.org/downloads">chromedriver</a> and extract it to:
"C:/webdrivers/chromedriver.exe"

### Change settings in [`settings.py`](settings.py):

```python
# Username
Username='type Username here'
# Password
Password='type Password here'
# Source (an instagram page you want to follow his followers)
Source='type Source here'
# Number of Hours the bot will work (Default: 6)
Hours = 6
```

## Usage:

```python
python run.py
```
