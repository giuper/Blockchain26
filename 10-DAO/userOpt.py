import sys, json
from algosdk import logic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationOptInTxn, AssetTransferTxn, calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from daoutilities import DAOTokenName, DAOGovName, getIndexAssets

def main(MnemFile,appIndex,algodClient):

    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print(f'{"User address: ":24s}{Addr:s}')
    print(f'{"OptIn to: ":24s}{index:d}')  

    appAddr=logic.get_application_address(appIndex)
    listIndex=getIndexAssets(appAddr,[DAOTokenName,DAOGovName+"0",DAOGovName+"1",DAOGovName+"2"],algodClient)
    print(f'{"Escrow addr:":24s}{appAddr:s}')
    for idx in listIndex:
    	print(f'{"Asset index:":24s}{idx:d}')

    utx0=ApplicationOptInTxn(sender=Addr,sp=params,index=appIndex,foreign_assets=listIndex)
    listTx=[utx0]
    for idx in listIndex:
    	listTx.append(AssetTransferTxn(sender=Addr,sp=params,receiver=Addr,amt=0,index=idx))
    gid=calculate_group_id(listTx)
    for tx in listTx:
    	tx.group=gid

    listStx=[]
    for tx in listTx:
    	listStx.append(tx.sign(SK))

    txId=algodClient.send_transactions(listStx)
    print(f'{"Transaction id:":24s}{txId:s}')

    confirmed=wait_for_confirmation(algodClient,txId,4)
    dumpFile='TX/userOpt.stx'
    print(f'{"Transaction in:":24s}{dumpFile:s}')
    with open(dumpFile,"w") as f:
        json.dump(confirmed["txn"]["txn"],f,indent=4)

    txResponse=algodClient.pending_transaction_info(txId)


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    main(MnemFile,index,algodClient)
    
    
