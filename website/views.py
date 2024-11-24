from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Clothdetails, Student
from . import db
from flask_login import current_user
from . import student_login_required
from . import employee_login_required

views = Blueprint("views", __name__)

@views.route("/")
def portal():
    return render_template("front.html")


@views.route("/home", methods=["GET", "POST"])
@student_login_required
def home():
    cloth_detail = Clothdetails.query.filter_by(student_id=current_user.id).first()
    # if cloth_detail:
    #         return redirect(url_for('views.view_status'))
    if request.method == "POST":
        
        kurta = int(request.form.get("kurta") or 0)
        pajama = int(request.form.get("pajama") or 0)
        shirt = int(request.form.get("shirt") or 0)
        tshirt = int(request.form.get("tshirt") or 0)
        pant = int(request.form.get("pant") or 0)
        lower = int(request.form.get("lower") or 0)
        shorts = int(request.form.get("shorts") or 0)
        bedsheet = int(request.form.get("bedsheet") or 0)
        pillowcover = int(request.form.get("pillowcover") or 0)
        towel = int(request.form.get("towel") or 0)
        duppata = int(request.form.get("duppata") or 0)

        cloth = [kurta, pajama, shirt, tshirt, pant, lower, shorts, bedsheet, pillowcover, towel, duppata]
        total_clothes = sum(cloth)
        if total_clothes > 10:
            flash("Number of clothes must be less than or equal to 10!", category="error")
        elif total_clothes == 0:
            flash("You have not added any clothes!", category="error")
        else:
            Clothdetails.query.filter_by(student_id=current_user.id).delete()
            new_cloths = Clothdetails(
                kurta=kurta, pajama=pajama, shirt=shirt, tshirt=tshirt, pant=pant, lower=lower, shorts=shorts, bedsheet=bedsheet, pillowcover=pillowcover, towel=towel, duppata=duppata,  # Unpacking cloth_counts dictionary
                status = "submitted", student_id=current_user.id
            )
            db.session.add(new_cloths)
            db.session.commit()
            flash("Cloth details submitted", category="success")
            


            user_cloth_entries = Clothdetails.query.filter_by(student_id=current_user.id).order_by(Clothdetails.id.desc()).offset(2).all()
            for entry in user_cloth_entries:
                db.session.delete(entry)
            db.session.commit()

            return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user, cloth_detail=cloth_detail)


# @views.route('/view_status')
# def view_status():
#     cloth_detail = Clothdetails.query.filter_by(student_id=current_user.id).first()
#     return render_template('home.html', cloth_detail=cloth_detail, user=current_user, status=cloth_detail.status)

# @views.route('/view_status', methods=["GET", "POST"])
# def view_status():
#     cloth_detail = Clothdetails.query.filter_by(student_id=current_user.id).first()
#     if not cloth_detail:
#         flash("No cloth details found.", category="error")
#         return redirect(url_for('views.home'))  # If no cloth details found, redirect to home page
    
    # return render_template('home.html', cloth_detail=cloth_detail, user=current_user)

# @views.route("/", methods=["GET", "POST"])
# @login_required
# def home():
#     cloth_detail = Clothdetails.query.filter_by(student_id=current_user.id).first()
#     if cloth_detail:
#         return redirect(url_for('views.view_status'))  # Redirect to view status if cloth details exist

#     if request.method == "POST":
#         # Get the cloth details from the form submission
#         kurta = int(request.form.get("kurta") or 0)
#         pajama = int(request.form.get("pajama") or 0)
#         shirt = int(request.form.get("shirt") or 0)
#         tshirt = int(request.form.get("tshirt") or 0)
#         pant = int(request.form.get("pant") or 0)
#         lower = int(request.form.get("lower") or 0)
#         shorts = int(request.form.get("shorts") or 0)
#         bedsheet = int(request.form.get("bedsheet") or 0)
#         pillowcover = int(request.form.get("pillowcover") or 0)
#         towel = int(request.form.get("towel") or 0)
#         duppata = int(request.form.get("duppata") or 0)

#         # Sum of all clothes
#         cloth = [kurta, pajama, shirt, tshirt, pant, lower, shorts, bedsheet, pillowcover, towel, duppata]
#         total_clothes = sum(cloth)

#         # Validation checks
#         if total_clothes > 10:
#             flash("Number of clothes must be less than or equal to 10!", category="error")
#         elif total_clothes == 0:
#             flash("You have not added any clothes!", category="error")
#         else:
#             # Delete existing entries and add new cloth details
#             if Clothdetails.query.filter_by(student_id=current_user.id).first():
#                 Clothdetails.query.filter_by(student_id=current_user.id).delete()
            
#             new_cloths = Clothdetails(
#                 kurta=kurta, pajama=pajama, shirt=shirt, tshirt=tshirt, pant=pant, 
#                 lower=lower, shorts=shorts, bedsheet=bedsheet, pillowcover=pillowcover, 
#                 towel=towel, duppata=duppata, student_id=current_user.id
#             )
#             db.session.add(new_cloths)
#             db.session.commit()
#             flash("Cloth details submitted", category="success")

#             # Retain only the latest 2 entries
#             user_cloth_entries = Clothdetails.query.filter_by(student_id=current_user.id).order_by(Clothdetails.id.desc()).offset(2).all()
#             for entry in user_cloth_entries:
#                 db.session.delete(entry)
#             db.session.commit()

#             return redirect(url_for('views.view_status'))  # Redirect to view status page after submission

#     return render_template("home.html", user=current_user, cloth_detail=cloth_detail)

# @views.route('/view_status')
# def view_status():
#     cloth_detail = Clothdetails.query.filter_by(student_id=current_user.id).first()
#     if not cloth_detail:
#         flash("No cloth details found.", category="error")
#         return redirect(url_for('views.home'))  # If no cloth details found, redirect to home page
    
#     return render_template('home.html', cloth_detail=cloth_detail, user=current_user, status=cloth_detail.status)






# @views.route("/", methods=["GET", "POST"])
# @login_required
# def home():
#     status = "received"  # Default status

#     if request.method == "POST":
#         # Extract cloth counts from the form
#         kurta = int(request.form.get("kurta") or 0)
#         pajama = int(request.form.get("pajama") or 0)
#         shirt = int(request.form.get("shirt") or 0)
#         tshirt = int(request.form.get("tshirt") or 0)
#         pant = int(request.form.get("pant") or 0)
#         lower = int(request.form.get("lower") or 0)
#         shorts = int(request.form.get("shorts") or 0)
#         bedsheet = int(request.form.get("bedsheet") or 0)
#         pillowcover = int(request.form.get("pillowcover") or 0)
#         towel = int(request.form.get("towel") or 0)
#         duppata = int(request.form.get("duppata") or 0)

#         # Calculate total clothes
#         cloth = [kurta, pajama, shirt, tshirt, pant, lower, shorts, bedsheet, pillowcover, towel, duppata]
#         total_clothes = sum(cloth)

#         # Validation checks
#         if total_clothes > 10:
#             flash("Number of clothes must be less than or equal to 10!", category="error")
#         elif total_clothes == 0:
#             flash("You have not added any clothes!", category="error")
#         else:
#             # Set status as "submitted" when valid data is entered
#             status = "submitted"

#             # Delete all existing entries for the current user (optional)
#             Clothdetails.query.filter_by(student_id=current_user.id).delete()

#             # Add new cloth entry
#             new_cloths = Clothdetails(
#                 kurta=kurta,
#                 pajama=pajama,
#                 shirt=shirt,
#                 tshirt=tshirt,
#                 pant=pant,
#                 lower=lower,
#                 shorts=shorts,
#                 bedsheet=bedsheet,
#                 pillowcover=pillowcover,
#                 towel=towel,
#                 duppata=duppata,
#                 status=status,  # Set status in new entry
#                 student_id=current_user.id
#             )
#             db.session.add(new_cloths)
#             db.session.commit()
#             flash("Cloth details submitted", category="success")

#             # Retain only the latest two entries
#             user_cloth_entries = Clothdetails.query.filter_by(student_id=current_user.id).order_by(Clothdetails.id.desc()).offset(2).all()
#             for entry in user_cloth_entries:
#                 db.session.delete(entry)
#             db.session.commit()

#             return redirect(url_for("views.home"))

#     return render_template("home.html", user=current_user, status=status)



@views.route('/laundry_management', methods=['GET', 'POST'])
@employee_login_required
def laundry_management():
    query = request.args.get('query')  # Get search query from the GET request
    
    # If there's a search query, filter students based on LEN or email
    if query:
        students = Student.query.filter((Student.Len == query) | (Student.email == query)).all()
        cloth_entries = []
        for student in students:
            cloth_details = Clothdetails.query.filter_by(student_id=student.id).first()
            if cloth_details:
                cloth_entries.append((cloth_details, student))
    else:
        # If no query, display all cloth entries
        cloth_entries = []
        all_students = Student.query.all()
        for student in all_students:
            cloth_details = Clothdetails.query.filter_by(student_id=student.id).first()
            if cloth_details:
                cloth_entries.append((cloth_details, student))
    
    return render_template('laundrymain.html', cloth_entries=cloth_entries, user=current_user)

# Route to handle the update of cloth details and status
@views.route('/update_cloth_details', methods=['POST'])
def update_cloth_details():
    # Get the form data
    cloth_id = request.form.get('cloth_id')
    statusemp = request.form.get('status')
    
    # Get the updated quantities for each cloth type
    kurta = request.form.get('kurta', type=int)
    pajama = request.form.get('pajama', type=int)
    shirt = request.form.get('shirt', type=int)
    tshirt = request.form.get('tshirt', type=int)
    pant = request.form.get('pant', type=int)
    lower = request.form.get('lower', type=int)
    shorts = request.form.get('shorts', type=int)
    bedsheet = request.form.get('bedsheet', type=int)
    pillowcover = request.form.get('pillowcover', type=int)
    towel = request.form.get('towel', type=int)
    duppata = request.form.get('duppata', type=int)
    
    # Find the cloth entry by ID
    cloth_entry = Clothdetails.query.get(cloth_id)
    
    if cloth_entry:
        # Update the quantities for each cloth item
        cloth_entry.kurta = kurta
        cloth_entry.pajama = pajama
        cloth_entry.shirt = shirt
        cloth_entry.tshirt = tshirt
        cloth_entry.pant = pant
        cloth_entry.lower = lower
        cloth_entry.shorts = shorts
        cloth_entry.bedsheet = bedsheet
        cloth_entry.pillowcover = pillowcover
        cloth_entry.towel = towel
        cloth_entry.duppata = duppata
        
        # Update the status
        if statusemp == "dropped":
            cloth_entry.status = "dropped"
        elif statusemp == "completed":
            cloth_entry.status = "washed"
        elif statusemp == "pickedup":
            cloth_entry.status = "recieved"
        
        # Commit changes to the database
        db.session.commit()
        
    return redirect(url_for('views.laundry_management'))  # Redirect to the laundry management page
