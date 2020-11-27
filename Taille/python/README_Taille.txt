Ordre des premières méthodes développée et leur description, données en output et en input :

DE_Taille.py
============ 
| 	input	 : Projet IMC v2.xlsx
| 	desc	 : Prétraitement et nettoyage à partir des données brutes
| 	output : clean_taille.csv
|
|______ stats_taille.py
		===============
	| 	input	: clean_taille.csv 
	| 	desc	: Ajout colonne 'age_at_diag', 
	|			  calcul moyenne et écart-type pour cq patient
	| 	output: mean_std.csv, mean_std_uniq.csv, data_taille.csv, data_taille_yrs.csv
	|
	|______ groups_taille.py
	|		================
	|		input	: mean_std.csv	
	|		desc	: Séparation en groupe seln les intervalles d'age
	|		Boxplot : Taille ~ Intervalles age
	|		output	: boxplot_outliers.png, 
	|		outliers = {	age_inf_0.csv, 
	|						taille_sup_200_age_inf_20.csv, 
	|						taille_sup_250.csv  }
	|	 
	|______ scatter_plots.py
			==============
			input	: mean_std.csv
			desc	: Scatter plots of random patient height distribution
			output	: scatterplots = {scatter01.png, scatter02.png, ...}

Description des scripts python
-------

- dataset_manip.py : Ajout de nouvelles colonnes dataset :
    - 1ère date de saisie de taille
    - Dernière date de saisie de taille
    - Période entre la 1ère et la dernière date
    - Nombre d'observations par patients

- DE_Taille.py :  Nettoyage et Standardisation des données de poids
    - input : Projet IMC v2.xlsx
    - output: clean_taille.csv

- far_outliers_Taille.py : Catégorise en tant que outlier les points 
situés à +ou- x écarts-type de la moyenne

- groups_taille.py : Séparation du dataset en intervalles d'âge, 
Analyse de la distribution par Kernel Density Estimation.

- IQR_method.py : Détection des outliers : 
Détection par la méthode des Inter Quartile Range.

- isolation_forest.py : Détection des outliers : 
Détection par la méthode des Forêts d'Isolation.

- k_mean.py : Clusterisation des données patients puis 
analyses sur clusters (régression linéaire et isolation forest).

- mean_std_taille.py : Calcul de la moyenne et de l'écart-type pour chaque patient.

- mod_zscore.py : Calcul du z-score modifié. 
https://medium.com/analytics-vidhya/anomaly-detection-by-modified-z-score-f8ad6be62bac

- most_observ.py : Retourne les IPPRs des patients avec le plus d'observations.

- outliers_40+.py : Détection des outliers : 
Méthode de détection pour les patients de plus de 40 ans 
dont la taille commence à s'affaisser.

- poly_regression.py : Détection des outliers : 
Régression Polynomiale sur tout le dataset des < 20 ans.

- poly_regression_sm.py : Détection des outliers : 
Régression Polynomiale sur tout le dataset des < 20 ans. (Librairie statsmethods) 

- priority_lvl.py : Assigne une niveau de priorité à 
chaque valeur en fonction de leur Application d'Origine.

- scatter_plots.py : Observation des nuages de point 
de patients aléatoires.

- stats_taille.py : Ajout colonne 'age_at_diag', calcul moyenne 
et écart-type pour chaque patient.

- zscore.py : Détection des outliers : 
Méthode zscore et visualisation graphique des outliers.

- zscore_vs_iforest.py : Comparaison des résultats des méthodes 
z-score et Isolation Forest pour le même patient.
