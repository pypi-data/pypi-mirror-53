from collections import Counter

def predictionEnsembleModelUtility(ensemble):
    "Using a Weighted Moving Average, though the 'moving' part refers to the prediction index."
    ## using a weighted posterior_probability = potential/marginal_probability
    ## FORMULA: pv + ( (Uprediction_2-pv)*(Wprediction_2) + (Uprediction_3-pv)*(Wprediction_3)... )/mp
    if len(ensemble) > 0:
        principal_value = ensemble[0]["utility"]  ## Let's use the "best" match as our starting point. Alternatively, we can use,say, the average of all values before adjusting.
        principal_weight = ensemble[0]["potential"]
        marginal_probability = sum([x["potential"] for x in ensemble])
        u = principal_value + (sum([(x["utility"] - principal_value)*(x["potential"]) for x in ensemble[1:]]))/marginal_probability
        if u != 0:
            return u
    return None

def predictionEnsembleModelClassification(ensemble):
    "For classifications, we don't bother with marginal_probability because classifications are discrete symbols, not numeric values."
    predicted_value = None
    boosted_predicted_missing = Counter()
    if len(ensemble) != 0:
        for p in ensemble:
            ## Always look in the farthest part of the prediction, first, then work your way backwards.
            if not p['future']:
                ## Then look in the 'present':
                guessing_class = p['present'][-1][-1]  ## The last symbol in the last event of the present field
            else:
                guessing_class = p['future'][-1][-1]  ## The last symbol in the last event of the future field
            if ("VECTOR|" in guessing_class) or ("|name|" in guessing_class):
                guessing_class = None ## Skip since we know this ain't no damn classification!
            if not guessing_class:
                continue
            if "PRIMITIVE|" in guessing_class:  ## Without "VECTOR|" or "|name|"
                guessing_class = guessing_class.split("|")[-1]  ## grab the value
            boosted_predicted_missing[guessing_class] += 1 * p["potential"]
        if len(boosted_predicted_missing) > 0:
            predicted_value = boosted_predicted_missing.most_common(1)[0][0]
    return predicted_value

def hiveModelUtility(node_predictions):
    "Average of final node predictions."
    if node_predictions:
        p = [v for v in node_predictions if (v != 0 and v != None)]
        if p:
            return sum(p)/len(p)
    return None

def hiveModelClassification(node_predictions):
    "Every node gets a vote."

    # Crashes if list consists on only None values
    if node_predictions:
        # This just takes the first "most common", even if there are multiple that have the same frequency.
        common = Counter([p for p in node_predictions if p != None]).most_common()
        if common : return common[0][0]
    return None