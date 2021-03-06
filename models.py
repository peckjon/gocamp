class Equipment:
    """
    Tent, trailer, etc
    """

    def __init__(self, category_id, subcategory_id, name):
        self.category_id=category_id
        self.subcategory_id = subcategory_id
        self.name = name

    def __repr__(self):
        return self.name


class ResourceCategory:
    """
    Campsite, yurt, etc
    """

    def __init__(self, resource_id, name):
        self.resource_id = resource_id
        self.name = name

    def __repr__(self):
        return self.name


class Camp:
    """
    A state park
    """

    def __init__(self, map_id, resource_location_id, name):
        self.map_id = map_id
        self.resource_location_id = resource_location_id
        self.name = name

    def __repr__(self):
        return self.name


class CampArea:
    """
    section / "loop" of a park
    """

    def __init__(self, map_id, name, description):
        self.map_id = map_id
        self.name = name
        self.description = description

    def __repr__(self):
        return '%s: %s ' %(self.name,self.description)


class Site:
    """
    Individual campsite, boat slip, etc
    """

    def __init__(self, resource_id, name, description):
        self.resource_id = resource_id
        self.name = name
        self.description = description

    def __repr__(self):
        if self.description:
            return '%s (%s)'%(self.name,self.description)
        else:
            return self.name


class SiteAvailability:
    """
    Can this site be reserved on a specific date
    """

    def __init__(self, site, availability, allowed_equipment):
        self.site = site
        self.availability = availability
        self.allowed_equipment = allowed_equipment

    def __repr__(self):
        return '%s: %s'%(self.site.name,self.availability)