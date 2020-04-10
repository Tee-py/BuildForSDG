def estimator(data):
    import json
    covid_data = json.loads(data)
    impact_ci = covid_data['reportedCases']*10
    severe_ci = covid_data['reportedCases']*50
    if covid_data['periodType'] == 'days':
        impact_ibrt = int(impact_ci*(2**int((covid_data['timeToElapse']/3))))
        severe_ibrt = int(severe_ci*(2**int((covid_data['timeToElapse']/3))))
    elif covid_data['periodType'] == 'weeks':
        impact_ibrt = int(impact_ci*(2**int(((covid_data['timeToElapse']*7)/3))))
        severe_ibrt = int(severe_ci*(2**int(((covid_data['timeToElapse']*7)/3))))
    elif covid_data['periodType'] == 'months':
        impact_ibrt = int(impact_ci*(2**int(((covid_data['timeToElapse']*30)/3))))
        severe_ibrt = int(severe_ci*(2**int(((covid_data['timeToElapse']*30)/3))))
    """impact_scbrt = int(0.15*impact_ibrt)
    severe_scbrt = int(0.15*severe_ibrt)
    impact_hbbrt = int(0.35*covid_data['totalHospitalBeds']-impact_scbrt)
    severe_hbbrt = int(0.35*covid_data['totalHospitalBeds']-severe_scbrt)
    impact_icu = int(0.05*impact_ibrt)
    severe_icu = int(0.05*severe_ibrt)
    impact_venti = int(0.02*impact_ibrt)
    severe_venti = int(0.02*severe_ibrt)
    if covid_data['periodType'] == 'days':
        impact_dnflight = int((impact_ibrt*covid_data['region']['avgDailyIncomeInUSD']*covid_data['region']['avgDailyIncomePopulation'])*\
                            covid_data['timeToElapse'])
        severe_dnflight = int((severe_ibrt*covid_data['region']['avgDailyIncomeInUSD']*covid_data['region'][
          'avgDailyIncomePopulation'])*covid_data['timeToElapse'])
    elif covid_data['periodType'] == 'weeks':
        impact_dnflight = int((impact_ibrt*covid_data['region']['avgDailyIncomeInUSD']*covid_data['region']['avgDailyIncomePopulation'])*(covid_data['timeToElapse']*7))
        severe_dnflight = int((severe_ibrt* covid_data['region']['avgDailyIncomeInUSD'] * covid_data['region']['avgDailyIncomePopulation'])*(covid_data['timeToElapse']*7))
    elif covid_data['periodType'] == 'months':
        impact_dnflight = int((impact_ibrt*covid_data['region']['avgDailyIncomeInUSD'] * covid_data['region']['avgDailyIncomePopulation'])*\
                          (covid_data['timeToElapse']*30))
        severe_dnflight = int((severe_ibrt*covid_data['region']['avgDailyIncomeInUSD'] * covid_data['region']['avgDailyIncomePopulation'])*\
                          covid_data['timeToElapse']*30)"""
    python_return_data = {
      "estimate": {
        "impact": {
          "currentlyInfected": impact_ci,
          "infectionsByRequestTime": impact_ibrt,
        },
        "severeImpact": {
          "currentlyInfected": severe_ci,
          "infectionsByRequestTime": severe_ibrt,
        }
      }
    }


    return covid_data, json.dumps(python_return_data)
json_str = '{"region": {"name": "Africa", "avgAge": 19.7, "avgDailyIncomeInUSD": 4, "avgDailyIncomePopulation": 0.73},\
"periodType": "days", "timeToElapse": 38, "reportedCases": 2747, "population": 92931687, "totalHospitalBeds": 678874 }'
print(estimator(json_str))
