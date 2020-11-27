from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.posts.forms import PostForm

"""Create the Blueprint for posts"""
posts = Blueprint("posts", __name__)

"""Each section creates the page when the respective part is called"""


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        """Update the data base"""
        db.session.add(post)
        db.session.commit()
        """ Gives feedback notification after new notes posted with a green box showing: Your notes have been uploaded."""
        flash("Your notes have been uploaded!", "success")
        """After posting the new note, re-direct user back to home page"""
        return redirect(url_for("main.home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Notes"
    )


"""Access a specific post"""


@posts.route("/post/int:<post_id>")
def post(post_id):
    """If the post does not exist, return 404 error page"""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


"""Update a post"""


@posts.route("/post/int:<post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    """Access the note"""
    post = Post.query.get_or_404(post_id)
    """Check if the current login user is the user who wrote the note(only who wrote the note can edit the note)"""
    if post.author != current_user:
        """Forbid from deleting if the user is not the author"""
        abort(403)
    """validattion and update to the data base about what has just been changed"""
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        """Notification of actions completed with a green box"""
        flash("Your note has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Notes", form=form, legend="Update Notes"
    )


"""Create the page when a user wants to delete a note"""


@posts.route("/post/int:<post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    """Access the note"""
    post = Post.query.get_or_404(post_id)
    """Validate if the user is the same who wrote"""
    if post.author != current_user:
        """Forbid from deleting if the user is not the author"""
        abort(403)
    """Update the database about what has been deleted"""
    db.session.delete(post)
    db.session.commit()
    flash("Your note has been deleted!", "success")
    return redirect(url_for("main.home"))