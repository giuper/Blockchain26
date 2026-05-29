# *Blockchain*
## UNISA Spring 26 (based on code from Spring 25) ##

## Inner transactions ##

Furthering our NIM implementation on Algorand, let us consider 
one extra feature. Now that players pay to opt-in it seems only fair
that they receive something in return.
Let us then modify our NIM so that each player pays a fee to the
application (not to the creator of the application as in the previous
case) when they optin the app and the winning player receives
some Algo at the end of the game from the application and the remainder goes to the creator. 

Two questions arise:

1. How can the application receive Algo?

    This is very simple as an application is associated to an *escrow account* whose address is
   computed from its index in the following way. 

```python
    import algosdk.encoding as e
    appAddr=e.encode_address(e.checksum(b'appID'+index.to_bytes(8, 'big')))
```
Let us go deeper into this. 
The ```algosdk.encoding.checksum```
function calculates the SHA-512 of a given byte string truncated to 256 bits.
In this case, the byte string hashed is the string ```appID``` followed by the ```index``` encoded as 8 bytes.
The 32-byte string is then passed to ```encode_address``` to construct an address.
The whole process is hidden in the ```logic``` package by the following call

```python
    from algosdk import logic
    appAddr=logic.get_application_address(index)
```
We modify the PyTEAL source to check that the OptingIn transaction is part of a group of two transactions and the first transaction is a payment transaction of one Algo
to the escrow account of the application

```python
   handle_optin=If(And(Global.group_size()==Int(2),
                        Gtxn[0].type_enum()==TxnType.Payment,
                        Gtxn[0].receiver()==Global.current_application_address(),
                        Gtxn[0].amount()>=Int(1_000_000),
                    )).Then(Approve()).Else(Reject())
```

```Global.current_application_address()```  returns the address of the escrow account of the application.

2. How can the application send out Algo?
    
    We add to the code for ```NoOp``` a check for ```heap==0```.
    In this case the application generate two *inner transactions*
    The first transfers some Algos to the sender of the application call being
    executed (that is, the winner of the game)

```python
             InnerTxnBuilder.Begin(),
             InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: Int(1_500_000),
                TxnField.receiver: Txn.sender()
             }),
             InnerTxnBuilder.Submit(),
```
and the second transaction close the escrow account of the application and sends the curent balance to the creator
```python
    InnerTxnBuilder.Begin(),
    InnerTxnBuilder.SetFields({
       TxnField.type_enum: TxnType.Payment,
       TxnField.amount: Int(0),
       TxnField.close_remainder_to: Dealer
       }),
      InnerTxnBuilder.Submit(),
```

## Recap ##
We now spell out the steps to use the NIM application on Algorand

1. Run the pyTEAL [script](nim.py) to obtain the file ``nim.teal`` The command line requires the (filename containing) the addresses of the two players and the address of the creator of the app.
2. Deploy the application by running the script [01-createApp](../06-dAppTEAL/01-createApp.py) by assing the following two arguments on the command line
    * (the name of the file containing) the mnem of the creator
    * the TEAL approval program (in our case ``nim.teal`` produced at the previous step).
Note that the script returns the application index to be used in subsequent calls.
3. The two players optin the application by running the opt-in [script](../08A-OptInGroups/optin.py) by passing the mnem of the user and the application index.
4. Players alternate in making moves by running [makeMove](./makeMove.py). For each move the user must specify the mnem file, the application index, the move, and the creator addr.
