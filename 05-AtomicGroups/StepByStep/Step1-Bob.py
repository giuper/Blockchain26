import sys
from algosdk.v2client import algod
from algosdk.transaction import AssetTransferTxn, write_to_file
from utilities import algodAddress, algodToken

TXFolder="TX/"

def step1(pk1,pk2,algodClient,assetIDX):

    params=algodClient.suggested_params()
    txn1=AssetTransferTxn(
        sender=pk1,sp=params,receiver=pk2,amt=4,index=assetIDX)
    write_to_file([txn1],TXFolder+"step1A1.utx")

if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python "+sys.argv[0]+" <addr1 sending asset> <addr2 sending algo> <asset index>")
        exit()

    account1=sys.argv[1]
    account2=sys.argv[2]
    with open(account1,'r') as f:
        pk1=f.read()[:58]
    with open(account2,'r') as f:
        pk2=f.read()[:58]
    assetIDX=int(sys.argv[3])

    algodClient=algod.AlgodClient(algodToken,algodAddress)
    step1(pk1,pk2,algodClient,assetIDX)
