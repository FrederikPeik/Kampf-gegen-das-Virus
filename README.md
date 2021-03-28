# Kampf-gegen-das-Virus

Ein kleines Python Programm, das Ausbreitung und Bekämpfung eines Virus simuliert.

von Jakob Dubischar und Frederik Peik im Rahmen von Jugend forscht 2020/2021

# Installation

Für die Verwendung des Programms wird der Interpreter "Python3" sowie die Bibleotheken "matplotlib" und "Pygame" benötigt

# Verwendung

Bei Programmstart öffnet sich ein Fenster mit verschiedenen Reglern.
Diese können beliebig verschoben werden um unterschiedliche Ergebnisse zu erzielen.
Bei Drücken der Leertaste startet die Simulation.
Wärend der Simulation kann die Ausbreitung des Virus in eiem Raster beobachtet werden.
Außerdem werden zu verschiedenen Werten Graphen erstellt.
Um die Graphen in den Hintergrund zu stellen und die Einstellungen benutzen zu können muss auf das Simulationsfenster geklickt werden während die Entertaste gedrückt gehalten wird.
Durch erneutes Drücken der Entertaste kommen die Graphen wieder in den Vordergrund und werden weiter gezeichnet.
Wird die Leertaste während der Simulation gedrückt, wird die Simulation abgebrochen.
Ansonsten ist die Simulation beendet sobald das Virus ausgerottet.
Dann kann durch erneutes Drücken der Leertaste das Programm neugestartet werden.

# Farb-Legende

Jeder Pixel im Raster stellt einen Menschen dar.
um die unterschiedlichen Eigenschaften erkennen zu können werden sie in verschiedenen Farben angezeigt.

•	Leere Plätze sind schwarz. 

•	Die gesunden nicht-Risiko-Menschen ohne Maske sind blau verfärbt. 

•	Mit Maske sind sie hellblau.

•	Die gelben Menschen sind Risikopersonen. Sie haben eine höhere Sterbewahrscheinlichkeit. 

•	Wenn Menschen mit dem Virus infiziert werden, dann werden sie rot. 

•	Die Toten verfärben sich grau.

•	Geimpfte und immune Menschen werden grün.
