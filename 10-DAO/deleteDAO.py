import sys
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationDeleteTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr
from daoutilities import DAOTokenName,DAOGovName
def getIndexAssets(creatorAddr,assetNames,algodClient):

    accountInfo=algodClient.account_info(creatorAddr)
    noca=len(accountInfo['created-assets'])
    listIndex=[]
    if noca==0:
        return listIndex
    for asset in accountInfo['created-assets']:
        if (asset['params']['name'] in assetNames):
            listIndex.append(asset['index'])
    return listIndex

def deleteApp(MnemFile,appIndex,algodClient):

    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print(f'{"User address:":24s}{Addr:s}')
    print(f'{"Deleting:":24s}{appIndex:d}')
    print(f'{"Looking for:":24s}{DAOTokenName:s}')
    print(f'{"":24s}{DAOGovName+"0":s}')
    print(f'{"":24s}{DAOGovName+"1":s}')
    print(f'{"":24s}{DAOGovName+"2":s}')

    listIndex=getIndexAssets(Addr,[DAOTokenName,DAOGovName+"0",DAOGovName+"1",DAOGovName+"2"],algodClient)
    print(f'{"Found:":24s},{listIndex[0]:d}')
    print(f'{"Found:":24s},{listIndex[1]:d}')
    print(f'{"Found:":24s},{listIndex[2]:d}')
    print(f'{"Found:":24s},{listIndex[3]:d}')
    return
    utx=ApplicationDeleteTxn(sender=Addr,sp=params,index=appIndex,foreign_assets=listIndex)
    stx=utx.sign(SK)
    txId=stx.transaction.get_txid()
    print(f'{"Transaction id:":24s}{txId:s}')

    algodClient.send_transactions([stx])
    wait_for_confirmation(algodClient,txId,4)


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <creator mnem> <app index>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    deleteApp(MnemFile,index,algodClient)


