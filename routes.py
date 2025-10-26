from flask import render_template, url_for, flash, redirect, request, abort
import datetime
from app import app, db, bcrypt
from forms import RegistrationForm, LoginForm, TicketForm, TicketResponseForm, AssignAgentForm, ChangeStatusForm
from models import User, Ticket, TicketResponse
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc
import functools

# --- Helper Decorators for Authorization ---
def agent_required(f):
    @functools.wraps(f)
    @login_required
    def wrap(*args, **kwargs):
        if not current_user.is_agent and not current_user.is_admin:
            flash('You do not have permission to view this page.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return wrap

def admin_required(f):
    @functools.wraps(f)
    @login_required
    def wrap(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have admin permission to view this page.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return wrap

# --- Public Routes ---
@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        elif current_user.is_agent:
            return redirect(url_for('agent_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    return render_template('index.html', title='Welcome')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# --- User Portal Routes ---
@app.route("/user_dashboard")
@login_required
def user_dashboard():
    # Regular users don't have agent/admin access, so filter their own tickets
    if current_user.is_agent or current_user.is_admin:
        flash('You are logged in as an agent/admin. Redirecting to your dashboard.', 'info')
        return redirect(url_for('home')) # Redirect to appropriate dashboard based on home logic
    
    tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(desc(Ticket.date_posted)).all()
    return render_template('user_dashboard.html', title='My Tickets', tickets=tickets)

@app.route("/submit_ticket", methods=['GET', 'POST'])
@login_required
def submit_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, description=form.description.data,
                        category=form.category.data, priority=form.priority.data,
                        author=current_user)
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been submitted!', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('submit_ticket.html', title='Submit Ticket', form=form)

@app.route("/ticket/<int:ticket_id>", methods=['GET', 'POST'])
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # Authorization check: only author, assigned agent, or admin can view
    if not (ticket.user_id == current_user.id or
            ticket.agent_id == current_user.id or
            current_user.is_admin):
        flash('You do not have permission to view this ticket.', 'danger')
        return redirect(url_for('user_dashboard')) # Redirect to user's dashboard if not authorized

    response_form = TicketResponseForm()
    if response_form.validate_on_submit():
        if not current_user.is_agent and not current_user.is_admin and response_form.is_internal_note.data:
            flash('Only agents/admins can add internal notes.', 'danger')
            return redirect(url_for('view_ticket', ticket_id=ticket.id))

        response = TicketResponse(content=response_form.content.data,
                                  ticket=ticket,
                                  responder=current_user,
                                  is_internal_note=response_form.is_internal_note.data)
        db.session.add(response)
        ticket.last_updated = datetime.utcnow()
        db.session.commit()
        flash('Your response has been added!', 'success')
        return redirect(url_for('view_ticket', ticket_id=ticket.id))
    
    # Filter responses for regular users
    if not current_user.is_agent and not current_user.is_admin:
        responses = [res for res in ticket.responses if not res.is_internal_note]
    else:
        responses = ticket.responses

    # Admin/Agent specific forms
    assign_form = AssignAgentForm()
    change_status_form = ChangeStatusForm()

    if current_user.is_admin or current_user.is_agent:
        agents = User.query.filter((User.is_agent == True) | (User.is_admin == True)).order_by(User.username).all()
        assign_form.agent.choices = [(agent.id, agent.username) for agent in agents]
        if ticket.agent:
            assign_form.agent.data = ticket.agent.id # Pre-select current agent

    return render_template('ticket_detail.html', title=f'Ticket {ticket.id}', ticket=ticket,
                           response_form=response_form, responses=responses,
                           assign_form=assign_form, change_status_form=change_status_form)

# --- Agent/Admin Portal Routes ---
@app.route("/agent_dashboard")
@agent_required
def agent_dashboard():
    # Only show tickets assigned to the agent or unassigned tickets
    tickets = Ticket.query.filter(
        (Ticket.agent_id == current_user.id) | (Ticket.agent_id == None)
    ).order_by(desc(Ticket.date_posted)).all()
    return render_template('agent_dashboard.html', title='Agent Dashboard', tickets=tickets)

@app.route("/admin_dashboard")
@admin_required
def admin_dashboard():
    tickets = Ticket.query.order_by(desc(Ticket.date_posted)).all() # All tickets
    agents = User.query.filter((User.is_agent == True) | (User.is_admin == True)).count()
    users = User.query.count()
    open_tickets = Ticket.query.filter_by(status='Open').count()
    in_progress_tickets = Ticket.query.filter_by(status='In Progress').count()
    resolved_tickets = Ticket.query.filter_by(status='Resolved').count()

    # Basic analytics data (can be expanded)
    ticket_status_data = {
        'Open': open_tickets,
        'In Progress': in_progress_tickets,
        'Resolved': resolved_tickets,
        'Closed': Ticket.query.filter_by(status='Closed').count()
    }
    
    return render_template('admin_dashboard.html', title='Admin Dashboard', tickets=tickets,
                           agents_count=agents, users_count=users,
                           open_tickets=open_tickets, in_progress_tickets=in_progress_tickets,
                           resolved_tickets=resolved_tickets,
                           ticket_status_data=ticket_status_data)

@app.route("/ticket/<int:ticket_id>/assign", methods=['POST'])
@agent_required
def assign_agent(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = AssignAgentForm()
    agents = User.query.filter((User.is_agent == True) | (User.is_admin == True)).order_by(User.username).all()
    form.agent.choices = [(agent.id, agent.username) for agent in agents]

    if form.validate_on_submit():
        agent = User.query.get(form.agent.data)
        if agent:
            ticket.agent = agent
            db.session.commit()
            flash(f'Ticket assigned to {agent.username}.', 'success')
        else:
            flash('Selected agent not found.', 'danger')
    else:
        flash('Invalid agent selection.', 'danger')
    return redirect(url_for('view_ticket', ticket_id=ticket.id))

@app.route("/ticket/<int:ticket_id>/status", methods=['POST'])
@agent_required
def change_ticket_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = ChangeStatusForm()
    if form.validate_on_submit():
        ticket.status = form.status.data
        ticket.last_updated = datetime.utcnow()
        db.session.commit()
        flash(f'Ticket status updated to {ticket.status}.', 'success')
    else:
        flash('Invalid status selection.', 'danger')
    return redirect(url_for('view_ticket', ticket_id=ticket.id))

@app.route("/manage_users")
@admin_required
def manage_users():
    users = User.query.order_by(User.username).all()
    return render_template('manage_users.html', title='Manage Users', users=users)

@app.route("/user/<int:user_id>/toggle_agent_status", methods=['POST'])
@admin_required
def toggle_agent_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_agent = not user.is_agent
    db.session.commit()
    flash(f'{user.username} agent status toggled to {user.is_agent}.', 'success')
    return redirect(url_for('manage_users'))

@app.route("/user/<int:user_id>/toggle_admin_status", methods=['POST'])
@admin_required
def toggle_admin_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'{user.username} admin status toggled to {user.is_admin}.', 'success')
    return redirect(url_for('manage_users'))