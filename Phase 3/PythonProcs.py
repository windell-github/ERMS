# lets keep all our sql functions in here to make it easy on the TA's.
from string import Template


def getUserData(name, password):
    s = Template('SELECT name FROM cs6400_su18_team039.User WHERE username = "$name" AND password = "$password"')
    return s.substitute(name=name, password=password)


def getUserInfo(name):
    s = Template('SELECT name FROM cs6400_su18_team039.User WHERE username = "$name"')
    return s.substitute(name=name)


def getIncidentName(incidentId):
    s = Template('SELECT description FROM cs6400_su18_team039.Incident WHERE id = "$incidentId"')
    return s.substitute(incidentId=incidentId)


def getMunicipalityInfo(username):
    s = Template('SELECT category FROM Municipality WHERE username = "$username";')
    return s.substitute(username=username)


def getGovernmentInfo(username):
    s = Template('SELECT local_office, agency_name FROM GovernmentAgency WHERE username = "$username";')
    return s.substitute(username=username)


def getHeadQuartersInfo(username):
    s = Template('SELECT headquarters, number_of_employees FROM Company WHERE username = "$username";')
    return s.substitute(username=username)


def getDeclarations():
    s = 'SELECT declaration_description, declaration_abbreviation FROM Declaration;'
    return s


def getESF():
    s = 'SELECT ESF_DESCRIPTION, ESF_DESIGNATION FROM ESF;'
    return s


def getAddESF(primaryESF):
    s = Template('SELECT ESF_DESCRIPTION, ESF_DESIGNATION FROM ESF WHERE ESF_DESCRIPTION != "$primaryESF";')
    return s.substitute(primaryESF=primaryESF)


def getIncidents(username):
    s = Template('SELECT id, description FROM Incident WHERE owner = "$username";')
    return s.substitute(username=username)


def getDeclaration(abbr):
    s = Template('SELECT declaration_type FROM Declaration WHERE Declaration.declaration_abbreviation="$abbr";')
    return s.substitute(abbr=abbr)


def getNumberOfIncidentsWithDeclaration(dec):
    s = Template('SELECT COUNT(declaration) FROM Incident WHERE Incident.declaration="$dec";')
    return s.substitute(dec=dec)


def insertRequest(username, incidentId, resourceId, date):
    s = Template('''INSERT into Request (username, id_incident, id_resource, expected_return_date) 
    VALUES("$username","$incidentId","$resourceId", "$date");''')
    return s.substitute(username=username, incidentId=incidentId, resourceId=resourceId, date=date)

def insertDeploy(incidentId, resourceId):
    s = Template('INSERT into Deployed (id_incident, id_resource, date_deployed) VALUES("$incidentId","$resourceId",CURDATE());')
    return s.substitute(incidentId=incidentId, resourceId=resourceId)


def insertRqu(_id, _username, description, d, dec_type, lat, longitude):
    s = Template('''INSERT into Incident (id, owner, description, date, declaration, 
           location_latitude, location_longitude) VALUES("$id","$user","$des","$d","$dec","$lat","$lon");''')
    return s.substitute(id=_id, user=_username, des=description, d=d, dec=dec_type, lat=lat, lon=longitude)


def getCost(costAmount, costPer):
    s = Template('SELECT cost_ID FROM Cost WHERE amount ="$costAmount" AND unit_of_measure = "$costPer";')
    return s.substitute(costAmount=costAmount, costPer=costPer)


def insertCost(costAmount, costPer):
    s = Template('INSERT INTO Cost (amount, unit_of_measure) VALUES("$costAmount","$costPer");')
    return s.substitute(costAmount=costAmount, costPer=costPer)


def insertAddEsf(resourceID, addEsfCurrent):
    s = Template('INSERT INTO HasSecondaryEsfDesignation (id, esf_designation) VALUES("$resourceID", "$addEsfCurrent");')
    return s.substitute(resourceID=resourceID, addEsfCurrent=addEsfCurrent)


def insertCapability(resourceID, capability):
    s = Template('INSERT INTO ResourceCapability (id, capability) VALUES("$resourceID", "$capability");')
    return s.substitute(resourceID=resourceID, capability=capability)


def getEsfDesignation(esfPrimaryDescription):
    s = Template('''SELECT esf_designation FROM ESF WHERE esf_description = "$esfPrimaryDescription";''')
    return s.substitute(esfPrimaryDescription=esfPrimaryDescription)


def insertResource(_username, description, status, maxDistance, model, latitude, longitude, costID,
                   esf_primary_designation):
    if isinstance(maxDistance, unicode):
        s = Template('''INSERT into Resource (owner, name, status, model, home_location_latitude, 
        home_location_longitude, cost_id, esf_primary_designation) VALUES("$_username", "$description", "$status" , "$model", 
        "$latitude", "$longitude", "$costID", "$esf_primary_designation");''')
    else:
        s = Template('''INSERT into Resource (owner, name, status, max_distance, model, home_location_latitude, 
        home_location_longitude, cost_id, esf_primary_designation) VALUES("$_username", "$description", "$status", 
        "$maxDistance", "$model", "$latitude", "$longitude", "$costID", "$esf_primary_designation");''')
    return s.substitute(_username=_username, description=description, status=status, maxDistance=maxDistance,
                        model=model, latitude=latitude, longitude=longitude, costID=costID,
                        esf_primary_designation=esf_primary_designation)


def getReportInformation(user):
    s = Template('''SELECT ESF.ESF_designation,ESF.ESF_description,
                    SUM(CASE when Resource.owner='$user' then 1 else 0 end) 'Total_Resources',
                    SUM(CASE when Resource.status='IN USE' then 1 else 0 end) 'Resources_In_Use'
                    FROM ESF
                    Left JOIN Resource ON ESF.esf_designation = Resource.ESF_primary_designation
                    GROUP BY ESF.ESF_designation
                    Order By ESF.esf_designation;''')
    return s.substitute(user=user)


def getNextResourceID():
    s = 'SELECT MAX(id) + 1 FROM Resource;'
    return s


def getMaxResourceID():
    s = 'SELECT MAX(id) FROM Resource;'
    return s


def getCostPer():
    s = 'SELECT UNIT_OF_MEASURE FROM CostPer;'
    return s


def getDistance(incident):
    s = Template('''SELECT @lat2 := r.home_location_latitude, @lon2 := r.home_location_longitude, 
    @lat1 := i.location_latitude, @lon1 := i.location_longitude, @dlat := @lat2 - @lat1, 
    @dlon := @lon2 - @lon1, @a := POW(SIN(RADIANS(@dlat)/2),2) + 
    (COS(RADIANS(@lat1))*COS(RADIANS(@lat2))*POW(SIN(RADIANS(@dlon)/2),2)), @c := 2*ATAN2(SQRT(@a),SQRT(1-@a)),
     r.id, r.name, r.owner, c.amount, c.unit_of_measure, r.status, @e='', @d := 6371*@c AS Distance 
     FROM Resource r, Incident i, Cost c WHERE r.cost_id=c.cost_id AND i.id="$incident"  
     ORDER BY Distance;''')
    return s.substitute(incident=incident)


def getKeywordResult(keyword):
    s = Template('''SELECT DISTINCT r.id, r.name, r.owner, c.amount, c.unit_of_measure, r.status, req.expected_return_date FROM Resource r
		    LEFT JOIN ResourceCapability rc ON rc.id = r.id
		    LEFT JOIN Cost c ON c.cost_id = r.cost_id
		    LEFT JOIN Request req ON req.id_resource = r.id
		    WHERE (r.name LIKE "%$keyword%" OR r.model LIKE "%$keyword%" OR rc.capability LIKE "%$keyword%");''')
    return s.substitute(keyword=keyword)

def findResourceByEesf(esf):
    s = Template('''SELECT DISTINCT r.id, r.name, r.owner, c.amount, c.unit_of_measure, r.status, req.expected_return_date FROM Resource r
            LEFT OUTER JOIN HasSecondaryESFDesignation h ON r.id = h.id
            LEFT JOIN Cost c ON c.cost_id = r.cost_id
            LEFT JOIN Request req ON req.id_resource = r.id
            WHERE r.cost_id = c.cost_id AND (r.esf_primary_designation="$esf" OR h.esf_designation = "$esf");''')
    return s.substitute(esf=esf)

def findAllResources():
    s = Template('''SELECT DISTINCT r.id, r.name, r.owner, c.amount, c.unit_of_measure, r.status, req.expected_return_date FROM Resource r
            LEFT OUTER JOIN HasSecondaryESFDesignation h ON r.id = h.id
            LEFT OUTER JOIN Cost c ON c.cost_id = r.cost_id
            LEFT JOIN Request req ON req.id_resource = r.id
            WHERE r.cost_id = c.cost_id;''')
    return s.substitute()

def getReturnDate(resourceID):
    s = Template('SELECT expected_return_date FROM Request r, Deployed d WHERE r.id_resource = "$resourceID" AND r.id_incident = d.id_incident;')
    return s.substitute(resourceID=resourceID)


def getDeployedAlready(incidentId, resourceId):
    s = Template('SELECT * FROM Deployed d WHERE d.id_incident="$incidentId" AND d.id_resource="$resourceId";')
    return s.substitute(incidentId=incidentId, resourceId=resourceId)


def getProximityResources():
    s = 'SELECT r.id, r.name, r.owner, c.amount,c.unit_of_measure, r.status FROM Resource r, Cost c WHERE c.cost_id=r.cost_id;'
    return s

def getResourcesInUse(username):
    s = Template('''SELECT r.id, r.name, i.description, r.owner, dep.date_deployed, IFNULL(req.expected_return_date, 'Not Listed'), i.id as id_incident
                    FROM Deployed dep
                    LEFT JOIN Resource r ON r.id = dep.id_resource
                    LEFT JOIN Incident i ON i.id = dep.id_incident
                    LEFT JOIN Request req 
                    ON req.id_resource = dep.id_resource AND req.id_incident = dep.id_incident
                    WHERE r.status = "IN USE" AND i.owner = "$username" AND dep.actual_return_date IS Null;''')
    return s.substitute(username=username)


def getResourcesRequested(username):
    s = Template('''SELECT r.id, r.name, i.description, r.owner, IFNULL(req.expected_return_date, 'Not Listed')
                    FROM Request req
                    LEFT JOIN Resource r ON r.id = req.id_resource
                    LEFT JOIN Incident i ON i.id = req.id_incident
                    LEFT OUTER JOIN Deployed dep ON req.id_incident = dep.id_incident AND req.id_resource = dep.id_resource
                    WHERE req.username = "$username" AND dep.date_deployed IS NULL;''')
    return s.substitute(username=username)


def getResourceRequestsReceived(username):
    s = Template('''SELECT r.id, r.name, i.description, req.username, IFNULL(req.expected_return_date, 'Not Listed'), r.status, i.id as id_incident  
                    FROM Request req
                    LEFT JOIN Resource r ON r.id = req.id_resource
                    LEFT JOIN Incident i ON i.id = req.id_incident
                    LEFT OUTER JOIN Deployed dep ON req.id_incident = dep.id_incident AND req.id_resource = dep.id_resource
                    WHERE r.owner = "$username" AND dep.date_deployed IS NULL;''')
    return s.substitute(username=username)


def getResourceOwner(resourceId):
    s = Template('SELECT owner FROM Resource WHERE id = "$resourceId"')
    return s.substitute(resourceId=resourceId)


def insertIncident(_id, _username, description, d, dec_type, lat, longitude):
    s = Template('''INSERT into Incident (id, owner, description, date, declaration, 
           location_latitude, location_longitude) VALUES("$id","$user","$des","$d","$dec","$lat","$lon");''')
    return s.substitute(id=_id, user=_username, des=description, d=d, dec=dec_type, lat=lat, lon=longitude)


def setResourceStatusDeploy(resourceId):
    s = Template('UPDATE resource SET status = "IN USE" WHERE id = $resourceId;')
    return s.substitute(resourceId=resourceId)

def findIncidentResourceRequest(incidentId, resourceId):
    s = Template('SELECT expected_return_date FROM Request WHERE id_incident = "$incidentId" AND id_resource = "$resourceId";')
    return s.substitute(incidentId=incidentId, resourceId=resourceId)


#def findResourceByEesf(esf):
#    s = Template('SELECT r.id, r.name, r.owner, c.amount, c.unit_of_measure, r.status FROM Resource r LEFT OUTER JOIN HasSecondaryESFDesignation h ON r.id = h.id, Cost c WHERE r.cost_id = c.cost_id AND (r.esf_primary_designation="$esf" OR h.esf_designation = "$esf");')
#    return s.substitute(esf=esf)


def deleteResourceRequest(username, id):
    s = Template('''Delete From request 
                    Where username = '$user' and id_resource = $id''')
    return s.substitute(id=id, user=username)

def deleteResourceRequestReturn(id_resource, id_incident):
    s = Template('''Delete From Request WHERE id_resource = $id_resource AND id_incident = "$id_incident"''')
    return s.substitute(id_resource=id_resource, id_incident=id_incident)

def deleteResourceRequestReject(id_resource, id_incident):
    s = Template('''Delete From Request Where id_resource = $id_resource AND id_incident = "$id_incident"''')
    return s.substitute(id_resource=id_resource, id_incident=id_incident)

def updateStatus(id):
    s = Template('''Update resource Set status = 'AVAILABLE' where id = $id;''')
    return s.substitute(id=id)

def updateStatusINUSE(id):
    s = Template('''Update Resource Set status = 'IN USE' where id = $id;''')
    return s.substitute(id=id)

def updateDeploy(id):
    s = Template('''Update deployed set actual_return_date = curdate() where id_resource = $id AND actual_return_date IS NULL;''')
    return s.substitute(id=id)

#def updateRequestExpectedReturnDate(id_resource, id_incident, expected_return_date):
#    s = Template('''Update request set expected_return_date = $expected_return_date where id_resource = $id_resource AND id_incident = $id_incident ;''')
#    return s.substitute(id_resource=id_resource, id_incident=id_incident, expected_return_date=expected_return_date)

def findExistingRequest(incidentId, resourceId):
    s = Template('SELECT id_incident FROM Request WHERE id_incident = "$incidentId" AND id_resource = "$resourceId";')
    return s.substitute(incidentId=incidentId, resourceId=resourceId)


def getMaxDistance(resourceID):
    s = Template('SELECT max_distance FROM Resource WHERE id = "$resourceID";')
    return s.substitute(resourceID=resourceID)