from cbc_sdk import CBCloudAPI
from cbc_sdk.platform.alerts import Alert

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from typing import List


def perform_kmeans(alert_list: List[str], alert: str, num_clusters: int = 4) -> List[str]:
    """Perform k-means alerts.

    Performs the k-means algorithm on all the retrieved and grouped alerts.
    Then predict, to which cluster the alert belongs to and return only the texts
    for the alerts from the same cluster.

    Args:
        alert_list (list): list of only the unique reasons for alerts.
        alert (str): cleaned reason for the alert for which we search for similar alerts.
        num_clusters (int): number of clusters

    Returns:
        list[str]: list of alerts reasons that are similar to the alert
    """
    # Vectorize the alert reasons
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(alert_list)

    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(vectors)

    # Get cluster assignments
    cluster_labels = kmeans.labels_

    clusters = {}
    for i, text in enumerate(alert_list):
        cluster_label = cluster_labels[i]
        if cluster_label not in clusters:
            clusters[cluster_label] = []
        clusters[cluster_label].append(text)

    # Vectorize the new example
    new_example_vector = vectorizer.transform([alert])

    # Predict the cluster for the new example
    predicted_cluster = kmeans.predict(new_example_vector)[0]
    # return only the cluster to which the alert belongs to
    return clusters[predicted_cluster]


def load_stop_words() -> List[str]:
    """Load and returns predefined list of stop words."""
    try:
        with open("stopwords.txt", "r") as file:
            content = file.read()
            stopwords = content.split(",")
            return stopwords
    except FileNotFoundError:
        return []


def get_alerts(**kwargs):
    """Get all alerts filter by alert type and severity if available

    Args:
        kwargs(dict): Settings for the search.

    Returns:
        list: list of alerts - either the similar or the initial one, depending on the settings.

    """
    # TODO - Do not hard-code
    cb = CBCloudAPI(profile="alert_matcher")

    if not (kwargs.get("alert_id") or kwargs.get("reason")):
        # get initial alerts, we do not want similar alerts yet
        alerts = cb.select(Alert)

        # check which alert types to get
        alert_types = []
        if kwargs.get("cb_analytics"):
            alert_types.append("CB_ANALYTICS")
        if kwargs.get("watchlists"):
            alert_types.append("WATCHLIST")
        if kwargs.get("usb_device_control"):
            alert_types.append("DEVICE_CONTROL")
        if kwargs.get("host_based_firewall"):
            alert_types.append("HOST_BASED_FIREWALL")
        if kwargs.get("intrusion_detection_system"):
            alert_types.append("INTRUSION_DETECTION_SYSTEM")
        if kwargs.get("containers_runtime"):
            alert_types.append("CONTAINER_RUNTIME")

        if alert_types:
            alerts = alerts.add_criteria("type", alert_types)
        if kwargs.get("severity"):
            alerts = alerts.set_minimum_severity(kwargs.get("severity"))

        dict_alerts = {}
        if not kwargs.get("group"):
            for al in alerts:
                dict_alerts[al.id] = dict(type=al.type, severity=al.severity, reason=al.reason, raw=al.to_json())
            return dict_alerts
        else:
            index = -1
            reasons = []
            for al in alerts:
                if al.reason not in reasons:
                    index += 1
                    reasons.append(al.reason)
                    dict_alerts[index] = dict(reason=al.reason, alerts=dict())

                dict_alerts[index]["alerts"][al.id] = dict(
                    type=al.type, severity=al.severity, reason=al.reason, raw=al.to_json()
                )
        return dict_alerts
    else:
        # get similar alerts
        return get_similar_alerts(cb, **kwargs)


def get_similar_alerts(cb: CBCloudAPI, **kwargs) -> dict:
    """Get similar alerts for specific period and group them by reason.

    Arg:
        cb (BaseAPI): Reference to API object used to communicate with the server.
        kwargs (dict): Settings

    Returns:
        dict: information about the similar alerts
    """
    # get stop word, which are going to be removed from the words of the text
    STOP_WORDS = load_stop_words()

    # get the alert and prepare it for clustering
    if kwargs.get("alert_id"):
        alert = cb.select(Alert, kwargs.get("alert_id"))
        clean = " ".join([item for item in alert.reason.lower().split() if item not in STOP_WORDS])
    else:
        clean = " ".join([item for item in kwargs.get("reason").lower().split() if item not in STOP_WORDS])

    # get all the alerts in the said period
    alerts = cb.select(Alert)
    if kwargs.get("start_time") and kwargs.get("end_time"):
        alerts = alerts.add_time_criteria(
            "backend_update_timestamp", start=kwargs.get("start_time"), end=kwargs.get("end_time")
        )

    # create the mappings, get the unique reasons, so that the algorithm works on smaller set of records
    alerts_mappings = {}
    for alert in alerts:
        clean = " ".join([item for item in alert.reason.lower().split() if item not in STOP_WORDS])
        if clean not in alerts_mappings:
            alerts_mappings[clean] = [alert]
        else:
            alerts_mappings[clean].append(alert)

    # use k-means to cluster the unique reasons
    cluster_texts = perform_kmeans(alerts_mappings.keys(), clean)

    # prepare the data to be displayed
    similar_alerts = {}
    if not kwargs.get("similar_group"):
        for label in cluster_texts:
            curr_alerts = alerts_mappings.get(label)
            for al in curr_alerts:
                similar_alerts[al.id] = dict(type=al.type, severity=al.severity, reason=al.reason)
    else:
        index = 0
        for label in cluster_texts:
            curr_alerts = alerts_mappings.get(label)
            similar_alerts[index] = dict(reason=curr_alerts[0].reason, alerts=dict())
            for al in curr_alerts:
                similar_alerts[index]["alerts"][al.id] = dict(type=al.type, severity=al.severity, reason=al.reason)
            index += 1
    return similar_alerts
