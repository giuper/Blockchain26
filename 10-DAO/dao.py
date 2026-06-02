import sys
from pyteal import *
from daoutilities import DAOTokenName, DAOGovName, DAOTokenUnit, DAOGovUnit, DAOURL

cmd=ScratchVar(TealType.bytes)

##handle_deleteapp=If(Or(Txn.sender()==Alice,Txn.sender()==Bob,Txn.sender()==Charlie)).Then(
    ##Seq([
        ##InnerTxnBuilder.Begin(),
        ##InnerTxnBuilder.SetFields({
            ##TxnField.type_enum: TxnType.AssetConfig,
            ##TxnField.config_asset: App.globalGet(Bytes("assetIDGov"))
         ##}),
         ##InnerTxnBuilder.Submit(),
##
         ##InnerTxnBuilder.Begin(),
         ##InnerTxnBuilder.SetFields({
            ##TxnField.type_enum: TxnType.AssetConfig,
            ##TxnField.config_asset: App.globalGet(Bytes("assetIDToken"))
         ##}),
##         InnerTxnBuilder.Submit(),

         ##InnerTxnBuilder.Begin(),
         ##InnerTxnBuilder.SetFields({
            ##TxnField.type_enum: TxnType.Payment,
            ##TxnField.amount: Int(0),
            ##TxnField.receiver: Charlie,
            ##TxnField.close_remainder_to: Charlie,
         ##}),
         ##InnerTxnBuilder.Submit(),
         ##Approve()])).Else(Reject()
##)
##
	
def handle_start():
    h_start=If(And(Global.group_size()==Int(2),
        Gtxn[0].type_enum()==TxnType.Payment,
        Gtxn[0].receiver()==Global.current_application_address(),
        Gtxn[0].amount()>=Int(500_000),
     )).Then(
        Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_total: Int(1_000_000),
                TxnField.config_asset_decimals: Int(3),
                TxnField.config_asset_name: Bytes(DAOTokenName),
                TxnField.config_asset_unit_name: Bytes(DAOTokenUnit),
                TxnField.config_asset_url: Bytes(DAOURL),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address()
             }),
             InnerTxnBuilder.Submit(),
             App.globalPut(Bytes("IDToken"),InnerTxn.created_asset_id()),

             InnerTxnBuilder.Begin(),
             InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_total: Int(1),
                TxnField.config_asset_decimals: Int(0),
                TxnField.config_asset_unit_name: Concat(Bytes(DAOGovName),Bytes("1")),
                TxnField.config_asset_name: Bytes(DAOGovUnit),
                TxnField.config_asset_url: Bytes(DAOURL),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address()
             }),
             InnerTxnBuilder.Submit(),
             App.globalPut(Bytes("IDGov1"),InnerTxn.created_asset_id()),

             InnerTxnBuilder.Begin(),
             InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_total: Int(1),
                TxnField.config_asset_decimals: Int(0),
                TxnField.config_asset_unit_name: Concat(Bytes(DAOGovName),Bytes("2")),
                TxnField.config_asset_name: Bytes(DAOGovUnit),
                TxnField.config_asset_url: Bytes(DAOURL),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address()
             }),
             InnerTxnBuilder.Submit(),
             App.globalPut(Bytes("IDGov2"),InnerTxn.created_asset_id()),

             InnerTxnBuilder.Begin(),
             InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_total: Int(1),
                TxnField.config_asset_decimals: Int(0),
                TxnField.config_asset_unit_name: Concat(Bytes(DAOGovName),Bytes("3")),
                TxnField.config_asset_name: Bytes(DAOGovUnit),
                TxnField.config_asset_url: Bytes(DAOURL),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address()
             }),
             InnerTxnBuilder.Submit(),
             App.globalPut(Bytes("IDGov3"),InnerTxn.created_asset_id()),

             Approve()])).Else(Reject())

    return h_start

def approval_program(Alice,Bob,Charlie):

    handle_creation=Seq([
        App.globalPut(Bytes("bproposer"),Alice),
        App.globalPut(Bytes("sproposer"),Alice),
        App.globalPut(Bytes("bpprice"),Int(0)),
        App.globalPut(Bytes("spprice"),Int(0)),
        App.globalPut(Bytes("bcurrentPrice"),Int(900_000)),
        App.globalPut(Bytes("scurrentPrice"),Int(1_000_000)),
        App.globalPut(Bytes("IDToken"),Int(0)),
        App.globalPut(Bytes("IDGov1"),Int(0)),
        App.globalPut(Bytes("IDGov2"),Int(0)),
        App.globalPut(Bytes("IDGov3"),Int(0)),
        Approve()])

    handle_optin=Cond(
        [Txn.sender()==Alice,Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: App.globalGet(Bytes("IDGov1"))
             }),
             InnerTxnBuilder.Submit(),
             Approve()])],
        [Txn.sender()==Bob,Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: App.globalGet(Bytes("IDGov2"))
             }),
             InnerTxnBuilder.Submit(),
             Approve()])],
        [Txn.sender()==Charlie,Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: App.globalGet(Bytes("IDGov3"))
             }),
             InnerTxnBuilder.Submit(),
             Approve()])],
    	)

    handle_closeout=Seq([Approve()])

    handle_noop=Seq([
        cmd.store(Txn.application_args[0]),
        Cond(
            #[cmd.load()==Bytes("sp"),handle_price("s")],
            #[cmd.load()==Bytes("bp"),handle_price("b")],
            #[cmd.load()==Bytes("b"),handle_buy],
            [cmd.load()==Bytes("s"),handle_start()],)
        ,Approve()])

    handle_deleteapp=If(Txn.sender()==Charlie).Then(Approve()).Else(Reject())

    program = Cond(
        [Txn.application_id()==Int(0), handle_creation],
        [Txn.on_completion()==OnComplete.OptIn, handle_optin],
        [Txn.on_completion()==OnComplete.CloseOut, handle_closeout],
        #[Txn.on_completion()==OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion()==OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion()==OnComplete.NoOp, handle_noop]
    )

    return compileTeal(program, Mode.Application, version=5)

if __name__=='__main__':
    if len(sys.argv)!=4:
        print("Usage: python",sys.argv[0],"<Alice ADDR file> <Bob ADDR file> <Charlie ADDR file>")
        exit()

    with open(sys.argv[1]) as f:
        alice=Addr(f.read())
    with open(sys.argv[2]) as f:
        bob=Addr(f.read())
    with open(sys.argv[3]) as f:
        charlie=Addr(f.read())

    program=approval_program(alice,bob,charlie)
    with open("dao.teal","w") as f:
        f.write(program)
