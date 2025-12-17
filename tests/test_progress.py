import io
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ajout du répertoire parent au chemin Python pour importer le module principal
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import de la fonction à tester
from progress import update_progress


class TestProgressUpdate:
    """Tests pour la fonction update_progress"""

    def test_progress_output(self):
        """Teste que la sortie de la fonction est correctement formatée"""
        # On capture la sortie standard
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            # Appel de la fonction avec des valeurs de test
            update_progress(30, 100)

            # Vérification du format de sortie
            output = mock_stdout.getvalue()
            assert "30/100" in output
            assert "30.0%" in output

    def test_progress_100_percent(self):
        """Teste que la progression à 100% est correctement affichée"""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            update_progress(100, 100)
            output = mock_stdout.getvalue()
            assert "100/100" in output
            assert "100.0%" in output

    def test_progress_zero_division_handling(self):
        """Teste la gestion du cas où total_frames est 0"""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            update_progress(0, 0)
            output = mock_stdout.getvalue()
            # Vérifie que la sortie contient au moins le format attendu
            assert "/0" in output

    def test_progress_with_large_numbers(self):
        """Teste le comportement avec de grands nombres"""
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            update_progress(123456, 1000000)
            output = mock_stdout.getvalue()
            assert "123456/1000000" in output
            assert "12.3%" in output  # Vérifie l'arrondi à une décimale
