from collections import OrderedDict
from datetime import timedelta
import requests

from models import Camp, CampArea, Equipment, ResourceCategory, Site, SiteAvailability


ENDPOINTS = {
    'LIST_RESOURCECATEGORY': 'https://washington.goingtocamp.com/api/resourcecategory',
    'LIST_EQUIPMENT': 'https://washington.goingtocamp.com/api/equipment',
    'LIST_RESOURCESTATUS': 'https://washington.goingtocamp.com/api/availability/resourcestatus',
    'MAPDATA': 'https://washington.goingtocamp.com/api/maps/mapdatabyid',
    'LIST_CAMPGROUNDS': 'https://washington.goingtocamp.com/api/resourcelocation/rootmaps',
    'SITE_DETAILS': 'https://washington.goingtocamp.com/api/resource/details',
    'CAMP_DETAILS': 'https://washington.goingtocamp.com/api/resourcelocation/locationdetails',
    'DAILY_AVAILABILITY': 'https://washington.goingtocamp.com/api/availability/resourcedailyavailability',
}


def get_json(endpoint, params=None):
    return requests.get(ENDPOINTS[endpoint], params=params).json()


def post_json(endpoint, data=None):
    return requests.post(ENDPOINTS[endpoint], headers={'Content-Type': 'application/json'}, json=data).json()


def get_reservation_link(party_size, start_date, end_date, map_id, resource_location_id, equipment_id, sub_equipment_id):
    return\
        'https://washington.goingtocamp.com/create-booking/results?mapId=%s&bookingCategoryId=0&startDate=%s&endDate=%s&isReserving=true&equipmentId=%s&subEquipmentId=%s&partySize=%s&resourceLocationId=%s'\
        %(map_id, start_date.isoformat(), end_date.isoformat(), equipment_id, sub_equipment_id, party_size, resource_location_id)


def list_resource_categorys():
    return [ResourceCategory(e['resourceCategoryId'],e['localizedValues'][0]['name']) for e in get_json('LIST_RESOURCECATEGORY')]


def list_equipments():
    equipments = []
    equipment_all = sorted(get_json('LIST_EQUIPMENT'), key=lambda e: e['order'])
    for category in equipment_all:
        equipment = category['subEquipmentCategories']
        equipments.extend([Equipment(category['equipmentCategoryId'],e['subEquipmentCategoryId'],e['localizedValues'][0]['name']) for e in equipment])
    return equipments


def list_camps(resource_category_id):
    camps = []
    for camp in get_json('LIST_CAMPGROUNDS'):
        if camp['resourceLocationId'] and resource_category_id in camp['resourceCategoryIds']:
            camp = Camp(camp['resourceLocationLocalizedValues']['en-US'], camp['mapId'], camp['resourceLocationId'])
            camps.append(camp)
    return camps


def get_camp_detail(resourcelocationid):
    return get_json('CAMP_DETAILS', {'resourceLocationId':resourcelocationid})


def get_site_detail(resourceId):
    return get_json('SITE_DETAILS', {'resourceId':resourceId})


def list_camp_areas(mapid, start_date, end_date, equipment_type):
    data = {
       'mapId':mapid,
       'bookingCategoryId':0,
       'startDate':start_date.isoformat(),
       'endDate':end_date.isoformat(),
       'isReserving':True,
       'getDailyAvailability':True,
       'partySize':1,
       'equipmentId':equipment_type,
       'subEquipmentId':equipment_type,
       'generateBreadcrumbs':False,
    }
    results = post_json('MAPDATA', data)
    camp_areas = []
    for map_id, info in results['mapLinkLocalizedValues'].items():
        for entry in info:
            camp_areas.append(CampArea(map_id, entry['title'],entry['description']))
    return camp_areas


def list_sites(map_id, start_date, end_date, equipment_type):
    data = {
       'mapId':map_id,
       'bookingCategoryId':0,
       'startDate':start_date.isoformat(),
       'endDate':end_date.isoformat(),
       'isReserving':True,
       'getDailyAvailability':True,
       'partySize':1,
       'equipmentId':equipment_type,
       'subEquipmentId':equipment_type,
       'generateBreadcrumbs':False,
    }
    results = post_json('MAPDATA', data)
    sites = []
    for entry in results['resourcesOnMap']:
        sites.append(Site(entry['resourceId'], entry['localizedValues'][0]['name'],entry['localizedValues'][0]['description']))
    sites.sort(key=lambda site: site.name.zfill(3))
    return sites


def list_site_availability(map_id, start_date, end_date, equipment_type):
    data = {
       'mapId':map_id,
       'bookingCategoryId':0,
       'startDate':start_date.isoformat(),
       'endDate':end_date.isoformat(),
       'isReserving':True,
       'getDailyAvailability':True,
       'partySize':1,
       'equipmentId':equipment_type,
       'subEquipmentId':equipment_type,
       'generateBreadcrumbs':False,
    }
    results = post_json('MAPDATA', data)
    sites_availability = {}
    for entry in results['resourcesOnMap']:
        site = Site(entry['resourceId'], entry['localizedValues'][0]['name'],entry['localizedValues'][0]['description'])
        allowed_equipment = [Equipment(e['item1'],e['item2'], None) for e in entry['allowedEquipment']]
        availability = [
            SiteAvailability(site, e['availability'], allowed_equipment)
            for e in results['resourceAvailabilityMap'][str(site.resource_id)]
        ]
        sites_availability[site] = availability
    return OrderedDict(sorted(sites_availability.items(), key=lambda sa: sa[0].name.zfill(3)))