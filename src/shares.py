"""!
@file shares.py
This file contains a task sharing library implementing both shares and queues.

@details Implements a very simple interface for sharing data between multiple tasks.
    
"""
class Share:
    """!
    This class creates a standard shared variable.
    """
    def __init__(self, initial_value=None):
        """!
        Constructs a shared variable.
        @param initial_value    An optional initial value for the shared variable.
        """
        ## Buffer value for shared variable
        self._buffer = initial_value
    
    def write(self, item):
        """!
        Updates the value of the shared variable.
        @param item    The new value for the shared variable.
        """
        ## Buffer value for shared variable
        self._buffer = item
        
    def read(self):
        """!
        Accesses the value of the shared variable.
        @returns    The value of the shared variable.
        """
        return self._buffer

class Queue:
    """!
    This class creates a queue of shared data.
    """
    def __init__(self):
        """!
        Constructs an empty queue of shared values.
        """
        ## Initialisation of empty buffer variable
        self._buffer = []
    
    def put(self, item):
        """!
        This method Adds an item to the end of the queue.
        @param item    The new item to append to the queue.
        """ 
        self._buffer.append(item)
        
    def get(self):
        """!
        Removes the first item from the front of the queue.
        @returns    The value of the item removed.
        """
        return self._buffer.pop(0)
    
    def num_in(self):
        """!
        Finds the number of items in the queue. Call before get().
        @returns    The number of items in the queue.
        """
        return len(self._buffer)