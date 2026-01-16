from enum import Enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CampaignStatus(Enum):
    PLANIFICADA = "planificada"
    PENDIENTE = "pendiente"
    ACTIVA = "activa"
    FINALIZADA = "finalizada"


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    campaigns = db.relationship(
        "Campaign", back_populates="game", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Game {self.name}>"


class Campaign(db.Model):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    status = db.Column(
        db.Enum(CampaignStatus), nullable=False, default=CampaignStatus.PLANIFICADA
    )

    abandoned = db.Column(db.Boolean, nullable=False, default=False)

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)

    game = db.relationship("Game", back_populates="campaigns")

    def __repr__(self):
        return f"<Campaign {self.name} ({self.status.value})>"
