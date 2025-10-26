from app import db
from flask_login import UserMixin
from datetime import datetime # Don't forget this import for default=datetime.utcnow

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_agent = db.Column(db.Boolean, default=False) # Based on your routes.py
    is_admin = db.Column(db.Boolean, default=False) # Based on your routes.py

    # Relationship for tickets created by this user
    tickets_created = db.relationship(
        'Ticket',
        backref='author',
        lazy=True,
        foreign_keys='Ticket.user_id' # Explicitly links to Ticket.user_id
    )

    # Relationship for tickets assigned to this user
    tickets_assigned = db.relationship(
        'Ticket',
        backref='agent',
        lazy=True,
        foreign_keys='Ticket.agent_id' # Explicitly links to Ticket.agent_id
    )

    # NEW: Relationship for responses made by this user
    ticket_responses_made = db.relationship( # Renamed for clarity, original backref was 'ticket_responses'
        'TicketResponse',
        backref='responder',
        lazy=True,
        foreign_keys='TicketResponse.user_id' # Explicitly links to TicketResponse.user_id
    )

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Found in your routes.py
    status = db.Column(db.String(20), nullable=False, default='Open') # Found in your routes.py
    category = db.Column(db.String(50), nullable=False, default='General') # Found in your routes.py
    priority = db.Column(db.String(20), nullable=False, default='Low') # Found in your routes.py

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign key for the ticket creator
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Foreign key for the assigned agent

    # NEW: Relationship for responses associated with this ticket
    responses = db.relationship(
        'TicketResponse',
        backref='ticket',
        lazy=True,
        cascade="all, delete-orphan" # Optional: deletes responses if the parent ticket is deleted
    )

    def __repr__(self):
        return f"Ticket('{self.title}', '{self.date_posted}')"

class TicketResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_internal_note = db.Column(db.Boolean, default=False) # Found in your routes.py

    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # The user who made the response

    # The relationships `ticket` and `responder` are already set up via backref in Ticket and User respectively.
    # No need to redefine them here with db.relationship

    def __repr__(self):
        return f"TicketResponse('{self.content[:20]}...', 'Ticket ID: {self.ticket_id}', 'User ID: {self.user_id}')"