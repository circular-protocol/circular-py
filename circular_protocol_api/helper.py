# Author: Danny De Novi
# Last Modified: 2024-09-22
# Purpose: Circular Python SDK

from datetime import datetime
import hashlib
import json
import requests
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.util import sigencode_der
from ecdsa.rfc6979 import generate_k
import circular_protocol_api.circular_exception as ce


def sendRequest(data, nag_function, NAG_URL):
    try:
        url = NAG_URL + nag_function
        headers = {'Content-Type': 'application/json'} 
        body = json.dumps(data)

        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status() 
        return response.json()

    except requests.exceptions.RequestException as e:
        raise ce.CircularException("Error during the request") from e


######## Helper functions ########
## Function to add a leading zero to numbers less than 10
def padNumber(num) -> str:
    return f"{num:02d}"

## Generate Timestamp formatted
def getFormattedTimestamp() -> str:
    now = datetime.now()
    year = now.year
    month = padNumber(now.month)
    day = padNumber(now.day)
    hours = padNumber(now.hour)
    minutes = padNumber(now.minute)
    seconds = padNumber(now.second)
    return f'{year}:{month}:{day}-{hours}:{minutes}:{seconds}'

def signMessage(message, private_key):
    key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
    msgHash = hashlib.sha256(message.encode()).digest()
    
    # Generate a deterministic k value (RFC 6979)
    k = generate_k(
        key.curve.order,                      # Order of the curve
        key.privkey.secret_multiplier,        # Private key multiplier 
        hash_func=hashlib.sha256,             # Hash function
        data=msgHash                          # Data to hash
    )
    # Sign the message using the private key and the deterministic k value
    signature = key.sign_digest(msgHash, sigencode=sigencode_der, k=k)
    print("signature", signature.hex())
    return signature.hex()

## Verify Message Signature
def verifySignature(publicKey, message, signature):
    key = VerifyingKey.from_string(bytes.fromhex(publicKey), curve=SECP256k1)
    msgHash = hashlib.sha256(message.encode()).digest()
    return key.verify(signature, msgHash)

## Generate Hash
def getPublicKey(privateKey):
    key = SigningKey.from_string(bytes.fromhex(privateKey), curve=SECP256k1)
    return key.get_verifying_key().to_string().hex()

## String to Hex
def stringToHex(string):
    return string.encode().hex()

## Hex to String
def hexToString(hexString):
    return bytes.fromhex(hexString).decode()

def hexFix(word) -> str:
    if isinstance(word, int):
        word = hex(word)
    if isinstance(word, str):
        if word.startswith('0x'):
            word = word[2:]
        return word
    return ''

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()


######## NODES SETTINGS ########    
def setParameter(parameterName, value, NAG_URL):
    data = {
        'Name': parameterName,
        'Value': value
    }

    url = NAG_URL + 'Circular_SetParameter'   
    headers = {
        'Content-Type': 'application/json',
    }

    body = json.dumps(data)

    try:
        response = requests.post(url, headers=headers, data=body)
        return response
    except requests.exceptions.RequestException as e:
        print('Error: ' + e)


