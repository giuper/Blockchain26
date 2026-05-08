import sys
from algosdk.v2client import algod
from algosdk.transaction import AssetTransferTxn, write_to_file
from utilities import algodAddress, algodToken

TXFolder="TX/"

def step1(pkBob,pkAlice,algodClient,assetIDX):

    params=algodClient.suggested_params()
    txn=AssetTransferTxn(
        sender=pkBob,
        sp=params,
        receiver=pkAlice,
        amt=4,
        index=assetIDX)
    write_to_file([txn],TXFolder+"step1Bob.utx")
    print(txn)
    
if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python "+sys.argv[0]+" <file Bob addr> <file Alice addr> <asset index>")
        exit()

    account1=sys.argv[1]
    account2=sys.argv[2]
    with open(sys.argv[1],'r') as f:
        pkBob=f.read()[:58]
    with open(sys.argv[2],'r') as f:
        pkAlice=f.read()[:58]
    assetIDX=int(sys.argv[3])

    algodClient=algod.AlgodClient(algodToken,algodAddress)
    step1(pkBob,pkAlice,algodClient,assetIDX)
