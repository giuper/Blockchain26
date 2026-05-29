import sys
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationDeleteTxn, ApplicationClearStateTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def listApp(MnemFile,algodClient):

	SK,Addr=getSKAddr(MnemFile)
	print(f'{"User address: ":32s}{Addr:s}')
	params=algodClient.suggested_params()
	account_info = algodClient.account_info(Addr)
	#print(account_info.keys())

	createdApps=account_info['created-apps']
	for app in createdApps:
		print(f'{"Created app: ":32s}{app['id']:d}')
		r=input("Do you want to remove it? ")
		if (r=='y'):
    			utx=ApplicationDeleteTxn(Addr,params,app['id'])
    			stx=utx.sign(SK)
    			txId=stx.transaction.get_txid()
    			print(f'{"Removing app:":32s}{app['id']:d}')
    			print(f'{"Transaction id:":32s}{txId:s}')
    			algodClient.send_transactions([stx])
    			wait_for_confirmation(algodClient,txId,4)

	optedApps=account_info['apps-local-state']
	for app in optedApps:
		print(f'{"Opted-in app: ":32s}{app['id']:d}')
		r=input("Do you want to remove it? ")
		if (r=='y'):
    			utx=ApplicationClearStateTxn(Addr,params,app['id'])
    			stx=utx.sign(SK)
    			txId=stx.transaction.get_txid()
    			print(f'{"Clearing app:":32s}{app['id']:d}')
    			print(f'{"Transaction id:":32s}{txId:s}')
    			algodClient.send_transactions([stx])
    			wait_for_confirmation(algodClient,txId,4)

if __name__=='__main__':
	if len(sys.argv)!=2:
        	print("usage: python3 "+sys.argv[0]+" <user mnem>")
        	exit()

	MnemFile=sys.argv[1]
	algodClient=algod.AlgodClient(algodToken,algodAddress)
	listApp(MnemFile,algodClient)


