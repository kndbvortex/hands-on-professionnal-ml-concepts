# AI Observability - Monitoring & Debugging LLMs in Production

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![Arize Phoenix](https://img.shields.io/badge/Phoenix-22.0.0-orange?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat-square&logo=openai&logoColor=white)
![Google AI](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square&logo=google&logoColor=white)

> Projet personnel de suivi de la formation LinkedIn Learning sur l'observabilité des LLMs en production. Ce repo documente mon apprentissage et contient mes expérimentations avec Phoenix, Langfuse et d'autres outils de monitoring LLM.

**Lien formation:** [AI Observability: Monitoring and Debugging LLMs in Production](https://www.linkedin.com/learning/ai-observability-monitoring-and-debugging-llms-in-production)
**Plan d'adoption:** [Guide 30 jours](https://www.linkedin.com/learning/ai-observability-monitoring-and-debugging-llms-in-production/articles/next-steps-a-30-day-adoption-plan?autoSkip=true&resume=false&u=2245297)

---

## Pourquoi ce projet ?

Quand on déploie des applications utilisant des LLMs en production, on se retrouve vite face à des questions difficiles :
- Est-ce que mon modèle hallucine ?
- Pourquoi cette requête a pris 10 secondes ?
- Combien je dépense réellement en tokens ?
- Comment savoir si la qualité des réponses se dégrade avec le temps ?

Cette formation m'a permis de mettre en place des outils concrets pour répondre à ces questions. Phoenix d'Arize est l'outil principal utilisé, complété par Langfuse pour certains aspects.

## Ce que j'ai appris

Le projet couvre plusieurs aspects de l'observabilité des LLMs :

| Concept | Ce que ça résout | Notebook |
|---------|------------------|----------|
| **Hallucination Detection** | Détecter quand le modèle invente des informations | `01_hallunication.ipynb` |
| **Drift Monitoring** | Surveiller si les performances se dégradent dans le temps | `drift.ipynb` |
| **Nested Spans** | Tracer des workflows LLM complexes avec plusieurs appels | `03_03_nested_spans.ipynb` |
| **Feedback Scores** | Collecter et analyser les retours utilisateurs | `03_04_feedback_scores.ipynb` |
| **Phoenix Traces** | Instrumenter complètement une application LLM | `04_02_phoneix_traces.ipynb` |
| **Automatic Evaluation** | Valider automatiquement la qualité des réponses | `04_03_phoenix_evaluator.ipynb` |
| **Trace Slicing** | Analyser des sous-ensembles de traces pour déboguer | `04_04_slice_trace.ipynb` |
| **SDK Instrumentation** | Intégrer l'observabilité directement dans le code | `sdk_instrumentation.ipynb` |

---

## Stack technique

### Outils principaux

**Arize Phoenix (v22.0.0)** - L'outil central du projet
- Interface web pour visualiser les traces
- Évaluateurs automatiques pour la qualité
- Détection d'anomalies et de drift
- Support OpenTelemetry pour l'instrumentation

**Langfuse (v5.2.0)** - Complément pour certains cas d'usage
- Suivi des coûts et analytics
- Gestion des versions de prompts
- Collecte de feedback

### Modèles utilisés

- **OpenAI GPT-3.5/4** pour les tests de génération
- **Google Gemini** pour les tests multimodaux
- **LangChain** pour orchestrer les appels

### Environnement

- Python 3.12+
- Jupyter pour les notebooks
- Pandas pour la manipulation de données
- GraphQL pour l'API Phoenix

---

## Structure du projet

```
AI Observability/
├── README.md                           # Ce fichier
├── test_phoenix.py                     # Script pour lancer Phoenix rapidement
│
├── Notebooks d'apprentissage
│   ├── 01_hallunication.ipynb         # Détection d'hallucinations
│   ├── drift.ipynb                     # Monitoring de drift
│   ├── sdk_instrumentation.ipynb      # Instrumentation avec le SDK
│   ├── 03_03_nested_spans.ipynb       # Traces hiérarchiques
│   ├── 03_04_feedback_scores.ipynb    # Gestion du feedback
│   ├── 04_02_phoneix_traces.ipynb     # Traces Phoenix avancées
│   ├── 04_03_phoenix_evaluator.ipynb  # Évaluateurs automatiques
│   └── 04_04_slice_trace.ipynb        # Analyse de traces
│
├── Résultats d'évaluation
│   ├── final_result.csv                # Résultats finaux
│   └── shopbot_eval_results.csv       # Éval du Shopbot
│
└── shared/
    ├── shopbot_agent.py                # Agent conversationnel exemple
    └── shopbot_config.py               # Config de l'agent
```

---

## Installation et setup

### Prérequis

Vous avez besoin de Python 3.12 minimum. J'utilise `uv` comme gestionnaire de paquets mais `pip` fonctionne aussi.

```bash
python --version  # Vérifier la version
```

### Installation

Les dépendances sont gérées au niveau du projet parent dans `pyproject.toml`:

```bash
# Depuis la racine du projet
uv sync
```

### Configuration des API keys

Créez un fichier `.env` à la racine avec vos clés:

```env
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
```

### Lancer Phoenix

Phoenix est l'interface web principale pour visualiser les traces:

```bash
# Option simple
python "AI Observability/test_phoenix.py"

# Ou depuis un notebook
import phoenix as px
session = px.launch_app()
print(session.url)  # Par défaut: http://localhost:6006
```

### Explorer les notebooks

```bash
jupyter lab
# Puis naviguer vers AI Observability/
```

---

## Exemple concret : Shopbot

Le dossier `shared/` contient un agent conversationnel pour un e-commerce fictif. C'est l'exemple utilisé dans la formation pour montrer comment instrumenter une vraie application.

### Ce que fait le Shopbot

- Répond aux questions sur des produits
- Aide au suivi de commandes
- Fait des recommandations personnalisées

### Métriques suivies

| Métrique | Pourquoi c'est important | Objectif |
|----------|-------------------------|----------|
| **Latence** | Temps de réponse ressenti par l'utilisateur | < 2s |
| **Tokens** | Impact direct sur les coûts | Minimiser |
| **Quality Score** | Pertinence de la réponse | > 0.8 |
| **Hallucination Rate** | Fiabilité des informations | < 5% |
| **Satisfaction** | Retour utilisateur | > 4/5 |

Les fichiers CSV contiennent des résultats d'évaluation réels après avoir fait tourner l'agent.

---

## Problèmes rencontrés et solutions

### Erreur GraphQL avec Phoenix

**Problème:**
```
CustomGraphQLEnumType.parse_value() takes 2 positional arguments but 3 were given
```

C'était un conflit de version entre `graphql-core` 3.2.14 et Phoenix 14.6.0. Phoenix utilisait l'ancienne signature de la méthode.

**Solution:** Upgrade vers Phoenix 22.0.0 qui supporte `graphql-core` 3.3+. Les versions sont maintenant fixées dans `pyproject.toml`.

### Warning ipywidgets dans les notebooks

**Problème:**
```
TqdmWarning: IProgress not found. Please update jupyter and ipywidgets.
```

Les barres de progression tqdm ne s'affichaient pas correctement dans Jupyter.

**Solution:** Ajout de `ipywidgets>=8.1.0` aux dépendances.

### Port déjà utilisé

**Problème:**
```
Failed to bind to address 127.0.0.1:4317
```

Phoenix était déjà lancé dans un autre terminal.

**Solution:**
```bash
# Tuer les processus Phoenix
lsof -ti:4317 | xargs kill -9
lsof -ti:6006 | xargs kill -9
```

---

## Ressources utiles

### Documentation

- [Phoenix Docs](https://docs.arize.com/phoenix/) - Doc officielle complète
- [Langfuse Docs](https://langfuse.com/docs) - Guide Langfuse
- [OpenAI Platform](https://platform.openai.com/docs) - Référence API OpenAI
- [Google AI Studio](https://ai.google.dev/) - Docs Gemini

### Formation

- [Formation complète sur LinkedIn Learning](https://www.linkedin.com/learning/ai-observability-monitoring-and-debugging-llms-in-production)
- [Plan d'adoption 30 jours](https://www.linkedin.com/learning/ai-observability-monitoring-and-debugging-llms-in-production/articles/next-steps-a-30-day-adoption-plan?autoSkip=true&resume=false&u=2245297) - Approche progressive recommandée

### Communautés

- [Arize Community Slack](https://arize.com/community) - Aide rapide de la communauté
- [Langfuse Discord](https://discord.gg/langfuse) - Discussions techniques
- [Phoenix sur GitHub](https://github.com/Arize-ai/phoenix) - Code source et issues

---

## Plan d'apprentissage

La formation recommande une approche progressive sur 30 jours. Voici comment j'ai organisé mon apprentissage:

### Semaine 1 - Bases (Jours 1-7)
- Comprendre ce qu'est l'observabilité pour les LLMs
- Installer Phoenix et explorer l'interface
- Travailler sur la détection d'hallucinations
- Comprendre le monitoring de drift

**Notebooks:** `01_hallunication.ipynb`, `drift.ipynb`

### Semaine 2 - Instrumentation (Jours 8-14)
- Apprendre le tracing avec nested spans
- Mettre en place la collecte de feedback
- Instrumenter du code avec le SDK

**Notebooks:** `03_03_nested_spans.ipynb`, `03_04_feedback_scores.ipynb`, `sdk_instrumentation.ipynb`

### Semaine 3 - Techniques avancées (Jours 15-21)
- Maîtriser les traces Phoenix
- Configurer des évaluateurs automatiques
- Utiliser le trace slicing pour déboguer

**Notebooks:** `04_02_phoneix_traces.ipynb`, `04_03_phoenix_evaluator.ipynb`, `04_04_slice_trace.ipynb`

### Semaine 4 - Pratique (Jours 22-30)
- Analyser le Shopbot en détail
- Appliquer les concepts sur un projet perso
- Configurer des alertes
- Optimiser en fonction des métriques

---

## Notes

Ce projet est personnel et fait partie de mon apprentissage du LLMOps. Les notebooks contiennent mes expérimentations et notes. Si vous trouvez des erreurs ou avez des suggestions, n'hésitez pas à ouvrir une issue ou PR.

### Versions actuelles

- Phoenix 22.0.0 avec support GraphQL 3.3
- ipywidgets 8.1.9 pour les notebooks
- OpenAI API 3.57.0
- Google Gemini 2.30.0

Le projet est maintenu à jour avec les dernières versions stables des dépendances.

---

## Licence

Projet éducatif - Code libre d'utilisation pour l'apprentissage.
