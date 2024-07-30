from datetime import datetime as dt


def avatar_upload(instance, filename):
    now = dt.now()
    return 'avatar/profile_No{id}/{Y}/{m}/{d}/{filename}'.format(
        id=instance.profile.pk,
        Y=now.strftime("%Y"),
        m=now.strftime("%m"),
        d=now.strftime("%d"),
        filename=filename,
    )

