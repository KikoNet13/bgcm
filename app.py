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
    view = request.args.get("view", "games")
    if view not in {"games", "campaigns"}:
        view = "games"

    if request.method == "POST":

        # Alta de juego
        if "game_name" in request.form:
            view = "games"
            name = request.form.get("game_name", "").strip()
            if name:
                game = Game(name=name)
                db.session.add(game)
                db.session.commit()

        # Alta de campaña
        if "campaign_name" in request.form:
            view = "campaigns"
            name = request.form.get("campaign_name", "").strip()
            game_id = request.form.get("game_id")
            status = request.form.get("status")
            abandoned = request.form.get("abandoned") == "on"

            if name and game_id and status:
                campaign = Campaign(
                    name=name,
                    game_id=int(game_id),
                    status=CampaignStatus(status),
                    abandoned=abandoned,
                )
                db.session.add(campaign)
                db.session.commit()

        if request.headers.get("HX-Request"):
            campaigns = Campaign.query.all()
            games = Game.query.order_by(Game.name).all()
            return render_template(
                "index.html", campaigns=campaigns, games=games, view=view
            )

        return redirect(url_for("index", view=view))

    campaigns = Campaign.query.all()
    games = Game.query.order_by(Game.name).all()

    return render_template("index.html", campaigns=campaigns, games=games, view=view)


if __name__ == "__main__":
    app.run(debug=True)
