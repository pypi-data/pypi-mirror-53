from random_survival_forest import RandomSurvivalForest
from lifelines import CoxPHFitter, KaplanMeierFitter
from .helper import drop_correlated_features
from lifelines.metrics import concordance_index


def c_index(prediction, labels):
    return concordance_index(labels["donor_survival_time"], prediction, labels["donor_vital_status"])


def random_survival_forest_prediction(features, labels, timeline=range(0, 10, 1), n_estimators=100,
                                      n_jobs=-1,  min_leaf=3, unique_deaths=3, random_state=None):
    rsf = RandomSurvivalForest(n_estimators=n_estimators, timeline=timeline, n_jobs=n_jobs, min_leaf=min_leaf,
                               unique_deaths=unique_deaths, random_state=random_state)
    rsf.fit(features, labels)
    return rsf


def cox_proportional_hazard_regression(features, labels, penalizer=0, corr=0.95, drop_features=None):
    if drop_features is not None:
        features = features.drop(drop_features, axis=1)
    features = drop_correlated_features(features, corr)
    features.loc[:, "donor_survival_time"] = labels["donor_survival_time"]
    features.loc[:, "donor_vital_status"] = labels["donor_vital_status"]
    cph = CoxPHFitter(penalizer=penalizer)
    cph.fit(features, 'donor_survival_time', 'donor_vital_status')

    return cph


def kaplan_meier_fit(labels):
    kmf = KaplanMeierFitter()
    kmf.fit(labels['donor_survival_time'], labels['donor_vital_status'])

    return kmf