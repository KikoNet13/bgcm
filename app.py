from flask import Flask, render_template, request, redirect, url_for

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
    if request.method == "POST":

        # Alta de juego
        if "game_name" in request.form:
            name = request.form.get("game_name", "").strip()
            if name:
                game = Game(name=name)
                db.session.add(game)
                db.session.commit()
            return redirect(url_for("index"))

        # Alta de campaña
        if "campaign_name" in request.form:
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

            return redirect(url_for("index"))

    campaigns = Campaign.query.all()
    games = Game.query.order_by(Game.name).all()

    return render_template("index.html", campaigns=campaigns, games=games)


if __name__ == "__main__":
    app.run(debug=True)
