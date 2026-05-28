import sys, base64, json
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationOptInTxn, PaymentTxn, calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(MnemFile,index,algodClient):

    print(f'{"Opting in: ":32s}{index:d}')

#compute escrow address for app from its index
    AppAddr=logic.get_application_address(index)
    print(f'{"App Addr:":32s}{AppAddr}')

#extract user sk and addr from Mnem
    SK,Addr=getSKAddr(MnemFile)
    print(f'{"User address: ":32s}{Addr:s}')

    params=algodClient.suggested_params()

#create the two txns
    utxPay=PaymentTxn(sender=Addr,sp=params,receiver=AppAddr,amt=1_000_000,note=b"Paying fee for NIM")
    utxOpt=ApplicationOptInTxn(Addr,params,index)

#compute the gid of the two txns
    gid=calculate_group_id([utxPay,utxOpt])

#add the gid to the two txns
    utxPay.group=gid
    utxOpt.group=gid

#sign the two transactions
    stxPay=utxPay.sign(SK)
    stxOpt=utxOpt.sign(SK)

    txId=algodClient.send_transactions([stxPay,stxOpt])
    confirmedtx=wait_for_confirmation(algodClient,txId,4)
    print("Transaction information:\n{}".format(json.dumps(confirmedtx, indent=4)))


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    main(MnemFile,index,algodClient)


