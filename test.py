class test:
    def __init__(self, name):
        self.nom = name
    
    def bonjour(self):
        print(f"Salut je m'appelle {self.nom}")

personnage = test("Gabriel")