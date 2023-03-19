import csv
import json
from algosdk.v2client import algod
from algosdk.v2client import indexer
from collections import Counter

# Global vars
creator_address = 'enter-creator-wallet'  # Add creator wallet address here
indexer_api = 'https://mainnet-idx.algonode.network'

# Algo vars
algod_token = ""
headers = {'User-Agent': 'py-algorand-sdk'}
idx = indexer.IndexerClient(indexer_token='',
                            headers=headers,
                            indexer_address=indexer_api)

# Fetch Holder's Data using creator_address and page it by 1000 at a clip
next_page = ""
assets = []
while next_page != None:
    accounts_interim = idx.lookup_account_asset_by_creator(
        address=creator_address, next_page=next_page, limit=1000, block=None, round_num=None, include_all=False
    )
    #print(accounts_interim)
    assets.extend(accounts_interim.get("assets", []))
    next_page = accounts_interim.get("next-token", None)
 
#print(len(assets))

asset_list = []
asa_holders_address = []

# Populate ASAs to asset_list
for v in assets:
    asset_id = v['index']
    #put any ASAs here you want to skip / ignore from the generated list
    if(asset_id != 465393419) and (asset_id != 251014570):
        asset_list.append(asset_id)


# Search for balances of assets using ASAs from asset_list
def fetch_holder(asa_id):
    print(asa_id)
    res = idx.asset_balances(asset_id=asa_id)
    asset_bal = res['balances']
    for owner in asset_bal:
        if owner['amount'] == 1:
            asa_holders_address.append(owner['address'])

print("asset count")
print(len(asset_list))

for x in range(0, len(asset_list)):
    fetch_holder(asset_list[x])

asa_count = list(Counter(asa_holders_address).items())
item_length = len(asa_count[0])
for i in asa_count:
    print(i)

with open('asa_holders_by_creator_wallet.csv', 'w') as csvfile: 
    write = csv.writer(csvfile) 
    write.writerows(asa_count) 