from urlparse import urlparse
import json
import re
import argparse
import csv
import grequests
from bs4 import BeautifulSoup



def parse_app_csv(path):
    with open(path) as csvfile:
        apps = list(csv.DictReader(csvfile))
        for app in apps:
            app_url = app['App Store URL']
            app['Country'] = urlparse(app_url).path.split('/')[1]

        return apps


def has_all(target):
    return lambda given: all(x in given for x in target)


def is_country(country):
    return lambda c: c == country


def filter_key(key, filter_func, flist):
    return [item for item in flist if filter_func(item[key])]


def parse_body(body, script_tag_id='shoebox-ember-data-store'):
    soup = BeautifulSoup(body, 'html.parser')
    json_str_node = soup.find('script', id=script_tag_id)
    if json_str_node is None:
        return None
    return json.loads(json_str_node.get_text())


def find(element, obj):
    path = element.split('.')
    data = obj
    for i,_ in enumerate(path):
        data = data[path[i]]
    return data


def contains_str(key):
    return lambda s: re.search(key, s, re.IGNORECASE)


def map_app_data(json_data):
    '''  name - string - The name of the app
    app_identifier - number - The App Store's identifier of the app (eg. 1261357853 for Fortnite)
    minimum_ios_version - string - The minimum iOS version required to run the app
    languages - array of strings, sorted alphabetically - All of the languages that the app supports '''
    app_info = {}
    app_info['id'] = int(find('data.id', json_data))
    app_info['languages'] = sorted([l.strip() for l in find(
        'data.attributes.softwareInfo.languagesDisplayString', json_data).split(',')])
    app_info['minimum_ios_version'] = find(
        'data.attributes.minimumOSVersion', json_data)
    app_info['name'] = find('data.attributes.name', json_data)

    return app_info


def fetch_apps_parallel(urls, concurrent=3):
    def exception_handler(request, exception):
        print('Request for {} failed\n {}'.format(request.url, exception))
    reqs = ([grequests.get(url) for url in urls])
    requester = (
        grequests.imap(
            reqs,
            size=concurrent,
            exception_handler=exception_handler))
    results = [(req.url, req.text) for req in requester if req is not None]
    return [
        req for req in sorted(
            results,
            key=lambda result: urls.index(
                result[0]))]


def humanize_lang_list(langs):
    def undie_list():
        ls = map(str.lower, langs)
        if len(ls) > 1:
            return '_'.join(ls[:-1]) + '_and_' + str(ls[-1:][0])
        return '_'.join(ls)

    return 'apps_in_' + undie_list()


def humanize_has_in_name(name_has):
    return 'apps_with_{}_in_name'.format(name_has.lower())


def scrape_apps(
        input_csv_path,
        concurrent=3,
        name_has='insta',
        languages=[
            'Spanish',
            'Tagalog'],
        filtered_path='filtered_apps.json',
        apps_path='apps.json'):

    apps = parse_app_csv(input_csv_path)

    country_apps = filter_key('Country', is_country('us'), apps)

    print('Fetching {} app(s)...'.format(len(country_apps)))

    urls = [app['App Store URL'] for app in country_apps]

    apps_fetched = fetch_apps_parallel(urls, concurrent)

    if len(apps_fetched) < len(urls):
        urls_fetched = [app[0] for app in apps_fetched]
        failed_names = [app['App Name']
                        for app in country_apps if app['App Store URL'] not in urls_fetched]
        print('Failed to fetch: {}'.format(failed_names))

    apps_info = [
        map_app_data(body) for body in (
            parse_body(
                app[1]) for app in apps_fetched) if body is not None]

    has_in_name_apps = sorted([app['id'] for app in filter_key(
        'name', contains_str(name_has), apps_info)])
    # without filter_key could be: app['id'] for app in apps_info if
    # contains_str('insta')(app['name'])

    lang_apps = sorted([app['id'] for app in filter_key(
        'languages', has_all(languages), apps_info)])

    print('Finished fetching apps, writing ...')

    with open(filtered_path, 'w') as filtered_file, open(apps_path, 'w') as apps_file:
        json.dump({
            humanize_lang_list(languages): lang_apps,
            humanize_has_in_name(name_has): has_in_name_apps
        }, filtered_file)

        json.dump(apps_info, apps_file)

    print('Done!')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=' iTunes Scraper (MightySignal Coding Challenge) ')

    parser.add_argument('input_csv_path')

    parser.add_argument('--concurrent', type=int, default=3)
    parser.add_argument('--name-has', type=str, default='insta')
    parser.add_argument(
        '--languages',
        nargs='+',
        default=[
            'Tagalog',
            'Spanish'])

    pargs = parser.parse_args()

    scrape_apps(**vars(pargs))
