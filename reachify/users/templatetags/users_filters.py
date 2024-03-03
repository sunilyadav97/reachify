from django import template

register = template.Library()


@register.filter(name="update_or_add_page_param")
def update_or_add_page_param(url, page_number):
    """
    Update or add the 'page' parameter in the given URL.
    Usage: {{ request.get_full_path|update_or_add_page_param:"2" }}
    """
    if '?' in url:
        # URL already has query parameters
        url_parts = url.split('?')
        base_url = url_parts[0]
        query_params = url_parts[1].split('&')

        updated = False
        for i, param in enumerate(query_params):
            key, value = param.split('=')
            if key == 'page':
                query_params[i] = f"page={page_number}"
                updated = True
                break

        if not updated:
            query_params.append(f"page={page_number}")

        return f"{base_url}?{'&'.join(query_params)}"
    else:
        # URL does not have query parameters
        return f"{url}?page={page_number}"
