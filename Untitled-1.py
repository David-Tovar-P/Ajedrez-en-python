# -*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *

pygame.init()
visor = pygame.display.set_mode((560,560))
pygame.display.set_caption("ajedrez")

casilla=[0,0,70,140,210,280,350,420,490,560,999]

ocupadas=[
[0,0,0,0,0,0,0,0,0],#esta linia y el 0 de mas es para kitar el 0 de los indices
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0]
]
cocupadas=[#color de las ocupadas
[0,0,0,0,0,0,0,0,0],#esta linia y el 0 de mas es para kitar el 0 de los indices
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0]
]

class metapieza():
	def __init__(self,x,y,color):
		self.movida = 0
		self.casx=x
		self.casy=y
		self.pos=(casilla[x],casilla[y])
		self.color=color
		self.casposibles=[]
		if self.casx < 9 and self.casy < 9:
			ocupadas[self.casy][self.casx] = self
			cocupadas[self.casy][self.casx] = self.color
	def cambiasilla(self,x,y):
		ocupadas[self.casy][self.casx]=cocupadas[self.casy][self.casx] = 0
		self.__init__(x,y)
		self.movida = 1
	def casillaocupada(self):
		return self.casy,self.casx
	def movlineal(self,movmax=8):
		casi = 0
		oriz = ordr = vrab = vrar = True
		while casi < movmax:
			casi+=1
			if 0 < self.casy <= 8 and 0 < self.casx-casi <= 8 and oriz:
				oriz = cocupadas[self.casy][self.casx-casi] != self.color
				if oriz:
					self.casposibles.append((self.casx-casi,self.casy))
					oriz = cocupadas[self.casy][self.casx-casi] != 3-self.color
			if 0 < self.casy <= 8 and 0 < self.casx+casi <= 8 and ordr:
				ordr = cocupadas[self.casy][self.casx+casi] != self.color
				if ordr:
					self.casposibles.append((self.casx+casi,self.casy))
					ordr = cocupadas[self.casy][self.casx+casi] != 3-self.color				
			if 0 < self.casy-casi <= 8 and 0 < self.casx <= 8 and vrab:		
				vrab = cocupadas[self.casy-casi][self.casx] != self.color
				if vrab:
					self.casposibles.append((self.casx,self.casy-casi))
					vrab = cocupadas[self.casy-casi][self.casx] != 3-self.color
			if 0 < self.casy+casi <= 8 and 0 < self.casx <= 8 and vrar:		
				vrar = cocupadas[self.casy+casi][self.casx] != self.color
				if vrar:
					self.casposibles.append((self.casx,self.casy+casi))
					vrar = cocupadas[self.casy+casi][self.casx] != 3-self.color
		return self.casposibles
		
	def movdiagonal(self,movmax=8):
		casi = 0
		ariz = abdr = ardr = abiz = True
		while casi < movmax:
			casi+=1
			if 0 < self.casy-casi <= 8 and 0 < self.casx-casi <= 8 and ariz:		
				ariz = cocupadas[self.casy-casi][self.casx-casi] != self.color
				if ariz:
					self.casposibles.append((self.casx-casi,self.casy-casi))
					ariz = cocupadas[self.casy-casi][self.casx-casi] != 3-self.color
			if 0 < self.casy+casi <= 8 and 0 < self.casx+casi <= 8 and abdr:		
				abdr = cocupadas[self.casy+casi][self.casx+casi] != self.color
				if abdr:
					self.casposibles.append((self.casx+casi,self.casy+casi))
					abdr = cocupadas[self.casy+casi][self.casx+casi] != 3-self.color
			if 0 < self.casy-casi <= 8 and 0 < self.casx+casi <= 8 and ardr:		
				ardr = cocupadas[self.casy-casi][self.casx+casi] != self.color
				if ardr:
					self.casposibles.append((self.casx+casi,self.casy-casi))
					ardr = cocupadas[self.casy-casi][self.casx+casi] != 3-self.color
			if 0 < self.casy+casi <= 8 and 0 < self.casx-casi <= 8 and abiz:		
				abiz = cocupadas[self.casy+casi][self.casx-casi] != self.color
				if abiz:
					self.casposibles.append((self.casx-casi,self.casy+casi))
					abiz = cocupadas[self.casy+casi][self.casx-casi] != 3-self.color
		return self.casposibles

class metaballo(metapieza):
	def movcaballo(self):
		for x in [-2,-1,1,2]:
			for y in [-(3-abs(x)),3-abs(x)]:
				if 0 < self.casy+y <= 8 and 0 < self.casx+x <= 8:
					if cocupadas[self.casy+y][self.casx+x] == 0 or \
					cocupadas[self.casy+y][self.casx+x] == 3-self.color:
						self.casposibles.append((self.casx+x,self.casy+y))
		return self.casposibles

class metapeon(metapieza):
	def movpeon(self):
		lpeon=[0,-1,1,5,4]
		if 0 < self.casy+lpeon[self.color] <= 8 and 0 < self.casx <= 8:
			if cocupadas[self.casy+lpeon[self.color]] == 0:	
				self.casposibles.append((self.casx,self.casy+lpeon[self.color]))
				if self.movida == 0 and cocupadas[lpeon[self.color+2]][self.casx] == 0:
					self.casposibles.append((self.casx,lpeon[self.color+2]))
		if 0 < self.casy+lpeon[self.color] <= 8 and 0 < self.casx+1 <= 8:
			if cocupadas[self.casy+lpeon[self.color]][self.casx+1] == 3-self.color:
				self.casposibles.append((self.casx+1,self.casy+lpeon[self.color]))
		if 0 < self.casy+lpeon[self.color] <= 8 and 0 < self.casx-1 <= 8:
			if cocupadas[self.casy+lpeon[self.color]][self.casx-1] == 3-self.color:
				self.casposibles.append((self.casx-1,self.casy+lpeon[self.color]))
		return self.casposibles

	def transformar(self):
		# Menú o diálogo para seleccionar pieza
		print("¡El peón ha llegado al final! Selecciona una pieza: reina, torre, alfil o caballo.")
		# Puedes implementar un método para recoger la elección del jugador
		# Aquí simplemente transformamos a reina como ejemplo
		self.__class__ = metareina  # Transforma a reina

class metareina(metapieza):
	def movreina(self):
		# La reina puede moverse en cualquier dirección
		return self.movlineal(8) + self.movdiagonal(8)

# Agregar otros tipos de piezas de manera similar

def dibujarborde():
	#Dibuja el tablero
	for x in range(9):
		for y in range(9):
			if (x+y) % 2 == 0:
				pygame.draw.rect(visor, (255,255,255), (casilla[x], casilla[y], 70, 70))
			else:
				pygame.draw.rect(visor, (0,0,0), (casilla[x], casilla[y], 70, 70))

def dibujarpeon(peon):
	pygame.draw.rect(visor, (255, 0, 0), (peon.pos[0], peon.pos[1], 70, 70))  # Color rojo para el peón

# Se puede agregar más funciones de dibujo para otras piezas

def main():
	peones = [metapeon(4, 1, 1), metapeon(4, 6, 2)]  # Ejemplo de dos peones
	while True:
		visor.fill((0, 0, 0))
		dibujarborde()
		for peon in peones:
			dibujarpeon(peon)
			peon.casposibles = peon.movpeon()  # Calcular posiciones posibles
			if peon.casy == 0 or peon.casy == 8:  # Si el peón alcanza la última fila
				peon.transformar()  # Transformar el peón

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()

main()
