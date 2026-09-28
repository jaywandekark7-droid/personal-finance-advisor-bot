from collections import defaultdict
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Income, Expense
from .advisor import get_advice

main_bp = Blueprint("main", __name__)

def totals():
    income = sum(x.amount for x in current_user.incomes)
    expense = sum(x.amount for x in current_user.expenses)
    return income, expense, income - expense

@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    income, expense, balance = totals()
    cats = defaultdict(float)
    for e in current_user.expenses:
        cats[e.category] += e.amount
    labels = list(cats.keys())
    values = [round(cats[x], 2) for x in labels]
    return render_template(
        "dashboard.html", income=income, expense=expense, balance=balance,
        labels=labels, values=values, recent=current_user.expenses[-5:][::-1]
    )

@main_bp.route("/income", methods=["POST"])
@login_required
def add_income():
    try:
        amount = float(request.form["amount"])
        if amount <= 0: raise ValueError
    except ValueError:
        flash("Enter a valid positive income amount.", "danger")
        return redirect(url_for("main.dashboard"))
    db.session.add(Income(user_id=current_user.id, source=request.form["source"], amount=amount))
    db.session.commit()
    flash("Income added.", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.route("/expense", methods=["POST"])
@login_required
def add_expense():
    try:
        amount = float(request.form["amount"])
        if amount <= 0: raise ValueError
    except ValueError:
        flash("Enter a valid positive expense amount.", "danger")
        return redirect(url_for("main.dashboard"))
    db.session.add(Expense(
        user_id=current_user.id,
        category=request.form["category"],
        description=request.form.get("description", ""),
        amount=amount
    ))
    db.session.commit()
    flash("Expense added.", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.route("/advisor")
@login_required
def advisor():
    income = [{"amount": x.amount} for x in current_user.incomes]
    expenses = [{"amount": x.amount, "category": x.category} for x in current_user.expenses]
    advice = get_advice(income, expenses)
    return render_template("advisor.html", advice=advice)

@main_bp.route("/reports")
@login_required
def reports():
    income, expense, balance = totals()
    monthly = defaultdict(lambda: {"income": 0, "expense": 0})
    for x in current_user.incomes:
        monthly[x.date.strftime("%b %Y")]["income"] += x.amount
    for x in current_user.expenses:
        monthly[x.date.strftime("%b %Y")]["expense"] += x.amount
    months = list(monthly.keys())
    return render_template(
        "reports.html", income=income, expense=expense, balance=balance,
        months=months,
        monthly_income=[monthly[m]["income"] for m in months],
        monthly_expense=[monthly[m]["expense"] for m in months]
    )
