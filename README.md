# Python script to update the SC2 MMR ranges in SC2 Liquipedia

<https://liquipedia.net/starcraft2/Battle.net_Leagues#League_MMR_Ranges>

## HOWTO

* Install ![Python 3](https://www.python.org/downloads/)
* Clone or download the source code
* Install the required packages via pip with `pip install -r requirements.txt`
* Register an application at <https://develop.battle.net/access/> and generate API credentials
* Create `credentials.py` with the following content using the generated API credentials:

```python
client_id = 'ENTER-YOUR-CLIENT-ID-HERE'
secret = 'ENTER-YOUR-SECRET'
```

* Run script via `python3 mmr_ranges.py`
* Copy content of newly generated `liquipedia_ranges.txt` to <https://liquipedia.net/starcraft2/Battle.net_Leagues#League_MMR_Ranges>

