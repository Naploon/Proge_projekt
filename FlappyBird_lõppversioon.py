import pygame #toob sisse pygame mooduli
import random #toob sisse random'i mooduli
import sys 

#defineerime mängu funktsioonid

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
            surma_heli.play()
            return False
        
    if lind_rect.top <= -100 or lind_rect.bottom >= 900:
        return False
    
    return True

#tulemuse esitamine
def tulemusnäidik(hetk_mängus):
    if hetk_mängus == "mängus":
        tulemuspilt = mängu_font.render(f'Score: {int(tulemus)}', True,(255, 255, 255))
        tulemus_rect = tulemuspilt.get_rect(center = (288, 100))
        ekraan.blit(tulemuspilt, tulemus_rect)
    if hetk_mängus == "mäng_läbi":
        tulemuspilt = mängu_font.render(f'Score: {int(tulemus)}', True,(255, 255, 255))
        tulemus_rect = tulemuspilt.get_rect(center = (288, 100))
        ekraan.blit(tulemuspilt, tulemus_rect)
        
        #parima tulemuse esitamine
        parim_tulemuspilt = mängu_font.render(f'High score: {int(parim_tulemus)}', True,(255, 255, 255))
        parim_tulemus_rect = parim_tulemuspilt.get_rect(center = (288, 850))
        ekraan.blit(parim_tulemuspilt, parim_tulemus_rect)

#hoiab meeles parimat tulemust
def tulemused(tulemus, parim_tulemus):
    if tulemus > parim_tulemus:
        parim_tulemus = tulemus
    return parim_tulemus

def tulemus_torudelt():
    global tulemus, võib_lugeda
    if toru_järjend:
        for toru in toru_järjend:
            if 95 < toru.centerx < 105 and võib_lugeda:
                tulemus += 1
                skoori_heli.play()
                võib_lugeda = False
            if toru.centerx < 0:
                võib_lugeda = True

#linnu n-ö kallutamine animatsiooni jaoks
def keera_lindu(lind):
    keeratud_lind = pygame.transform.rotozoom(lind, -linnu_liikumine * 3, 1)
    return keeratud_lind

#linnu tiibade liigutamine
def linnu_animatsioon():
    animeeritud_lind = lind_kaadrid[lind_index]
    animeeritud_lind_rect = animeeritud_lind.get_rect(center = (100, lind_rect.centery))
    return animeeritud_lind, animeeritud_lind_rect


pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512) #mängib heli normaalselt       
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


#laeb linnu pildifailid sisse, animatsiooni jaoks
lind_tiib_all = pygame.image.load("assets/lind_tiib_all.png").convert_alpha()
lind_tiib_all = pygame.transform.scale2x(lind_tiib_all)
lind_tiib_keskel = pygame.image.load("assets/lind_tiib_keskel.png").convert_alpha()
lind_tiib_keskel = pygame.transform.scale2x(lind_tiib_keskel)
lind_tiib_üleval = pygame.image.load("assets/lind_tiib_üleval.png").convert_alpha()
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
pygame.time.set_timer(tekita_toru, 1200)
toru_kõrgus = [400, 600, 800]
toru_järjend = []

#pilt kui mäng saab läbi
mäng_läbi_pilt = pygame.image.load("assets/sõnum_algus.png").convert_alpha()
mäng_läbi_pilt = pygame.transform.scale2x(mäng_läbi_pilt)
mäng_läbi_rect = mäng_läbi_pilt.get_rect(center = (288, 512))

#mängu muutujad
gravitatsioon = 0.4
linnu_liikumine = 0
tulemus = 0
parim_tulemus = 0
mängu_staatus = True
võib_lugeda = True
mängu_font = pygame.font.Font("font/04B_19.ttf", 40)

#helid
tiiva_heli = pygame.mixer.Sound('audio/sfx_wing.wav')
surma_heli = pygame.mixer.Sound('audio/sfx_hit.wav')
skoori_heli = pygame.mixer.Sound('audio/sfx_point.wav')
skoori_heli_arvestaja = 100


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
                tiiva_heli.play()
            if event.key == pygame.K_SPACE and mängu_staatus == False:
                mängu_staatus = True
                toru_järjend.clear()
                lind_rect.center = (100,512)
                linnu_liikumine = 0
                tulemus = 0
        if event.type == tekita_toru:
            toru_järjend.extend(loo_toru())
        if event.type == linnulend:
            if lind_index < 2:
                lind_index += 1
            else:
                lind_index = 0
            
            linnu_pilt, lind_rect = linnu_animatsioon()
    
    ekraan.blit(taust,(0, 0)) #lisab taustapildi ekraanile kindlale kohale
    if mängu_staatus:
        #linnu liikumine
        linnu_liikumine += gravitatsioon
        keeratud_lind = keera_lindu(lind_hetkes)
        lind_rect.centery += linnu_liikumine
        ekraan.blit(keeratud_lind, lind_rect)
        mängu_staatus = kokkupõrge(toru_järjend)
        #torud ekraanile
        toru_järjend = torude_liigutamine(toru_järjend)
        aseta_torud(toru_järjend)
        
        #skoor
        tulemus_torudelt()
        tulemusnäidik("mängus")
        
    else:
        ekraan.blit(mäng_läbi_pilt, mäng_läbi_rect)
        parim_tulemus = tulemused(tulemus, parim_tulemus)
        tulemusnäidik("mäng_läbi")
        
        

    maapinna_x -= 1 #muudab maapinna pildifaili x-koordinaati
    maapinna_liikumine() #lisab maapinna pildifaili ekraanile       
    if maapinna_x < -576: #tagab maapinna lõpmatu liikumise
        maapinna_x = 0
    pygame.display.update()
    aeg.tick(120)
