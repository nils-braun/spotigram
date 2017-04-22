def add_views(app):
    from flask import request

    from spotigram.web.models import User
    from spotigram import db
    from spotigram.spotify.functions import tokenize
    from spotigram.spotify.datatypes import client
    from spotigram.utilities.functions import query_messages

    @app.route("/spotify/accept/", methods=["GET"])
    def accept():
        access = tokenize(request.args.get("code"), client)

        user = User.query.filter_by(id=request.args.get("state")).first()
        user.refresh_code = access.refresh_token

        db.session.merge(user)
        db.session.commit()

        return ""

    @app.route("/check", methods=["GET"])
    def check():
        try:
            query_messages()
            return "OK"
        except Exception as e:
            return e
