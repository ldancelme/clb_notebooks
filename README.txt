DE_Taille.py
============ 
| input	 : Projet IMC v2.xlsx
| desc	 : Prétraitement et nettoyage à partir des 
| output : clean_taille.csv
|
|______ stats_taille.py
	===============
	| input	: clean_taille.csv 
	| desc	: Ajout colonne 'age_at_diag', 
	|	  calcul moyenne et écart-type pour cq patient
	| output: mean_std.csv, mean_std_uniq.csv, data_taille.csv, data_taille_yrs.csv
	|
	|______ groups_taille.py
	|	================
	|	input	: mean_std.csv	
	|	desc	: Séparation en groupe seln les intervalles d'age
	|		  Boxplot : Taille ~ Intervalles age
	|	output	: boxplot_outliers.png, 
	|		  outliers = {	age_inf_0.csv, 
	|				taille_sup_200_age_inf_20.csv, 
	|				taille_sup_250.csv  }
	|	 
	|______ scatter_plt.py
		==============
		input	: mean_std.csv
		desc	: Scatter plots of random patient height distribution
		output	: scatterplots = {scatter01.png, scatter02.png, ...}


https://www.dataquest.io/blog/jupyter-notebook-tutorial/#:~:text=Your%20first%20Jupyter%20Notebook%20will,you%20your%20notebook%20is%20running.