import sys
from algosdk import logic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationNoOpTxn, PaymentTxn, calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr


def startApp(mnemFile,appIndex,algodClient):

    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(mnemFile)
    print(f'{"User address:":25s}{Addr:s}')

    #transfer to fund the application
    appAddr=logic.get_application_address(appIndex)
    ptxn=PaymentTxn(Addr,params,appAddr,2_000_000)

    #application call to start as indicated by argument s
    ctxn=ApplicationNoOpTxn(sender=Addr,sp=params,index=appIndex,app_args=["s".encode()],)

    gid=calculate_group_id([ptxn,ctxn])
    ctxn.group=gid
    ptxn.group=gid

    sptxn=ptxn.sign(SK)
    sctxn=ctxn.sign(SK)
    txId=algodClient.send_transactions([sptxn,sctxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python "+sys.argv[0]+" <mnem> <app index> ")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    startApp(MnemFile,index,algodClient)

