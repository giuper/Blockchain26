import sys
import json
import base64
from algosdk import logic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, OnComplete, StateSchema
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(creatorMnemFile,approvalFile,algodClient):

    creatorSK,creatorAddr=getSKAddr(creatorMnemFile)
    print(f'{"Creator address: ":32s}{creatorAddr:s}')

    # declare application state storage (immutable)
    # define global schema
    global_ints=5
    global_bytes=1
    globalSchema=StateSchema(global_ints,global_bytes)

    # define local schema
    local_ints=3
    local_bytes=1
    localSchema=StateSchema(local_ints,local_bytes)

    print(f'{"Compiling the clear program:":32s}{"TEAL/clear.teal":s}')
    with open("TEAL/clear.teal",'r') as f:
        clearProgramSource=f.read()
    compile_response=algodClient.compile(clearProgramSource)
    clearProgram=base64.b64decode(compile_response["result"])

    print(f'{"Reading approval file:":32s}{approvalFile:s}')
    with open(approvalFile,'r') as f:
        approvalProgramSource=f.read()
    print(f'{"Compiling approval file:":32s}')
    approvalProgramResponse=algodClient.compile(approvalProgramSource)
    approvalProgram=base64.b64decode(approvalProgramResponse['result'])

    approvalProgramAddress=approvalProgramResponse["hash"]
    print(f'{"Hash approval file:":32s}{approvalProgramAddress:s}')

    params=algodClient.suggested_params()
    utx=ApplicationCreateTxn(
        creatorAddr,
        params,
        OnComplete.NoOpOC,
        approval_program=approvalProgram,
        clear_program=clearProgram,
        global_schema=globalSchema,
        local_schema=localSchema,
    )
    stx=utx.sign(creatorSK)

    txId=stx.transaction.get_txid()
    print(f'{"Transaction id:":32s}{txId:s}')
    txId=algodClient.send_transactions([stx])
    confirmed_txn=wait_for_confirmation(algodClient,txId,4)

    txResponse=algodClient.pending_transaction_info(txId)
    appId=txResponse['application-index']
    print(f'{"App id:":32s}{appId:d}');
    appaddr=logic.get_application_address(appId)
    print(f'{"App address:":32s}{appaddr:32}')

    dumpFile="TX/create.stx"
    print(f'{"Transaction information in:":32s}{dumpFile:s}')
    with open(dumpFile,"w") as f:
        json.dump(confirmed_txn["txn"]["txn"],f, indent=4)

if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <creator mnem> <approval file>")
        exit()

    creatorMnemFile=sys.argv[1]
    approvalFile=sys.argv[2]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    main(creatorMnemFile,approvalFile,algodClient)




