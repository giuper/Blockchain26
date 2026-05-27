import sys
import base64
import json
import algosdk.encoding as e
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationOptInTxn, PaymentTxn
from algosdk.transaction import calculate_group_id
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(MnemFile,index,algodClient):

    params=algodClient.suggested_params()

    appAddr=e.encode_address(e.checksum(b'appID'+index.to_bytes(8, 'big')))
    print(f'{"app id:":32s}{index}')
    print(f'{"app Addr:":32s}{appAddr}')
    print(f'{"app Addr from logic:":32s}{logic.get_application_address(index)}')

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK,playerAddr=getSKAddr(MnemFile)
    print(f'{"User address: ":32s}{playerAddr:s}')

    note="Opt in fee"
    payTx=PaymentTxn(playerAddr,params,appAddr,10_000_000,None,note)
    optTx=ApplicationOptInTxn(playerAddr,params,index)
    gid=calculate_group_id([payTx, optTx])

    payTx.group=gid
    with open("TX/PayOpt.utx","w") as f:
        json.dump(payTx.dictify(),f,indent=4)

    optTx.group=gid
    with open("TX/Opt.utx","w") as f:
        json.dump(optTx.dictify(),f,indent=4)

    sPayTx=payTx.sign(SK)
    with open("TX/PayOpt.stx","w") as f:
        json.dump(sPayTx.dictify(),f,indent=4)

    sOptTx=optTx.sign(SK)
    with open("TX/Opt.stx","w") as f:
        json.dump(sOptTx.dictify(),f,indent=4)

    txId=algodClient.send_transactions([sPayTx,sOptTx])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    main(MnemFile,index,algodClient)
    
    
