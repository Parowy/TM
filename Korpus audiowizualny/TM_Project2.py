#biblioteka do sterowania przeglądarką - by uruchomić trzeba mieć specjalne drivery do przeglądarki, z której korzystacie
#tutaj do chrome
#https://sites.google.com/a/chromium.org/chromedriver/
#tutaj do firefox
#https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html



from selenium import webdriver
import time
import xlrd
import os
import shutil



#czytanie POI_Plused
wb = xlrd.open_workbook('POI_Plused.xlsx')
sheet = wb.sheet_by_index(0)

#czytanie POI_Spaced
wb_spaced = xlrd.open_workbook('POI_Spaced.xlsx')
sheet_spaced = wb.sheet_by_index(0)



#przypisywanie POI_Plused.xlsx do listy names

names = []

for i in range(0, sheet.nrows):
    names.append(sheet.cell_value(i, 0))

#przypisywanie POI_Spaced.xlsx do listy names_spaced

names_spaced = []

for i in range(0, sheet_spaced.nrows):
    names_spaced.append(sheet_spaced.cell_value(i, 0))



#ścieżka do ściągniętgo drivera
browser = webdriver.Chrome('D:\chromedriver.exe')



#pobieranie ublock na starcie
browser.get('https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm?hl=pl')

time.sleep(15)
#wyłączenie popup na tej stronie
browser.get('https://www.onlinevideoconverter.com/pl/youtube-converter')
time.sleep(15)
#zmiana folderu download
browser.get('chrome://settings/?search=Downloads')
time.sleep(15)


texts = []

for i in range(5, 10):
    a = 'https://www.youtube.com/results?search_query='+names[i]+'+wywiad'
    browser.get(a)

    for j in range(0, 9):
        matched_elements = browser.find_elements_by_id("dismissable")
        matched_elements[j].click()
        b = browser.current_url
        browser.get('https://www.onlinevideoconverter.com/pl/youtube-converter')
        searchbar = browser.find_element_by_id("texturl")
        searchbar.send_keys(b)
        start = browser.find_element_by_id("convert1")
        start.click()
        k = 0
        while (k<12):
            try:
                element = browser.find_element_by_id("downloadq")
                break
            except:
                k = k + 1
                time.sleep(5)
                continue
        while (k<6):
            try:
                element.click()
                break
            except:
                k = k + 1
                time.sleep(5)
                continue
        a = 'https://www.youtube.com/results?search_query='+names[i]+'+wywiad'
        browser.get(a)
    time.sleep(60)    
    #tu idą pobrane pliki
    source = 'D:\Source'
    #tu są przenoszone
    os.chdir('D:\Destination')
    #tworzymy folder na konkretną osobę
    folder_name = names_spaced[i]
    os.mkdir(folder_name)
    dest1 = 'D:\Destination\\' + folder_name

    files = os.listdir(source)

    for f in files:
        shutil.move(source+"\\"+f, dest1)