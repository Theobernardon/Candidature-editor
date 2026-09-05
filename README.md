# Candidature Editor

Candidature Editor automatise la recherche d'offres, la préparation de candidatures et la conversion de CV HTML en PDF. Le projet s'exécute localement avec Docker et comprend n8n, ses workflows et un service de conversion PDF.

> Les données générées (CV, lettres et PDF) sont enregistrées dans `shared_data`. Ne partagez jamais le fichier `.env` ni vos clés API.

## 1. Installer Docker

1. Téléchargez et installez [Docker Desktop pour Windows](https://www.docker.com/products/docker-desktop/).
2. Pendant l'installation, conservez l'option d'utilisation de WSL 2 si elle est proposée, puis redémarrez Windows si Docker le demande.
3. Lancez Docker Desktop et attendez que son statut indique qu'il est en cours d'exécution.
4. Ouvrez PowerShell et vérifiez l'installation :

   ```powershell
   docker --version
   docker compose version
   ```

Les deux commandes doivent afficher un numéro de version. Docker Desktop doit rester ouvert pour utiliser l'application.

## 2. Démarrer l'environnement

### Préparer la configuration

Ouvrez le fichier `.env` à la racine du projet et vérifiez au minimum les paramètres suivants :

```env
GENERIC_TIMEZONE=Europe/Paris
TZ=Europe/Paris
N8N_DEFAULT_LOCALE=fr

N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=ajouter_un_password
N8N_ENCRYPTION_KEY=ajouter_une_clef

EXECUTIONS_DATA_MAX_AGE=1440

N8N_HOST_PORT=5678
WORKDIR_HOST=C:\chemin\vers\Candidature editor\shared_data
```

Remplacez `WORKDIR_HOST` par le chemin absolu vers le dossier `shared_data` de votre copie du projet. Sous Windows, utilisez des antislashs (`\`). Conservez une valeur unique et secrète pour `N8N_ENCRYPTION_KEY`, ainsi que vos propres identifiants pour `N8N_BASIC_AUTH_USER` et `N8N_BASIC_AUTH_PASSWORD`.

### Lancer les conteneurs

Dans PowerShell, placez-vous à la racine du dépôt, puis lancez :

```powershell
docker compose up -d --build
```

Au premier lancement, Docker télécharge les images et installe Chromium pour le convertisseur PDF ; cette opération peut prendre quelques minutes. n8n importe automatiquement les workflows inclus dans `n8n/workflows`.

Ouvrez ensuite [http://localhost:5678](http://localhost:5678) et remplissez le formulaire de première connexion.

Commandes utiles :

```powershell
# Voir l'état des services
docker compose ps

# Consulter les journaux si n8n ne démarre pas
docker compose logs -f n8n

# Arrêter les services sans effacer les données n8n
docker compose down
```

## 3. Initialiser les tables n8n

Cette étape est obligatoire une seule fois, après le premier démarrage avec un volume n8n vide.

1. Dans n8n, ouvrez le workflow **Création des tables**.
2. Cliquez sur **Execute workflow**.
3. Attendez la fin de l'exécution et vérifiez qu'aucun nœud n'est en erreur.

Le workflow crée les tables utilisées par l'application : informations de CV, formations, compétences, expériences, postes recherchés et mémoire des offres. Ne le relancez pas sur une installation déjà initialisée : les tables existent alors déjà. Si vous le désirez, vous pouvez supprimer le orflow de créations d'étapes, vous n'en aurez plus besoin.
Il ne vous restera plus que remplir les tables avec les informations nécessaires. À l'édition du CV et à la recherche de jobs.

## 4. Configurer les clés API

### Mistral AI

Les workflows de génération utilisent le credential **Mistral Cloud account**.

1. Connectez-vous au [tableau de bord Mistral AI](https://admin.mistral.ai/organization/api-keys), créez une clé API puis copiez-la.
2. Dans n8n, ouvrez **Credentials**, puis le credential **Mistral Cloud account**.
3. Collez la clé dans le champ API key et enregistrez.

![Accès aux clés Mistral](asset/tuto/Mistral%20key.png)

![Enregistrement de la Mistral](asset/tuto/Mistral%20key%20registery.png)

![Copie de la clé Mistral](asset/tuto/Mistral%20key%20copy.png)

### JSearch via RapidAPI

1. Créez un compte sur [RapidAPI](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch), puis souscrivez au plan JSearch adapté à votre usage (En toute logique, le plan gratuit devrait suffire Environ 6 requêtes par jour).
2. Copiez votre clé API RapidAPI. (La partie droit sur le côté peut être sélectionnée avec la souris pour copier coller)
3. Dans n8n, ouvrez le workflow **Job Research**.
4. Ouvrez le nœud de requête JSearch, puis remplacez la valeur de l'en-tête `x-rapidapi-key` par votre clé.
5. Enregistrez le workflow.

![Création du compte RapidAPI](asset/tuto/Créer%20un%20compte%20rapide%20API.png)

![Souscription à JSearch](asset/tuto/Souscrire%20au%20plan%20basique%20de%20JSearch.png)

![Remplacement de la clé JSearch](asset/tuto/Copier,%20collez%20votre%20clé%20API%20JSearch%20Dans%20le%20workflow%20Search%20Job.png)

![Accès au nœud JSearch](asset/tuto/Allez%20dans%20la%20partie%20request%20De%20Search%20Job.png)

![Collez votre clé à pays dans l'emplacement prévu](asset\tuto\Collez%20la%20clé%20API%20à%20l'endroit%20indiqué.png)
Pour activer la recherche planifiée, réglez l'heure du nœud **Schedule Trigger** dans **Job Research**, puis publiez le workflow.

![Réglage de la recherche automatique](asset/tuto/Pour%20activer%20La%20recherche%20automatique%20via%20l'API%20Réglez%20votre%20heure%20De%20recherche%20Puis%20publier%20le%20worflow.png)

## 5. Créer les raccourcis Bureau

Les outils suivants sont des formulaires n8n : **Job Manual candidate** pour préparer une candidature à partir d'une offre, et **Convert html to pdf** pour convertir un fichier HTML en PDF. (Ne fonctionne qu'au sein du dossier shared_data)

Pour chacun des deux workflows :

1. Ouvrez le workflow dans n8n et vérifiez qu'il est publié.
2. Cliquez sur le nœud **On form submission**.
3. Copiez l'URL **Production** du formulaire.
4. Sur le Bureau Windows, faites un clic droit, puis choisissez **Nouveau** > **Raccourci**.
5. Collez l'URL dans le champ d'emplacement, cliquez sur **Suivant**, puis donnez-lui le nom du workflow.

![Nœud de formulaire de candidature manuelle](asset/tuto/Allez%20sur%20le%20nœud%20De%20formulaire%20De%20jobs%20manual%20candidate.png)

![Copie du lien de production](asset/tuto/Copier%20le%20lien%20de%20production%20Du%20formulaire.png)

![Création d'un raccourci Windows](asset/tuto/Dans%20votre%20bureau,%20faites%20clic%20gauche,%20puis%20nouveau,%20puis%20raccourci.png)

Répétez l'opération pour obtenir deux raccourcis nommés :

- `Job Manual candidate`
- `Convert html to pdf`

Pour le convertisseur, indiquez dans le formulaire le chemin du fichier HTML situé dans `shared_data`, le chemin complet À partir du disque Dans un format Windows est supporté. Le PDF est créé dans le même dossier, sous le même nom.

## Utilisation courante

1. Renseignez vos informations, expériences, formations et compétences dans les tables n8n prévues à cet effet.
2. Ajoutez vos critères dans la table **Postes recherchee** et activez **Job Research** pour récupérer des offres automatiquement.
3. Ouvrez le raccourci **Job Manual candidate** pour traiter une offre précise manuellement.
4. Retrouvez les documents produits dans `shared_data`, puis utilisez le raccourci **Convert html to pdf** si nécessaire.  
   (Cela peut s'avérer nécessaire si vous voulez modifier Quelque chose sur le fichier HTML, puis reconvertir le PDF)

## Dépannage

- **n8n est inaccessible** : vérifiez que Docker Desktop fonctionne et exécutez `docker compose ps`.
- **Le port est déjà utilisé** : modifiez `N8N_HOST_PORT` dans `.env`, redémarrez avec `docker compose down` puis `docker compose up -d` et ouvrez le nouveau port.
- **Une génération échoue** : vérifiez le credential Mistral et ses crédits disponibles.
- **La recherche d'offres échoue** : vérifiez la clé RapidAPI, l'abonnement JSearch et la valeur de `x-rapidapi-key` dans **Job Research**.
