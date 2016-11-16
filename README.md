# CaptCharmander

Automatically solve captcha on your Pokémon Go account. Only support PTC accounts for now. 

Require a 2captcha account. Get yours [here](http://2captcha.com/?from=2242107) (referral link).

##Features:

* Automatically sovle captcha with 2captcha.
* Loops multiple times to keep checking accounts for captcha.
* Output banned, captcha, error & usable accounts to csv files.

Put your accounts in `account.csv` with format: `username,password`

Edit your settings in `captCharmander.py`.

Run `python captCharmander.py`

Output multiple files with format: `username,password`

* `ban.csv`: banned accounts
* `captcha.csv`: accounts with captcha need to be solved
* `error.csv`: bad accounts (can't login)
* `ok.csv`: usable accounts (no captcha or solved)

MIT License

# TODO

* Support individual location
* Support Google login
* Support parameters from command line