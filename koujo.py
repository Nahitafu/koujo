import math

KENPO_RYOURITSU = 9.98
KENPO_RYOURITSU_WITH_KAIGO = 11.58
NENKIN_RYOURITSU = 18.3

def gesshu(nenshu):
    return nenshu / 12

def kenpo_toukyu(gesshu:float) -> int:
    """
    健保等級を計算する

    Parameters
    ----------
    gesshu : float
        月収(万円) 給料だけでなく、交通費や社宅、現物支給などあらゆる報酬を合算した金額

    Returns
    ----------
    toukyu : int
        健保等級(1～50) 健康保険の計算では給料に応じて1～50までのランクにわけられます
    """

    # limitは千円単位の階級閾値
    limit = (63,73,83,93,101,107,114,122,130,138,146,155,165,175,185,195,210,230,
             250,270,290,310,330,350,370,395,425,455,485,515,545,575,605,635,
             665,695,730,770,810,855,905,955,1005,1055,1115,1175,1235,1295,1355)
    for toukyu in range(0,len(limit)):
        if(gesshu * 10 < limit[toukyu]):
            return toukyu + 1
    return len(limit) + 1

def kenpo_hyoujungetsugaku(toukyu:int) -> float:
    """
    健保の標準月額報酬を計算する

    Parameters
    ----------
    toukyu : int
        健保等級(1～50)

    Returns
    ----------
    hyoujun : float
        標準月額報酬(万円) 給与額ではなく等級に変換してから求められた標準報酬月額が計算の基礎に用いられます

    """

    getsugaku = (58,68,78,88,98,105,110,118,126,134,142,150,160,170,180,190,
                 200,220,240,260,280,300,320,340,360,380,410,440,470,500,530,
                 560,590,620,650,680,710,750,790,830,880,930,980,1030,1090,1150,1210,1270,1330,1390)
    if(toukyu <= 0):
            return 0
    if(toukyu >= len(getsugaku)):
            return getsugaku[len(getsugaku) - 1] / 10
    return getsugaku[toukyu - 1] / 10

def nenkin_toukyu(gesshu:float) -> int:
    """
    年金等級を計算する

    Parameters
    ----------
    gesshu : float
        月収(万円) 給料だけでなく、交通費や社宅、現物支給などあらゆる報酬を合算した金額が用いられます

    Returns
    ----------
    toukyu : int
        年金等級(1～32) 厚生年金の計算では給料に応じて1～32までのランクにわけられます(健保よりランクが少なく、上限が低い)
    """

    # limitは千円単位の階級閾値
    limit = (93,101,107,114,122,130,138,146,155,165,175,185,195,210,230,
             250,270,290,310,330,350,370,395,425,455,485,515,545,575,605,635)
    for toukyu in range(0,len(limit)):
        if(gesshu * 10 < limit[toukyu]):
            return toukyu + 1
    return len(limit) + 1

def nenkin_hyoujungetsugaku(toukyu:int) -> float:
    """
    厚生年金の標準月額報酬を計算する

    Parameters
    ----------
    toukyu : int
        年金等級(1～32)

    Returns
    ----------
    hyoujun : float
        標準月額報酬(万円) 給与額ではなく等級に変換してから求められた標準報酬月額が計算の基礎に用いられます

    """

    getsugaku = (88,98,105,110,118,126,134,142,150,160,170,180,190,
                 200,220,240,260,280,300,320,340,360,380,410,440,470,500,530,
                 560,590,620,650)
    if(toukyu <= 0):
            return 0
    if(toukyu >= len(getsugaku)):
            return getsugaku[len(getsugaku) - 1] / 10
    return getsugaku[toukyu - 1] / 10

def kenpo_calc(gesshu:float, age40over:bool, shachou: bool = False):
    """
    健康保険金額を計算する

    Parameters
    ----------
    gesshu : float
        月収(万円) 給料だけでなく、交通費や社宅、現物支給などあらゆる報酬を合算した金額が用いられます
    age40over : bool
        40歳から64歳はTrueとしてください。介護保険料が上乗せされます
    shachou : float
        貴方が社長ならTrueとしてください。会社負担分は実質的に貴方の負担です

    Returns
    ----------
    kenpo : float
        健保保険料(万円)
    """
    toukyu = kenpo_toukyu(gesshu)
    return round(kenpo_hyoujungetsugaku(toukyu) * (KENPO_RYOURITSU_WITH_KAIGO if age40over else KENPO_RYOURITSU) / 100.0 / (1 if shachou else 2),4)

def nenkin_calc(gesshu:float, shachou: bool = False):
    """
    厚生年金保険料を計算する

    Parameters
    ----------
    gesshu : float
        月収(万円) 給料だけでなく、交通費や社宅、現物支給などあらゆる報酬を合算した金額が用いられます
    shachou : float
        貴方が社長ならTrueとしてください。会社負担分は実質的に貴方の負担です

    Returns
    ----------
    nenkin : float
        厚生年金保険料(万円)
    """
    toukyu = nenkin_toukyu(gesshu)
    return round(nenkin_hyoujungetsugaku(toukyu) * NENKIN_RYOURITSU / 100.0 / (1 if shachou else 2),4)

def kisokoujo_calc(nenshu):
    if(nenshu <= 2400):
         return 48
    if(nenshu <= 2450):
        return 32
    if(nenshu <= 2500):
         return 16
    return 0

def kyuyoshotokukoujo_calc(nenshu):
    if(nenshu <= 162.5):
        return 55
    if(nenshu <= 180):
        return nenshu * 0.4 - 10
    if(nenshu <= 360):
        return nenshu * 0.3 + 10
    if(nenshu <= 660):
        return nenshu * 0.2 + 44
    if(nenshu <= 850):
        return nenshu * 0.1 + 110
    return 195

def shotokuzei_calc(kazeishotoku):
    kazeishotoku = round(kazeishotoku,1)
    zeiritsu = 0
    koujo = 0
    if(kazeishotoku <=194.9):
        zeiritsu = 5
        koujo = 0
    elif(kazeishotoku <=329.9):
        zeiritsu = 10
        koujo = 9.75
    elif(kazeishotoku <=694.9):
        zeiritsu = 20
        koujo = 42.75
    elif(kazeishotoku <=899.9):
        zeiritsu = 23
        koujo = 63.6
    elif(kazeishotoku <=1799.9):
        zeiritsu = 33
        koujo = 153.6
    elif(kazeishotoku <=3999.9):
        zeiritsu = 40
        koujo = 279.6
    elif(kazeishotoku >= 4000):
        zeiritsu = 45
        koujo = 479.6
    return kazeishotoku * zeiritsu / 100 - koujo

def kazeishotoku_calc(nenshu,koujo_total):
	if(nenshu <= koujo_total):
		return 0
	tmp = (nenshu - koujo_total) * 10 # 千円単位に換算
	return math.floor(tmp) / 10

def koyouhoken_calc(nenshu):
     gesshu = round(nenshu / 12 * 10000)
     return round(gesshu * 0.006) * 12 / 10000

#ここからメイン

age40over = True
shaho_kanyu = True
koyou_kanyu = True

f = open("result.txt","w")

nenshu = 100
nenshu_prev = 100
totai_zei_prev = 0
while (nenshu <= 10000):
	kenpo = kenpo_calc(nenshu / 12,age40over) * 12 if(shaho_kanyu) else 0
	nenkin = nenkin_calc(nenshu / 12) * 12 if(shaho_kanyu) else 0 
	koyouhoken = koyouhoken_calc(nenshu) if (koyou_kanyu) else 0
	kisokoujo = kisokoujo_calc(nenshu)
	kyuyokoujo = kyuyoshotokukoujo_calc(nenshu)
	koujo_total = kenpo + nenkin + koyouhoken + kisokoujo + kyuyokoujo
	kazeishotoku = kazeishotoku_calc(nenshu,koujo_total)
	juminzei = (kazeishotoku + 5) * 0.1 + 0.5
	shotokuzei = shotokuzei_calc(kazeishotoku)
	fukkou = shotokuzei * 0.021
	shotokuzeif  = math.floor((shotokuzei + fukkou) * 100) / 100
	tedori = round(nenshu - kenpo - nenkin - koyouhoken - shotokuzeif - juminzei,4)
	f.write(str(nenshu)+"\t")
	f.write(str(kenpo)+"\t")
	f.write(str(nenkin)+"\t")
	f.write(str(kenpo + nenkin)+"\t")
	f.write(str(koyouhoken)+"\t")
	f.write(str(kisokoujo)+"\t")
	f.write(str(kyuyokoujo)+"\t")
	f.write(str(kazeishotoku)+"\t")
	f.write(str(shotokuzei) +"\t")
	f.write(str(shotokuzeif - fukkou)+"\t")
	f.write(str(juminzei)+"\t")
	f.write(str(tedori)+"\t")
	totai_zei = nenshu - tedori
	f.write(str(totai_zei)+"\t")
	f.write(str(round(totai_zei/nenshu * 100,1))+"\t")
	if(nenshu == nenshu_prev):
		f.write("\t")
	else:
		f.write(str((totai_zei - totai_zei_prev) / (nenshu - nenshu_prev) * 100)+"\t")
	totai_zei_prev = totai_zei
	nenshu_prev = nenshu
	f.write("\n")
	if(nenshu < 300):
		nenshu += 0.5
	elif(nenshu < 1200):
		nenshu += 1
	elif(nenshu < 2400):
		nenshu += 1
	elif(nenshu < 2600):
		nenshu += 0.5
	else:
		nenshu += 5

# gesshu = 1 # 月収(万円)
# f.write("月収(万円)\t健保等級\t健保標準報酬月額\t年金等級\t年金標準報酬月額\t健保額\t年金額\t合計\n")
# while (gesshu <= 150):
#     f.write(str(round(gesshu,1))+"\t")
#     f.write(str(kenpo_toukyu(gesshu))+"\t"+str(kenpo_hyoujungetsugaku(kenpo_toukyu(gesshu)))+"\t")
#     f.write(str(nenkin_toukyu(gesshu))+"\t"+str(nenkin_hyoujungetsugaku(nenkin_toukyu(gesshu)))+"\t")
#     kenpo = kenpo_calc(gesshu,age40over);
#     nenkin = nenkin_calc(gesshu);
   
#     f.write(str(kenpo)+"\t")
#     f.write(str(nenkin)+"\t")
#     f.write(str(round(kenpo + nenkin,4))+"\t")
# #    f.write(str(nenkin(nenkin_hyoujungetsugaku(nenkin_toukyu(gesshu))))+"\t")
#     f.write("\n")
#     gesshu += 0.1

f.close()
