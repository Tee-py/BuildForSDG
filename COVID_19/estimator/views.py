from django.shortcuts import render
from django.http import HttpResponse

def estimator(data):

    #calculations for the currentlyInfected property
    impact_ci = data['reportedCases']*10
    severe_ci = data['reportedCases']*50

    #calculations for the inFectedByRequestTime
    if data['periodType'] == 'days':
        impact_ibrt = int(impact_ci*(2**int((data['timeToElapse']/3))))
        severe_ibrt = int(severe_ci*(2**int((data['timeToElapse']/3))))

    elif data['periodType'] == 'weeks':
        factor = int((data['timeToElapse']*7)/3)
        impact_ibrt = int(impact_ci*(2**factor))
        severe_ibrt = int(severe_ci*(2**factor))

    elif data['periodType'] == 'months':
        factor = int((data['timeToElapse']*30)/3)
        impact_ibrt = int(impact_ci*(2**factor))
        severe_ibrt = int(severe_ci*(2**factor))

    impact_scbrt = int(0.15*impact_ibrt)
    severe_scbrt = int(0.15*severe_ibrt)
    impact_hbbrt = int(0.35*data['totalHospitalBeds']-impact_scbrt)
    severe_hbbrt = int(0.35*data['totalHospitalBeds']-severe_scbrt)
    impact_icu = int(0.05*impact_ibrt)
    severe_icu = int(0.05*severe_ibrt)
    impact_venti = int(0.02*impact_ibrt)
    severe_venti = int(0.02*severe_ibrt)

    if data['periodType'] == 'days':
        impact_dnflight = ((impact_ibrt*data['region']['avgDailyIncomeInUSD']*data['region']\
        ['avgDailyIncomePopulation'])/data['timeToElapse'])
        severe_dnflight = ((severe_ibrt*data['region']['avgDailyIncomeInUSD']*data['region'][\
        'avgDailyIncomePopulation'])/data['timeToElapse'])

    elif data['periodType'] == 'weeks':
        denum_var = data['timeToElapse']*7
        impact_dnflight = ((impact_ibrt*data['region']['avgDailyIncomeInUSD']*data['region']\
        ['avgDailyIncomePopulation'])/denum_var)
        severe_dnflight = ((severe_ibrt* data['region']['avgDailyIncomeInUSD'] * data['region']\
        ['avgDailyIncomePopulation'])/denum_var)

    elif data['periodType'] == 'months':
        denum_var = data['timeToElapse']*30
        impact_dnflight = ((impact_ibrt*data['region']['avgDailyIncomeInUSD'] * data['region']\
        ['avgDailyIncomePopulation'])/denum_var)
        severe_dnflight = ((severe_ibrt*data['region']['avgDailyIncomeInUSD'] * data['region']\
        ['avgDailyIncomePopulation'])/denum_var)

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
          "hospitalBedsByRequestedTime": impact_hbbrt,
          "casesForICUByRequestedTime": impact_icu,
          "casesForVentilatorsByRequestedTime": impact_venti,
          "dollarsInFlight": int(impact_dnflight),

        },
        "severeImpact": {
          "currentlyInfected": severe_ci,
          "infectionsByRequestedTime": severe_ibrt,
          "severeCasesByRequestedTime": severe_scbrt,
          "hospitalBedsByRequestedTime": severe_hbbrt,
          "casesForICUByRequestedTime": severe_icu,
          "casesForVentilatorsByRequestedTime": severe_venti,
          "dollarsInFlight": int(severe_dnflight),
        }
    }
    #return the json format of the input data and python return data
    return python_return_data


# Create your views here.

def home(request):
    import json
    response = json.dumps({})
    return HttpResponse(response, content_type='text/json')

def endpoint(request):
    import json
    if request.method == 'POST':
        data = request.POST
        response = json.dumps(estimator(data))
    else:
        response = json.dumps({})
    return HttpResponse(response, content_type='text/json')

def xml(request):
    return render(request, "xml.html")

def json(request):
    return render(request, "json.html")

def logs(request):
    return render(request, "logs.html")
