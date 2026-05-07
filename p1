#!/bin/bash

ACCOUNTDir="./Accounts"
SENDER=${ACCOUNTDir}"/sender"
RECEIVER=${ACCOUNTDir}"/receiver"

TXDir="./TX"
UNSIGNEDTX=${TXDir}"/Pay.utx"
SIGNEDTX=${TXDir}"/Pay.stx"

mkdir -p ${ACCOUNTDir}
mkdir -p ${TXDir}

echo "Creating the sender account"
python createSingle.py ${SENDER}
read
clear -x

echo "Creating the receiver account"
python createSingle.py ${RECEIVER} read
clear -x

echo "Executing a single sender payment transaction"
python payTX.py ${SENDER}.mnem ${RECEIVER}.addr 
read
clear -x

