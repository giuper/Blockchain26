import sys, json
from algosdk import logic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationOptInTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from daoutilities import DAOTokenName

def getIndexAsset(creatorAddr,assetName,algodClient):

    accountInfo=algodClient.account_info(creatorAddr)
    noca=len(accountInfo['created-assets'])
    if noca==0:
        return None
    for asset in accountInfo['created-assets']:
        if (asset['params']['name']==assetName):
            return asset['index']
    return None

def main(MnemFile,appIndex,algodClient):

    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print(f'{"User address: ":24s}{Addr:s}')
    print(f'{"OptIn to: ":24s}{index:d}')  

    appAddr=logic.get_application_address(appIndex)
    assetIndex=getIndexAsset(appAddr,DAOTokenName,algodClient)
    print(f'{"Escrow addr:":24s}{appAddr:s}')
    print(f'{"Asset index:":24s}{assetIndex:d}')

    utx0=ApplicationOptInTxn(sender=Addr,sp=params,index=appIndex,foreign_assets=[assetIndex])
    utx1=AssetTransferTxn(sender=Addr,sp=parames,receiver=Addr,amt=0,index=assetIndex)
    gid=calculate_group_id([utx0,utx1])
    
    utx0.group=gid
    utx1.group=gid

    stx0=utx0.sign(SK)
    stx1=utx1.sign(SK)

    txId=stx.transaction.get_txid()
    print(f'{"Transaction id:":24s}{txId:s}')
    algodClient.send_transactions([stx0,stx1])

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
    
    
