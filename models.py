class Equipment:

    def __init__(self, category_id, subcategory_id, name):
        self.category_id=category_id
        self.subcategory_id = subcategory_id
        self.name = name

    def __repr__(self):
        return self.name


class ResourceCategory:

    def __init__(self, resource_id, name):
        self.resource_id = resource_id
        self.name = name

    def __repr__(self):
        return self.name


class Camp:

    def __init__(self, name, map_id, resource_location_id):
        self.name = name
        self.map_id = map_id
        self.resource_location_id = resource_location_id

    def __repr__(self):
        return self.name


class CampArea:

    def __init__(self, map_id, name, description):
        self.map_id = map_id
        self.name = name
        self.description = description

    def __repr__(self):
        return '%s: %s ' %(self.name,self.description)


class Site:

    def __init__(self, resource_id, name, description):
        self.resource_id = resource_id
        self.name = name
        self.description = description

    def __repr__(self):
        return '%s: %s'%(self.name,self.description)


class SiteAvailability:

    def __init__(self, site, availability, allowed_equipment):
        self.site = site
        self.availability = availability
        self.allowed_equipment = allowed_equipment

    def __repr__(self):
        return '%s: %s'%(self.site.name,self.availability)