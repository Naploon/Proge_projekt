import pygame #toob sisse pygame mooduli
import random #toob sisse random'i mooduli
import sys 


def maapinna_liikumine(): #paneb maapinna liikuma vasakule
    ekraan.blit(maapind,(maapinna_x ,900))
    ekraan.blit(maapind,(maapinna_x + 576 ,900))

def loo_toru(): #loob suvalised torude kõrgused nii alla kui üles
    suvaline_positsioon = random.choice(toru_kõrgus)
    alumine_toru = toru.get_rect(midtop = (700, suvaline_positsioon))
    ülemine_toru = toru.get_rect(midbottom = (700, suvaline_positsioon - 300))
    return alumine_toru, ülemine_toru

def torude_liigutamine(torud): #liigutab torud ekraani keskele, et n-ö pildilt maha ei sõidaks
    for el in torud:
        el.centerx -= 5
    return torud

def aseta_torud(torud): #asetab torud ekraanile nii üles kui ka alla
    for el in torud:
        if el.bottom >= 1024:
            ekraan.blit(toru, el)
            
        else:
            keeratud_toru = pygame.transform.flip(toru,False,True)
            ekraan.blit(keeratud_toru, el)

def kokkupõrge(torud): #kontrollib, kas lind on põrganud kokku toru, lae või põrandaga
    for el in torud:
        if lind_rect.colliderect(el):
            #surmaheli peaks siia sisestama
            return False
        
    if lind_rect.top <= -100 or lind_rect.bottom >= 900:
        return False
    
    return True

pygame.init() #alustab pygame'i moodulit
ekraan = pygame.display.set_mode((576, 1024)) #loob mängu jaoks akna
aeg = pygame.time.Clock()

#taustapilt
taust = pygame.image.load("assets/taust_päev.png").convert() #leiab taustafaili ja converdib selle pygame paremini loetavaks
taust = pygame.transform.scale2x(taust) #teeb tausta suuremaks
#maapind
maapind = pygame.image.load("assets/maapind.png").convert() #leiab maapinnafaili ja converdib selle pygame paremini loetavaks
maapind = pygame.transform.scale2x(maapind) #teeb maapinna suuremaks
maapinna_x = 0

#linnu pilt
linnu_pilt = pygame.image.load("assets/lind_tiib_keskel.png").convert_alpha()
linnu_pilt = pygame.transform.scale2x(linnu_pilt)
lind_rect = linnu_pilt.get_rect(center = (100, 512))

#laeb sisse torude pildifailid
toru = pygame.image.load("assets/toru_roheline.png").convert()
toru = pygame.transform.scale2x(toru)
tekita_toru = pygame.USEREVENT
pygame.time.set_timer(tekita_toru, 1500)
toru_kõrgus = [400, 600, 800]
toru_järjend = []

#pilt kui mäng saab läbi
mäng_läbi_pilt = pygame.image.load("assets/sõnum_lõpp.png").convert_alpha()
mäng_läbi_pilt = pygame.transform.scale2x(mäng_läbi_pilt)
mäng_läbi_rect = mäng_läbi_pilt.get_rect(center = (288, 512))

#mängu muutujad
gravitatsioon = 0.25
linnu_liikumine = 0
mängu_staatus = True

#mängu loop
while True:
    for event in pygame.event.get(): #pygame jälgib user inputi ja kogub neid
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and mängu_staatus:
                linnu_liikumine = 0
                linnu_liikumine -= 12
            if event.key == pygame.K_SPACE and mängu_staatus == False:
                mängu_staatus = True
                toru_järjend.clear()
                lind_rect.center = (100,512)
                linnu_liikumine = 0
        if event.type == tekita_toru:
            toru_järjend.extend(loo_toru())
    
    ekraan.blit(taust,(0, 0)) #lisab taustapildi ekraanile kindlale kohale
    if mängu_staatus:
        #linnu liikumine
        linnu_liikumine += gravitatsioon
        lind_rect.centery += linnu_liikumine
        ekraan.blit(linnu_pilt, lind_rect)
        mängu_staatus = kokkupõrge(toru_järjend)
        #torud ekraanile
        toru_järjend = torude_liigutamine(toru_järjend)
        aseta_torud(toru_järjend)
    else:
        ekraan.blit(mäng_läbi_pilt, mäng_läbi_rect)
        

        
    maapinna_x -= 1 #muudab maapinna pildifaili x-koordinaati
    maapinna_liikumine() #lisab maapinna pildifaili ekraanile       
    if maapinna_x < -576: #tagab maapinna lõpmatu liikumise
        maapinna_x = 0
    pygame.display.update()
    aeg.tick(120)


