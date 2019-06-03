from collections import OrderedDict
import datetime
from dateutil import parser
from datatypes import Camp, CampArea, Equipment, ResourceCategory, Site, SiteAvailability
import requests
import uuid

HEADERS_JSON = {'Content-Type': 'application/json'}

ENDPOINTS = {
    'LIST_RESOURCECATEGORY': 'https://washington.goingtocamp.com/api/resourcecategory',
    'LIST_EQUIPMENT': ' https://washington.goingtocamp.com/api/equipment',
    'LIST_RESOURCESTATUS': 'https://washington.goingtocamp.com/api/availability/resourcestatus',
    'MAPDATA': 'https://washington.goingtocamp.com/api/maps/mapdatabyid',
    'LIST_CAMPGROUNDS': 'https://washington.goingtocamp.com/api/resourcelocation/rootmaps',
    'SITE_DETAILS': 'https://washington.goingtocamp.com/api/resource/details',
    'CAMP_DETAILS': 'https://washington.goingtocamp.com/api/resourcelocation/locationdetails',
    'DAILY_AVAILABILITY': 'https://washington.goingtocamp.com/api/availability/resourcedailyavailability',
}


def main():

    resource_categorys = list_resource_categorys()
    for i, rc in enumerate(resource_categorys):
        print(i, rc)
    print('SELECT A CATEGORY:')
    resource_category = resource_categorys[int(input())]
    print(resource_category)

    equipments = list_equipments()
    for i, e in enumerate(equipments):
        print(i, e)
    print('SELECT EQUIPMENT:')
    equipment = equipments[int(input())]
    print(equipment)

    # TBD: allow user to select equipment type... where to find?
    equipment_category_tent = -32767
    equipment_id_tent = -32768

    # pick a camp
    camps = list_camps(resource_category.resource_id)
    for i, camp in enumerate(camps):
        print(i, camp)
    print('SELECT A CAMP:')
    camp = camps[int(input())]
    detail = get_camp_detail(camp.resource_location_id)
    print(detail['localizedDetails'][0]['description'])

    # TBD: collect dates from user
    start_date_raw = '2019-07-01T07:00:00.000Z'
    end_date_raw = '2019-7-02T06:59:59.999Z'
    start_date = parser.parse(start_date_raw)
    end_date = parser.parse(end_date_raw)
    dates = [(start_date + datetime.timedelta(days=x)).strftime('%y-%b-%d') for x in range(0, (end_date+datetime.timedelta(days=2)-start_date).days)]

    # TBD: OOP and I/O
    camp_areas = list_camp_areas(camp.map_id, start_date_raw, end_date_raw, equipment.subcategory_id)
    for i, camp_area in enumerate(camp_areas):
        print(i, camp_area)
    print('SELECT A CAMP AREA:')
    camp_area = camp_areas[int(input())]
    print(camp_area)
    # TBD: not really sure what availabilityType and reservabilityStatus indicate/values
    # for site in list_sites(camp_area.map_id, start_date_raw, end_date_raw, equipment.subcategory_id):
    #     print('  ',site) # get_site_detail(resourceId)
    #     site_availabilitys = get_site_availability(site, start_date_raw, end_date_raw, equipment.subcategory_id)
    #     for i, site_availability in enumerate(site_availabilitys):
    #         print('    %s %s'%(dates[i],site_availability))
    for site, site_availabilitys in list_site_availability(camp_area.map_id, start_date_raw, end_date_raw, equipment.subcategory_id).items():
        print('  ',site) # get_site_detail(resourceId)
        for i, site_availability in enumerate(site_availabilitys):
            print('    %s %s'%(dates[i],site_availability.availability==0))


def list_resource_categorys():
    return [ResourceCategory(e['resourceCategoryId'],e['localizedValues'][0]['name']) for e in requests.get(ENDPOINTS['LIST_RESOURCECATEGORY']).json()]


def list_equipments():
    equipment_all = sorted(requests.get(ENDPOINTS['LIST_EQUIPMENT']).json(), key=lambda e: e['order'])
    equipment = equipment_all[0]['subEquipmentCategories']
    return [Equipment(e['subEquipmentCategoryId'],e['localizedValues'][0]['name']) for e in equipment]


def list_camps(resource_category_id):
    camps = []
    for camp in requests.get(ENDPOINTS['LIST_CAMPGROUNDS']).json():
        if camp['resourceLocationId'] and resource_category_id in camp['resourceCategoryIds']:
            camp = Camp(camp['resourceLocationLocalizedValues']['en-US'], camp['mapId'], camp['resourceLocationId'])
            camps.append(camp)
    return camps


def get_camp_detail(resourcelocationid):
    return requests.get(ENDPOINTS['CAMP_DETAILS'],params={'resourceLocationId':resourcelocationid}).json()


def get_site_detail(resourceId):
    return requests.get(ENDPOINTS['SITE_DETAILS'],params={'resourceId':resourceId}).json()


# def get_site_availability(site, start_date, end_date, equipment_id):
#     params = {
#         'resourceId': site.resource_id,
#         'cartUid':uuid.uuid4(),
#         'startDate':start_date,
#         'endDate': end_date,
#         'equipmentId':equipment_id
#     }
#     # return requests.get(ENDPOINTS['DAILY_AVAILABILITY'],params=params).json()
#     return [SiteAvailability(site, e['availabilityType'], e['reservabilityStatus']) for e in requests.get(ENDPOINTS['DAILY_AVAILABILITY'],params=params).json()]


def list_camp_areas(mapid, start_date, end_date, equipment_type):
    data = {
       'mapId':mapid,
       'bookingCategoryId':0,
       'startDate':start_date,
       'endDate':end_date,
       'isReserving':True,
       'getDailyAvailability':True,
       'partySize':1,
       'equipmentId':equipment_type,
       'subEquipmentId':equipment_type,
       'generateBreadcrumbs':False,
    }
    results = requests.post(ENDPOINTS['MAPDATA'], headers=HEADERS_JSON, json=data).json()
    camp_areas = []
    for map_id, info in results['mapLinkLocalizedValues'].items():
        for entry in info:
            camp_areas.append(CampArea(map_id, entry['title'],entry['description']))
    return camp_areas


def list_sites(map_id, start_date, end_date, equipment_type):
    data = {
       'mapId':map_id,
       'bookingCategoryId':0,
       'startDate':start_date,
       'endDate':end_date,
       'isReserving':True,
       'getDailyAvailability':True,
       'partySize':1,
       'equipmentId':equipment_type,
       'subEquipmentId':equipment_type,
       'generateBreadcrumbs':False,
    }
    results = requests.post(ENDPOINTS['MAPDATA'], headers=HEADERS_JSON, json=data).json()
    sites = []
    for entry in results['resourcesOnMap']:
        sites.append(Site(entry['resourceId'], entry['localizedValues'][0]['name'],entry['localizedValues'][0]['description']))
    sites.sort(key=lambda site: site.name.zfill(3))
    return sites


def list_site_availability(map_id, start_date, end_date, equipment_type):
    data = {
       'mapId':map_id,
       'bookingCategoryId':0,
       'startDate':start_date,
       'endDate':end_date,
       'isReserving':True,
       'getDailyAvailability':True,
       'partySize':1,
       'equipmentId':equipment_type,
       'subEquipmentId':equipment_type,
       'generateBreadcrumbs':False,
    }
    results = requests.post(ENDPOINTS['MAPDATA'], headers=HEADERS_JSON, json=data).json()
    sites_availability = {}
    for entry in results['resourcesOnMap']:
        site = Site(entry['resourceId'], entry['localizedValues'][0]['name'],entry['localizedValues'][0]['description'])
        availability = [
            SiteAvailability(site, e['availability'])
            for e in results['resourceAvailabilityMap'][str(site.resource_id)]
        ]
        sites_availability[site] = availability
    return OrderedDict(sorted(sites_availability.items(), key=lambda sa: sa[0].name.zfill(3)))


if __name__ == '__main__':
    main()