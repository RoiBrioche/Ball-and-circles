"""Configuration des tests pour pytest"""

import pytest
from unittest.mock import patch, MagicMock

# Ici, vous pouvez ajouter des fixtures communes à plusieurs tests
# Par exemple, des mocks pour pygame ou d'autres dépendances


@pytest.fixture
def mock_pygame():
    """Fixture pour simuler Pygame dans les tests"""
    with patch("pygame.init"), patch("pygame.display.set_mode"), patch("pygame.display.set_caption"), patch(
        "pygame.quit"
    ):
        yield
