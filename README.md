# Pygame Circles Breaker


Simulation Pygame d’une balle qui rebondit et traverse des cercles avec une ouverture.  

La balle casse un cercle lorsqu’elle le franchit via son ouverture.


## Installation


Il est recommandé d’utiliser un **environnement virtuel** pour isoler les dépendances du projet.


### Créer un environnement virtuel


```bash

python -m venv .venv

````


### Activer l’environnement


* **Windows (PowerShell)** :


```powershell

.venv\Scripts\Activate

```


* **macOS / Linux (bash/zsh)** :


```bash

source .venv/bin/activate

```


### Installer les dépendances


```bash

pip install -r requirements.txt

```


## Lancer le projet


```bash

python main.py

```


## 🧪 Tests

Le projet inclut des tests unitaires pour s'assurer du bon fonctionnement du code.

### Prérequis

- Python 3.8+
- pip

### Installation des dépendances de test

```bash
pip install -r requirements-dev.txt
```

### Exécution des tests
Pour lancer tous les tests :
```bash
python -m pytest tests/ -v
```

Pour voir la couverture de code :

```bash
python -m pytest --cov=. tests/
```