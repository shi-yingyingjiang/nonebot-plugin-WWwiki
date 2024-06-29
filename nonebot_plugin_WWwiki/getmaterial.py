from bs4 import BeautifulSoup



def getelementarymaterials(html):
    elementary_materials = {}
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')[1]
    td1 = table.find_all('td')[0]
    img = td1.find('img')['src']
    a = td1.find('a')
    text = a.get_text(strip=True)

    elementary_materials['img'] = img
    elementary_materials['title'] = text

    return elementary_materials

# print(getelementarymaterials(html_fragment_1))
def getintermediatematerials(html):

    intermediate_materials = {}
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')[1]
    td1 = table.find_all('td')[0]
    img = td1.find('img')['src']
    a = td1.find('a')
    text = a.get_text(strip=True)
    intermediate_materials['img'] = img
    intermediate_materials['title'] = text

    return intermediate_materials

def getseniormaterials(html):
    senior_materials = {}
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')[1]
    td1 = table.find_all('td')[0]
    img = td1.find('img')['src']
    a = td1.find('a')
    text = a.get_text(strip=True)
    senior_materials['img'] = img
    senior_materials['title'] = text

    return senior_materials

def getultimatematerials(html):
    ultimate_materials = {}
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')[1]

    td1 = table.find_all('td')[0]
    ultimatematerialimg = td1.find('img')['src']
    a1 = td1.find('a')
    ultimatematerialtext = a1.get_text(strip=True)
    ultimate_materials['img'] = ultimatematerialimg
    ultimate_materials['title'] = ultimatematerialtext

    td2 = table.find_all('td')[1]
    footageimg = td2.find('img')['src']
    a2 = td2.find('a')
    footagetext = a2.get_text(strip=True)
    ultimate_materials['footageimg'] = footageimg
    ultimate_materials['footagetitle'] = footagetext

    td3 = table.find_all('td')[2]
    universalimg = td3.find('img')['src']
    a3 = td3.find('a')
    universaltext = a3.get_text(strip=True)
    ultimate_materials['universalimg'] = universalimg
    ultimate_materials['universaltitle'] = universaltext


    return ultimate_materials


def getskillmaterials(html):
    skill_materials = {}
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('table')[2]
    tr = table.find_all('tr')[2]
    td1 = tr.find_all('td')[0]
    p1 = td1.find('p')
    elementaryimg = p1.find_all('img')[1]['src']
    a1 = td1.find_all('a')[1]
    elementarytext = a1.get_text(strip=True)
    skill_materials['elementaryimg'] = elementaryimg
    skill_materials['elementarytitle'] = elementarytext
    td2 = tr.find_all('td')[2]
    intermediateimg = td2.find_all('img')[1]['src']
    a2 = td2.find_all('a')[1]
    intermediatetext = a2.get_text(strip=True)
    skill_materials['intermediateimg'] = intermediateimg
    skill_materials['intermediatetitle'] = intermediatetext
    td3 = tr.find_all('td')[4]
    seniorimg = td3.find_all('img')[1]['src']
    a3 = td3.find_all('a')[1]
    seniortext = a3.get_text(strip=True)
    skill_materials['seniorimg'] = seniorimg
    skill_materials['seniortitle'] = seniortext
    td4 = tr.find_all('td')[5]
    ultimateimg = td4.find_all('img')[1]['src']
    a4 = td4.find_all('a')[1]
    ultimatetext = a4.get_text(strip=True)
    skill_materials['ultimateimg'] = ultimateimg
    skill_materials['ultimatetitle'] = ultimatetext
    extraimg = td4.find_all('img')[2]['src']
    a5 = td4.find_all('a')[2]
    extratext = a5.get_text(strip=True)
    skill_materials['extraimg'] = extraimg
    skill_materials['extratitle'] = extratext

    return skill_materials



