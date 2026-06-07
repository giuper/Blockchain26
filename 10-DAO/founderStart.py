import sys
from algosdk import logic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationNoOpTxn, PaymentTxn, calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from daoutilities import DAOTokenName, DAOGovName, getIndexAssets



def startFounder(mnemFile,indexApp,algodClient):

    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(mnemFile)
    print(f'{"User address:":24s}{Addr:s}')

    appAddr=logic.get_application_address(indexApp)
    listIndex=getIndexAssets(appAddr,[DAOTokenName,DAOGovName+"0",DAOGovName+"1",DAOGovName+"2"],algodClient)
    print(f'{"Escrow addr:":24s}{appAddr:s}')
    for idx in listIndex:
    	print(f'{"Asset index:":24s}{idx:d}')

    #application call to by as indicated by the parameter b
    appArgs=["f".encode()]
    ctxn=ApplicationNoOpTxn(sender=Addr,sp=params,index=indexApp,app_args=appArgs,foreign_assets=listIndex)

    sctxn=ctxn.sign(SK)
    txId=algodClient.send_transactions([sctxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python "+sys.argv[0]+" <mnem> <app index> ")
        exit()

    MnemFile=sys.argv[1]
    indexApp=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    startFounder(MnemFile,indexApp,algodClient)

