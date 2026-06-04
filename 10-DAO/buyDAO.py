import sys
from algosdk import logic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationNoOpTxn, PaymentTxn, calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr


def buyCoin(mnemFile,indexApp,nc,price,algodClient):

    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(mnemFile)
    print(f'{"User address:":25s}{Addr:s}')

    #transfer to fund the application
    appAddr=logic.get_application_address(indexApp)
    ptxn=PaymentTxn(Addr,params,appAddr,nc*price)

    #application call to by as indicated by the parameter b
    appArgs=["b".encode(),nc.to_bytes(8,'big')]
    ctxn=ApplicationNoOpTxn(sender=Addr,sp=params,index=indexApp,app_args=appArgs)

    gid=calculate_group_id([ptxn,ctxn])
    ctxn.group=gid
    ptxn.group=gid

    sptxn=ptxn.sign(SK)
    sctxn=ctxn.sign(SK)
    txId=algodClient.send_transactions([sptxn,sctxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)


if __name__=='__main__':
    if len(sys.argv)!=5:
        print("usage: python "+sys.argv[0]+" <mnem> <app index> <number of coin> <price>")
        exit()

    MnemFile=sys.argv[1]
    indexApp=int(sys.argv[2])
    nc=int(sys.argv[3])
    price=int(sys.argv[4])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    buyCoin(MnemFile,indexApp,nc,price,algodClient)

