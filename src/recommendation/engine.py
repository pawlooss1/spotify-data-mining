from typing import List

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from db.gateway import TracksGateway
from domain.track import AudioFeatures

FEATURE_NAMES = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
CAT_FEATURES = ['key', 'mode', 'time_signature']
CAT_COLUMN_NAMES = ['key_0', 'key_1', 'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 'key_9', 'key_10',
                    'key_11', 'mode_0', 'mode_1', 'time_signature_0', 'time_signature_1', 'time_signature_2',
                    'time_signature_3', 'time_signature_4', 'time_signature_5']

scaler = MinMaxScaler()

tracks_gw = TracksGateway()
features = tracks_gw.fetch_all().drop('genres', axis=1)


def preprocess_features(features_df: pd.DataFrame) -> pd.DataFrame:
    features_df = features_df[FEATURE_NAMES]
    for cat_feature in CAT_FEATURES:
        dummies = pd.get_dummies(features_df[cat_feature], prefix=cat_feature)
        features_df = pd.concat([features_df, dummies], axis=1)
    for col in CAT_COLUMN_NAMES:
        if col not in features_df:
            features_df[col] = 0
    features_df = features_df.drop(columns=CAT_FEATURES)
    features_df_scaled = pd.DataFrame(scaler.fit_transform(features_df.to_numpy()), columns=features_df.columns)
    return features_df_scaled


features_scaled = preprocess_features(features)


def get_similarities(tracks_user: pd.DataFrame) -> np.ndarray:
    user_vector = preprocess_features(tracks_user).to_numpy()
    user_vector_scaled = scaler.transform(user_vector)
    user_vector_scaled = np.sum(user_vector_scaled, axis=0, keepdims=True)

    return cosine_similarity(features_scaled, user_vector_scaled)


def create_recommendations(tracks_user: List[AudioFeatures]) -> List[str]:
    tracks_user_df = pd.DataFrame(tracks_user)
    similarities = get_similarities(tracks_user_df)
    tracks_with_similarities = features.assign(similarity=similarities)
    top_recommendations = tracks_with_similarities.sort_values('similarity', ascending=False).iloc[:10]
    return [track_id for track_id in top_recommendations.index]
