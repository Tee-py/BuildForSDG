def estimator(data):
    import json
    covid_data = json.loads(data)
    impact_currently_infected = covid_data['reportedCases']*10
    severe_impact_curently_infected = covid_data['reportedCases']*50
    if covid_data['periodType'] == 'days':
        impact_infections_by_request_time = int(impact_currently_infected*(2**(covid_data['timeToElapse']/3)))
        severe_impact_infections_by_request_time = int(severe_impact_curently_infected*(2**(covid_data['timeToElapse']/3)))
    elif covid_data['periodType'] == 'weeks':
        impact_infections_by_request_time = int(impact_currently_infected*(2**(covid_data['timeToElapse']*7/3)))
        severe_impact_infections_by_request_time = int(severe_impact_curently_infected*(2**(covid_data['timeToElapse']*7/3)))
    elif covid_data['periodType'] == 'months':
        impact_infections_by_request_time = int(impact_currently_infected*(2**(covid_data['timeToElapse']*30/3)))
        severe_impact_infections_by_request_time=int(severe_impact_curently_infected*(2**(covid_data['timeToElapse']*30/3)))
    
    python_return_data = {
      "impact": {
        "currentlyInfected": impact_currently_infected,
        "infectionsByRequestTime": impact_infections_by_request_time,
      },
      "severeImpact": {
        "currentlyInfected": severe_impact_curently_infected,
        "infectionsByRequestTime": severe_impact_infections_by_request_time,
      }
    }


    return json.dumps(python_return_data)
json_str = '{"region": {"name": "Africa", "avgAge": 19.7, "avgDailyIncomeInUSD": 5, "avgDailyIncomePopulation": 0.71}, "periodType": "days", "timeToElapse": 58, "reportedCases": 674, "population": 66622705, "totalHospitalBeds": 1380614 }'
print(estimator(json_str))
