# Author: Danny De Novi
# Last Modified: 2024-10-12
# Purpose: Circular Python SDK

import json
import time
import circular_protocol_api.nag_functions as nag
import circular_protocol_api.helper as helper
import hashlib
class CircularProtocolAPI:


    # Private attributes
    __version__ = '1.0.8'
    __NAG_URL__ = 'https://nag.circularlabs.io/NAG.php?cep='
    __NAG_KEY__ = ''
    __lastError__ = ''

    def __init__(self):
        pass

    ######## NAG GETTERS AND SETTERS ########
    def setNAGKey(self, key):
        self.__NAG_KEY__ = key

    def setNAGURL(self, url):
        self.__NAG_URL__ = url

    def getNAGKey(self):
        return self.__NAG_KEY__
    
    def getNAGURL(self):
        return self.__NAG_URL__

    def getError(self):
        return self.__lastError__

    ################################ SMART CONTRACT ########################################


    def testContract(self, blockchain, sender, project):

        """
        Test the execution of a smart contract
        
        Args:
            blockchain: Blockchain name
            sender: Developer's wallet address
            project: Hyper Code Light Smart Contract Project
            
        Returns:
            returns the response of the smart contract
    """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'From': helper.hexFix(sender),
            'Timestamp': helper.getFormattedTimestamp(),
            'Project': helper.hexFix(project),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._TEST_CONTRACT, self.__NAG_URL__)
        
  

    def callContract(self, blockchain, sender, address, request):
        
        """
        Local Smart Contract Call
        
        Args:
            blockchain: Blockchain name
            sender: caller wallet address
            address: contract address
            request: smart contract local endpoint

        Returns:
            returns the response of the smart contract
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'From': helper.hexFix(sender),
            'Address': helper.hexFix(address),
            'Request': helper.stringToHex(request),
            'Timestamp': helper.getFormattedTimestamp(),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._CALL_CONTRACT, self.__NAG_URL__)
        

    ################################ WALLET FUNCTIONS ########################################


    def checkWallet(self, blockchain, address):

        """
        Check if a wallet is registered on the blockchain

        Args:
            blockchain: Blockchain name
            address: Wallet address

        Returns:
            The wallet status in json parsed format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Address': helper.hexFix(address),
            'Version': self.__version__
        }
        
        return helper.sendRequest(data, nag._CHECK_WALLET, self.__NAG_URL__)
    

    def getWallet(self, blockchain, address):
        
        """
        Retrieves a wallet information

        Args:
            blockchain: Blockchain name
            address: Wallet address

        Returns:
            Wallet information in json parsed format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Address': helper.hexFix(address),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_WALLET, self.__NAG_URL__)
    

    def getWalletBalance(self, blockchain, address, asset) :
        
        """
        Retrieves the wallet balance

        Args:
            blockchain: Blockchain name
            address: Wallet address
            asset: Asset name (example CIRX)

        Returns:
            Wallet balance and a description in list format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Address': helper.hexFix(address),
            'Asset': helper.hexFix(asset),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_WALLET_BALANCE, self.__NAG_URL__)
    
    def getWalletNonce(self, blockchain, address):
        """
        Retrieves the wallet nonce
        
        Args:
            blockchain: Blockchain name
            address: Wallet address
            
        Returns:
            Wallet nonce in a dictionary format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Address': helper.hexFix(address),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_WALLET_NONCE, self.__NAG_URL__)
        
        
    def registerWallet(self, blockchain, publicKey):

        """
        Register a wallet on a desired blockchain
        The same wallet can be registered on multiple blockchains

        Args:
            blockchain: Blockchain name
            publicKey: Wallet public key

        Returns:
            Transaction ID
        """
        
        blockchain = helper.hexFix(blockchain)
        publicKey = helper.hexFix(publicKey)

        sender = helper.sha256(publicKey)
        to = sender
        nonce = '0'
        type = 'C_TYPE_REGISTERWALLET'
        payloadObj = {
            "Action" : "CP_REGISTERWALLET",
            "PublicKey": publicKey,
            }
        
        jsonStr = json.dumps(payloadObj) 
        payload = jsonStr.encode().hex()
        timestamp = helper.getFormattedTimestamp()
        dataToHash = blockchain + sender + to + payload + nonce + timestamp


        id = helper.sha256(dataToHash)
        signature = ""

        return self.sendTransaction(id, sender, to, timestamp, type, payload, nonce, signature, blockchain)
    

    ######################################## DOMAINS MANAGEMENT ########################################


    def getDomain(self, blockchain, name):
            
        """
        Resolves the domain name returning the wallet address associated to the domain name

        Args:
            blockchain: Blockchain name
            name: Domain name

        Returns:
            Wallet address associated to the domain name
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Domain': helper.stringToHex(name),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_DOMAIN, self.__NAG_URL__)
        
    ######################################## PARAMETRIC ASSETS MANAGEMENT ########################################


    def getAssetList(self, blockchain):
        
        """
        Retrieves the list of assets minted on a specific blockchain

        Args:
            blockchain: Blockchain name

        Returns:
            List of assets in json parsed format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_ASSET_LIST, self.__NAG_URL__)
        


    def getAsset(self, blockchain, name: str):

        """
        Retrieves the asset descriptor

        Args:
            blockchain: Blockchain name where the asset is minted
            name: Asset name (example CIRX)

        Returns:
            Token descriptor in json parsed format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'AssetName': name,
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_ASSET, self.__NAG_URL__)


    def getAssetSupply(self, blockchain, name):

        """
        Retrieves the asset supply

        Args:
            blockchain: Blockchain name
            name: Asset name (example CIRX)

        Returns:
            Asset supply in a dictionary format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'AssetName': helper.hexFix(name),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_ASSET_SUPPLY, self.__NAG_URL__)
        
    ######################################## VOUCHERS MANAGEMENT ########################################

    def getVoucher(self, blockchain, code: str):

        """
        Retrieves the voucher information

        Args:
            blockchain: Blockchain name
            code: Voucher code

        Returns:
            Voucher information in json parsed format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Code': code, 
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_VOUCHER, self.__NAG_URL__)

      
    ######################################## BLOCKS MANAGEMENT ########################################

    def getBlockRange(self, blockchain, start, end):

        """
        Retrieves all blocks in a specified range
        
        Args:
            blockchain: Blockchain name
            start: Start block number
            end: End block number. If end = 0 then start is the number of blocks from the last one minted
            
        Returns:
            List of blocks in json parsed format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Start': start,
            'End': end,
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_BLOCK_RANGE, self.__NAG_URL__)
        

    def getBlock(self, blockchain, number):
        
        """
        Retrieves a block

        Args:
            blockchain: Blockchain name
            number: Block number

        Returns:
            Block information in json parsed format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'BlockNumber': number,
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_BLOCK, self.__NAG_URL__)
    


    def getBlockCount(self, blockchain):

        """
        Retrieves the number of blocks minted on a blockchain
        
        Args:
            blockchain: Blockchain name
            
        Returns:
            Number of blocks minted
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_BLOCK_COUNT, self.__NAG_URL__)
    
    ######################################## ANALYTICS ########################################


    def getAnalytics(self, blockchain):

        """
        Retrieves the blockchain analytics

        Args:
            blockchain: Blockchain name

        Returns:
            Blockchain analytics in dictionary format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_ANALYTICS, self.__NAG_URL__)
        

    def getBlockchains(self):
        
        """
        Retrieves the list of blockchains available on the network
        """

        data = {}
        
        return helper.sendRequest(data, nag._GET_BLOCKCHAINS, self.__NAG_URL__)

        
    
    ######################################## TRANSACTIONS ########################################


    def getPendingTransaction(self, blockchain, TxID):

        """
        Retrieves a pending transaction
        
        Args:
            blockchain: Blockchain name
            TxID: Transaction ID 

        Returns:
            Transaction information in a dictionary format
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'ID': helper.hexFix(TxID),
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_PENDING_TRANSACTION, self.__NAG_URL__)
        

    def getTransactionByID(self, blockchain, TxID, start, end):

        """
        Searches a transaction by its ID

        Args:
            blockchain: Blockchain name
            TxID: Transaction ID
            Start: Start block number
            End: End block number. If end = 0 then start is the number of blocks from the last one minted

        Returns:
            Transaction information in a dictionary format

        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'ID': helper.hexFix(TxID),
            'Start': start, 
            'End': end,
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_TRANSACTION_BY_ID, self.__NAG_URL__)
        

    def getTransactionByNode(self, blockchain, nodeId, start, end):

        """
        Searches all transactions broadcasted by a specific node

        Args:
            blockchain: Blockchain name
            nodeId: Node ID
            start: Start block number
            end: End block number. If end = 0 then start is the number of blocks from the last one minted

        Returns:
            List of transactions in a list of dictionaries list[dict]

        

        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'NodeID': helper.hexFix(nodeId),
            'Start': start, 
            'End': end, 
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_TRANSACTION_BY_NODE, self.__NAG_URL__)
        

    def getTransactionsByAddress(self, blockchain, address, start, end):
        
        """
        Searches all transactions involving a specified address

        Args:
            blockchain: Blockchain name
            address: Wallet address
            start: Start block number
            end: End block number

        Returns:
            List of transactions in a list of dictionaries list[dict] 
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Address': helper.hexFix(address),
            'Start': start,
            'End': end,
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_TRANSACTIONS_BY_ADDRESS, self.__NAG_URL__)
        

    def getTransactionByDate(self, blockchain, address, startDate, endDate):


        """
        Searches all transactions involving a specified address in a specified timeframe

        Args:
            blockchain: Blockchain name
            address: Wallet address
            startDate: Start date
            endDate: End date

        Returns:
            List of transactions in a list of dictionaries list[dict] 
        """

        data = {
            'Blockchain': helper.hexFix(blockchain),
            'Address': helper.hexFix(address),
            'StartDate': startDate,
            'EndDate': endDate,
            'Version': self.__version__
        }

        return helper.sendRequest(data, nag._GET_TRANSACTION_BY_DATE, self.__NAG_URL__)


    def sendTransaction(self, id, sender, to, timestamp, type, payload, nonce, signature, blockchain):

        """
        Sends a transaction to a desired blockchain

        Args:
            id: Transaction ID
            sender: Wallet address
            to: Destination wallet address
            timestamp: Transaction timestamp
            type: Transaction type
            payload: Transaction payload
            nonce: Transaction nonce
            signature: Transaction signature
            blockchain: Blockchain name

        Returns:
            Transaction ID
        """

        data = {
            'ID': helper.hexFix(id),
            'From': helper.hexFix(sender),
            'To': helper.hexFix(to),
            'Timestamp': timestamp,
            'Type': type,
            'Payload': helper.hexFix(payload),
            'Nonce': nonce,
            'Signature': helper.hexFix(signature),
            'Blockchain': helper.hexFix(blockchain),
            'Version': self.__version__
        } 

        return helper.sendRequest(data, nag._SEND_TRANSACTION, self.__NAG_URL__)
        
    
    def getTransactionOutcome(self, Blockchain, TxID, timeoutSec, intervalSec=10):


        """
        Recursive transaction finality polling

        Args:
            Blockchain: Blockchain name
            TxID: Transaction ID
            intervalSec: Polling interval in seconds
            timeoutSec: Timeout in seconds

        Returns:
            Transaction outcome
        """

        def checkTransaction():
            elapsedTime = time.time() - startTime
            print('Checking transaction...', elapsedTime, timeout)

            if elapsedTime > timeout:
                print('Timeout exceeded')
                raise TimeoutError('Timeout exceeded')

            data = self.getTransactionByID(Blockchain, TxID, 0, 10)
            print('Data received:', data)
            if data['Result'] == 200 and data['Response'] != 'Transaction Not Found' and data['Response']['Status'] != 'Pending':
                return data['Response']
            else:
                print('Transaction not yet confirmed or not found, polling again...')
                time.sleep(interval)
                checkTransaction()

        startTime = helper.datetime.now()
        interval = intervalSec * 1000
        timeout = timeoutSec * 1000

        return checkTransaction()

