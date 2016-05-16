#added a comment

class Manuscript:

    def __init__(self, msid):
        info = msid.split('-')
        self.category = info[0]
        self.number = info[1] + '-' + info[2]
        try:
        	if (info[3] == 'MS'): self.has_MS = True
        except IndexError:
       		self.has_MS = False
