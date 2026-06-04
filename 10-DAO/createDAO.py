import sys, json, base64
from algosdk import logic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, OnComplete, StateSchema
from utilities import algodAddress, algodToken, wait_for_confirmation, getSKAddr

def main(creatorMnemFile,approvalFile,algodClient):

    params=algodClient.suggested_params()
    print(f'{"Getting parameters from client":24s}')

    creatorSK,creatorAddr=getSKAddr(creatorMnemFile)
    print(f'{"Creator address: ":24s}{creatorAddr:s}')


    # global schema
    # 8 integers and 2 strings
    globalSchema=StateSchema(8,2)

    # no user local variables
    localSchema=StateSchema(0,0)

    print(f'{"Compiling clear:":24s}{"TEAL/clear.teal":s}')
    with open("TEAL/clear.teal",'r') as f:
        clearProgramSource=f.read()
    compile_response=algodClient.compile(clearProgramSource)
    clearProgram=base64.b64decode(compile_response["result"])

    print(f'{"Compiling approval":24s}')
    with open(approvalFile,'r') as f:
        approvalProgramSource=f.read()
    approvalProgramResponse=algodClient.compile(approvalProgramSource)
    approvalProgram=base64.b64decode(approvalProgramResponse['result'])

    print(f'{"Creating tx":24s}')
    on_complete=OnComplete.NoOpOC.real
    utxn=ApplicationCreateTxn(creatorAddr,params,on_complete, \
                                        approvalProgram,clearProgram, \
                                        globalSchema,localSchema)
    stxn=utxn.sign(creatorSK)

    txId=stxn.transaction.get_txid()
    print(f'{"Transaction id:":24s}{txId:s}')
    algodClient.send_transactions([stxn])

    confirmed=wait_for_confirmation(algodClient,txId,4)
    dumpFile="TX/daoCreation.stx"
    print(f'{"Transaction in:":24s}{dumpFile:s}')
    with open(dumpFile,"w") as f:
        json.dump(confirmed["txn"]["txn"],f,indent=4)

    txResponse=algodClient.pending_transaction_info(txId)
    appId=txResponse['application-index']
    print(f'{"App id:":24s}{appId:d}')
    print(f'{"App address:":24s},{logic.get_application_address(appId):s}')

if __name__=='__main__':
    if len(sys.argv)!=3:
        print("usage: python3 "+sys.argv[0]+" <creator mnem> <approval file>")
        exit()

    creatorMnemFile=sys.argv[1]
    approvalFile=sys.argv[2]
    algodClient=algod.AlgodClient(algodToken,algodAddress)
    main(creatorMnemFile,approvalFile,algodClient)
