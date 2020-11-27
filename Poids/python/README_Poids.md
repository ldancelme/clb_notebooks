Description des scripts pythons
------
* **`DE_Poids.py`** : Nettoyage et Standardisation des données de poids
    - *input* : `Projet IMC v2.xlsx`
    - *output* : `all_data.csv`
* **`isolation_forest_Poids.py`** : *Détection des outliers* : Méthode des forêt d'isolation pour les valeurs de Poids.
* **`lvls_Poids.py`** : Assigne une niveau de priorité à chaque valeur en fonction de leur Application d'Origine.
* **`mean_method.py`** : *Détection des outliers* : Pour chaque point, cherche la moyenne des mois suivant et mois précédent et calcul le % d'écart dans le poids.
* **`mean_method_historique.py`** : Historique des différentes vesrions de l'algorithme des moyennes
* **`mean_method_plot.py`** : Trace le nuage de point faisant apparaitre les outliers repérés par le script 
* **`MAD.py`** : Script explorant la méthode de Median Absolute Deviation pour repèrer les outliers. [Statistics How To : Median Absolute Deviation](https://www.statisticshowto.com/median-absolute-deviation/)
* **`med_count.py`** : Trouve la médiane du nombre de mesures pour les populations suivantes :
    - Tous les patients
    - Patients < 20 ans
    - Patients > 20 ans
* **`README_Taille txt`** : Version .txt de ce README
* **`slope_method.py`** : *Détection des outliers* : Calcul de la pente entre chaque points. Utilisation d'une valeur limite de pente pour détecter les points qui dérivent trop du reste des autres.
* **`stats_poids.py`** : Calcule quelques stats descriptives sur l'ensemble du dataset