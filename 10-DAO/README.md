# *Blockchain*
## UNISA Spring 26 (based on code from Spring 25) ##

## A Simple DAO (Distributed Autonomous Organization) ##

This contains a simple implementation of a DAO.
The DAO mints and owns a certain number of *B26Unisa* tokens that are sold in exchange for Algos.
The DAO is governed by three governors that initially coincide with the three founders of the DAO and each is given one distinct token during the opting in. The tokens are called *B26-Gov0, B26-Gov1, B26-Gov2* and can be exchanged over the blockchain and the transfer carries over the governor privilege.

We have the following steps:

1. The TEAL code of the DAO is compiled from the the PyTEAL code found in [dao.py](dao.py).
At this stage, the (names of the files containing) the addresses of the three founders are specified 
on the command line. It contains a big switch that executes the relevant of the program.
```python
    program = Cond(
         [Txn.application_id()==Int(0), handle_creation],
         [Txn.on_completion()==OnComplete.OptIn, handle_optin],
         [Txn.on_completion()==OnComplete.CloseOut, handle_closeout],
         [Txn.on_completion()==OnComplete.UpdateApplication, handle_updateapp],
         [Txn.on_completion()==OnComplete.DeleteApplication, handle_deleteapp],
         [Txn.on_completion()==OnComplete.NoOp, handle_noop]
     )

     return compileTeal(program, Mode.Application, version=10)
```

2. The DAO is created by having one of the founder run [createDAO.py](createDAO.py) which constructs and submits
an ``ApplicationCreateTxn``
When the transaction is executed and approved, 
the following fragment of PyTEAL is executed

```python
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

```
This fragments creates the variables that will be used by the DAO.
         ``bcurrentPrice`` holds the price at which the DAO will by the token and 
         ``scurrentPrice`` holds the selluing price  for the token.
         ``IDToken, IDGov0, IDGov1,`` and ``IDGov2`` hold the indices of the
4 assets the DAO will deal with: the actual coin and the three governors coins.
The coins will be created during start-up and the variables are initialized to 0.

The role of the other variables will become clear as we continue the description.

    
3. The DAO is started by running [startDAO.py](startDAO.py) that calls the application 
with a transaction created with ``ApplicationNoOpTxn`` by passing *s* (for start) as a parameter.
The NoOP call is handled by the following switch
```python
     handle_noop=Seq([
         cmd.store(Txn.application_args[0]),
         Cond(
             [cmd.load()==Bytes("s"),handle_start]
             [cmd.load()==Bytes("b"),handle_buy],
         ),
         Approve()])
```
The start of the DAO is handled by the following PyTEAL fragments.

We start by checking if there is payment transaction that transfers 1 Algo to the escrow account 
(whose address is returned by ``Global.current_application_address()``).
The funds are needed to pay the fees of the first transactions.

```python
    If(And(Global.group_size()==Int(2),
         Gtxn[0].type_enum()==TxnType.Payment,
         Gtxn[0].receiver()==Global.current_application_address(),
         Gtxn[0].amount()>=Int(1_000_000),
      )).Then(
```
If the check is passed successfully, then the dApp mints the coins and the 
asset id is stored in the variable ``IDToken``.

```python
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
```
The the dApp moves to create the three governor tokens, one for each founder, whose
ids are stored in the variables ``IDGov1``, ``IDGov2``, ``IDGov3``. 
The id of the asset created by inner transaction is obtained by invoking
``Global.current_application_address()``
The following fragment creates the first such token. 
The others are created in a similar way.

```python
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
```




