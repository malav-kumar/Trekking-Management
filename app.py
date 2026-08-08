from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from extensions import db
from datetime import datetime

# We pass __name__ so Flask knows where our application lives and can locate resources correctly.
app = Flask(__name__)

# Load all settings from the Config class into the Flask application.
app.config.from_object(Config)

# to connect SQLAlchemy with my Flask application.
db.init_app(app)

from models import User,Trek,Booking

def create_admin():
    admin = User.query.filter(User.role == "admin").first()
    if admin is None:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password="admin123",
            role="admin",
            approved=True,
            blacklisted=False
        )
        db.session.add(admin)
        db.session.commit()


# Create an application context.
# Some Flask operations (like creating database tables)
# need to know which Flask application is currently running.
with app.app_context():

    # Create all tables (User, Trek, Booking)
    # if they do not already exist.
    db.create_all()
    create_admin()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/admin")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    total_users = User.query.filter(User.role == "user").count()
    total_staff = User.query.filter(User.role == "staff").count()
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings
    )


@app.route("/user")
def user_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "user":
        return "Access Denied"

    return render_template("user_dashboard.html")


@app.route("/available_treks")
def available_treks():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "user":
        return "Access Denied"

    location = request.args.get("location")
    difficulty = request.args.get("difficulty")

    treks = Trek.query.filter(
        Trek.status == "Open",
        Trek.available_slots > 0
    )

    if location:
        treks = treks.filter(Trek.location.contains(location))

    if difficulty:
        treks = treks.filter(Trek.difficulty == difficulty)

    treks = treks.all()

    return render_template(
        "available_treks.html",
        treks=treks
    )

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "user":
        return "Access Denied"

    user = User.query.get(session["user_id"])

    if request.method == "GET":
        return render_template("edit_profile.html", user=user)

    elif request.method == "POST":

        user.name = request.form["name"]
        user.email = request.form["email"]
        user.password = request.form["password"]

        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for("user_dashboard"))


@app.route("/book_trek/<int:id>")
def book_trek(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "user":
        return "Access Denied"

    trek = Trek.query.get(id)

    if trek is None:
        return "Trek Not Found"

    if trek.available_slots <= 0:
        flash("No slots available for this trek.", "warning")
        return redirect(url_for("available_treks"))

    existing_booking = Booking.query.filter(
        Booking.user_id == session["user_id"],
        Booking.trek_id == id
    ).first()

    if existing_booking:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("available_treks"))

    new_booking = Booking(
        user_id=session["user_id"],
        trek_id=id
    )

    db.session.add(new_booking)

    trek.available_slots -= 1

    db.session.commit()

    flash("Trek booked successfully!", "success")
    return redirect(url_for("booking_history"))

@app.route("/booking_history")
def booking_history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "user":
        return "Access Denied"

    bookings = Booking.query.filter(
        Booking.user_id == session["user_id"]
    ).all()

    return render_template(
        "booking_history.html",
        bookings=bookings,
        Trek=Trek
    )




@app.route("/staff")
def staff_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "staff":
        return "Access Denied"

    return render_template("staff_dashboard.html")

@app.route("/assigned_treks")
def assigned_treks():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "staff":
        return "Access Denied"

    staff_id = session["user_id"]
    treks = Trek.query.filter(Trek.assigned_staff_id == staff_id).all()
    return render_template("assigned_treks.html", treks=treks)

@app.route("/update_slots/<int:id>", methods=["GET", "POST"])
def update_slots(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "staff":
        return "Access Denied"

    trek = Trek.query.get(id)

    if trek is None:
        return "Trek Not Found"

    if request.method == "GET":
        return render_template("update_slots.html", trek=trek)

    elif request.method == "POST":

        available_slots = request.form["available_slots"]

        trek.available_slots = int(available_slots)

        db.session.commit()

        flash("Update saved successfully!", "success")
        return redirect(url_for("assigned_treks"))


@app.route("/update_status/<int:id>", methods=["GET", "POST"])
def update_status(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "staff":
        return "Access Denied"

    trek = Trek.query.get(id)

    if trek is None:
        return "Trek Not Found"

    if request.method == "GET":
        return render_template("update_status.html", trek=trek)

    elif request.method == "POST":

        trek.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("assigned_treks"))


@app.route("/participants/<int:id>")
def view_participants(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "staff":
        return "Access Denied"

    trek = Trek.query.get(id)

    if trek is None:
        return "Trek Not Found"

    bookings = Booking.query.filter(Booking.trek_id == id).all()

    return render_template(
        "view_participants.html",
        trek=trek,
        bookings=bookings,
        User=User
    )

@app.route("/staffs")
def view_staff():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    staffs = User.query.filter(User.role == "staff").all()

    return render_template("view_staff.html", staffs=staffs)


@app.route("/approve_staff/<int:id>")
def approve_staff(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    staff = User.query.get(id)

    if staff is None:
        return "Staff Not Found"

    staff.approved = True

    db.session.commit()

    flash("Staff approved successfully!", "success")
    return redirect(url_for("view_staff"))


@app.route("/blacklist_staff/<int:id>")
def blacklist_staff(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    staff = User.query.get(id)

    if staff is None:
        return "Staff Not Found"

    staff.blacklisted = True

    db.session.commit()

    flash("Staff blacklisted successfully!", "warning")
    return redirect(url_for("view_staff"))

@app.route("/assign_staff/<int:id>", methods=["GET", "POST"])
def assign_staff(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    trek = Trek.query.get(id)

    if trek is None:
        return "Trek Not Found"

    staffs = User.query.filter(User.role == "staff").all()

    if request.method == "GET":
        return render_template(
            "assign_staff.html",
            trek=trek,
            staffs=staffs
        )

    elif request.method == "POST":

        staff_id = request.form["staff_id"]
        trek.assigned_staff_id = int(staff_id)
        db.session.commit()

        flash("Staff assigned successfully!", "success")
        return redirect(url_for("view_treks"))

@app.route("/bookings")
def view_bookings():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    bookings = Booking.query.all()

    return render_template("view_bookings.html", bookings=bookings)


@app.route("/users")
def view_users():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    users = User.query.filter(User.role == "user").all()

    return render_template("view_users.html", users=users)


@app.route("/blacklist_user/<int:id>")
def blacklist_user(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    user = User.query.get(id)

    if user is None:
        return "User Not Found"

    user.blacklisted = True

    db.session.commit()

    flash("User blacklisted successfully!", "warning")
    return redirect(url_for("view_users"))


@app.route("/create_trek", methods=["GET", "POST"])
def create_trek():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    # Show the form
    if request.method == "GET":
        return render_template("create_trek.html")

    # Form submitted
    elif request.method == "POST":

        # Read form data
        trek_name = request.form["trek_name"]
        location = request.form["location"]
        difficulty = request.form["difficulty"]
        duration = int(request.form["duration"])
        available_slots = int(request.form["available_slots"])
        status = request.form["status"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # Convert string dates to Python date objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Create Trek object
        new_trek = Trek(
            trek_name=trek_name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            available_slots=available_slots,
            status=status,
            start_date=start_date,
            end_date=end_date
        )

        # Save to database
        db.session.add(new_trek)
        db.session.commit()

        flash("Trek created successfully!", "success")
        return redirect(url_for("view_treks"))



@app.route("/treks")
def view_treks():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    treks = Trek.query.all()

    return render_template("view_treks.html", treks=treks)


@app.route("/edit_trek/<int:id>", methods=["GET", "POST"])
def edit_trek(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    trek = Trek.query.get(id)

    if trek is None:
        return "Trek not found"

    if request.method == "GET":
        return render_template("edit_trek.html", trek=trek)

    elif request.method == "POST":

        trek.trek_name = request.form["trek_name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = int(request.form["duration"])
        trek.available_slots = int(request.form["available_slots"])
        trek.status = request.form["status"]

        db.session.commit()

        flash("Trek updated successfully!", "success")
        return redirect(url_for("view_treks"))

@app.route("/delete_trek/<int:id>")
def delete_trek(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return "Access Denied"

    trek = Trek.query.get(id)

    if trek is None:
        return "Trek Not Found"

    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully!", "success")
    return redirect(url_for("view_treks"))


@app.route("/register", methods=["GET", "POST"])
def register():

    # If the user opens the registration page
    if request.method == "GET":
        return render_template("register.html")

    # If the user submits the registration form
    elif request.method == "POST":

        # Read form data
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        # Check if the email already exists
        existing_user = User.query.filter(User.email == email).first()

        if existing_user is not None:
            flash("Email already exists. Please use a different email.", "danger")
            return redirect(url_for("register"))

        # Decide approval status
        if role == "user":
            approved = True
        else:
            approved = False

        # Create a new user object
        new_user = User(
            name=name,
            email=email,
            password=password,
            role=role,
            approved=approved,
            blacklisted=False
        )

        # Save the user
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        existing_user = User.query.filter(User.email == email).first()

        if existing_user is None:
            flash("Invalid email.", "danger")
            return redirect(url_for("login"))

        if existing_user.password != password:
            flash("Invalid password.", "danger")
            return redirect(url_for("login"))

        if not existing_user.approved:
            flash("Your account is waiting for admin approval.", "warning")
            return redirect(url_for("login"))

        if existing_user.blacklisted:
            flash("Your account has been blacklisted.", "danger")
            return redirect(url_for("login"))

        session["user_id"] = existing_user.id
        session["name"] = existing_user.name
        session["role"] = existing_user.role

        if existing_user.role == "admin":
            flash("Login successful!", "success")
            return redirect(url_for("admin_dashboard"))
        elif existing_user.role == "staff":
            flash("Login successful!", "success")
            return redirect(url_for("staff_dashboard"))
        elif existing_user.role == "user":
            flash("Login successful!", "success")
            return redirect(url_for("user_dashboard"))

        return "Invalid Role"


@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))

if __name__ == "__main__": #if another file import app then server does not automatically starts   
    app.run(debug=True)







