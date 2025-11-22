def volume_ma(volume, length=20):
    return volume.rolling(length).mean()
