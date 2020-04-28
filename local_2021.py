from console import *


def search(party_size, year, start_month, start_day, end_month, end_day, resource_category, equipment, max_camps=0):
    # sanity check
    start_date = datetime.datetime(year, start_month, start_day, 7, tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime(year, end_month, end_day, 7, tzinfo=datetime.timezone.utc)
    dates = [(start_date + datetime.timedelta(days=x)).strftime('%y-%b-%d') for x in range(0, (end_date-start_date).days)]
    if len(dates) == 0:
        raise Exception("must stay at least 1 night")
    equipment_id_subid = (equipment.category_id, equipment.subcategory_id)
    # search
    print('%s, %s, %s, %s ppl' %(dates,resource_category,equipment,party_size))
    if max_camps:
        camps = list_camps(resource_category.resource_id)[:max_camps]
    else:
        camps = list_camps(resource_category.resource_id)
    for camp in camps:
        output = []
        for camp_area in list_camp_areas(camp, start_date, end_date, equipment.subcategory_id):
            equipment_id_subid = (equipment.category_id, equipment.subcategory_id)
            available_sites = []
            for site, site_availabilitys in list_site_availability(camp_area, start_date, end_date, equipment.subcategory_id).items():
                if is_available(site, dates, site_availabilitys, equipment_id_subid):
                    available_sites.append(site.name)
            if(len(available_sites)):
                output.append('    %s: %s' %(camp_area, available_sites))
                reservation_link = get_reservation_link(party_size, start_date, end_date, camp_area, camp.resource_location_id, equipment.category_id, equipment.subcategory_id)
                output.append('    %s' %reservation_link)
        if output:
            print('  %s'%get_camp_description(camp.resource_location_id))
            for line in output:
                print(line)


if __name__ == '__main__':
    resource_category = list_resource_categorys()[0] #campground
    equipment = list_equipments()[0] #1tent
    party_size = 4
    year = 2020
    max_camps = 2
    search(party_size, year, 6, 15, 5, 28, resource_category, equipment, max_camps)
    # search(party_size, year, 5, 26, 6, 28, resource_category, equipment, max_camps)