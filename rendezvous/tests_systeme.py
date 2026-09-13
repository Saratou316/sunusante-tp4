"""
TP4, partie 2 — Test système (chapitre 4).

Un test système exerce l'application ENTIÈRE, de bout en bout, comme le
ferait un utilisateur : formulaire -> soumission -> facture. Contrairement
aux tests unitaires (TP1/TP2) ou aux tests d'intégration vue par vue
(TP3), on ne teste pas ici un composant isolé, mais l'enchaînement complet
à travers plusieurs apps (patients + rendezvous).

TODO (TP4) : écrivez un test qui, dans une seule méthode :
1. crée un patient (Patient.objects.create)
2. affiche le formulaire de prise de rendez-vous (GET /rendezvous/) et
   vérifie que le patient y apparaît
3. soumet une prise de rendez-vous (POST /rendezvous/)
4. consulte la facture du patient (GET /rendezvous/facture/<id>/) et
   vérifie que le total affiché correspond au tarif attendu

Comparez avec solution/rendezvous/tests_systeme.py une fois terminé.
"""
from django.test import TestCase

from patients.models import Patient

from .models import TypeConsultation


class ParcoursCompletRendezVousTest(TestCase):
    def test_parcours_complet_de_la_prise_de_rendez_vous_a_la_facture(self):
        # 1. Créer un patient
        patient = Patient.objects.create(
            nom="Diop",
            prenom="Awa",
            email="awa.diop@example.com",
            est_vip=False,
        )

        # 2. Afficher le formulaire et vérifier que le patient y apparaît
        reponse = self.client.get("/rendezvous/")
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "Awa")
        self.assertContains(reponse, "Diop")

        # 3. Soumettre une prise de rendez-vous (lundi, pas de majoration
        # weekend ; patient non VIP, pas de réduction -> prix = 5000 FCFA)
        reponse = self.client.post(
            "/rendezvous/",
            {
                "patient": patient.id,
                "type_consultation": TypeConsultation.GENERALISTE,
                "date": "2026-09-14",  # lundi
                "notes": "",
            },
        )
        self.assertRedirects(reponse, "/rendezvous/")

        # 4. Consulter la facture et vérifier le total attendu
        reponse = self.client.get(f"/rendezvous/facture/{patient.id}/")
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "5000")
