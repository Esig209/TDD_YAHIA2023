import unittest # importation du module unittest : permet de faire des tests unitaires
from CompteBancaire import CompteBancaire # importation de la classe CompteBancaire du module BankAccount

class TestCompteBancaire(unittest.TestCase): # création de la classe TestCompteBancaire qui hérite de la classe TestCase du module unittest
    def setUp(self):
        self.compte = CompteBancaire("Yahia Ben ", "Chemin du Loup 23", solde_initial=1000)

    def test_consulter_solde(self):
        self.assertEqual(self.compte.consulter_solde(), 1000)

    def test_effectuer_depot(self):
        self.compte.effectuer_depot(500)
        self.assertEqual(self.compte.consulter_solde(), 1500)

    def test_effectuer_retrait(self):
        self.compte.effectuer_retrait(200)
        self.assertEqual(self.compte.consulter_solde(), 800)

    def test_transfert_d_argent(self):
        destinataire = CompteBancaire("Jean du Jardin", "Chemin du Grand Berger 23", solde_initial=500)
        self.compte.transfert_d_argent(destinataire, 300)
        self.assertEqual(self.compte.consulter_solde(), 700)
        self.assertEqual(destinataire.consulter_solde(), 800)

    def test_consulter_historique(self): # test de la méthode consulter_historique
        self.compte.effectuer_depot(300)
        self.compte.effectuer_retrait(100)
        historique = self.compte.consulter_historique()
        self.assertEqual(len(historique), 2)
        self.assertEqual(historique[0]['montant'], 300)
        self.assertEqual(historique[1]['montant'], -100)

    class TestCompteBancaireAvecDecouvert(unittest.TestCase):
        def setUp(self):
            self.compte = CompteBancaire("John Doe", "123 Main St", solde_initial=1000, limite_decouvert_quotidien=200)

        def test_retrait_autorise_dans_limite_decouvert(self):
            self.assertTrue(self.compte.effectuer_retrait(500))

        def test_retrait_autorise_avec_limite_decouvert_quotidien_depassee(self):
            self.compte.effectuer_retrait(300)
            self.assertFalse(self.compte.effectuer_retrait(500))

        def test_retrait_autorise_apres_reinitialisation_limite_decouvert(self):
            self.compte.effectuer_retrait(300)
            # Attendre plus de 24 heures pour réinitialiser la limite de découvert
            self.compte.date_dernier_decouvert = datetime.now() - timedelta(days=2)
            self.assertTrue(self.compte.effectuer_retrait(500))

if __name__ == '__main__':
    unittest.main()
