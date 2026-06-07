import sys
from pyteal import *
from daoutilities import DAOTokenName, DAOGovName, DAOTokenUnit, DAOGovUnit, DAOURL

cmd=ScratchVar(TealType.bytes)
amt=ScratchVar(TealType.uint64)

def approval_program(fAddr):

    handle_start=If(And(Global.group_size()==Int(2),
        Gtxn[0].type_enum()==TxnType.Payment,
        Gtxn[0].receiver()==Global.current_application_address(),
        Gtxn[0].amount()>=Int(1_000_000),
     )).Then(
        Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_total: Int(1_000_000),
                TxnField.config_asset_decimals: Int(0),
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
                TxnField.config_asset_unit_name: Bytes(DAOGovUnit),
                TxnField.config_asset_name: Concat(Bytes(DAOGovName),Bytes("0")),
                TxnField.config_asset_url: Bytes(DAOURL),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address()
             }),
             InnerTxnBuilder.Submit(),
             App.globalPut(Bytes("IDGov0"),InnerTxn.created_asset_id()),

             InnerTxnBuilder.Begin(),
             InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_total: Int(1),
                TxnField.config_asset_decimals: Int(0),
                TxnField.config_asset_unit_name: Bytes(DAOGovUnit),
                TxnField.config_asset_name: Concat(Bytes(DAOGovName),Bytes("1")),
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
                TxnField.config_asset_unit_name: Bytes(DAOGovUnit),
                TxnField.config_asset_name: Concat(Bytes(DAOGovName),Bytes("2")),
                TxnField.config_asset_url: Bytes(DAOURL),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address()
             }),
             InnerTxnBuilder.Submit(),
             App.globalPut(Bytes("IDGov2"),InnerTxn.created_asset_id()),

             Approve()])).Else(Reject())

    handle_creation=Seq([
        App.globalPut(Bytes("bproposer"),fAddr[0]),
        App.globalPut(Bytes("sproposer"),fAddr[0]),
        App.globalPut(Bytes("bpprice"),Int(0)),
        App.globalPut(Bytes("spprice"),Int(0)),
        App.globalPut(Bytes("bcurrentPrice"),Int(900_000)),
        App.globalPut(Bytes("scurrentPrice"),Int(1_000_000)),
        App.globalPut(Bytes("IDToken"),Int(0)),
        App.globalPut(Bytes("IDGov0"),Int(0)),
        App.globalPut(Bytes("IDGov1"),Int(0)),
        App.globalPut(Bytes("IDGov2"),Int(0)),
        Approve()])

    handle_optin=Seq([
            Cond(
        [Txn.sender()==fAddr[0],Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: App.globalGet(Bytes("IDGov0"))
             }),
             InnerTxnBuilder.Submit(),
             ])],

        [Txn.sender()==fAddr[1],Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: App.globalGet(Bytes("IDGov1"))
             }),
             InnerTxnBuilder.Submit(),
             ])],

        [Txn.sender()==fAddr[2],Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: App.globalGet(Bytes("IDGov2"))
             }),
             InnerTxnBuilder.Submit(),
             ])],
    	),Approve()])

    handle_optin=If(Txn.sender()==fAddr[2]
        ).Then(Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: Int(1),
                TxnField.xfer_asset: App.globalGet(Bytes("IDGov2"))
             }),
             InnerTxnBuilder.Submit(),
	     Approve()
    	     ])).Else(Approve())

    handle_optin=Approve()
    handle_buy=Seq([
        amt.store(Btoi(Txn.application_args[1])),
        If(And(
            Global.group_size()==Int(2),
            Gtxn[0].type_enum()==TxnType.Payment,
            Gtxn[0].receiver()==Global.current_application_address(),
            Gtxn[0].amount()>=Mul(amt.load(),App.globalGet(Bytes("scurrentPrice")))
        )).Then(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: amt.load(),
                TxnField.xfer_asset: App.globalGet(Bytes("IDToken"))
             }),
             InnerTxnBuilder.Submit(),
             Approve()
        ).Else(Reject())
        ])


    handle_noop=If(Global.group_size()==Int(2)).Then(
        Seq([
            cmd.store(Txn.application_args[0]),
            Cond(
                [cmd.load()==Bytes("s"),handle_start],
                [cmd.load()==Bytes("b"),handle_buy]
            ),
            Approve()
        ])).Else(Reject())


    handle_closeout=Seq([Approve()])
    handle_deleteapp=If(Txn.sender()==fAddr[2]).Then(
	Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
		TxnField.type_enum: TxnType.AssetConfig,
		TxnField.config_asset: App.globalGet(Bytes("IDToken")),
            }),
            InnerTxnBuilder.Submit(),

            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
		TxnField.type_enum: TxnType.AssetConfig,
		TxnField.config_asset: App.globalGet(Bytes("IDGov0")),
            }),
            InnerTxnBuilder.Submit(),

            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
		TxnField.type_enum: TxnType.AssetConfig,
		TxnField.config_asset: App.globalGet(Bytes("IDGov1")),
            }),
            InnerTxnBuilder.Submit(),

            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
		TxnField.type_enum: TxnType.AssetConfig,
		TxnField.config_asset: App.globalGet(Bytes("IDGov2")),
            }),
            InnerTxnBuilder.Submit(),

            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: Int(0),
                TxnField.receiver: Txn.sender(),
		TxnField.close_remainder_to: Txn.sender()
            }),
            InnerTxnBuilder.Submit(),

	    Approve()
	)
    ).Else(Reject())

    handle_updateapp=If(Txn.sender()==fAddr[0]).Then(Approve()).Else(Reject())

    program = Cond(
        [Txn.application_id()==Int(0), handle_creation],
        [Txn.on_completion()==OnComplete.OptIn, handle_optin],
        [Txn.on_completion()==OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion()==OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion()==OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion()==OnComplete.NoOp, handle_noop]
    )

    return compileTeal(program, Mode.Application, version=10)

if __name__=='__main__':
    if len(sys.argv)!=4:
        print("Usage: python",sys.argv[0],"<F0 ADDR file> <F1 ADDR file> <F2 ADDR file>")
        exit()

    fAddr=[]
    for i in range(1,4):
        with open(sys.argv[i]) as f:
            fAddr.append(Addr(f.read()))

    program=approval_program(fAddr)
    with open("dao.teal","w") as f:
        f.write(program)
