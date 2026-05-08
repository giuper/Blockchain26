# *Blockchain*
## UNISA Spring 26 (based on code from Spring 25) ##

## Transaction groups ##

Algorand supports *groups* of transactions  that are *atomic* in the sense that either all transactions of the group are accepted or none is.

To create a group of transactions from a list of transactions ``ListTX``, first obtain the group id:

```python
    gid=transaction.calculate_group_id(ListTX)
```
then, add the group id to each transaction

```python
    txn.group=gid
```
and finally sign each transaction. Transaction could be signed by a single key, by multiple keys or
logically. The transactions need not to be signed by the same address but need to be submitted 
together
```python
    txid=algodClient.send_transactions(signedListTX)
```


### Step by step  ###
Next we discuss an example in which we construct and submitted 
an atomic group of two transactions:

1. Bob sends 4 instances of an ASA to Alice
2. Alice sends 1 Algo to Bob

Script [atomicSwap.py](./atomicSwap.py) takes as input two account addresses and an asset id, and 
submits the group of transactions.

In [folder](./StepByStep) the steps needed to submit a group are implemented in independent scripts.

1. In the [first step of Alice](./StepByStep/Step1-Alice.py), Alice creates a payment transaction for 1 Algo to Bob 
    and writes it in file TX/step1Alice.utx. This is an unsigned transaction.
2. In the [first step of Bob](./StepByStep/Step1-Bob.py), Bob creates an asset transfer transaction for 4 coints to Alice
    and writes it in file TX/step1Bob.utx. This is an unsigned transaction.
3. In the [second step by Alice](./StepByStep/Step2-Alice.py), Alice computes the group id of the two transactions 
        created by the previous two steps, adds to both transactions and signs hers. 
        The two unsigned transactions with group id are in file TX/AliceWithGid.utx and TX/BobWithGid.utx.
        Alice's signed transaction is in file TX/AliceWithGid.stx.
4. In the [third step by Bob](./StepByStep/Step3-Bob.py), Bob signs the transaction found in TX/BobWithGid.utx and stores
        it in TX/BobWithGid.stx.
5. In the [fourth](./StepByStep/Step4.py), the two signed transactions are sent to a node.

