class livre():
    def __init__(self, id, titre, auteur):
        self.id     = id
        self.titre  = titre
        self.auteur = auteur


class utilisateur():
    def __init__(self, matricule, prenom, nom, specialty):
        self.matricule = matricule
        self.prenom    = prenom
        self.nom       = nom
        self.specialty = specialty