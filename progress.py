import os

from flask import Flask, make_response, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret_l801#+#a&^1mz)_p&qyq51j51@20_74c-xi%&i)b*u_dt^2=2key")


def get_progress_color(progress, scale):
    ratio = progress/scale

    if ratio < 0.3:
        return "#d9534f"
    if ratio < 0.7:
        return "#f0ad4e"

    return "#5cb85c"


def get_template_fields(progress):
    title = request.args.get("title")

    template_fields = {
        "title": title,
        "title_width": 10 + 6*len(title) if title else 0,
        "scale": 100,
        "progress": progress,
        "progress_width": 60 if title else 90,
        "suffix": request.args.get("suffix", "%"),
    }

    try:
        template_fields["progress_width"] = int(request.args.get("width"))
    except:
        pass

    try:
        template_fields["scale"] = int(request.args.get("scale"))
    except:
        pass

    template_fields["color"] = get_progress_color(progress, template_fields["scale"])

    return template_fields


@app.route("/<int:progress>/")
def getProgressSVG(progress):
    template_fields = get_template_fields(progress)

    template = render_template("progress.svg", **template_fields)

    response = make_response(template)
    response.headers["Content-Type"] = "image/svg+xml"
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
