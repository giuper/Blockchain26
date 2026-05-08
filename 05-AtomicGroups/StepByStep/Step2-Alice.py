import sys
from algosdk.transaction import AssetTransferTxn, PaymentTxn, retrieve_from_file, write_to_file, calculate_group_id
from utilities import getSKAddr

TXFolder="TX/"

def cgid(fileTxAlice,fileTxBob,fileMnemAlice):

    skAlice,pkAlice=getSKAddr(fileMnemAlice)

    ltxnAlice=retrieve_from_file(fileTxAlice)
    txnAlice=ltxnAlice[0]

    ltxn2=retrieve_from_file(fileTXBob)
    txnBob=ltxn2[0]

    gid=calculate_group_id([txnAlice,txnBob])
    txnAlice.group=gid
    txnBob.group=gid
    write_to_file([txnAlice],TXFolder+"AliceWithGid.utx")
    write_to_file([txnBob],TXFolder+"BibWithGid.utx")

    stxnAlice=txnAlice.sign(skAlice)
    write_to_file([stxnAlice],TXFolder+"AliceWithGid.stx")



if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python "+sys.argv[0]+" <file txAlice> <file txBob> <file mnem Alice>")
        exit()
    cgid(sys.argv[1],sys.argv[2],sys.argv[3])
