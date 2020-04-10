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
    impact_severe_cases_by_requested_time = int(15/100*impact_infections_by_request_time)
    severe_impact_severe_cases_by_requested_time = int(15/100*severe_impact_infections_by_request_time)
    impact_hospital_bed_by_requested_time = covid_data['totalHospitalBeds'] - impact_severe_cases_by_requested_time
    severe_hospital_bed_by_requested_time = covid_data['totalHospitalBeds']-severe_impact_severe_cases_by_requested_time
    impact_icu = 5/100*impact_infections_by_request_time
    severe_icu = 5/100*severe_impact_infections_by_request_time
    impact_venti = 2/100*impact_infections_by_request_time
    severe_venti = 2/100*severe_impact_infections_by_request_time
    if covid_data['periodType'] == 'days':
        impact_dnflight = int((impact_infections_by_request_time*covid_data['region']['avgDailyIncomeInUSD']*covid_data['region']['avgDailyIncomePopulation'])/\
                            covid_data['timeToElapse'])
        severe_dnflight = int((severe_impact_infections_by_request_time * covid_data['region']['avgDailyIncomeInUSD'] * covid_data['region'][
          'avgDailyIncomePopulation']) / \
                              covid_data['timeToElapse'])
    elif covid_data['periodType'] == 'weeks':
        impact_dnflight = int((impact_infections_by_request_time*covid_data['region']['avgDailyIncomeInUSD'] * covid_data['region']['avgDailyIncomePopulation']) / \
                          (covid_data['timeToElapse']*7))
        severe_dnflight = int(
          (severe_impact_infections_by_request_time * covid_data['region']['avgDailyIncomeInUSD'] * covid_data['region'][
            'avgDailyIncomePopulation']) / \
          covid_data['timeToElapse'])
    elif covid_data['periodType'] == 'months':
        impact_dnflight = int((impact_infections_by_request_time*covid_data['region']['avgDailyIncomeInUSD'] * covid_data['region']['avgDailyIncomePopulation']) / \
                          (covid_data['timeToElapse']*30))
        severe_dnflight = int((severe_impact_infections_by_request_time * covid_data['region']['avgDailyIncomeInUSD'] * covid_data['region']['avgDailyIncomePopulation']) / \
                          covid_data['timeToElapse'])
    python_return_data = {
      "estimate": {
        "impact": {
          "currentlyInfected": impact_currently_infected,
          "infectionsByRequestTime": impact_infections_by_request_time,
          "severeCasesByRequestedTime": impact_severe_cases_by_requested_time,
          "hospitalBedByRequestedTime": impact_hospital_bed_by_requested_time,
          "casesForICUByRequestedTime": impact_icu,
          "casesForVentilatorsByRequestedTime": impact_venti,
          "dollarsInFlight": impact_dnflight,
        },
        "severeImpact": {
          "currentlyInfected": severe_impact_curently_infected,
          "infectionsByRequestTime": severe_impact_infections_by_request_time,
          "severeCasesByRequestedTime": severe_impact_severe_cases_by_requested_time,
          "hospitalBedByRequestedTime": severe_hospital_bed_by_requested_time,
          "casesForICUByRequestedTime": severe_icu,
          "casesForVentilatorsByRequestedTime": severe_venti,
          "dollarsInFlight": severe_dnflight,
        }
      }

    }


    return json.dumps(python_return_data)
json_str = '{"region": {"name": "Africa", "avgAge": 19.7, "avgDailyIncomeInUSD": 5, "avgDailyIncomePopulation": 0.71},\
"periodType": "weeks", "timeToElapse": 5, "reportedCases": 674, "population": 66622705, "totalHospitalBeds": 1380614 }'
print(estimator(json_str))
