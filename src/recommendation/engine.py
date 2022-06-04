from typing import List

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from db.gateway import TracksGateway
from domain.track import AudioFeatures
from recommendation import UserVector

FEATURE_NAMES = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'n_streams']
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
    features_df_scaled = pd.DataFrame(scaler.fit_transform(features_df.to_numpy()),
                                      columns=features_df.columns,
                                      index=features_df.index)
    return features_df_scaled


features_scaled = preprocess_features(features)


def get_similarities(user_vector: UserVector, popularity_rate: float = 0):
    n_streams = features_scaled.n_streams.to_numpy().reshape(-1, 1)
    features_scaled = features_scaled.drop(['n_streams'], axis=1)

    audio_similarities = cosine_similarity(
                            features_scaled, user_vector.vec)
    similarities = audio_similarities + popularity_rate*n_streams

    return similarities


def create_recommendations(tracks_user: List[AudioFeatures]) -> List[str]:
    tracks_user_df = pd.DataFrame(tracks_user)
    user_vector = UserVector(tracks_user, scaler)

    similarities = get_similarities(user_vector)
    tracks_with_similarities = db_mock.assign(similarity=similarities)

    # Drop tracks that are already there in user history
    # to not recommend what user listened to already
    tracks_with_similarities.drop(tracks_user_df.index, inplace=True)

    top_recommendations = tracks_with_similarities.sort_values('similarity', ascending=False).iloc[:10]
    return [track_id for track_id in top_recommendations.index]
