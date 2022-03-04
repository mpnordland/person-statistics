import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, abort, Response
import marshmallow
from person_statistics.models import UserListSchema
from person_statistics.processing import *

app = Flask(__name__)

@app.get('/')
def index():
    return render_template("how_to_use.html")


@app.post('/')
def output_statistics():
    output_mimetype = request.accept_mimetypes.best_match(['application/json', 'text/plain', 'application/xml'])
    if not output_mimetype:
        abort(406)

    if not request.is_json:
        abort(415)

    try:
        users = UserListSchema().load(request.get_json())['results']
    except marshmallow.ValidationError as err:
        return err.messages, 400

    data = {
        "percentage_female_vs_male": percentage_female_v_male(users),
        "percentage_first_name_start_a_n": percentage_first_name_start_a_n(users),
        "percentage_last_name_start_a_n": percentage_last_name_start_a_n(users),
        "percentage_people_in_states": percentage_people_in_states(users),
        "percentage_females_in_states": percentage_females_in_states(users),
        "percentage_males_in_states": percentage_males_in_states(users),
        "percentage_people_in_age_ranges": percentage_people_in_age_ranges(users),
    }

    if output_mimetype == "text/plain":
        return Response(render_template("plain_text_response.txt", **data), 200, content_type="text/plain")
    elif output_mimetype == "application/json":
        return data
    elif output_mimetype == "application/xml":
        tree = ET.Element("statistics")

        for k, v in data.items():
            stat = ET.SubElement(tree, 'stat', {'name': k})
            stat.text = str(v)

        return Response(ET.canonicalize(xml_data=ET.tostring(tree)), 200, content_type="application/xml")
