class Itemslots:
    MAX_SLOTS = 6

    def __init__(self):
        cur_slots = 0
        itemlist = []

    def addItem(item):
        """ 
            Adds the item object to the current itemslot instance
            Returns True if added, False if error
        """
        if (len(itemlist) >= MAX_SLOTS):
            return False

        ## Need to check whether the item can only be bought once

        cur_slots += 1
        itemlist.append(item)
        return True
        
    def getNumberOfFreeSlots():
        return cur_slots

