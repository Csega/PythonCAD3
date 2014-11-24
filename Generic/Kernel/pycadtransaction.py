class Transaction(object):
    
    def __init__(self, connection):
        
        self._connection = connection
        self._cursor = self._connection.cursor()
        
        
    def _GetCursor(self):
        return self._cursor
    
    Cursor = property(_GetCursor, None, None, "gets the cursor")
    
    
    def Close(self, commit):
        
        if commit == True:
            # commit transaction
            self._connection.commit()
        else:
            # abort transaction
            self._connection.abort()
        # close cursor
        self._cursor.close()
