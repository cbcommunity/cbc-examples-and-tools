from cbc_sdk import CBCloudAPI
from cbc_sdk.platform.alerts import Alert

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import datetime
from typing import List, Tuple



def perform_kmeans(alert_list: List[str], alert: str, num_clusters: int=4) -> List[str]:
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
    vectorizer = TfidfVectorizer(stop_words='english')
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


def get_alerts(cb: CBCloudAPI, alert_id: str, start_time: str=None, end_time: str=None) -> Tuple[str, dict]:
    """Get all alerts for specific period and group them by reason.

    Arg:
        cb (BaseAPI): Reference to API object used to communicate with the server.
        alert_id (str): The id for the alert, for which similar alerts are retrieved.
        start_time (str): start date for the period
        end_time (str): end date for the period

    Returns:
        tuple (str, dict): cleaned reason for alert and dictionary with keys the labels and values a list of alerts that have that reason.
    """
    # get the alert and prepare it for clustering
    STOP_WORDS = load_stop_words()
    alert = cb.select(Alert, ID)
    clean = " ".join([item for item in alert.reason.lower().split() if item not in STOP_WORDS])

    # get all the alerts in the said period
    alerts = cb.select(Alert)
    if start_time and end_time:
        alerts = alerts.add_time_criteria("backend_update_timestamp", start=start_time, end=end_time)

    # create the mappings
    alerts_mappings = {}
    for alert in alerts:
        clean = " ".join([item for item in alert.reason.lower().split() if item not in STOP_WORDS])
        if clean not in alerts_mappings:
            alerts_mappings[clean] = [alert]
        else:
            alerts_mappings[clean].append(alert)
    return clean, alerts_mappings


if __name__ == "__main__":
    cb = CBCloudAPI()
    # TO DELETE
    ID = "6f648cfb-3bbf-d434-0cd9-5b47f38ed5ad"
    timestamp = datetime.datetime.utcnow()
    start_time = "{}Z".format(timestamp.isoformat())
    end_time = start_time
    start_time = "2024-01-10T11:38:39.767683Z"
    GROUP = True

    clean, alerts_mappings = get_alerts(cb, ID, start_time, end_time)
    cluster_texts = perform_kmeans(alerts_mappings.keys(), clean)
    # 1.  id -> type, severity reason
    # 2.  index -> reason, alert_list [id -> type severity reason]
    if not GROUP:
        similar_alerts = {}
        for label in cluster_texts:    
            curr_alerts = alerts_mappings.get(label)
            for al in curr_alerts:
                similar_alerts[al.id] = dict(type=al.type,
                                             severity=al.severity,
                                             reason=al.reason)

        print(f"Checking for {clean}, found: {len(similar_alerts)} similar.")
    else:
        similar_alerts = {}
        index = 0
        for label in cluster_texts:    
            curr_alerts = alerts_mappings.get(label)
            similar_alerts[index] = dict(reason = curr_alerts[0].reason, alerts = dict())
            for al in curr_alerts:
                similar_alerts[index]["alerts"][al.id] = dict(type=al.type,
                                                              severity=al.severity,
                                                              reason=al.reason)
            index += 1

        print(f"Checking for {clean}, found: {len(similar_alerts)} similar grouped.")
        print(similar_alerts)
