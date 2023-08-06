class comp:
    def __init__(self):
        self.com = [
            'Google', 
            'Microsoft', 
            'Amazon', 
            'Apple', 
            'Facebook',
            'Pied Piper'
        ]
 
 
    def displayComp(self):
        print('Displaying a handful of the most influental tech companies!')
        for __it__ in self.com:
            print('\t%s ' % __it__)
