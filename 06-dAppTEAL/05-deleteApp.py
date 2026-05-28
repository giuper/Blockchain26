import sys
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationDeleteTxn
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def deleteApp(MnemFile,index,algodClient):

    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print(f'{"User address: ":32s}{Addr:s}')
    print(f'{"Deleting: ":32s}{index:d}')

    utx=ApplicationDeleteTxn(Addr,params,index)
    stx=utx.sign(SK)
    txId=stx.transaction.get_txid()
    print(f'{"Transaction id:":32s}{txId:s}')

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


