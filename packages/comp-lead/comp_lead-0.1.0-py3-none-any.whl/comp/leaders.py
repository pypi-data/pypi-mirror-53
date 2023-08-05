class lead:
    def __init__(self):
        self.person = [
            'Bill Gates', 
            'Jeff Bezos', 
            'Elon Musk', 
            'Linus Torvalds', 
            'Richard Hendricks',
            'test'
        ]
 
 
    def printLead(self):
        print('Printing a handful of the most influental tech leaders!')
        for __it__ in self.person:
            print('\t%s ' % __it__)
