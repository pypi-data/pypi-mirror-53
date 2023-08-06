# Zaach

_Zaach_ is an austrian term for exhausting/bothersome. Its a shortest way to express that you would rather do something else instead.

This package includes tested helpers that I wrote once and now use in a couple of projects. They should work with Python 2 and 3.

A base64 variant that is safe to be used in URLs and filesystems:

- zaach.base64url.encode(unencoded)
- zaach.base64url.decode(encoded)

ISO 8601 compliant time formatting:

- zaach.time.formatter.iso_8601_duration(seconds)

Milliseconds to timecode

- zaach.time.formatter.ms_to_timecode(ms, fps=None)

_Easily_ getting a UNIX timestamp in UTC:

- zaach.time.timestamp(utc_dt=None)

Converting a UTC datetime object to CET/CEST, whatever is used at that date and time in the _bestest_ timezone

- zaach.time.tzconversion.utc_to_cet_or_cest(utc_dt)

A Borg object:

- zaach.oop.borg.Borg

A Mixin to store and retrieve (expiring) values in a class

- zaach.oop.cache.CacheMixin

Calculate the product of an iterable (like `sum` for multiplication)

- zaach.math.prod
