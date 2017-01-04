# CaptCharmander

Automatically solve captcha on your Pokémon Go account. Only support PTC accounts for now. 

Require a 2captcha account. Get yours [here](http://2captcha.com/?from=2242107) (referral link).

Hashing server is supported too, require a hashing key. More info here: https://hashing.pogodev.org

##Features:

* Automatically sovle captcha with 2captcha.
* Support hashing servers.
* Loops multiple times to keep checking accounts for captcha.
* Output banned, captcha, error & usable accounts to csv files.

Put your accounts in `account.csv` with format: 
```
username1,password1
username2,password2
```

Edit your settings in `captCharmander.py`.

Run `python captCharmander.py`

Output multiple files with format: 
```
username1,password1
username2,password2
```

* `ban.csv`: banned accounts
* `captcha.csv`: accounts with captcha need to be solved
* `error.csv`: bad accounts (can't login)
* `ok.csv`: usable accounts (no captcha or solved)

MIT License

# TODO

* Support individual location
* Support Google login
* Support parameters from command line