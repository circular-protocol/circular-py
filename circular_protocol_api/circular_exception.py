class CircularException(Exception):
    
    def __init__(self, message):
        self.message = message
        print("ERROR:", message)

    def __str__(self):
        return self.message

class BlockchainNotFoundException(Exception):
        def __init__(self, message):
            self.message = message
            print("WARNING:", message)
    
        def __str__(self):
            return self.message
        
class TokenNotFoundException(Exception):
    
    def __init__(self, message):
        self.message = message
        print("WARNING:", message)

    def __str__(self):
        return self.message
    
