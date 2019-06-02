import requests
import uuid
from camp import Camp

RESOURCECATEGORY_CAMPGROUND = -2147483648  # from LIST_RESOURCETYPES

HEADERS_JSON = {'Content-Type': 'application/json'}

ENDPOINTS = {
    'LIST_RESOURCETYPES': 'https://washington.goingtocamp.com/api/resourcecategory',
    'LIST_RESOURCESTATUS': 'https://washington.goingtocamp.com/api/availability/resourcestatus',
    'MAPDATA': 'https://washington.goingtocamp.com/api/maps/mapdatabyid',
    'LIST_CAMPGROUNDS': 'https://washington.goingtocamp.com/api/resourcelocation/rootmaps',
    'SITE_DETAILS': 'https://washington.goingtocamp.com/api/resource/details',
    'CAMP_DETAILS': 'https://washington.goingtocamp.com/api/resourcelocation/locationdetails',
    'DAILY_AVAILABILITY': 'https://washington.goingtocamp.com/api/availability/resourcedailyavailability',
}


def main():
    camps = list_camps(RESOURCECATEGORY_CAMPGROUND)
    for i, camp in enumerate(camps):
        print(i, camp.name)
    print("Camp:")
    camp = camps[int(input())]
    detail = get_camp_detail(camp.resource_location_id)
    print(detail['localizedDetails'][0]['description'])

    for camp_area_id, camp_area_info in list_camp_areas(camp.map_id).items():
        print(camp_area_info)
        sites = get_site_availability(camp_area_id)
        for site in sites:
            site_info = get_site_detail(camp_area_id)
            print(' SITE:%s'%site_info)
            print(' AVAIL:%s'%site)


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


def get_site_availability(resourceId):
    params = {
        'resourceId': resourceId,
        'cartUid':uuid.uuid4(),
        'startDate':'2019-07-01T07:00:00.000Z',
        'endDate':'2020-10-01T06:59:59.999Z',
        'equipmentId':'32768'

    }
    return requests.get(ENDPOINTS['DAILY_AVAILABILITY'],params=params).json()


def list_camp_areas(mapid):
    data = {
       'mapId':mapid,
       'bookingVersion':{
          'bookingCapacityCategoryCounts':[
             {
                'capacityCategoryId':-32767,
                'subCapacityCategoryId':None,
                'count':1
             }
          ],
          'rateCategoryId':-32768,
          'startDate':'2019-06-01T14:00:00.000Z',
          'endDate':'2019-06-02T14:00:00.000Z',
          'releasePersonalInformation':False,
          'equipmentCategoryId':-32768,
          'subEquipmentCategoryId':-32768,
          'requiresCheckout':False,
          'bookingStatus':0,
          'completedDate':'2019-06-01T12:38:32.676Z'
       },
       'bookingCategoryId':0,
       'startDate':'2019-06-01T07:00:00.000Z',
       'endDate':'2019-06-02T07:00:00.000Z',
       'isReserving':False,
       'getDailyAvailability':True,
       'partySize':1,
       'equipmentId':-32768,
       'subEquipmentId':-32768,
       'generateBreadcrumbs':False
    }
    results = requests.post(ENDPOINTS['MAPDATA'], headers=HEADERS_JSON, json=data).json()
    camp_areas_by_id = {}
    for id, info in results['mapLinkLocalizedValues'].items():
        camp_areas_by_id[id] = [(entry['title'],entry['description']) for entry in info]
    return camp_areas_by_id


if __name__ == "__main__":
    main()