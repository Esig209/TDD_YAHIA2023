import unittest # importation du module unittest : permet de faire des tests unitaires
from CompteBancaire import CompteBancaire # importation de la classe CompteBancaire du module BankAccount

class TestCompteBancaire(unittest.TestCase): # création de la classe TestCompteBancaire qui hérite de la classe TestCase du module unittest
    def setUp(self): # méthode setUp : permet de créer un compte avant chaque test
        self.compte = CompteBancaire("Yahia Ben ", "Chemin du Loup 23", solde_initial=1000) # création d'un compte avec un solde initial de 1000

    def test_consulter_solde(self): # test de la méthode consulter_solde
        self.assertEqual(self.compte.consulter_solde(), 1000)   # test si le solde du compte est bien égal à 1000

    def test_effectuer_depot(self): # test de la méthode effectuer_depot
        self.compte.effectuer_depot(500) # dépôt de 500
        self.assertEqual(self.compte.consulter_solde(), 1500) # test si le solde du compte est bien égal à 1500

    def test_effectuer_retrait(self): # test de la méthode effectuer_retrait
        self.compte.effectuer_retrait(200) # retrait de 200
        self.assertEqual(self.compte.consulter_solde(), 800) # test si le solde du compte est bien égal à 800

    def test_transfert_d_argent(self): # test de la méthode transfert_d_argent
        destinataire = CompteBancaire("Jean du Jardin", "Chemin du Grand Berger 23", solde_initial=500) # création d'un compte destinataire
        self.compte.transfert_d_argent(destinataire, 300) # transfert de 300 au destinataire
        self.assertEqual(self.compte.consulter_solde(), 700) # test si le solde du compte est bien égal à 700
        self.assertEqual(destinataire.consulter_solde(), 800) # test si le solde du destinataire est bien égal à 800

    def test_consulter_historique(self): # test de la méthode consulter_historique
        self.compte.effectuer_depot(300) # dépôt de 300
        self.compte.effectuer_retrait(100) # retrait de 100
        historique = self.compte.consulter_historique() # récupération de l'historique
        self.assertEqual(len(historique), 2)     # test si la longueur de l'historique est bien égale à 2
        self.assertEqual(historique[0]['montant'], 300) # test si le montant du dépôt est bien égal à 300
        self.assertEqual(historique[1]['montant'], -100) # test si le montant du retrait est bien égal à -100

    class TestCompteBancaireAvecDecouvert(unittest.TestCase): # création de la classe TestCompteBancaireAvecDecouvert qui hérite de la classe TestCase du module unittest
        def setUp(self):
            self.compte = CompteBancaire("John Doe", "123 Main St", solde_initial=1000, limite_decouvert_quotidien=200) # création d'un compte avec une limite de découvert quotidien de 200

        def test_retrait_autorise_dans_limite_decouvert(self): # test de la méthode effectuer_retrait
            self.assertTrue(self.compte.effectuer_retrait(500)) # test si le retrait de 500 est autorisé

        def test_retrait_autorise_avec_limite_decouvert_quotidien_depassee(self): # test de la méthode effectuer_retrait
            self.compte.effectuer_retrait(300)
            self.assertFalse(self.compte.effectuer_retrait(500)) # test si le retrait de 500 est autorisé

        def test_retrait_autorise_apres_reinitialisation_limite_decouvert(self): # test de la méthode effectuer_retrait
            self.compte.effectuer_retrait(300)
            # Attendre plus de 24 heures pour réinitialiser la limite de découvert quotidien
            self.compte.date_dernier_decouvert = datetime.now() - timedelta(days=2) # réinitialisation de la date du dernier découvert
            self.assertTrue(self.compte.effectuer_retrait(500)) # test si le retrait de 500 est autorisé

if __name__ == '__main__':
    unittest.main()
