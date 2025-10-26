from datetime import datetime
from app import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_agent = db.Column(db.Boolean, default=False)
    tickets = db.relationship('Ticket', backref='author', lazy=True)
    assigned_tickets = db.relationship('Ticket', foreign_keys='Ticket.agent_id', backref='agent', lazy=True)
    responses = db.relationship('TicketResponse', backref='responder', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', Admin:{self.is_admin}, Agent:{self.is_agent})"

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default='Medium') # Low, Medium, High, Urgent
    status = db.Column(db.String(20), nullable=False, default='Open') # Open, In Progress, Resolved, Closed
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Agent assigned to the ticket
    responses = db.relationship('TicketResponse', backref='ticket', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Ticket('{self.title}', '{self.status}', '{self.author.username}')"

class TicketResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # User who made the response (can be customer or agent)
    is_internal_note = db.Column(db.Boolean, default=False) # True for agent-only notes

    def __repr__(self):
        return f"TicketResponse('{self.content[:20]}...', '{self.ticket_id}')"