from flask import Flask, render_template, json, request, Response
from flaskext.mysql import MySQL
from PythonProcs import *
from datetime import date, datetime
import datetime
import time

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'J5pjKOlgbzy50F07QFUh'
app.config['MYSQL_DATABASE_DB'] = 'cs6400_su18_team039'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/login')
def loginPage():
    return render_template('login.html')


@app.route('/submitLogin', methods=['POST'])
def loginSubmitForm():
    try:
        _name = request.form['username']
        _password = request.form['password']
        # probably want to escape this string to avoid sql injections.
        # and we should definetly never try this in a prod environment. Literally the worst way to authenticate someone. 

        if _name and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getUserData(_name, _password))
            ((data,),) = cursor.fetchall()

            if len(data) is not 0:
                conn.commit()
                return Response(json.dumps({'message': str(data[0].encode('utf-8'))}), status=200,
                                mimetype='application/json')
            else:
                return Response(json.dumps({'error': str(data)}), status=401, mimetype='application/json')
        else:
            return Response(json.dumps({'html': '<span>Missing Name or Password Field</span>'}), status=400,
                            mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/main')
def mainPage():
    return render_template('main.html')


@app.route('/getUserInfo', methods=['POST'])
def getUserInformation():
    try:
        _username = request.form['username']

        if _username:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getUserInfo(_username))
            data = cursor.fetchall()

            if len(data) is not 0:
                ((name,),) = data
                message = getAdditionalUserInformation(_username, name.encode('utf-8'), cursor)
                conn.commit()
                return Response(json.dumps({'message': str(message)}), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({'error': str(data)}), status=401, mimetype='application/json')
        else:
            return Response(json.dumps({'html': '<span>Missing Username</span>'}), status=400,
                            mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/incident')
def incidentPage():
    return render_template('incident.html')


@app.route('/getDeclarations', methods=['GET'])
def getDeclarationsInfo():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(getDeclarations())
        data = cursor.fetchall()
        conn.commit()
        j = buildDeclarationJson(data)
        return Response(j, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def buildDeclarationJson(data):
    (unpackedData) = data
    j = []
    for (des, abbr) in unpackedData:
        j.append({"desc": des.encode('utf-8'), "abbr": abbr.encode('utf-8')})
    return json.dumps(j)


# used to populate a list of ESF
@app.route('/getESF', methods=['GET'])
def getESFInfo():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(getESF())
        data = cursor.fetchall()
        conn.commit()
        j = buildESFJson(data)
        return Response(j, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def buildESFJson(data):
    (unpackedData) = data
    j = []
    for (des, desig) in unpackedData:
        j.append({"desc": des.encode('utf-8'), "desig": desig})
    return json.dumps(j)



# used to populate a list of Additional ESF
@app.route('/getAddESF', methods=['POST'])
def getAddESFInfo():
    try:
        primaryESF = request.form['primaryESF']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(getAddESF(primaryESF))
        data = cursor.fetchall()
        conn.commit()
        j = buildAddESFJson(data)
        return Response(j, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def buildAddESFJson(data):
    (unpackedData) = data
    j = []
    for (des, desig) in unpackedData:
        j.append({"desc": des.encode('utf-8'), "desig": desig})
    return json.dumps(j)


# used to populate a list of incidents
@app.route('/getIncidents', methods=['POST'])
def getIncidentInfo():
    try:
        _username = request.form['username']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(getIncidents(_username))
        data = cursor.fetchall()
        conn.commit()
        j = buildESFJson(data)
        return Response(j, status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def buildIncidentJson(data):
    (unpackedData) = data
    j = []
    for (des, desig) in unpackedData:
        j.append({"desc": des.encode('utf-8'), "desig": desig})
    return json.dumps(j)

@app.route('/insertIncident', methods=['POST'])
def insertIncidentInfo():
    try:
        _username = request.form['username']
        incident_date = request.form['date']
        lat = request.form['lat']
        longitude = request.form['long']
        declaration = request.form['declaration']
        description = request.form['description']
        if _username and incident_date and lat and longitude and declaration and description:
            if -90.0 <= float(lat) <= 90.0 and -180.0 <= float(longitude) <= 180.0:
                d = datetime.datetime.strptime(incident_date, "%Y-%m-%d")
                conn = mysql.connect()
                cursor = conn.cursor()
                declaration_type = cursor.execute(getDeclaration(declaration))
                dec_type = cursor.fetchone()
                result = int(dec_type[0])
                count = cursor.execute(getNumberOfIncidentsWithDeclaration(result))
                result2 = cursor.fetchone()
                result2 = int(result2[0]) + 1
                _id = declaration + "-" + str(result2)
                message = cursor.execute(insertIncident(_id, _username, description, d, result, lat, longitude))
                conn.commit()
                return Response(json.dumps({'message': str(message)}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({'html': '<span>Missing data</span>'}), status=400, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/resource')
def resourcePage():
    return render_template('resource.html')

@app.route('/getUserName', methods=['POST'])
def getUserName():
    try:
        _username = request.form['username']

        if _username:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getUserInfo(_username))
            data = cursor.fetchall()

            if len(data) is not 0:
                ((name,),) = data
                message = name.encode('utf-8')
                conn.commit()
                return Response(json.dumps({'message': str(message)}), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({'error': str(data)}), status=401, mimetype='application/json')
        else:
            return Response(json.dumps({'html': '<span>Missing Username</span>'}), status=400,
                            mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/getIncidentName', methods=['POST'])
def getIncidentNameInfo():
    try:
        _incidentID = request.form['incidentID']
        if _incidentID:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getIncidentName(_incidentID))
            data = cursor.fetchall()

            if len(data) is not 0:
                ((name,),) = data
                message = name.encode('utf-8')
                conn.commit()
                return Response(json.dumps({'message': str(message)}), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({'error': str(data)}), status=401, mimetype='application/json')
        else:
            return Response(json.dumps({'html': '<span>Missing Username</span>'}), status=400,
                            mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# used to find next resource ID
@app.route('/getResourceID', methods=['GET'])
def getResourceIDInfo():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(getNextResourceID())
        data = cursor.fetchall()
        conn.commit()
        j = buildResourceIdJson(data)
        return Response(j, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def buildResourceIdJson(data):
    (unpackedData) = data
    j = []
    for (resID) in unpackedData:
        j.append({"resourceID": resID})
    return json.dumps(j)


# used to populate a list of ESF
@app.route('/getCostPer', methods=['GET'])
def getCostPerInfo():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(getCostPer())
        data = cursor.fetchall()
        conn.commit()
        j = buildCostPerJson(data)
        return Response(j, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def buildCostPerJson(data):
    (unpackedData) = data
    j = []
    for (uOm) in unpackedData:
        j.append({"uOm": uOm})
    return json.dumps(j)

@app.route('/insertResource', methods=['POST'])
def insertResourceInfo():
    try:
        _username = request.form['username']
        description = request.form['resourceName']
        status = "AVAILABLE"
        maxDistance = request.form['maxDistance']
        maxDistanceFlag = True
        if len(maxDistance) != 0:
            maxDistance = float(maxDistance)
        model = request.form['model']
        latitude = request.form['lat']
        longitude = request.form['long']
        costAmount = request.form['costAmount']
        addESF = request.form.getlist('addEsfDescription[]')
        capabilities = request.form.getlist('capabilities[]')
        if len(costAmount) != 0:
            costAmount = float(costAmount)
        costPer = request.form['costPer']
        esfPrimaryDescription = request.form['esfPrimaryDescription']

        if costAmount and costPer:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getCost(costAmount, costPer))
            costID = cursor.fetchone()
            if costID == None:
                cursor.execute(insertCost(costAmount, costPer))
                conn.commit()
                cursor.execute(getCost(costAmount, costPer))
                costID = cursor.fetchone()
            costID = int(costID[0])

        if _username and description and esfPrimaryDescription and latitude and longitude:
            if -90.0 <= float(latitude) <= 90.0 and -180.0 <= float(longitude) <= 180.0:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(getEsfDesignation(esfPrimaryDescription))
                esf_primary_designation = cursor.fetchone()
                esf_primary_designation = int(esf_primary_designation[0])
                message = cursor.execute(insertResource(_username, description, status, maxDistance, model, latitude,
                                                        longitude, costID, esf_primary_designation))
                conn.commit()

                conn = mysql.connect()
                cursor = conn.cursor()
                resourceID = cursor.execute(getMaxResourceID())
                resourceID = cursor.fetchone()
                resourceID = int(resourceID[0])


                if (len(addESF) > 0):
                    for i in range(0, len(addESF)):
                        addEsfDescription = addESF[i]
                        cursor.execute(getEsfDesignation(addEsfDescription))
                        esf_add_designation = cursor.fetchone()
                        esf_add_designation = int(esf_add_designation[0])
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(insertAddEsf(resourceID, esf_add_designation))
                        conn.commit()

                if (len(capabilities) > 0):
                    for i in range(0, len(capabilities)):
                        capabilitiesCurrent = capabilities[i]
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(insertCapability(resourceID, capabilitiesCurrent))
                        conn.commit()

                return Response(json.dumps({'message': str(message)}), status=200, mimetype='application/json')

        else:
            return Response(json.dumps({'html': '<span>Missing data</span>'}), status=400, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



@app.route('/getResourceInfo', methods=['POST'])
def getResourceInfo():
    try:
        _username = request.form['username']

        if _username:
            conn = mysql.connect()
            cursor = conn.cursor()
            message = getResourceInformation(_username, cursor)
            conn.commit()
            return Response(json.dumps({'message': str(message)}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({'html': '<span>Missing Name or Password Field</span>'}), status=400,
                            mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def getResourceInformation(username, cursor):
    return ''


@app.route('/searchResources', methods=['GET'])
def searchResources():
    try:
        keyword = request.args.get('keyword')
        esf = request.args.get('esf')
        kilometers = request.args.get('kilos')
        incident = request.args.get('incident')
        username = request.args.get('username')
        incident_flag = False
        keyword_flag = False
        esf_flag = False
        total_search = True
        data_array = []

        # search for resources associated with a keyword:
        if len(keyword):
            keyword_flag = True
            total_search = False
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getKeywordResult(keyword))
            data_keyword = cursor.fetchall()
            data_array_keyword = buildArray(data_keyword)
#            return Response(d, status=200, mimetype='application/json')

        # search for resources associated with an ESF:
        if esf != 'null':
            esf_flag = True
            total_search = False
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(findResourceByEesf(esf))
            data_esf = cursor.fetchall()
            data_array_esf = buildArray(data_esf)
#            return Response(d, status=200, mimetype='application/json')

        # search for resources associated with an incident:
        if incident != 'null':
            incident_flag = True
            total_search = False
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getDistance(incident))
            data = cursor.fetchall()
            resources = []
            x = []
            within_range = []
            for i in range(0,len(data)):
                resources.append(list(data[i]))
                x.append(resources[i][8:len(resources[i])])
                x[i][3] = round(x[i][3]*100)/100
                x[i][3] = '$' + str(x[i][3]) + '/' + str(x[i][4])
                x[i].remove(x[i][4])
                conn = mysql.connect()
                cursor = conn.cursor()
                resourceID = x[i][0]
                cursor.execute(getReturnDate(resourceID))
                dateCheck = cursor.fetchall()
                if len(dateCheck) > 0:
                    branch = dateCheck[0][0].strftime('%Y/%m/%d')
                    x[i][5] = unicode(branch)
                else:
                    x[i][5] = 'NOW'
                conn = mysql.connect()
                cursor = conn.cursor()

                if (str(x[i][2]) == str(username))&(str(x[i][4]) == "AVAILABLE"):
                    x[i].append("Deploy")
                else:
                    x[i].append("Request")

                con = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(getDeployedAlready(incident, resourceID))
                deployCheck = cursor.fetchall()
                con = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(getMaxDistance(resourceID))
                maxDistance = cursor.fetchall()
                rangeWithinCheck = False
                maxDistanceCheck = False
                max = maxDistance[0][0]
                if len(deployCheck) == 0:
                        if(len(kilometers)==0):
                            rangeWithinCheck = True
                        else:
                            if(float(x[i][6]) <= float(kilometers)):
                                rangeWithinCheck = True

                        if(not maxDistance[0][0]):
                            maxDistanceCheck = True
                        else:
                            if(float(x[i][6]) <= float(maxDistance[0][0])):
                                maxDistanceCheck = True

                        if(rangeWithinCheck & maxDistanceCheck):
                            within_range.append(x[i])

            data_array_incident = within_range
#            return Response(d, status=200, mimetype='application/json')

        if(total_search):
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(findAllResources())
            data = cursor.fetchall()
            data_array = buildArray(data)
            d = buildDistanceJson(data_array)
            return Response(d, status=200, mimetype='application/json')
        if(incident_flag):
            if(keyword_flag):
                for i in range(0, len(data_array_incident)):
                    for j in range(0, len(data_array_keyword)):
                        if data_array_incident[i][0] == data_array_keyword[j][0]:
                            data_array.append(data_array_incident[i])
                data_array_incident = data_array
            if (esf_flag):
                data_array = []
                for i in range(0, len(data_array_incident)):
                    for j in range(0, len(data_array_esf)):
                        if data_array_incident[i][0] == data_array_esf[j][0]:
                            data_array.append(data_array_incident[i])
            else:
                data_array = data_array_incident
        elif(keyword_flag):
            if(esf_flag):
                for i in range(0, len(data_array_keyword)):
                    for j in range(0, len(data_array_esf)):
                        if data_array_keyword[i][0] == data_array_esf[j][0]:
                            data_array.append(data_array_keyword[i])
            else:
                data_array = data_array_keyword
        elif(esf_flag):
            data_array = data_array_esf
        else:
            return Response(status=400)

        d = buildDistanceJson(data_array)
        return Response(d, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def buildArray(data):
    x = []
    for i in range(0,len(data)):
        x.append(list(data[i]))
        x[i][3] = round(x[i][3]*100)/100
        x[i][3] = '$' + str(x[i][3]) + '/' + str(x[i][4])
        x[i].remove(x[i][4])
        conn = mysql.connect()
        cursor = conn.cursor()
        resourceID = x[i][0]
        cursor.execute(getReturnDate(resourceID))
        dateCheck = cursor.fetchall()
        print(dateCheck)
        if len(dateCheck) > 0:
            branch = dateCheck[0][0].strftime('%Y/%m/%d')
            x[i][5] = unicode(branch)
        else:
            x[i][5] = 'NOW'
        x[i].append(float(0.0))
        x[i].append(unicode(None))

    return(x)

def buildDistanceJson(data):
    (unpackedData) = data
    #print(data)
    d = []
    for (id, name, owner, cost, status, nextAvailable, distance, action) in unpackedData:
        d.append({"idResource": int(id), "nameResource": str(name), "owner": str(owner), "cost": str(cost), "status": str(status), "nextAvailable": nextAvailable.encode('utf-8'),
                  "distance" : float(distance), "actionText":action.encode('utf-8')})
	#print(d)
    return json.dumps(d)



@app.route('/search')
def searchPage():
    return render_template('search.html')

@app.route('/request', methods=['POST'])
def requestPage():
    try:
        username = request.form['username']
        incidentId = request.form['incidentId']
        date = request.form['date']
        resourceId = request.form['resourceId']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(findExistingRequest(incidentId, resourceId))
        existingRequest = cursor.fetchall()
        if len(existingRequest) > 0:
            return Response(status=400)
        cursor.execute(insertRequest(username, incidentId, resourceId, date))
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(getResourceOwner(resourceId))
        data = cursor.fetchall()
        resourceOwner = data[0][0]

        cursor.execute(getReturnDate(resourceId))
        dateCheck = cursor.fetchall()
        if len(dateCheck) == 0:
            if username == resourceOwner:
                cursor.execute(insertDeploy(incidentId, resourceId))
                cursor.execute(setResourceStatusDeploy(resourceId))
                conn.commit()
        return Response(status=200)
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/searchResults')
def searchResultsPage():
    return render_template('searchResults.html')

@app.route('/status')
def statusPage():
    return render_template('status.html')

@app.route('/report')
def reportPage():
    return render_template('report.html')


@app.route('/getReport', methods=['GET'])
def getReport():
    try:
        username = request.args.get('username')
        if username:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getReportInformation(username))
            data = cursor.fetchall()
            conn.commit()
            j = buildReportJson(data)
            return Response(j, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def buildReportJson(data):
    (unpackedData) = data
    j = []
    for (esf, support, total, used) in unpackedData:
        j.append({"esf": int(esf), "support": support.encode('utf-8'), "total": int(total), "used": int(used)})
    return json.dumps(j)


@app.route('/getResourcesInUseInfo', methods=['GET'])
def getResourcesInUseInfo():
    try:
        username = request.args.get('username')
        if username:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getResourcesInUse(username))
            data = cursor.fetchall()
            conn.commit()
            j = buildResourcesInUseJson(data)
            return Response(j, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def buildResourcesInUseJson(data):
    (unpackedData) = data
    j = []
    for (d) in unpackedData:
        j.append({"name": d[1], "Id": d[0], "description": d[2], "owner": d[3], "date_deployed": d[4], "expected_return_date": d[5], "id_incident": d[6]})
    return json.dumps(j)


@app.route('/getResourcesRequestedInfo', methods=['GET'])
def getResourcesRequestedInfo():
    try:
        username = request.args.get('username')
        if username:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getResourcesRequested(username))
            data = cursor.fetchall()
            conn.commit()
            j = buildResourcesRequestedJson(data)
            return Response(j, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def buildResourcesRequestedJson(data):
    (unpackedData) = data
    j = []
    for (d) in unpackedData:
        j.append({"name": d[1], "Id": d[0], "description": d[2], "owner": d[3], "expected_return_date": d[4]})
    return json.dumps(j)


@app.route('/getResourceRequestsReceivedInfo', methods=['GET'])
def getResourceRequestsReceivedInfo():
    try:
        username = request.args.get('username')
        if username:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(getResourceRequestsReceived(username))
            data = cursor.fetchall()
            conn.commit()
            j = buildResourceRequestsReceivedJson(data)
            return Response(j, status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def buildResourceRequestsReceivedJson(data):
    (unpackedData) = data
    j = []
    for (d) in unpackedData:
        used = False
        if d[5] == "IN USE":
            used = True
        j.append({"name": d[1], "Id": d[0], "description": d[2], "username": d[3], "expected_return_date": d[4], "id_incident": d[6], "used": used})
    return json.dumps(j)

def getAdditionalUserInformation(username, name, cursor):
    cursor.execute(getGovernmentInfo(username))
    data = cursor.fetchall()
    if len(data) is not 0:
        ((local_office, agency_name),) = data
        return name + "<br>" + local_office.encode('utf-8') + "<br>" + agency_name.encode('utf-8')

    cursor.execute(getHeadQuartersInfo(username))
    data = cursor.fetchall()
    if len(data) is not 0:
        ((headquarters, number_of_employees),) = data
        return name + "<br>" + headquarters.encode('utf-8') + "<br>" + str(number_of_employees) + " employees"

    cursor.execute(getMunicipalityInfo(username))
    data = cursor.fetchall()
    if len(data) is not 0:
        ((category,),) = data
        return name + "<br>" + category.encode('utf-8')

    return name


@app.route('/onClickCancel', methods=['GET'])
def onClickCancel():
    try:
        id = request.args.get('id')
        username = request.args.get('username')
        if username and id:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(deleteResourceRequest(username, id))
            data = cursor.fetchall()
            conn.commit()
            return Response(status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/returnResource', methods=['GET'])
def returnResource():
    try:
        id = request.args.get('id')
        id_incident = request.args.get('id_incident')
        if id:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(updateStatus(id))
            cursor.execute(updateDeploy(id))
            cursor.execute(deleteResourceRequestReturn(id, id_incident))
            data = cursor.fetchall()
            conn.commit()
            return Response(status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/rejectRequest', methods=['GET'])
def rejectRequest():
    try:
        id_resource = request.args.get('id_resource')
        id_incident = request.args.get('id_incident')
        username = request.args.get('username')
        if id:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(deleteResourceRequestReject(id_resource, id_incident))
            data = cursor.fetchall()
            conn.commit()
            return Response(status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/deployRequest', methods=['GET'])
def deployRequest():

    try:
        id_resource = request.args.get('id')
        id_incident = request.args.get('id_incident')
        username = request.args.get('username')
        if id:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(updateStatusINUSE(id_resource))
            cursor.execute(insertDeploy(id_incident, id_resource))
            data = cursor.fetchall()
            conn.commit()
            return Response(status=200, mimetype='application/json')

    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
