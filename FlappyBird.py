import pygame #toob siise pygame mooduli
import random #toob siise random'i mooduli
import sys 

def tulemusnäidik(hetk_mängus): #tulemuse esitamine
    if hetk_mängus == "mängus":
        tulemuspilt = game.font.render(str(int(tulemus)), True,(255, 255, 255))
        tulemus_rect = tulemuspilt.get_rect(center = (288, 100))
        ekraan.blit(tulemuspilt, tulemus_rect)
    if hetk_mängus == "mäng läbi":
        tulemuspilt = game_font.render(f"Tulemus: {int(tulemus)}", True,(255, 255, 255))
        tulemus_rect = tulempilt.get_rect(center = (288, 100))
        ekraan.blit(tulemuspilt, tulemus_rect)
        
        #parima tulemuse esitamine
        parim_tulemuspilt = game_font.render(f"Parim tulemus: {int(parim_tulemus)}", True,(255, 255, 255))
        parim_tulemus_rect = tulempilt.get_rect(center = (288, 850))
        ekraan.blit(parim_tulemuspilt, parim_tulemus_rect)

def tulemused(tulemus, parim_tulemus): #hoiab meeles parimat tulemust
    if tulemus > parim_tulemus:
        parim_tulemus = tulemus
    return parim_tulemus


def keera_lindu(lind): #linnu kallutamine animatsiooni jaoks
    keeratud_lind = pygame.transform.rotozoom(lind, -linnu_liikumine * 3, 1)
    return keeratud_lind

def linnu_animatsioon(): #linnu tiibade liigutamine
    animeeritud_lind = lind_kaadrid[lind_index]
    animeeritud_lind_rect = animeeritud_lind.get_rect(center = (100, lind_rect.centery))
    return animeeritud_lind, animeeritud_lind_rect


def loo_toru(): #loob suvalised torude kõrgused nii alla kui üles
    suvaline_positsioon = random.choice(toru_kõrgus)
    alumine_toru = toru.get_rect(midtop = (700, suvaline_positsioon))
    ülemine_toru = toru.get_rect(midbottom = (700, suvaline_positsioon - 300))
    return alumine_toru, ülemine_toru

def torude_liigutamine(torud): #pole hetkel 100% kindel mida see teeb
    for el in torud:
        el.centerx -= 5
    return torud

def aseta_torud(torud): #asetab torud ekraanile nii üles kui ka alla
    for el in torud:
        if el.bottom >= 1024:
            ekraan.blit(toru, el)
            
        else:
            keeratud_toru = pygame.transform.flip(toru,False,True)
            screen.blit(keeratud_toru, el)
    
def eemalda_toru(torud): #eemaldab ebasobivale positsioonile tekkinud toru
    for el in torud:
        if el.centerx == -600:
            torud.remove(el)
            
    return torud
    


def kokkupõrge(torud): #kontrollib, kas lind on põrganud kokku toru, lae või põrandaga
    for el in torud:
        if lind_rect.colliderect(el):
            #surmaheli peaks siia sisestama
            return False
        
    if lind_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    
    return True
            

def maapinna_liikumine(): #paneb maapinna liikuma vasakule
    ekraan.blit(maapind,(maapinna_x ,900))
    ekraan.blit(maapind,(maapinna_x + 576 ,900))



pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init() #alustab pygame'i moodulit
ekraan = pygame.display.set_mode((576, 1024)) #loob mängu jaoks akna
aeg = pygame.time.Clock()



taust = pygame.image.load("assets/taust_päev.png").convert() #leiab taustafaili ja converdim selle pygame paremini loetamaks
taust = pygame.transform.scale2x(taust) #teeb tausta suuremaks
maapind = pygame.image.load("assets/maapind.png").convert() #leiab maapinnafaili ja converdim selle pygame paremini loetamaks
maapind = pygame.transform.scale2x(maapind) #teeb maapinna suuremaks
maapinna_x = 0

gravitatsioon = 0.25
linnu_liikumine = 0
tulemus = 0
parim_tulemus = 0
mängu_staatus = True
#mängu_font = pygame.font.Font("04B_19.ttf", 40)


#laeb linnu pildifailid sisse
lind_tiib_all = pygame.image.load("assets/lind_tiib_all.png").convert()
lind_tiib_all = pygame.transform.scale2x(lind_tiib_all)
lind_tiib_keskel = pygame.image.load("assets/lind_tiib_keskel.png").convert()
lind_tiib_keskel = pygame.transform.scale2x(lind_tiib_keskel)
lind_tiib_üleval = pygame.image.load("assets/lind_tiib_üleval.png").convert()
lind_tiib_üleval = pygame.transform.scale2x(lind_tiib_üleval)
lind_index = 0
lind_kaadrid = [lind_tiib_all, lind_tiib_keskel, lind_tiib_üleval] #järjend linnu olekutega
lind_hetkes = lind_kaadrid[lind_index]
lind_rect = lind_hetkes.get_rect(center = (100, 512))
linnulend = pygame.USEREVENT + 1
pygame.time.set_timer(linnulend, 200)


#laeb sisse torude pildifailid
toru = pygame.image.load("assets/toru_roheline.png").convert()
toru = pygame.transform.scale2x(toru)
tekita_toru = pygame.USEREVENT
pygame.time.set_timer(tekita_toru, 1500)
toru_kõrgus = [400, 600, 600]
toru_järjend = []

#mänguhelid
    #siia tulevad hiljem mänguhelid, aga ma veel pole neid leidnud


#pilt kui mäng saab läbi
mäng_läbi_pilt = pygame.image.load("assets/sõnum_lõpp.png")
mäng_läbi_pilt = pygame.transform.scale2x(mäng_läbi_pilt)
mäng_läbi_rect = mäng_läbi_pilt.get_rect(center = (288, 512))





while True:
    for event in pygame.event.get(): #pygame jälgib user inputi ja kogub neid
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    ekraan.blit(taust,(0, 0)) #lisab taustapildi ekraanile kindlale kohale
    maapinna_x -= 1 #muudab maapinna pildifaili x-kordinaati
    maapinna_liikumine() #lisab maapinna pildifaili ekraanile       
    if maapinna_x < -576: #tagab maapinna lõpmatu liikumise
        maapinna_x = 0 
    
    
    
    pygame.display.update()
    aeg.tick(160)




pygame.quit() # lülitab pygame'i välja