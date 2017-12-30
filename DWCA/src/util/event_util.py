from definitions import AD_HOC


def update_adhoc_dict(event, ad_hoc_dict):
    if ad_hoc_dict == {}:
        event[AD_HOC] = ad_hoc_dict
    else:
        ad_hoc_state = event.get(AD_HOC, {})
        ad_hoc_state.update(ad_hoc_dict)
        event[AD_HOC] = ad_hoc_state
    return event
