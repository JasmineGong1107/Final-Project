from flask import Blueprint, render_template, request
from app.models import Post

"""Create a Blueprint"""
main = Blueprint("main", __name__)


"""create the home page when it is called"""


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    """Order notes by most recently posted, set number of notes per page =4"""
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("home.html", posts=posts)


"""create the about page when it is called"""


@main.route("/about")
def about():
    return render_template("about.html", title="About")