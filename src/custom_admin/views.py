from django.shortcuts import render, get_object_or_404

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AngelViewSerializer

from .models import *

# scraping modules
import urllib2
import urllib
from bs4 import BeautifulSoup

import time
from datetime import datetime
import dateutil.relativedelta

from selenium import webdriver

from django_cron import CronJobBase, Schedule

## this  is  api not a scheduler.
class AngelView(APIView):

    def moreData(self, soup, driver):
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        results = soup.find("div", {"class":"results"})
        
        companies = results.find_all("div", {"class": "base startup"})
        li = []

        for data in companies:
            name = data.find("div", {"name"}).a
            description = data.find("div", {"pitch"})
            image_url  = data.find("div", {"photo"}).img.get("src")
            joined = data.find("div", {"column joined"}).find("div", {"value"})
            location = data.find("div", {"column location"}).find("div", {"tag"})
            market = data.find("div", {"column market"}).find("div", {"tag"})
            website = data.find("div", {"column website"}).find("div", {"website"})
            employee =  data.find("div", {"column company_size"}).find("div", {"value"})
            stage = data.find("div", {"column stage"}).find("div", {"value"})
            total_raised = data.find("div", {"column hidden_column raised"}).find("div", {"value"})
            newDict = {
                'name': name.text,
                'description': description.text.strip() if description else '-',
                'image_url': image_url if image_url else '-',
                'joined': joined.text.strip() if joined else '-',
                'location': location.text if location else '-',
                'market': market.text if market else '-',
                'website': website.a.text if website else '-',
                'employee': employee.text.strip() if employee else '-',
                'stage': stage.text.strip() if stage else '-',
                'total_raised': total_raised.text.strip() if total_raised else '-'
            }
            print newDict
            result = CompaniesData.objects.filter(website__contains=newDict['website'])
            if not result or newDict['website'] == '-':
                CompaniesData.objects.create(name=newDict['name'], description=newDict['description'], image_url=newDict['image_url'], joined=newDict['joined'], location=newDict['location'], market= newDict['market'], website= newDict['website'], employees = newDict['employee'], stage = newDict['stage'], total_raised=newDict['total_raised'])
            li.append(
                    newDict
                )
        return li

    def post(self, request, url=None, format=None):
        driver = webdriver.PhantomJS()
        if not url:
            url = "https://angel.co/companies"
        driver.get(url)

        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        lst = []
        flag = True
        page = 2
        while (flag == True):
            moreButton = soup.find("div", {"class":"more"})

            if moreButton or page == 2:
                time.sleep(3)
                lst = lst  + self.moreData(soup, driver)
                if moreButton:
                    next_page = driver.find_element_by_class_name("more")
                    next_page.click()
                else:
                    flag = False
                page = page+1
                if page == 21:
                    driver.quit()
                    flag = False
            else:
                flag = False

        return Response(lst, status=200)


## It is schadular
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'angel.my_cron_job'    # a unique code

    def moreData(self, soup, driver, filterDict):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find("div", {"class":"results"})
        li = []
        if results:
            companies = results.find_all("div", {"class": "base startup"})
            for data in companies:
                checkJoin = data.find("div", {"column joined"}) if data.find("div", {"column joined"}) else data.find("div", {"column hidden_column joined"})
                checkLocation = data.find("div", {"column location"}) if data.find("div", {"column location"}) else data.find("div", {"column hidden_column location"})
                checkMarket = data.find("div", {"column market"}) if data.find("div", {"column market"}) else data.find("div", {"column hidden_column market"})
                checkWebsite = data.find("div", {"column website"}) if data.find("div", {"column website"}) else data.find("div", {"column hidden_column website"})
                checkEmp = data.find("div", {"column company_size"}) if data.find("div", {"column company_size"}) else data.find("div", {"column company_size hidden_column"})
                checkStage = data.find("div", {"column stage"}) if data.find("div", {"column stage"}) else data.find("div", {"column hidden_column stage"})
                checkTotal = data.find("div", {"column raised"}) if data.find("div", {"column raised"}) else data.find("div", {"column hidden_column raised"})

                name = data.find("div", {"name"}).a
                description = data.find("div", {"pitch"})
                image_url  = data.find("div", {"photo"}).img.get("src")
                joined = checkJoin.find("div", {"value"})
                location = checkLocation.find("div", {"tag"})
                market = checkMarket.find("div", {"tag"})
                website = checkWebsite.find("div", {"website"})
                employee =  checkEmp.find("div", {"value"})
                stage = checkStage.find("div", {"value"})
                total_raised = checkTotal.find("div", {"value"})
                newDict = {
                    'name': name.text,
                    'description': description.text.strip() if description else '-',
                    'image_url': image_url if image_url else '-',
                    'joined': joined.text.strip() if joined else '-',
                    'location': location.text if location else '-',
                    'market': market.text if market else '-',
                    'website': website.a.text if website else '-',
                    'employee': employee.text.strip() if employee else '-',
                    'stage': stage.text.strip() if stage else '-',
                    'total_raised': total_raised.text.strip() if total_raised else '-'
                }
                print newDict
                result = CompaniesData.objects.filter(website__contains=newDict['website'])

                listFilter = ListSector.objects.get(id=filterDict['list']) if filterDict['list'] != '' else None
                typeFilter = TypeSector.objects.get(id=filterDict['type']) if filterDict['type'] != '' else None
                locationFilter = LocationSector.objects.get(id=filterDict['location']) if filterDict['location'] != '' else None
                marketFilter = MarketSector.objects.get(id=filterDict['market']) if filterDict['market'] != '' else None
                stageFilter = StageSector.objects.get(id=filterDict['stage']) if filterDict['stage'] != '' else None

                if not result or newDict['website'] == '-':
                    CompaniesData.objects.create(name=newDict['name'], description=newDict['description'], image_url=newDict['image_url'], joined=newDict['joined'], location=newDict['location'], market= newDict['market'], website= newDict['website'], employees = newDict['employee'], stage = newDict['stage'], total_raised=newDict['total_raised'], lists=listFilter, types=typeFilter, locationfil=locationFilter, marketfil=marketFilter, stagefil=stageFilter )
                li.append(
                        newDict
                    )
        return li

    def scraper(self, url=None, filterDict=None):
        # driver = webdriver.Firefox()
        driver = webdriver.PhantomJS()
        if not url:
            url = "https://angel.co/companies"
        driver.get(url)

        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        lst = []
        flag = True
        page = 2
        while (flag == True):
            moreButton = soup.find("div", {"class":"more"})

            if moreButton or page == 2:
                time.sleep(5)
                lst = lst  + self.moreData(soup, driver, filterDict)
                if moreButton:
                    next_page = driver.find_element_by_class_name("more")
                    next_page.click()
                page = page+1
                if page == 21:
                    driver.quit()
                    flag = False
            else:
                flag = False

        return True

    def do(self):
        query = Schedular.objects.all()
        for data in query:
            queryVal =  data.query if data.query else ''
            typeVal = data.types.name if data.types else ''
            locationVal =  data.location.name if data.location else ''
            marketVal = data.market.name if data.market else ''
            stageVal = data.stage.name if data.stage else ''

            if data.lists and data.lists.id == 1:
                url = "https://angel.co/companies?featured=Featured&keywords="+queryVal.strip().replace(" ", "+")+"&company_types[]="+typeVal.strip().replace(" ", "+")+"&locations[]="+locationVal.strip().replace(" ", "+")+"&markets[]="+marketVal.strip().replace(" ", "+")+"&stage="+stageVal.strip().replace(" ", "+")
            elif data.lists and data.lists.id == 2:
                url = "https://angel.co/companies?in_done_deals=Done+Deals&keywords="+queryVal.strip().replace(" ", "+")+"&company_types[]="+typeVal.strip().replace(" ", "+")+"&locations[]="+locationVal.strip().replace(" ", "+")+"&markets[]="+marketVal.strip().replace(" ", "+")+"&stage="+stageVal.strip().replace(" ", "+")
            else:
                url = "https://angel.co/companies?keywords="+queryVal.strip().replace(" ", "+")+"&company_types[]="+typeVal.strip().replace(" ", "+")+"&locations[]="+locationVal.strip().replace(" ", "+")+"&markets[]="+marketVal.strip().replace(" ", "+")+"&stage="+stageVal.strip().replace(" ", "+")
            print url

            filterDict = {
                'list': data.lists.id if data.lists else '',
                'type': data.types.id if data.types else '',
                'location': data.location.id if data.location else '',
                'market': data.market.id if data.market else '',
                'stage': data.stage.id if data.stage else ''
            }

            if data.selection.id == 2:
                schDate = str(data.schedule_date).split(' ')[0]
                todayDate = str(datetime.now()).split(' ')[0]

                if schDate == todayDate:
                    self.scraper(url, filterDict)
                    extended_date = data.schedule_date + dateutil.relativedelta.relativedelta(months=1)
                    Schedular.objects.filter(id=data.id).update(schedule_date=extended_date)
                    print extended_date
            else:
                self.scraper(url, filterDict)
        #driver.quit()


### not used code for testing purpose.
class TestView(APIView):
    urlopener = urllib2.build_opener()
    urlopener.addheaders = [('User-agent', 'Mozilla/5.0')]

    def post(self, request, format=None):

        if 'q' not in request.data:
            content = {
                'message' : "Parameter Missing",
            }
            return Response(content, status=400)
        page = 1
        li = []
        id = 1
        flag = True
        while (flag == True):
            if 'types' in request.data:
            	typeUser = request.data['types']
                html = self.urlopener.open('https://angel.co/search?q=%s&page=%s&type=%s'%(request.data['q'], page, request.data['types']))
            else:
            	typeUser = 'all'
                html = self.urlopener.open('https://angel.co/search?q=%s&page=%s'%(request.data['q'],page))
            soup = BeautifulSoup(html, 'html.parser')
            findResult = soup.find_all('div', {'class': 'result'})
            typeId = PostType.objects.filter(name=request.data['types'])
            if not typeId:
                typeId  = PostType.objects.create(name=request.data['types'])
                idType = typeId.id
            else:
                idType = typeId[0].id
            page = page+1
            if findResult:
                for data in findResult:
                    pic_val = data.find('div', {'class':  'result-pic'})
                    data_user = data.find('div', {'class':  'body'})

                    urlData = data_user.a.get('href').split('&')[-1]
                    urlEncoded = urlData.split('=')[1]

                    url=urllib.unquote(urlEncoded).decode('utf8')

                    result = Angel.objects.filter(url__contains=url)

                    picture = pic_val.img.get('src').split('?')[0]
                    
                    newDict = {
                        'id': id,
                        'pic': picture,
                        'url': url,
                        'name': data_user.a.text,
                        'type': typeUser,
                    }
                    
                    if not result:
                        Angel.objects.create(types_id=idType, name=str(data_user.a.text), pic=picture, url=url)

                    li.append(
                        newDict
                    )
                    id = id+1
            if not findResult:
                flag = False

        return Response(li, status=200)