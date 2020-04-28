import datetime

from app import *


def prompt_int(prompt, default=None, print_selection=False):
    if default==None:
        selection = int(input('%s: ' % prompt))
    else:
        selection = input('%s [%s]: ' % (prompt, default))
        selection = default if len(selection.strip()) == 0 else int(selection)
    if print_selection:
        print(selection)
    return selection


def prompt_collection(prompt, collection, default=None, print_selection=False):
    for i, e in enumerate(collection):
        print('%i: %s' % (i, e))
    if default==None:
        selection = collection[int(input('%s: ' % prompt))]
    else:
        selection = input('%s [%s]: ' % (prompt, default))
        selection = collection[default if len(selection.strip()) == 0 else int(selection)]
    if print_selection:
        print(selection)
    return selection


def is_available(site, dates, site_availabilitys, equipment_id_subid):
    for i, date in enumerate(dates):
        if site_availabilitys[i].availability == 0:
            site_allowed_equipment_text = [(e.category_id, e.subcategory_id) for e in site_availabilitys[i].allowed_equipment]
            if equipment_id_subid not in site_allowed_equipment_text:
                return False
        else:
            return False
    return True


def print_site_availabilitys(site, dates, site_availabilitys, equipment_id_subid):
    print(site)
    for i, date in enumerate(dates):
        site_availability_text = 'not available'
        if site_availabilitys[i].availability == 0:
            site_allowed_equipment_text = [(e.category_id, e.subcategory_id) for e in site_availabilitys[i].allowed_equipment]
            site_availability_text = 'AVAILABLE' if equipment_id_subid in site_allowed_equipment_text else 'equipment not allowed'
        print('  %s %s' % (dates[i], site_availability_text))


if __name__ == '__main__':

    # how many people?
    party_size = prompt_int('NUMBER OF PEOPLE', 2)

    # camping dates
    now = datetime.datetime.now(datetime.timezone.utc)
    year = prompt_int('Year', now.year)
    start_month = prompt_int('Start Month', now.month)
    start_day = prompt_int('Start Day', now.day)
    end_month = prompt_int('End Month', start_month)
    end_day = prompt_int('End Day', start_day+1)
    start_date = datetime.datetime(year, start_month, start_day, 7, tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime(year, end_month, end_day, 7, tzinfo=datetime.timezone.utc)
    dates = [(start_date + datetime.timedelta(days=x)).strftime('%y-%b-%d') for x in range(0, (end_date-start_date).days)]
    if len(dates) == 0:
        raise Exception("must stay at least 1 night")

    # campsite, cabin, etc... TBD: does this work for non-campsites?
    resource_category = prompt_collection('SELECT A CATEGORY', list_resource_categorys(), 0, True)

    # pick tent, RV, etc
    equipment = prompt_collection('SELECT EQUIPMENT', list_equipments(), 0, True)

    # pick a camp
    camp = prompt_collection('SELECT A CAMP', list_camps(resource_category.resource_id))
    print(get_camp_description(camp.resource_location_id))

    # pick section of the camp
    camp_area = prompt_collection('SELECT A CAMP AREA', list_camp_areas(camp, start_date, end_date, equipment.subcategory_id), None, True)

    # list availability
    equipment_id_subid = (equipment.category_id, equipment.subcategory_id)
    for site, site_availabilitys in list_site_availability(camp_area, start_date, end_date, equipment.subcategory_id).items():
        print_site_availabilitys(site, dates, site_availabilitys, equipment_id_subid)

    # web link to make reservation
    print(get_reservation_link(party_size, start_date, end_date, camp_area, camp.resource_location_id, equipment.category_id, equipment.subcategory_id))