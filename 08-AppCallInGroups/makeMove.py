import sys
import json
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import PaymentTxn, ApplicationNoOpTxn, calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr


def makeMove(MnemFile,DealerFile,index,move,algodClient):

    params=algodClient.suggested_params()
    SK,Addr=getSKAddr(MnemFile)

    with open(DealerFile,'r') as f:
        Dealer=f.read()

    appArgs=[move.to_bytes(8,'big')]
    ptxn=PaymentTxn(sender=Addr,sp=params,receiver=Dealer,amt=1_000_000)
    mtxn=ApplicationNoOpTxn(Addr,params,index,appArgs)
    gid=calculate_group_id([ptxn,mtxn])

    ptxn.group=gid
    sptxn=ptxn.sign(SK)

    mtxn.group=gid
    smtxn=mtxn.sign(SK)
    
    atomic=[sptxn,smtxn]
    atomicDic=[sptxn.dictify(),smtxn.dictify()]
    with open("TX/atomic.stx","w") as f:
            json.dump(atomicDic,f,indent=4)
    print("Transactions saved in file TX/atomic.stx")
    
    txId=algodClient.send_transactions(atomic)
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("Nim on Algorand")
    print("Player with address: ",Addr)
    print("\tMove:              ",move)
    print("\tInstance:          ",index)


if __name__=='__main__':
    if len(sys.argv)!=5:
        print("usage: python3 "+sys.argv[0]+" <player mnem> <dealer addr> <app index> <move>")
        exit()

    MnemFile=sys.argv[1]
    DealerFile=sys.argv[2]
    index=int(sys.argv[3])
    move=int(sys.argv[4])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    makeMove(MnemFile,DealerFile,index,move,algodClient)
    
