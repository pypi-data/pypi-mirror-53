class lead:
    def __init__(self):
        self.obj = [
            'Bill Gates', 
            'Jeff Bezos', 
            'Elon Musk', 
            'Linus Torvalds',
            'Evan Spiegel',
            'Richard Hendricks'
        ]
 
 
    def displayLead(self):
        print('Displaying a handful of the most influental tech leaders!')
        for __it__ in self.obj:
            print('\t%s ' % __it__)
