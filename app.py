from flask import Flask, redirect, render_template, request, url_for

from models import db, Game, Campaign, CampaignStatus


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.route("/", methods=["GET", "POST"])
def index():
    def get_filters():
        status = request.values.get("status", "").strip()
        game_id = request.values.get("game_id", "").strip()
        return status, game_id

    if request.method == "POST":
        # Alta de juego
        if "game_name" in request.form:
            name = request.form.get("game_name", "").strip()
            if name:
                game = Game(name=name)
                db.session.add(game)
                db.session.commit()

        # Alta de campaña
        if "campaign_name" in request.form:
            name = request.form.get("campaign_name", "").strip()
            game_id = request.form.get("game_id")
            status = request.form.get("status")

            if name and game_id and status:
                campaign = Campaign(
                    name=name,
                    game_id=int(game_id),
                    status=CampaignStatus(status),
                )
                db.session.add(campaign)
                db.session.commit()

        if request.headers.get("HX-Request"):
            filter_status, filter_game_id = get_filters()
            campaigns = filtered_campaigns(filter_status, filter_game_id)
            games = Game.query.order_by(Game.name).all()
            return render_template(
                "index.html",
                campaigns=campaigns,
                games=games,
                filter_status=filter_status,
                filter_game_id=filter_game_id,
            )

        return redirect(url_for("index"))

    filter_status, filter_game_id = get_filters()
    campaigns = filtered_campaigns(filter_status, filter_game_id)
    games = Game.query.order_by(Game.name).all()
    form = request.args.get("form")

    return render_template(
        "index.html",
        campaigns=campaigns,
        games=games,
        filter_status=filter_status,
        filter_game_id=filter_game_id,
        form=form,
    )


def filtered_campaigns(status_filter, game_id_filter):
    query = Campaign.query

    if status_filter == "abandonada":
        query = query.filter(Campaign.abandoned.is_(True))
    elif status_filter:
        try:
            query = query.filter(Campaign.status == CampaignStatus(status_filter))
        except ValueError:
            pass

    if game_id_filter.isdigit():
        query = query.filter(Campaign.game_id == int(game_id_filter))

    return query.all()


if __name__ == "__main__":
    app.run(debug=True)
