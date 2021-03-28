# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

############################################################################### Bibleotheken importieren

import pygame
from pygame.locals import *
from random import randint
from time import sleep
import matplotlib.pyplot as plt

from classes import *

############################################################################### Bilder laden

image = pygame.image.load("/home/fred/Python/jugendforscht/coronaknopfpressed.png")
coronapressed = pygame.transform.scale(image, (image.get_width(), image.get_height()))
image = pygame.image.load("/home/fred/Python/jugendforscht/coronaknopf.png")
corona = pygame.transform.scale(image, (image.get_width(), image.get_height()))

############################################################################### Programm starten

pygame.init()
bigfont = pygame.font.SysFont("", 100)
font = pygame.font.SysFont("", 50)
def textobjekt(text,font):
    textflache = font.render(text,True,(100,100,100))
    return textflache,textflache.get_rect()

############################################################################### Startwerte und Aktionen jedes Menschen definieren

class Mensch():
    def __init__(self, x, y, num):
        self.number = num
        self.x = x
        self.y = y
        self.infected = False
        self.ready = True
        self.infectfull = True
        self.stadium = 0
        self.alive = True
        self.defence = randint(5, 20) / 10
        self.imune = 0
        self.risk = randint(deathrate, 200 - deathrate)
        self.mask = False
        self.maskprio = randint(0, 99)
    def blit(self):
        if not self.alive:
            pygame.draw.rect(screen, (100, 100, 100), (self.x * size, self.y * size, size - size / 4, size - size / 4))
        elif self.imune:
            pygame.draw.rect(screen, (0, 200, 0), (self.x * size, self.y * size, size - size / 4, size - size / 4))
        elif self.infected:
            pygame.draw.rect(screen, (100, 0, 0), (self.x * size, self.y * size, size - size / 4, size - size / 4))
        elif self.risk - deathrate < (100 - deathrate) / 10:
            pygame.draw.rect(screen, (255, 255, 0), (self.x * size, self.y * size, size - size / 4, size - size / 4))
        elif self.mask:
            pygame.draw.rect(screen, (100, 100, 255), (self.x * size, self.y * size, size - size / 4, size - size / 4))
        else:
            pygame.draw.rect(screen, (0, 0, 100), (self.x * size, self.y * size, size - size / 4, size - size / 4))

############################################################################### Kästchen / Blöcke definieren

class Block():
    def __init__(self):
        self.infected = False
        self.duration = 0
        self.defence = 0

############################################################################### Einstellungsregler definieren

class Regler():
    def __init__(self,x,y,lange,text,wert, maxw):
        self.x = x
        self.y = y
        self.lange = lange
        self.rx = x + lange / 2
        self.aktiv = False
        self.text = text
        self.wert = wert
        self.maxwert = maxw * 1.1111111111111111111
    def draw(self):
        pygame.draw.rect(screen,(100,100,100),(self.x,self.y,self.lange,round(self.lange / 10)))
        pygame.draw.rect(screen,(200,200,200),(self.rx,self.y - self.lange / 7 / 8,self.lange / 10,self.lange / 7))
        textgrund,textkasten = textobjekt(self.text + "   " + str(round(self.wert)),font)
        textkasten.center = ((self.x + (self.lange / 2)),self.y - self.lange / 10)
        screen.blit(textgrund, textkasten)
    def get_regler(self):
        self.rx = self.wert * (self.lange / self.maxwert) + self.x
    def get_wert(self):
        self.wert = (self.rx - self.x) * (self.maxwert / self.lange)

############################################################################### Knöpfe definieren

class Button():
    def __init__(self, tag, x, y, image, pressed):
        self.x = x
        self.y = y
        self.tag = tag
        self.image = image
        self.pressedimage = pressed
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pressed = False
        self.cooldown = 50
    def gotpressed(self):
        screen.blit(self.image, (self.x, self.y))
        if self.cooldown > 0:
            self.cooldown -= 1
        else:
            if mouse[0] > self.x and mouse[0] < self.x + self.width:
                if mouse[1] > self.y and mouse[1] < self.y +self.height:
                    screen.blit(self.pressedimage, (self.x, self.y))
                    if click[0]:
                        self.cooldown = 30
                        return True

############################################################################### Algemeine Startwerte definieren

resolution = 150
size = int(1000 / resolution)
speed = 1
population = int(resolution**2)/1.5
deathrate = 1
duration = 10
imuneduration = 20
infectrange = 1
infectodds = 50
vaccineamount = 0
vaccineresearch = 100
vaccineduration = 50
vaccineproduktion = 5
vaccination = 100
maskpriority = 0
maskeffection = 50
days = 1

############################################################################### Programmschleife starten

running = True
while running:
    
    # Fenster öffnen
    
    width = size * resolution + size + 1000
    height = size * resolution + size + 100
    screen = pygame.display.set_mode((width, height))
    
    # alte Werte bei Programmwiederholung zurücksetzten
    
    win = False
    deathcounter = 0
    infectioncounter = 0
    speed = 0
    vaccineresearch = 100
    
    # Regler erstellen
    
    regler = []
    regler.append(Regler(100, 100, 500, "Population", population, resolution**2 * 2))
    regler.append(Regler(100, 250, 500, "Auflösung", resolution , 500))
    regler.append(Regler(100, 400, 500, "Pausierung", speed, 100))
    regler.append(Regler(100, 550, 500, "Sterberate", deathrate, 100))
    regler.append(Regler(1000, 100, 500, "Krankheitsdauer", duration, 100))
    regler.append(Regler(1000, 250, 500, "Impfstoff Entwicklungsdauer", vaccineresearch, 100))
    regler.append(Regler(1000, 400, 500, "Impfstoff Produktionsrate", vaccineproduktion, 100))
    regler.append(Regler(1000, 550, 500, "Impfhaltbarkeit", vaccineduration, 1000))
    regler.append(Regler(100, 700, 500, "Immunitätsdauer", imuneduration, 100))
    regler.append(Regler(1000, 700, 500, "Ansteckwahrscheinlichkeit", infectodds, 100))
    
    # Covid19-Knopf erstellen
    
    buttons = [Button(0, 500, 850, corona, coronapressed)]
    
    ########################################################################### Voreinstellungsschleife starten
    
    finish = False
    while not finish:
        
        # Reglerwerte den Begrenzungen anpassen
        
        regi = 0
        regler[regi].wert = population
        regi += 1
        regler[regi].wert = resolution
        regi += 1
        regler[regi].wert = speed
        regi += 1
        regler[regi].wert = deathrate
        regi += 1
        regler[regi].wert = duration
        regi += 1
        regler[regi].wert = vaccineresearch
        regi += 1
        regler[regi].wert = vaccineproduktion
        regi += 1
        regler[regi].wert = vaccineduration
        regi += 1
        regler[regi].wert = imuneduration
        regi += 1
        regler[regi].wert = infectodds
        
        # Eingaben überprüfen
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                finish = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    finish = True
                if event.key == pygame.K_SPACE:
                    finish = True
        
        # Regler den Eingaben anpassen
        
        for i in regler:
            i.get_regler()
            if i.aktiv == True or mouse[0] > i.rx and mouse[0] < i.rx + i.lange / 10 and mouse[1] > i.y - i.lange / 7 / 8 and mouse [1] < i.y - i.lange / 7 / 8 + i.lange / 7:
                if click[0] == 1:
                    i.aktiv = True
                    i.rx = mouse[0] - i.lange / 10 / 2
                else:
                    i.aktiv = False
            if i.rx > i.x + i.lange - i.lange / 10:
                   i.rx = i.x + i.lange - i.lange / 10
            if i.rx < i.x:
                i.rx = i.x
            i.get_wert()
            i.draw()
        
        # Bildschirm updaten und Werte den Reglern anpassen
        
        pygame.display.update()
        pygame.display.flip()
        screen.fill((0, 0, 0))
        if int(regler[0].wert) == 0:
            regler[0].wert = 1
        if int(regler[1].wert) == 0:
            regler[1].wert = 1
        regler[0].maxwert = resolution**2 * 2
        population = int(regler[0].wert)
        resolution = int(regler[1].wert)
        speed = int(regler[2].wert)
        deathrate = regler[3].wert
        duration = int(regler[4].wert)
        vaccineresearch = int(regler[5].wert)
        vaccineproduktion = int(regler[6].wert)
        vaccineduration = int(regler[7].wert)
        imuneduration = int(regler[8].wert)
        infectodds = int(regler[9].wert)
        
        # Covid19-Einstellungen bei Knopfdruck vornehmen
        
        for i in buttons:
            if i.gotpressed():
                resolution = 150
                size = int(1000 / resolution)
                speed = 0
                population = int(resolution**2)/1.5
                deathrate = 1
                duration = 10
                imuneduration = 20
                infectrange = 1
                infectodds = 50
                vaccineamount = 0
                vaccineresearch = 100
                vaccineduration = 50
                vaccineproduktion = 5
                vaccination = 100
                maskpriority = 0
                maskeffection = 50
    
    ########################################################################### Voreinstellungsschleife beenden
        
    # Programm bei Abbruch beenden
    
    gameover = False
    if not running:
        break
    
    # letzte Werte den Reglern anpassen
    
    if resolution == 0:
        resolution = 1
        gameover = True
    size = int(1000 / resolution)
    screen = pygame.display.set_mode((size * resolution + size + 1000, size * resolution + size))
    
    # Menschen generieren
    
    menschen = []
    for i in range(population):
        menschen.append(Mensch(randint(0,resolution), randint(0,resolution), i))
    menschen[0].infected = True
    
    # Risikogruppen hinzufügen
    
    risks = ([], [])
    for i in menschen:
        risks[0].append(10)
        risks[1].append(i.number)
    
    # Kästchen / Blöcke erstellen
    
    block = []
    for rx in range(resolution + 1):
        block.append([])
        for ry in range(resolution + 1):
            block[rx].append(Block())
    
    # Grafen erstellen
    
    ii = 0
    xx = []
    yy = {}
    yy = [[], [], [], [], []]
    xrange = 100
    ax = [0, 0, 0, 0, 0]
    line = [0, 0, 0, 0, 0]
    label = ["Tode pro Tag", "Neuinfektionen", "Genesungen", "Gesamtinfektionen", "Gesammtimmunität"]
    color = ["black", "r", "g","r", "g"]
    fig, (ax[0],ax[1], ax[2], ax[3], ax[4]) = plt.subplots(5,1,figsize=(5,5))
    for i in range(len(ax)):
        line[i], = ax[i].plot(xx,yy[i], color[i])
        line[i].set_linewidth(3)
        ax[i].set_ylim(0,population)
        ax[i].set_xlim(0,xrange)
        ax[i].grid()
        ax[i].set_ylabel(label[i])
        
    newinfection = 0
    allinfections = 1
    newimune = 0
    allimmun = 0
    deaths = 0
    
    # Live-Einstellungsregler erstellen
    
    regler = []
    regler.append(Regler(size * resolution + 300, 100, 200, "Pausierung", speed, 100))
    regler.append(Regler(size * resolution + 300, 200, 200, "Krankheitsdauer", duration, 100))
    regler.append(Regler(size * resolution + 300, 300, 200, "Impfstoff Entwicklungsdauer", vaccineresearch, 100))
    regler.append(Regler(size * resolution + 300, 400, 200, "Impfstoff Produktionsrate", vaccineproduktion, 100))
    regler.append(Regler(size * resolution + 300, 500, 200, "Impfhaltbarkeit", vaccineduration, 1000))
    regler.append(Regler(size * resolution + 300, 600, 200, "Immunitätsdauer", imuneduration, 100))
    regler.append(Regler(size * resolution + 300, 700, 200, "Ansteckwahrscheinlichkeit", infectodds, 100))
    regler.append(Regler(size * resolution + 300, 800, 200, "Maskenpflicht", maskpriority, 100))
    regler.append(Regler(size * resolution + 300, 900, 200, "Maskeneffektivität", maskeffection, 100))

    ########################################################################### Hauptschleife starten

    gameover = False
    graf = True
    while not gameover:
        days += 1
        
        ####################################################################### Eingaben überprüfen
        pause = speed
        print(pause)
        for timei in range(int(pause) + 1):
            
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        gameover = True
                    if event.key == pygame.K_SPACE:
                        gameover = True
                    if event.key == pygame.K_RETURN:
                        if graf == False:
                            graf = True
                        else:
                            graf = False
            
            ################################################################### Menschen anzeigen
            
            for i in menschen:
                i.blit()
            
            ################################################################### Bildschirm updaten
            
            textgrund,textkasten = textobjekt(str(days),font)
            textkasten.center = (width - 100, 20)
            screen.blit(textgrund, textkasten)
            
            pygame.display.update()
            pygame.display.flip()
                
            screen.fill((0, 0, 0))
            #sleep(speed / 10)
                
            ####################################################################### Live-Regler updaten
            
            # Regler werte den begrenzungen anpassen
            
            regi = 0
            regler[regi].wert = speed
            regi += 1
            regler[regi].wert = duration
            regi += 1
            regler[regi].wert = vaccineresearch
            regi += 1
            regler[regi].wert = vaccineproduktion
            regi += 1
            regler[regi].wert = vaccineduration
            regi += 1
            regler[regi].wert = imuneduration
            regi += 1
            regler[regi].wert = infectodds
            regi += 1
            regler[regi].wert = maskpriority
            regi += 1
            regler[regi].wert = maskeffection
            regi += 1
            
            # regler den Eingaben anpassen
            
            for i in regler:
                i.get_regler()
                if i.aktiv == True or mouse[0] > i.rx and mouse[0] < i.rx + i.lange / 10 and mouse[1] > i.y - i.lange / 7 / 8 and mouse [1] < i.y - i.lange / 7 / 8 + i.lange / 7:
                    if click[0] == 1:
                        i.aktiv = True
                        i.rx = mouse[0] - i.lange / 10 / 2
                    else:
                        i.aktiv = False
                if i.rx > i.x + i.lange - i.lange / 10:
                       i.rx = i.x + i.lange - i.lange / 10
                if i.rx < i.x:
                    i.rx = i.x
                i.get_wert()
                i.draw()
            
            # Werte den Reglern anpassen
            
            regi = 0
            speed = (regler[regi].wert)
            regi += 1
            duration = int(regler[regi].wert)
            regi += 1
            vaccineresearch = int(regler[regi].wert)
            regi += 1
            vaccineproduktion = int(regler[regi].wert)
            regi += 1
            vaccineduration = int(regler[regi].wert)
            regi += 1
            imuneduration = int(regler[regi].wert)
            regi += 1
            infectodds = int(regler[regi].wert)
            regi += 1
            maskpriority = int(regler[regi].wert)
            regi += 1
            maskeffection = int(regler[regi].wert)
            regi += 1
        
        ####################################################################### Grafen updaten
        
        if graf:
            plt.draw()
            plt.pause(0.001)
        
        #move_x = 0
        ii += 1
        xx.append(ii)
        yy[0].append(deaths)
        yy[1].append(newinfection)
        yy[2].append(newimune)
        yy[3].append(allinfections)
        yy[4].append(allimmun)
        for i in range(len(ax)):
            if len(xx) > xrange:
               ax[i].set_xlim(xx[-xrange],xx[-1])
            ax[i].set_ylim(0, max(yy[i]))
            line[i].set_xdata(xx)
            line[i].set_ydata(yy[i])
        #plt.draw()
        #plt.pause(0.001)
        
        newinfection = 0
        newimune = 0
        deaths = 0
        
        ####################################################################### Blöcke updaten
        
        for rx in block:
            for ry in rx:
                ry.duration += 1
                if ry.duration >= duration * ry.defence:
                    ry.infected = False
        
        ####################################################################### impfstoff updaten
        
        # Impfstoff entwickeln
        
        if vaccineresearch > 0:
            vaccineresearch -= 1
        else:
            
            # Impfstoff produzieren
            
            vaccineamount += vaccineproduktion
            if vaccineamount > 0:
                
                # impfen wenn Impfstoff vorhanden
                
                for i in range(vaccineamount):
                    mensch = randint(0, len(menschen) - 1)
                    menschen[mensch].imune = vaccineduration
                    vaccineamount -= 1
                
        ####################################################################### Menschen updaten
        
        allinfections = 0
        allimmun = 0
        win = True
        for i in menschen:
            if i.alive:
                
                # Menschen durch Keime infizieren
                
                if not i.infected and not i.imune:
                    if block[i.x][i.y].infected and randint(0, 100) < infectodds:
                        if not i.mask or randint(0, 100) > maskeffection:
                            i.infected = True
                            i.ready = False
                            i.infectfull = True
                            i.stadium = 0
                            infectioncounter += 1
                            newinfection += 1
                
                # Menschen genesen oder sterben lassen
                
                if i.imune > 0:
                    i.imune -= 1
                    if i.imune < 1:
                        i.imune = 0
                if i.imune:
                    allimmun += 1
                if i.infected:
                    allinfections += 1
                    win = False
                    i.stadium += 1
                    if i.stadium >= duration * i.defence:
                        if randint(0, i.risk) >= deathrate:
                            i.infected = False
                            i.imune = imuneduration + randint(-imuneduration, imuneduration) / 20
                            newimune += 1
                        else:
                            deathcounter += 1
                            i.alive = False
                            deaths += 1
                
                # Menschen Keime verbreiten lassen
                
                if i.infected and i.ready and i.infectfull:
                    for rx in range(-infectrange, infectrange + 1):
                        if i.x + rx > 0 and i.x + rx < resolution:
                            for ry in range(-infectrange, infectrange + 1):
                                if not i.mask or randint(0, 100) > maskeffection:
                                    if i.y + ry > 0 and i.y + ry < resolution:
                                        block[i.x + rx][i.y + ry].infected = True
                                        block[i.x + rx][i.y + ry].duration = i.stadium
                                        block[i.x + rx][i.y + ry].defence = i.defence
                                        i.infectfull = False
                
                # Menschen Masken aufsetzen lassen
                
                if i.maskprio < maskpriority:
                    i.mask = True
                else:
                    i.mask = False
                i.ready = True
        
        ####################################################################### Bildschirm und algemeine werte updaten
        
        # Virus ausrottung überprüfen
        
        if win:
            print(allinfections)
            gameover = True
    
    ########################################################################### Hauptschleife beenden
    
    if not running:
        break
    
    ########################################################################### Endbildschirm anzeigen
    graf = True
    for i in range(len(ax)):
        ax[i].set_xlim(0, xx[-1])
    finish = False
    while not finish:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                finish = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    running = False
                    finish = True
                if event.key == pygame.K_SPACE:
                    finish = True
                if event.key == pygame.K_RETURN:
                    if graf == False:
                        graf = True
                    else:
                        graf = False
        
        # Todeszahlen anzeigen
        
        if win:
            textgrund,textkasten = textobjekt("Das Virus ist ausgerottet",bigfont)
            textkasten.center = (size * resolution / 2, 300)
            screen.blit(textgrund, textkasten)
        else:
            textgrund,textkasten = textobjekt("Abgebrochen",bigfont)
            textkasten.center = (size * resolution / 2, 300)
            screen.blit(textgrund, textkasten)
        textgrund,textkasten = textobjekt("Es sind "+str(deathcounter)+" von "+str(population)+" Menschen gestorben",font)
        textkasten.center = (size * resolution / 2, 500)
        screen.blit(textgrund, textkasten)
        
        if graf:
            plt.draw()
            plt.pause(0.001)
        
        pygame.display.update()

        pygame.display.flip()
        
        # zum anfang der Programmschleife zurückgehen
        
############################################################################### Programm bei schließung beenden
    
pygame.quit()