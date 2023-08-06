DARARD.FR COMMON API PACK
-------------------------

This package is used by the APIs deployed on ``dadard.fr``.

It calls the Main API to check the subscriptions and the profiles' key.

Install it this way : ``pip install dadard-apis-common-pack``

You can import the package in your code this way :

.. code:: python

    from CommonPack import CommonCaller

    profile_key = 'some_private_key'

    # check if the key is associated to a valid user
    CommonCaller.check_profile_key(profile_key)

    # check if the api given has been subscribed by this key
    CommonCaller.check_is_subscribed(profile_key, api_name)

    # check if the api given has not been subscribed by this key
    CommonCaller.check_is_not_subscribed(profile_key, api_name)



