from pya3 import Aliceblue
#pip install pya3

username = '2559'
apiKey = 'Dzk0WGYUqqpQ9qqzUpsLD1eF1xyxuezg5JV9rdvN8XrmsC6iYl4qLhYXer8854TY5pWPUXynRCDfeoYdRFvJg8CQfSASSx1SFWiOB4AHKYuNTQKl9nHmH3RLpo1Nu'

alice = Aliceblue(user_id=username,api_key=apiKey)

a = (alice.get_session_id())
sessionId = a['sessionID']
print(sessionId)

with open("alice_username.txt", 'w') as file:
    file.write(username)
with open("alice_api.txt", 'w') as file:
    file.write(apiKey)
with open("alice_session.txt", 'w') as file:
    file.write(sessionId)

alice.get_contract_master("MCX")
alice.get_contract_master("NFO")
alice.get_contract_master("NSE")
alice.get_contract_master("BSE")
alice.get_contract_master("CDS")
alice.get_contract_master("BFO")
alice.get_contract_master("INDICES")


# print(alice.get_instrument_by_symbol('NSE','SBIN'))
# inst = alice.get_instrument_by_symbol('NSE','SBIN')
# print(inst)

# # ['NSE', 3045, 'SBIN', 'SBIN-EQ', '', 1]
# inst = [
#   {'exchange':inst[0],
#   'token':inst[1],
#   'symbol':inst[2],
#   'name':inst[3],
#   'expiry':inst[4],
#   'lot_size':inst[5]},
#   {'exchange':inst[0],
#   'token':inst[1],
#   'symbol':inst[2],
#   'name':inst[3],
#   'expiry':inst[4],
#   'lot_size':inst[5]}
# ]
# print(inst)

