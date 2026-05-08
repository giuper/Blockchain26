import sys
from algosdk.v2client import algod
from algosdk.transaction import PaymentTxn, write_to_file
from utilities import algodAddress, algodToken

TXFolder="TX/"

def step1(pkAlice,pkBob,algodClient):

    params=algodClient.suggested_params()

##Alice transfers 1 Algo  to Bob
    txn2=PaymentTxn(
        sender=pkAlice,
        sp=params,
        receiver=pkBob,
        amt=1_000_000)
    write_to_file([txn2],TXFolder+"step1Alice.utx")
    print(txn2)

if __name__=="__main__":
    if (len(sys.argv)!=3):
        print("Usage: python "+sys.argv[0]+" <file Alice addr> <file Bob addr>")
        exit()

    with open(sys.argv[1],'r') as f:
        pkAlice=f.read()[:58]
    with open(sys.argv[2],'r') as f:
        pkBob=f.read()[:58]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    step1(pkAlice,pkBob,algodClient)
