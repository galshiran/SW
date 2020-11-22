from flask import Flask, request, make_response

from sessionizing import *
from logger.logger import *

app = Flask(__name__)  # Create the flask app
sessionizing = Sessionizing()  # Main Sessionizing instance which holds all the processed data from input files.


@app.route('/initialize/', methods=['POST'])
def initialize():
    """
    Use with POST method.
    This view gets input files as single string argument and initialize the Sessionizing data structures:
        "url": "http://localhost:5000/initialize/"
        "data": {"input_files": "/absolute/path/to/input_1.csv, /absolute/path/to/input_2.csv"}
    """
    global sessionizing
    response = "Initialization finished successfully."
    input_files = request.form.get('input_files').split(",")
    input_files = list(map(str.strip, input_files))

    try:
        faulty_lines_counter = sessionizing.initialize(*input_files)
    except Exception as ex:
        return make_response(ex.__str__(), 500)
    else:
        if faulty_lines_counter:
            response += "\nThere were {} lines with incompatible data".format(faulty_lines_counter)

    logger.info(response)
    return make_response(response)


@app.route('/visitorsites/', methods=["GET"])
def get_unique_sites_per_user():
    """
    Use with GET method.
    This view gets visitor(s) id(s) and return the unique sites visited by visitor.
        "url": "http://localhost:5000/usersites/"
        "data": {"ids": "visitor_1, visitor_2"}
    """
    global sessionizing
    response = ""
    response_pattern = "Num of unique sites for {} = {}\n"
    error_pattern = "Visitor {} does not exist\n"
    visitors_ids = request.args['ids'].split(",")
    visitors_ids = list(map(str.strip, visitors_ids))

    for visitor_id in visitors_ids:
        visitor = sessionizing.visitors.get(visitor_id)
        if visitor:
            response += response_pattern.format(visitor_id, visitor.unique_sites)
        else:
            response += error_pattern.format(visitor_id)

    logger.info(response)
    return make_response(response)


@app.route('/sitesessions/', methods=["GET"])
def get_site_sessions_number():
    """
    Use with GET method.
    This view gets site(s) url(s) and return the number of session per each site.
        "url": "http://localhost:5000/sitesessions/"
        "data": {"urls": "www.example1.com, www.example2.com"}
    """
    global sessionizing
    response = ""
    response_pattern = "Num sessions for site {} = {}\n"
    error_pattern = "Site {} does not exist"
    sites_urls = request.args['urls'].split(",")
    sites_urls = list(map(str.strip, sites_urls))

    for site_url in sites_urls:
        site = sessionizing.sites.get(site_url)
        if site:
            response += response_pattern.format(site_url, site.num_of_sessions)
        else:
            response += error_pattern(site_url)

    logger.info(response)
    return make_response(response)


@app.route('/sitemedian/', methods=["GET"])
def get_site_median_session_length():
    """
    Use with GET method.
    This view gets site(s) url(s) and return the median (sorted by length) of site's sessions.
        "url": "http://localhost:5000/sitemedian/"
        "data": {"urls": "www.example1.com, www.example2.com"}
    """
    global sessionizing
    response = ""
    response_pattern = "Median session length for site {} = {}\n"
    error_pattern = "Site {} does not exist"
    sites_urls = request.args['urls'].split(",")
    sites_urls = list(map(str.strip, sites_urls))

    for site_url in sites_urls:
        site = sessionizing.sites.get(site_url)
        if site:
            response += response_pattern.format(site_url, site.get_site_sessions_median())
        else:
            response += error_pattern.format(site_url)

    logger.info(response)
    return make_response(response)


if __name__ == '__main__':
    app.run()
