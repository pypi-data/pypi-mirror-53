"""Handles searching offers and CRUD operations for data access offers.
"""
def search(_data=None, **kwargs):
    """Searches available data offers at the data custodian.

    Args:
        _data (dict): filter options for retrieving offers. Follows the model
            `OfferFilter`.

    Returns:
        list: of `dict` that match the model `OfferCollection`.
    """
    pass

def update(offer_did=None, _data=None, **kwargs):
    """Creates or updates a data offer.

    Args:
        offer_did (str): DID for the offer to update. If not specified, then
            the offer will be created with a new DID.
        _data (dict): offer details to create; follows the model `Offer`.
    """
    pass

def get(offer_did=None, **kwargs):
    """Returns the details of a data access offer.

    Args:
        offer_did (str): DID of the offer to retrieve details for.

    Returns:
        dict: with the format of the model `Offer`.
    """
    pass

def disable(offer_did=None, **kwargs):
    """Set an offer as unavailable.

    Args:
        offer_did (str): DID of the offer to set as unavailable.
    """
    pass

def enable(offer_did=None, **kwargs):
    """Set an offer as available.

    Args:
        offer_did (str): DID of the offer to set as available.
    """
    pass

def claim(offer_did=None, _data=None, **kwargs):
    """Claim a data access offer.

    Args:
        offer_did (str): DID of the offer that is being claimed.
        _data (dict): metadata proving the value exchange. Follows the format
            of the `OfferClaim` model.
    """
    pass
