import sys
from algosdk.v2client import algod
from algosdk.transaction import AssetTransferTxn, PaymentTxn, retrieve_from_file, write_to_file
from utilities import getSKAddr

TXFolder="TX/"

def signT(filet,filem):

    skBob,pkBob=getSKAddr(filem)
    ltxn=retrieve_from_file(filet)
    txn=ltxn[0]
    stxn=txn.sign(skBob)
    write_to_file([stxn],TXFolder+"BobWithGid.stx")



if __name__=="__main__":
    if (len(sys.argv)!=3):
        print("Usage: python "+sys.argv[0]+" <file with utx with fid> <file with Bob's mnem>")
        exit()

    filet=sys.argv[1]
    filem=sys.argv[2]
    signT(filet,filem)
