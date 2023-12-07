import pygame, simpleGE, random
    
class Ship(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("ship1.png")
        self.setSize(50, 50)
        self.setPosition((100, 100))
        self.shipSound = pygame.mixer.Sound("shipThrust.mp3")        
    
    def checkEvents(self):
        self.addForce(.1, 270)
        if self.scene.isKeyPressed(pygame.K_SPACE):
            self.setDY(0)
            self.addForce(5, 90)
            self.shipSound.play()

class UpperTentacle(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("TentacleDOWN.png")
        self.setPosition((600, 0))    
        self.setDX(-3)
        self.deathSound = pygame.mixer.Sound("shipExplosion.mp3")
        
    def checkBounds(self):
        #only check for leave left
        if self.x < 0:
            self.scene.tentacleReset()
            self.scene.lblScore.score += 1
            
    def checkEvents(self):
        if self.collidesWith(self.scene.ship):
            self.deathSound.play()
            self.scene.pauseGame()
            
class LowerTentacle(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("TentacleUP.png")
        self.setPosition((600, 0))    
        self.setDX(-3)
        self.deathSound = pygame.mixer.Sound("shipExplosion.mp3")
        
    def checkBounds(self):
        #only check for leave left
        if self.x < 0:
            self.scene.tentacleReset()
            self.scene.lblScore.score += 1
            
    def checkEvents(self):
        if self.collidesWith(self.scene.ship):
            self.deathSound.play()
            self.scene.pauseGame()
            
class Instructions (simpleGE.MultiLabel):
    def __init__(self):
        super().__init__()
        self.textLines = [
            "Dodge The Alien Tentacles!",
            "Use The Space Bar To Fly Your Ship.",
            "Survive For As Long As You Can.",
            "Click To Begin."]
        self.center = ((320, 240))
        self.size = ((640, 480))
        
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.score = 0
        self.hide()
        
    def update(self):
        super().update()
        self.text = f"Score: {self.score}"
        
class BtnQuit(simpleGE.Button):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.hide()
        self.text = "Quit"
        
    def update(self):
        super().update()
        if self.clicked:
            self.scene.stop()
        
class BtnReset(simpleGE.Button):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.hide()
        self.text = "Restart"
        
    def update(self):
        super().update()
        if self.clicked:
            self.scene.resetGame()        
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background = pygame.image.load("spaceBG1.png")
        
        pygame.mixer.music.load("FSbgMusic.wav")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(-1)
        
        self.ship = Ship(self)
        self.upperTentacle = UpperTentacle(self)
        self.lowerTentacle = LowerTentacle(self)
        self.instructions = Instructions()
        self.lblScore = LblScore()
        self.btnQuit = BtnQuit(self)
        self.btnReset = BtnReset(self)
        self.gap = 400
        self.sprites = [self.ship, self.upperTentacle, self.lowerTentacle, self.instructions, self.lblScore, self.btnQuit, self.btnReset]
        
    def tentacleReset(self):  
        self.topPosition = random.randint(0, 200)
        self.bottomPosition = self.topPosition + self.gap
        self.upperTentacle.setPosition((640, self.topPosition))
        self.lowerTentacle.setPosition((640, self.bottomPosition))
    
    def resetGame(self):
        self.tentacleReset()
        self.ship.setPosition((100, 100))
        self.lblScore.score = 0
        self.btnReset.hide()
        self.btnQuit.hide()
        
    def update(self):
        if self.instructions.clicked:
            self.instructions.hide()
            self.lblScore.show((100, 50))
            self.lblScore.score = 0
            self.tentacleReset()  
    
    def pauseGame(self):
        self.ship.setPosition((640, 480))
        self.upperTentacle.setPosition((2000, 2000))
        self.lowerTentacle.setPosition((2000, 2000))
        self.btnQuit.show((150, 200))
        self.btnReset.show((450, 200))
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
    
        