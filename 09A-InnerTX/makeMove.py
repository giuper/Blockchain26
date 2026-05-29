import datetime
import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import write_to_file
from algosdk.transaction import ApplicationNoOpTxn
from algosdk.transaction import OnComplete
from algosdk.transaction import StateSchema
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr


def main(MnemFile,CreatorAddFile,idx,move,algodClient):

    params=algodClient.suggested_params()

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    print(f'{"User address: ":32s}{Addr:s}')
    print(f'{"Calling in: ":32s}{idx:d}')
    print(f'{"Move: ":32s}{move:d}')
    with open(CreatorAddFile,'r') as f:
        CAddr=f.read()
    print(f'{"Creator: ":32s}{CAddr:s}')

    appArgs=[move.to_bytes(8,'big')]
    utx=ApplicationNoOpTxn(sender=Addr,sp=params,index=idx,accounts=[CAddr],app_args=appArgs)
    write_to_file([utx],"TX/move.utx")

    stx=utx.sign(SK)
    write_to_file([stx],"TX/move.stx")

    txId=stx.transaction.get_txid()
    print(f'{"Transaction id:":32s}{txId:s}')
    algodClient.send_transactions([stx])

    confirmedtx=wait_for_confirmation(algodClient,txId,4)
    dumpFile="TX/move.stx"
    print(f'{"Transaction information in:":32s}{dumpFile:s}')
    with open(dumpFile,"w") as f:
        json.dump(confirmedtx["txn"]["txn"],f,indent=4)

    txResponse=algodClient.pending_transaction_info(txId)
    idfromtx=txResponse['txn']['txn']['apid']
    print(f'{"Calling app-id: ":32s}{idfromtx:d}')  

if __name__=='__main__':
    if len(sys.argv)!=5:
        print("usage: python3 "+sys.argv[0]+" <user mnem file> <app index> <move> <creator addr file>")
        exit()
    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    move=int(sys.argv[3])
    CreatorAddFile=sys.argv[4]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    main(MnemFile,CreatorAddFile,index,move,algodClient)
    
    
