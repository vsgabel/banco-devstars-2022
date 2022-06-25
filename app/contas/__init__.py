from flask import Blueprint

contas = Blueprint('contas', __name__)

from app.contas import views