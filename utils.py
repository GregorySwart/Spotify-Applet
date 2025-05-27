def get_artist_ids_from_track(track):
    """
    Get the artist IDs given a list of track dicts

    :param track: dict
    :return: List[str]
    """
    return [artist["id"] for artist in track["artists"]]
