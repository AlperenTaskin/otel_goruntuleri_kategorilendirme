import os
import pandas as pd
from urllib import request

#veri setini okuduk
makeMyTripData = pd.read_csv('makemytrip_com-travel_sample.csv',error_bad_lines=False)
makemytripHead = makeMyTripData.head(5)

# istedigimiz kolon image_urls kolonu
imgUrls = makeMyTripData['image_urls']
imgUrls = imgUrls.dropna()

UrlList = []
tempList = []
tempPhotos = []

# url'ler // operatoru ile ayristirilmis. Bu yuzden kac tane url oldugunu bu sekilde tespit ediyoruz.
for item in imgUrls:
    tempList.append(item.split('|//'))

for list in tempList:
    for item in range(len(list)):
        tempPhotos.append(list[item])

for item in tempPhotos:
    if '//' in item or ' ' in item :
        item = item.replace('//','')
        item = item.replace(' ','%20')
        UrlList.append(item) 
    else:
        UrlList.append(item)

##bosluk yerine %20 koymazsak, urllib 400 bad request hatasi veriyor.
##örn .../Parking Area.jpg ---> .../Parking%20Area.jpg

imgCounter = 0

# fonksiyon icerisine goruntunun linkini ve nereye kaydedilecegini alıyor
def download_url_picture(img_url,folder_name):
    try:
        # kaydedilmek istenen klasor yoksa olusturuyor
        file_path = folder_name
        if not os.path.exists(file_path):
#            print('Dosya: ', "'", file_path, "'", ' olusturuldu')
            print("Dosya: '{}' olusturuldu!".format(file_path))
            os.makedirs(file_path)
          
        file_suffix = os.path.splitext(img_url)[1]
        
        global imgCounter
        
        # indirilen goruntulerin ismi sirasiyla 0.jpg 1.jpg gibi olacak
        file_name = str(imgCounter)
        imgCounter = imgCounter+1
        
        file_name = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
        
#        full_file_name = str(file_name) + '.jpg'
        request.urlretrieve(img_url, filename=file_name)
        return True
    
    except IOError as e:
        print('Hata', e)
        imgCounter -= 1
        return False
    
    except Exception as e:
        print('Hata ：', e)
        imgCounter -= 1
        return False

counter = 0

try:
    for counter in range(len(UrlList)):
        
        output = download_url_picture('http://' + UrlList[counter], '../photos')
        if output == True:
            print('{}. numarali goruntu basariyla indirildi! - Toplam indirilen goruntu sayisi : {}'.format(counter,imgCounter))
        else :
            print('{}. numarali goruntu indirilemedi!'.format(counter))
        
        if imgCounter == 5000:
            break
        
    print('Kontrol edilen goruntu sayisi:{}, Indirilen goruntu sayisi:{}'.format(counter,imgCounter))
        
except KeyboardInterrupt :
    # son olarak el ile indirme islemi durduruldugunda indirilmeyi denedigimiz ve indirdigimiz 
    # goruntu sayilarini gosteriyoruz
    print('Kontrol edilen goruntu sayisi:{}, Indirilen goruntu sayisi:{}'.format(counter,imgCounter))

