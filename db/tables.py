import sqlalchemy.orm

from db import Base


class WeeklyChart(Base):
    __tablename__ = "weekly_charts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    country_code = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.Date)
    tracks = sqlalchemy.orm.relationship("ChartTrack", lazy="joined")


class ChartTrack(Base):
    __tablename__ = "chart_tracks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    chart_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("weekly_charts.id"))
    position = sqlalchemy.Column(sqlalchemy.Integer)
    track_id = sqlalchemy.Column(sqlalchemy.VARCHAR(22), sqlalchemy.ForeignKey("tracks.track_id"))
    track = sqlalchemy.orm.relationship("Track", lazy="joined")
    n_streams = sqlalchemy.Column(sqlalchemy.Integer)


class Track(Base):
    __tablename__ = "tracks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    track_id = sqlalchemy.Column(sqlalchemy.VARCHAR(length=22), unique=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    artist = sqlalchemy.Column(sqlalchemy.String)
    danceability = sqlalchemy.Column(sqlalchemy.Float)
    energy = sqlalchemy.Column(sqlalchemy.Float)
    key = sqlalchemy.Column(sqlalchemy.Float)
    loudness = sqlalchemy.Column(sqlalchemy.Float)
    mode = sqlalchemy.Column(sqlalchemy.Float)
    speechiness = sqlalchemy.Column(sqlalchemy.Float)
    acousticness = sqlalchemy.Column(sqlalchemy.Float)
    instrumentalness = sqlalchemy.Column(sqlalchemy.Float)
    liveness = sqlalchemy.Column(sqlalchemy.Float)
    valence = sqlalchemy.Column(sqlalchemy.Float)
    tempo = sqlalchemy.Column(sqlalchemy.Float)
    duration_ms = sqlalchemy.Column(sqlalchemy.Float)
    time_signature = sqlalchemy.Column(sqlalchemy.Float)
