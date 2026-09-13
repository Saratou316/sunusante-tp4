"""
TP4, partie 2 — Test non fonctionnel de performance (chapitre 4).

"Est-ce que c'est rapide ?" On ne fait pas ici un vrai test de charge
(outils dédiés : Locust, k6 — hors scope de ce TP), mais un test de
performance minimal ("smoke test") qui échoue si une régression grossière
rend une page anormalement lente.

TODO (TP4) : mesurez le temps de réponse de GET /rendezvous/ avec
time.perf_counter() et vérifiez qu'il reste sous un seuil généreux
(ex. 1 seconde) pour rester fiable même sur une machine chargée.

Comparez avec solution/rendezvous/tests_performance.py une fois terminé.
"""
import time

from django.test import TestCase

SEUIL_SECONDES = 1


class PerformanceFormulaireTest(TestCase):
    def test_formulaire_repond_rapidement(self):
        debut = time.perf_counter()
        reponse = self.client.get("/rendezvous/")
        duree = time.perf_counter() - debut

        self.assertEqual(reponse.status_code, 200)
        self.assertLess(
            duree,
            SEUIL_SECONDES,
            f"GET /rendezvous/ a pris {duree:.3f}s (seuil : {SEUIL_SECONDES}s)",
        )
