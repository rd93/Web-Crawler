from urlparse import urlparse

# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ""

# Get the sub domain name (mail.name.example.com)
# extra comment
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ""