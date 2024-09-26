from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Posts, User, Like, Comment
from .import db

views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
@views.route("/home")
@login_required
def home():
    posts = Posts.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/posts", methods=['GET', 'POST'])
@login_required
def posts():
    if request.method == "POST":
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            posts = Posts(text=text, author=current_user.id)
            db.session.add(posts)
            db.session.commit()
            flash('Post created!', category='success')
        return redirect(url_for('views.posts'))

    return render_template("posts.html", user=current_user)

# this might be the issue for why the 's username appears


@views.route("/posts/<username>")
@login_required
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No user with that username exists.", category='error')
        return redirect(url_for('views.home'))

    posts = Posts.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@ views.route("/delete-posts/<id>")
@ login_required
def delete_post(id):
    posts = Posts.query.filter_by(id=id).first()
    if not posts:
        flash("Post does not exist.", category='error')
    elif posts.author != current_user.id:
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(posts)
        db.session.commit()
        flash("Post deleted.", category="success")
    return redirect(url_for('views.posts'))


@views.route("/like-posts/<posts_id>", methods=['POST'])
@login_required
def like(posts_id):
    posts = Posts.query.filter_by(id=posts_id).first()
    like = Like.query.filter_by(
        author=current_user.id, posts_id=posts_id).first()
    if not posts:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, posts_id=posts_id)
        db.session.add(like)
        db.session.commit()
    return jsonify({"likes": len(posts.likes), "liked": current_user.id in map(lambda x: x.author, posts.likes)})


@views.route("/create-comment/<posts_id>", methods=['POST'])
@login_required
def create_comment(posts_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        posts = Posts.query.filter_by(id=posts_id)
        if posts:
            comment = Comment(
                text=text, author=current_user.id, posts_id=posts_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')
    return redirect(url_for('views.posts'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.posts'))
