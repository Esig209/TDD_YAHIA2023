# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import uuid
from datetime import datetime, timedelta

class CompteBancaire:
    def __init__(self, proprietaire, adresse, solde_initial=0, limite_decouvert_quotidien=0):
        self.proprietaire = proprietaire
        self.adresse = adresse
        self.solde = solde_initial
        self.historique = []
        self.limite_decouvert_quotidien = limite_decouvert_quotidien
        self.date_dernier_decouvert = datetime.now()

    def consulter_solde(self):
        return self.solde

    def effectuer_depot(self, montant):
        self.solde += montant
        self._ajouter_transaction(montant)

    def effectuer_retrait(self, montant):
        if self._autoriser_retrait(montant):
            self.solde -= montant
            self._ajouter_transaction(-montant)
            return True
        else:
            return False

    def transfert_d_argent(self, destinataire, montant):
        if self._autoriser_retrait(montant):
            self.solde -= montant
            destinataire.effectuer_depot(montant)
            self._ajouter_transaction(-montant, destinataire.proprietaire)
            return True
        else:
            return False

    def consulter_historique(self):
        return self.historique

    def _ajouter_transaction(self, montant, destinataire=None):
        transaction = {'montant': montant, 'date': datetime.now(), 'destinataire': destinataire}
        self.historique.append(transaction)

    def _autoriser_retrait(self, montant):
        # Vérifier si la limite de découvert quotidien est dépassée
        if montant > 0 or (montant < 0 and self._limite_decouvert_depasse(montant)):
            return True
        else:
            return False

    def _limite_decouvert_depasse(self, montant):
        maintenant = datetime.now()
        # Réinitialiser la limite de découvert tous les 24 heures
        if maintenant - self.date_dernier_decouvert > timedelta(days=1):
            self.solde = max(0, self.solde + self.limite_decouvert_quotidien)
            self.date_dernier_decouvert = maintenant
        # Vérifier si le retrait est autorisé en fonction de la limite de découvert quotidien
        return self.solde + montant < -self.limite_decouvert_quotidien

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
