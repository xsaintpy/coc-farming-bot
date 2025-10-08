import time
from used_account import get_account_choice
from base_search import searchforbase

# --------------------------------------------- DE --------------------------------------------- #
# Die Main Logik. Hier wird die Account-Choice abgefragt und an "searchforbase" gepassed. Dann läuft der Loot-Prozess
# so lange, bis man den Code stoppt. (Noch ausbaufähig.)

# --------------------------------------------- ENG --------------------------------------------- #
# The main logic. Here the account choice is queried and passed to “searchforbase”. Then the loot process runs
# until the code is stopped. (Still expandable.)

used_account = "1"
while True:
    time.sleep(5)
    searchforbase(used_account)