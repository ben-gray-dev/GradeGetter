from time import sleep

from selenium import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import json
import re
import argparse
instructorList = set()
foundProfs = set()


geps = {'GK':14287, 'HUM' : 14281, 'SS': 14282, 'VPA': 15985, 'IDP': 33269,'USD': 14286  }
gradientCookie = ""
myPackCookie = ""
def waitAndClickCSS(css_selector, timeout, driver):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
    finally:
        element.click()

def waitAndTextCSS(css_selector, timeout, driver):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
    finally:
        return element.text


def waitAndClick(xPath, timeout, driver):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xPath))
        )
    finally:
        element.click()
        
def waitAndSendKeys(xPath, timeout, driver, keysToSend):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xPath))
        )
    finally:
        element.send_keys(keysToSend)
def loginRoutine(driver, myUsername, myPassword):
    waitAndSendKeys('//*[@id="username"]', 30, driver, myUsername)
    waitAndSendKeys('//*[@id="password"]', 30, driver, myPassword)
    waitAndClick('//*[@id="formSubmit"]', 10, driver)
    waitAndClickCSS('#content > main > form > div.shib-form  input:nth-child(2)', 10, driver)
    return
        #content > main > form > div.shib-form > p:nth-child(2) > input:nth-child(2)

def grabCookies(driver, myUsername, myPassword):
    gradientCookie = ""
    myPackCookie = ""
    driver.get("https://tools.wolftech.ncsu.edu/gradient/")
    loginRoutine(driver, myUsername, myPassword)
    cookieList = driver.get_cookies()
    shibCook = cookieList[-1]
    gradientCookie = str(shibCook['name']) + "=" + str(shibCook['value'])
    sleep(5) 
    waitAndSendKeys('//*[@id="subjectSelect"]', 10, driver, 'ACC')
    sleep(2)
    waitAndSendKeys('//*[@id="courseSelect"]', 10, driver, '200')
    waitAndClickCSS('#showButton > button', 5, driver)
    driver.get("https://mypack.ncsu.edu")
    waitAndClickCSS('#idpSelectPreferredIdPTile > div:nth-child(2) > a', 10, driver)
    sleep(3)
    waitAndClickCSS('#content > main > form > div.shib-form  input:nth-child(2)', 10, driver)
    myPackCookieList = driver.get_cookies()
    myPackCookieSize = len(myPackCookieList)
    for i, cookie in enumerate(myPackCookieList):
        if (i == myPackCookieSize - 1):
            myPackCookie += cookie['name'] + "=" + cookie['value']
        else:
            myPackCookie += cookie['name'] + "=" + cookie['value'] + "; "
    driver.get('https://cs92prd.acs.ncsu.edu/psc/CS92PRD_13/EMPLOYEE/NCSIS/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV')
    sleep(5)
    waitAndClickCSS(".ps_box-group .psc_layout .psa_vtab .psc_rowact:nth-of-type(2) > div", 10, driver)
    sleep(5)
    waitAndClickCSS(".ps_box-group .psc_layout .psa_vtab .psc_rowact:nth-of-type(4) > div", 10, driver)
    sleep(5)
    driver.execute_script("document.querySelector('.jquery-app').contentDocument.querySelector('h3').click()")
    sleep(5)
    driver.execute_script("document.querySelector('.jquery-app').contentDocument.querySelector('td:nth-child(8) > span').click()")
    sleep(2)

    with open('pastCookies.txt', 'w+') as f:
        f.write(gradientCookie)
        f.write("\n")
        f.write(myPackCookie)

    return gradientCookie, myPackCookie



def getRawData(department, classNum):
    url = "https://tools.wolftech.ncsu.edu/gradient/api.php?action=distributions&subject=" + str(department) + "&course=" + str(classNum)
    r = requests.get( url, headers={"Cookie": gradientCookie})
    try:
        data = r.json()
    except:
        return None
    keysList = {}
    composite = data['composite']['grades']
    individuals = data['individual']
    for i in individuals:
          if (i is not None):
              del i['googleChart']
              i['online'] = False
              if (int(re.sub('[^0-9]', '', i['courseId'].split("-")[2])) > 300):
                  i['online'] = True
              del i['courseId']
              i['instructorName'] = i['instructorName'].split(',')[0]
    keysList['composite'] = composite
    keysList['individuals'] = individuals
    return keysList

def parseByInstructor(rawData, profsOfInterest):
    instrDictList = {}
    instrDictCtr = {}
    nameList = rawData['individuals'][0]['courseName'].split()
    for i in rawData['individuals']:
        iName = i['instructorName'] + "*" + nameList[0] + nameList[1]
        if (iName not in profsOfInterest):
            continue
        foundProfs.add(iName)
        if ( iName not in instrDictList):
            instrDictList[iName] = []
            instrDictCtr[iName] = 1
            aComposite = {'totalA': 0, 'totalTaken': 0, 'percentA': 0.0}
            instrDictList[iName].append(aComposite)
        instrDictList[iName][0]['totalA'] += int(i['grades']['A']['raw'])
        instrDictList[iName][0]['totalTaken'] += int(i['grades']['TOTAL']['raw'])
        instrDictList[iName][0]['percentA'] = instrDictList[iName][0]['totalA']/ instrDictList[iName][0]['totalTaken'] 
        instrDictList[iName].append({})
        instrDictList[iName][instrDictCtr[iName]]['grades'] =  i['grades']
        instrDictList[iName][instrDictCtr[iName]]['courseSem']  = i['courseSem']
        instrDictList[iName][instrDictCtr[iName]]['online']  = i['online']
        instrDictCtr[iName] += 1
    sorted_instructor_list = sorted(instrDictList.items(), key = lambda kv: kv[1][0]['percentA'])
   
    return sorted_instructor_list
        
    
def findBestClass(runningList, classList, profsOfInterest):
    resulList = [runningList]
    
    for c in classList:
        cList = c.split()
        if len(resulList) == 0:
            rawResul = getRawData(cList[0], cList[1])
            if rawResul is None:
                continue
            resulList.append(parseByInstructor(rawResul,profsOfInterest))
        else:
            rawResul = getRawData(cList[0], cList[1])
            if rawResul is None:
                continue
            resulList[0] += parseByInstructor(rawResul, profsOfInterest)
    wrapperList = sorted(resulList[0], key = lambda kv: kv[1][0]['percentA'], reverse = True)
    #wrapperList = list(set(wrapperList))
    return wrapperList

def printClassRanks(listAn):
    if len(listAn) == 0:
        print("No available classes with grade distribution history for your search parameters.")
    for (idx, item) in enumerate(listAn):
        print("%s. %s %s" % (str(idx + 1), item[0], item[1][0]['percentA']))
    
def checkClassFit(department, classNum):
    r = requests.get("https://cs92prd.acs.ncsu.edu/psc/CS92PRD/EMPLOYEE/NCSIS/s/WEBLIB_ENROLL.ISCRIPT1.FieldFormula.IScript_getClassSearchResults?subject=" + department + "&catalogNbrOpt=E&catalogNbr=" + str(classNum) + "&instructorName=&filterCareer=&filterLocation=&filterGEP=&filterSession=&filterOpenSectionsOnly=1&filterFitCalendar=1", 
                     headers = {"Cookie": myPackCookie})
    data = r.json()
    matches = 0
    if (len(data['data']) == 0) :
        return False
    availSections = set()
    for (idx, entry) in enumerate(data['data']):
        availSections = set()
        if entry['enrl_status'] != 'W' and entry['requisite_met'][0] != 'N':
            reservedSeats = 0
            availSeats = int(entry['section_details'][0]['seat_availability'].split()[0])
            for i in entry['section_details'][0]['reserved_seats']:
                reservedSeats += int(i.split()[2])
            if (availSeats > reservedSeats):
                matches += 1
                availSections.add(idx)
    if (matches != 0):
        for i in availSections:
            try:
                instructorList.add(data['data'][i]['section_details'][0]['instructors'][0].split(",")[0] + "*" + department + str(classNum))
            except:
                continue
        return True
    return False
    
def scoutClasses(classList):
    runningList = []
    for classC in classList:
        classDets = classC.split()
        if (checkClassFit(classDets[0], classDets[1])):
            runningList = findBestClass(runningList, [classC], instructorList)    
    printClassRanks(runningList)

def lookUpFromDegreeAudit(ReqNum):
    r = requests.get("https://cs92prd.acs.ncsu.edu/psc/CS92PRD_34/EMPLOYEE/NCSIS/s/WEBLIB_DEGAUDIT.ISCRIPT1.FieldFormula.IScript_getRequirementList?requirement=0000" + str(ReqNum) + "&isExcReq=",
                     headers = {"Cookie": myPackCookie})
    data = r.json()
    potentials = []
    for w in data['rq_lines']:
        for i in w['courses']:
            print(i['subject'] + " " + i['catalog_nbr'])
            potentials.append(i['subject'] + " " + i['catalog_nbr'])
    return potentials

def getAllClasses(nonGrad, onlineOnly, minUnits, *args):
    allFittingClassesJson = requests.get("https://cs92prd.acs.ncsu.edu/psc/CS92PRD/EMPLOYEE/NCSIS/s/WEBLIB_ENROLL.ISCRIPT1.FieldFormula.IScript_getClassSearchResults?subject=&catalogNbrOpt=E&catalogNbr=&instructorName=&filterCareer=&filterLocation=&filterGEP=&filterSession=&filterOpenSectionsOnly=1&filterFitCalendar=1",
        headers = {"Cookie": myPackCookie}).json()
    wildcarded = False
    if (len(args) != 0):
        if (len(args) != 3):
            return
        courseSubject = args[0]
        courseNumber = args[1]
        wildcard = args[2]
        wildcarded = True
    potentials = set()
    if (wildcarded):
        data = allFittingClassesJson
        for i in data['data']:
            classData = i['classs'].split()
            courseSub = classData[0]
            courseNum = int(re.sub('[^0-9]', '',classData[1]))
            if courseSub != courseSubject:
                continue
            if wildcard == 'lt':
                if courseNumber < courseNum:
                    continue
            else:
                if courseNumber > courseNum:
                    continue 

            if (i['classs'] not in potentials):
                className = i['classs']
                potentials.add(className)
                print("adding %s" % className)
    else:
        data = allFittingClassesJson
        for i in data['data']:
            units = i['units']
            splitUnits = units.split('-')
            if (len(splitUnits) != 0):
                units = splitUnits[0]
            if (nonGrad and int(re.sub('[^0-9]', '',i['classs'].split()[1])) >= 500):
                continue
            if (onlineOnly and int(re.sub('[^0-9]', '', i['section_details'][0]['section'])) < 300):
                continue
            if (float(units) < minUnits):
                continue
            if (i['classs'] not in potentials):
                className = i['classs']
                potentials.add(className)
                print("adding %s" % className)
    return potentials
              
def getGEPClasses(*args):
    argList = list(args)
    resulList = lookUpFromDegreeAudit(geps[argList[0]])
    del argList[0]
    for i in argList:
         resulList = list(set(resulList).intersection(lookUpFromDegreeAudit(geps[i])))
    return resulList     

def getSession():
    global gradientCookie
    global myPackCookie
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(chrome_options=options,executable_path="chromedriver.exe")
    gradientCookie, myPackCookie = grabCookies(driver, args.username, args.password)
    driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("-u", "--username", help="User name (unity ID)", required=True)
    parser.add_argument("-p", "--password", help="Password", required=True)
    group.add_argument("-r", "--requirement", help="Degree audit requirement number", type=int)
    group.add_argument("-a", "--all_classes", help="flag to get all classes for ranking", action='store_true', default=False)
    parser.add_argument("-o", "--online_only", help="flag to get only online classes for ranking", action='store_true', default=False)
    parser.add_argument("-ng", "--non_grad", help="flag to get only non graduate-level classes for ranking", action='store_true', default=True)
    parser.add_argument("-m", "--min_units", help="flag to get only online classes for ranking", type=int, default=1)
    group.add_argument("-s", "--specific_class", help="flag to denote specific class to compile historical statistics", action='store_true', default=False)
    parser.add_argument("-cs", "--course_subject", help="subject of a specific course (string)", type=str.upper)
    parser.add_argument("-cn", "--course_number", help="subject of a specific course (string)", type=int)
    parser.add_argument("-w", "--wildcard", choices=['lt', 'gt'], help="wild card search with specific course information", type=str.lower)


    args = parser.parse_args()

    if args.specific_class and (args.course_subject is None or args.course_number is None):
        parser.error("--specific_class requires --course_subject and --course_number.")

    print('==================== testing if current session viable ====================')
    try:
        with open('pastCookies.txt', 'r') as f:
            lines = f.read().splitlines()
            gradientCookie, myPackCookie = lines
    except:
        print('==================== obtaining a session ==========================')
        getSession()


    

    completed = False

    while not completed:
        try:
            if args.all_classes:
                scoutClasses(getAllClasses(args.non_grad, args.online_only, args.min_units))
            elif args.requirement is not None:
                scoutClasses(lookUpFromDegreeAudit(args.requirement))
            elif args.specific_class:
                if args.wildcard is not None:
                    scoutClasses(getAllClasses(None, None, None, args.course_subject, args.course_number, args.wildcard))
                else:
                    scoutClasses([args.course_subject + " " + str(args.course_number)])
            completed = True
        except:
            print("================== Session not working or expired, obtaining new session ===============")
            getSession()

