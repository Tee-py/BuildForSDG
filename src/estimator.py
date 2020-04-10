"""
A nevelty COVID-19 Infections estimator function.
"""

def estimator(data):

    #import json
    #covid_data = json.loads(data)

    #calculations for the currentlyInfected property
    impact_ci = data['reportedCases']*10
    severe_ci = data['reportedCases']*50

    #calculations for the inFectedByRequestTime
    if data['periodType'] == 'days':
        impact_ibrt = int(impact_ci*(2**int((data['timeToElapse']/3))))
        severe_ibrt = int(severe_ci*(2**int((data['timeToElapse']/3))))

    elif data['periodType'] == 'weeks':
        impact_ibrt = int(impact_ci*(2**int(((data['timeToElapse']*7)/3))))
        severe_ibrt = int(severe_ci*(2**int(((data['timeToElapse']*7)/3))))

    elif data['periodType'] == 'months':
        impact_ibrt = int(impact_ci*(2**int(((data['timeToElapse']*30)/3))))
        severe_ibrt = int(severe_ci*(2**int(((data['timeToElapse']*30)/3))))

    impact_scbrt = int(0.15*impact_ibrt)
    severe_scbrt = int(0.15*severe_ibrt)
    impact_hbbrt = int(0.35*data['totalHospitalBeds']-impact_scbrt)
    severe_hbbrt = int(0.35*data['totalHospitalBeds']-severe_scbrt)
    impact_icu = int(0.05*impact_ibrt)
    severe_icu = int(0.05*severe_ibrt)
    impact_venti = int(0.02*impact_ibrt)
    severe_venti = int(0.02*severe_ibrt)
    if data['periodType'] == 'days':
        impact_dnflight = int((impact_ibrt*data['region']['avgDailyIncomeInUSD']*data['region']['avgDailyIncomePopulation'])*\
                            data['timeToElapse'])
        severe_dnflight = int((severe_ibrt*data['region']['avgDailyIncomeInUSD']*data['region'][
          'avgDailyIncomePopulation'])*data['timeToElapse'])
    elif data['periodType'] == 'weeks':
        impact_dnflight = int((impact_ibrt*data['region']['avgDailyIncomeInUSD']*data['region']['avgDailyIncomePopulation'])*(data['timeToElapse']*7))
        severe_dnflight = int((severe_ibrt* data['region']['avgDailyIncomeInUSD'] * data['region']['avgDailyIncomePopulation'])*(data['timeToElapse']*7))
    elif data['periodType'] == 'months':
        impact_dnflight = int((impact_ibrt*data['region']['avgDailyIncomeInUSD'] * data['region']['avgDailyIncomePopulation'])*\
                          (data['timeToElapse']*30))
        severe_dnflight = int((severe_ibrt*data['region']['avgDailyIncomeInUSD'] * data['region']['avgDailyIncomePopulation'])*\
                          data['timeToElapse']*30)

    #The returned data
    python_return_data = {
        "data": {
            "region": {
                "name": data['region']['name'],
                "avgAge": data['region']['avgAge'],
                "avgDailyIncomeInUSD": data['region']['avgDailyIncomeInUSD'],
                "avgDailyIncomePopulation": data['region']['avgDailyIncomePopulation']
            },
            "periodType": data['periodType'],
            "timeToElapse": data['timeToElapse'],
            "reportedCases": data['reportedCases'],
            "population": data['population'],
            "totalHospitalBeds": data['totalHospitalBeds']
        },
        "impact": {
          "currentlyInfected": impact_ci,
          "infectionsByRequestedTime": impact_ibrt,
          "severeCasesByRequestedTime": impact_scbrt,
          "hospitalBedsByRequestedTime": impact_hbbrt
        },
        "severeImpact": {
          "currentlyInfected": severe_ci,
          "infectionsByRequestedTime": severe_ibrt,
          "severeCasesByRequestedTime": severe_scbrt,
          "hospitalBedsByRequestedTime": severe_hbbrt,
        }
    }
    #return the json format of the input data and python return data
    return python_return_data

#edit this variable to change the input data
#json_str =  {"region": {"name": "Africa", "avgAge": 19.7, "avgDailyIncomeInUSD": 4, "avgDailyIncomePopulation": 0.73},\
            #"periodType": "days", "timeToElapse": 38, "reportedCases": 2747, "population": 92931687, "totalHospitalBeds"\
            #: 678874 }

#shows the output on the console
#test = estimator(json_str)
#print(test['impact']['severeCasesByRequestedTime'])
