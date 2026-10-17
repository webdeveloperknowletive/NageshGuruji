import os
import uuid
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.extensions import db
from app.models.content import BlogPost, Testimonial, GurujiProfile, MediaFile, Banner
from app.services.rbac_service import login_required, permission_required, get_current_admin
from app.services.audit_service import AuditService

content_bp = Blueprint("content", __name__, url_prefix="/admin/content")


# -------------------------------------------------------------
# Blog
# -------------------------------------------------------------
@content_bp.route("/blog")
@login_required
@permission_required("content", "view")
def blog_list():
    user = get_current_admin()
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template("content/blog.html", current_user=user, posts=posts, active_page="blog")


@content_bp.route("/blog/create", methods=["POST"])
@login_required
@permission_required("content", "create")
def blog_create():
    user = get_current_admin()
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "Vedic Wisdom").strip()
    content = request.form.get("content", "").strip()
    excerpt = request.form.get("excerpt", "").strip()
    cover_image = request.form.get("cover_image", "").strip()

    if not title or not content:
        flash("Title and content are required.", "danger")
        return redirect(url_for("content.blog_list"))

    slug = title.lower().replace(" ", "-").replace("/", "-")[:80] + f"-{int(datetime.now(timezone.utc).timestamp())}"
    post = BlogPost(
        title=title,
        slug=slug,
        category=category,
        content=content,
        excerpt=excerpt or content[:160],
        cover_image=cover_image or "/static/img/blog-default.jpg",
        author_name=user.full_name,
        is_published=True,
    )
    db.session.add(post)
    db.session.commit()

    AuditService.log(
        action="BLOG_POST_CREATE",
        module="content",
        actor_email=user.email,
        actor_user_id=user.id,
        entity_type="BlogPost",
        entity_id=str(post.id),
        details={"title": title},
    )
    flash("Blog article published successfully.", "success")
    return redirect(url_for("content.blog_list"))


@content_bp.route("/blog/<int:post_id>/edit", methods=["POST"])
@login_required
@permission_required("content", "edit")
def blog_update(post_id):
    user = get_current_admin()
    post = BlogPost.query.get_or_404(post_id)

    title = request.form.get("title", "").strip()
    category = request.form.get("category", post.category).strip()
    content = request.form.get("content", "").strip()
    excerpt = request.form.get("excerpt", "").strip()
    cover_image = request.form.get("cover_image", "").strip()
    is_published = request.form.get("is_published") == "1" or request.form.get("is_published") == "on"

    if title:
        post.title = title
    if content:
        post.content = content
    post.category = category
    if excerpt:
        post.excerpt = excerpt
    if cover_image:
        post.cover_image = cover_image
    post.is_published = is_published
    post.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    AuditService.log(
        action="BLOG_POST_UPDATE",
        module="content",
        actor_email=user.email,
        actor_user_id=user.id,
        entity_type="BlogPost",
        entity_id=str(post.id),
        details={"title": post.title, "is_published": post.is_published},
    )
    flash("Blog article updated successfully.", "success")
    return redirect(url_for("content.blog_list"))


@content_bp.route("/blog/<int:post_id>/delete", methods=["POST"])
@login_required
@permission_required("content", "delete")
def blog_delete(post_id):
    user = get_current_admin()
    post = BlogPost.query.get_or_404(post_id)
    title = post.title
    db.session.delete(post)
    db.session.commit()

    AuditService.log(
        action="BLOG_POST_DELETE",
        module="content",
        actor_email=user.email,
        actor_user_id=user.id,
        entity_type="BlogPost",
        entity_id=str(post_id),
        details={"title": title},
    )
    flash(f"Article '{title}' deleted.", "success")
    return redirect(url_for("content.blog_list"))


# -------------------------------------------------------------
# Testimonials
# -------------------------------------------------------------
@content_bp.route("/testimonials")
@login_required
@permission_required("content", "view")
def testimonials_list():
    user = get_current_admin()
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template("content/testimonials.html", current_user=user, testimonials=testimonials, active_page="testimonials")


@content_bp.route("/testimonials/create", methods=["POST"])
@login_required
@permission_required("content", "create")
def testimonial_create():
    user = get_current_admin()
    name = request.form.get("devotee_name", "").strip()
    city = request.form.get("devotee_city", "").strip()
    rating = request.form.get("rating", 5, type=int)
    service = request.form.get("service_or_product", "").strip()
    blessing = request.form.get("blessing_text", "").strip()

    if not name or not blessing:
        flash("Devotee name and blessing text are required.", "danger")
        return redirect(url_for("content.testimonials_list"))

    t = Testimonial(
        devotee_name=name,
        devotee_city=city,
        rating=rating,
        service_or_product=service,
        blessing_text=blessing,
        is_approved=True,
    )
    db.session.add(t)
    db.session.commit()
    flash("Testimonial added.", "success")
    return redirect(url_for("content.testimonials_list"))


@content_bp.route("/testimonials/<int:testimonial_id>/edit", methods=["POST"])
@login_required
@permission_required("content", "edit")
def testimonial_update(testimonial_id):
    user = get_current_admin()
    t = Testimonial.query.get_or_404(testimonial_id)
    t.devotee_name = request.form.get("devotee_name", t.devotee_name).strip()
    t.devotee_city = request.form.get("devotee_city", t.devotee_city).strip()
    t.rating = request.form.get("rating", t.rating, type=int)
    t.service_or_product = request.form.get("service_or_product", t.service_or_product).strip()
    t.blessing_text = request.form.get("blessing_text", t.blessing_text).strip()
    t.is_approved = request.form.get("is_approved") == "1" or request.form.get("is_approved") == "on"
    db.session.commit()

    AuditService.log(
        action="TESTIMONIAL_UPDATE",
        module="content",
        actor_email=user.email,
        actor_user_id=user.id,
        entity_type="Testimonial",
        entity_id=str(t.id),
        details={"name": t.devotee_name, "is_approved": t.is_approved},
    )
    flash("Testimonial updated.", "success")
    return redirect(url_for("content.testimonials_list"))


@content_bp.route("/testimonials/<int:testimonial_id>/delete", methods=["POST"])
@login_required
@permission_required("content", "delete")
def testimonial_delete(testimonial_id):
    user = get_current_admin()
    t = Testimonial.query.get_or_404(testimonial_id)
    name = t.devotee_name
    db.session.delete(t)
    db.session.commit()

    AuditService.log(
        action="TESTIMONIAL_DELETE",
        module="content",
        actor_email=user.email,
        actor_user_id=user.id,
        entity_type="Testimonial",
        entity_id=str(testimonial_id),
        details={"devotee_name": name},
    )
    flash(f"Testimonial from '{name}' deleted.", "success")
    return redirect(url_for("content.testimonials_list"))


# -------------------------------------------------------------
# Banners & Hero Announcements
# -------------------------------------------------------------
@content_bp.route("/banners")
@login_required
@permission_required("content", "view")
def banners_list():
    user = get_current_admin()
    banners = Banner.query.order_by(Banner.sort_order.asc(), Banner.created_at.desc()).all()
    return render_template("content/banners.html", current_user=user, banners=banners, active_page="banners")


@content_bp.route("/banners/create", methods=["POST"])
@login_required
@permission_required("content", "create")
def banner_create():
    user = get_current_admin()
    title = request.form.get("title", "").strip()
    subtitle = request.form.get("subtitle", "").strip()
    position = request.form.get("position", "hero").strip()
    image_url = request.form.get("image_url", "").strip()
    link_url = request.form.get("link_url", "#shop").strip()
    button_text = request.form.get("button_text", "Explore Collection →").strip()
    sort_order = request.form.get("sort_order", 0, type=int)

    if not title:
        flash("Banner title is required.", "danger")
        return redirect(url_for("content.banners_list"))

    # Handle image upload if provided
    if "banner_image" in request.files:
        file = request.files["banner_image"]
        if file and file.filename != "":
            orig_name = secure_filename(file.filename)
            ext = orig_name.rsplit(".", 1)[-1].lower() if "." in orig_name else ""
            allowed = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", {"jpg", "jpeg", "png", "webp", "svg"})
            if ext in allowed:
                prefix = "logo" if position == "logo" else ("bg" if "bg" in position else "banner")
                unique_filename = f"{prefix}_{uuid.uuid4().hex[:8]}_{orig_name}"
                upload_folder = os.path.join(current_app.root_path, "static", "uploads")
                os.makedirs(upload_folder, exist_ok=True)
                save_path = os.path.join(upload_folder, unique_filename)
                file.save(save_path)
                image_url = f"/static/uploads/{unique_filename}"

    banner = Banner(
        title=title,
        subtitle=subtitle,
        position=position,
        image_url=image_url or None,
        link_url=link_url,
        button_text=button_text,
        sort_order=sort_order,
        is_active=True,
    )
    db.session.add(banner)
    db.session.commit()

    AuditService.log(
        action="BANNER_CREATE",
        module="content",
        actor_email=user.email,
        actor_user_id=user.id,
        entity_type="Banner",
        entity_id=str(banner.id),
        details={"title": title, "position": position},
    )
    flash(f"Asset / Banner '{title}' created successfully.", "success")
    return redirect(url_for("content.banners_list"))


@content_bp.route("/banners/<int:banner_id>/edit", methods=["POST"])
@login_required
@permission_required("content", "edit")
def banner_update(banner_id):
    user = get_current_admin()
    banner = Banner.query.get_or_404(banner_id)

    if request.form.get("title"):
        banner.title = request.form.get("title").strip()
    if request.form.get("subtitle") is not None:
        banner.subtitle = request.form.get("subtitle").strip() or None
    if request.form.get("position"):
        banner.position = request.form.get("position").strip()

    # Handle image file upload or direct URL
    if "banner_image" in request.files:
        file = request.files["banner_image"]
        if file and file.filename != "":
            orig_name = secure_filename(file.filename)
            ext = orig_name.rsplit(".", 1)[-1].lower() if "." in orig_name else ""
            allowed = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", {"jpg", "jpeg", "png", "webp", "svg"})
            if ext in allowed:
                prefix = "logo" if banner.position == "logo" else ("bg" if "bg" in banner.position else "banner")
                unique_filename = f"{prefix}_{uuid.uuid4().hex[:8]}_{orig_name}"
                upload_folder = os.path.join(current_app.root_path, "static", "uploads")
                os.makedirs(upload_folder, exist_ok=True)
                save_path = os.path.join(upload_folder, unique_filename)
                file.save(save_path)
                banner.image_url = f"/static/uploads/{unique_filename}"
    elif request.form.get("image_url") is not None:
        banner.image_url = request.form.get("image_url").strip() or None

    if request.form.get("link_url") is not None:
        banner.link_url = request.form.get("link_url").strip() or "#shop"
    if request.form.get("button_text") is not None:
        banner.button_text = request.form.get("button_text").strip() or "Explore"
    if request.form.get("sort_order") is not None:
        banner.sort_order = request.form.get("sort_order", banner.sort_order, type=int)
    banner.is_active = request.form.get("is_active") == "1" or request.form.get("is_active") == "on"

    db.session.commit()

    AuditService.log(
        action="BANNER_UPDATE",
        module="content",
        actor_email=user.email,
        actor_user_id=user.id,
        entity_type="Banner",
        entity_id=str(banner.id),
        details={"title": banner.title, "is_active": banner.is_active},
    )
    flash("Banner updated successfully.", "success")
    return redirect(url_for("content.banners_list"))


@content_bp.route("/banners/<int:banner_id>/delete", methods=["POST"])
@login_required
@permission_required("content", "delete")
def banner_delete(banner_id):
    user = get_current_admin()
    banner = Banner.query.get_or_404(banner_id)
    title = banner.title
    db.session.delete(banner)
    db.session.commit()

    AuditService.log(
        action="BANNER_DELETE",
        module="content",
        actor_email=user.email,
        actor_user_id=user.id,
        entity_type="Banner",
        entity_id=str(banner_id),
        details={"title": title},
    )
    flash(f"Banner '{title}' deleted.", "success")
    return redirect(url_for("content.banners_list"))



# -------------------------------------------------------------
# Guruji Profile
# -------------------------------------------------------------
@content_bp.route("/guruji", methods=["GET", "POST"])
@login_required
@permission_required("content", "view")
def guruji_profile():
    user = get_current_admin()
    profile = GurujiProfile.query.first()
    if not profile:
        profile = GurujiProfile(
            full_title="Param Pujya Swami Dayanand Saraswati Ji",
            spiritual_lineage="Advaita Vedanta & Rig Vedic Tradition",
            bio="Guiding millions across the globe in spiritual wisdom, sacred Vedic pujas, and astrological alignment for peace and prosperity.",
            darshan_timings="Tuesday & Saturday: 09:00 AM - 12:30 PM",
            ashram_address="Shanti Dham Ashram, Rishikesh, Uttarakhand",
            contact_phone="+91 98765 43210",
            contact_email="seva@spiritualcommerce.org",
        )
        db.session.add(profile)
        db.session.commit()

    if request.method == "POST":
        if not user.has_permission("content", "edit") and not (user.role and user.role.code == "super_admin"):
            abort(403)
        profile.full_title = request.form.get("full_title", profile.full_title).strip()
        profile.spiritual_lineage = request.form.get("spiritual_lineage", profile.spiritual_lineage or "").strip()
        profile.bio = request.form.get("bio", profile.bio).strip()
        profile.secondary_bio = request.form.get("secondary_bio", profile.secondary_bio or "").strip()
        profile.experience_years = request.form.get("experience_years", profile.experience_years or "25+").strip()
        profile.consultations_count = request.form.get("consultations_count", profile.consultations_count or "10K+").strip()
        profile.pujas_count = request.form.get("pujas_count", profile.pujas_count or "5000+").strip()
        profile.button_text = request.form.get("button_text", profile.button_text or "Book Consultation →").strip()
        profile.button_url = request.form.get("button_url", profile.button_url or "#jyotish").strip()
        profile.darshan_timings = request.form.get("darshan_timings", profile.darshan_timings or "").strip()
        profile.ashram_address = request.form.get("ashram_address", profile.ashram_address or "").strip()
        profile.contact_phone = request.form.get("contact_phone", profile.contact_phone or "").strip()
        profile.contact_email = request.form.get("contact_email", profile.contact_email or "").strip()

        # Handle Profile Image: File upload takes precedence, then image URL
        if "profile_photo" in request.files:
            file = request.files["profile_photo"]
            if file and file.filename != "":
                orig_name = secure_filename(file.filename)
                ext = orig_name.rsplit(".", 1)[-1].lower() if "." in orig_name else ""
                allowed = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", {"jpg", "jpeg", "png", "webp", "svg"})
                if ext in allowed:
                    unique_filename = f"guruji_{uuid.uuid4().hex[:8]}_{orig_name}"
                    upload_folder = os.path.join(current_app.root_path, "static", "uploads")
                    os.makedirs(upload_folder, exist_ok=True)
                    save_path = os.path.join(upload_folder, unique_filename)
                    file.save(save_path)
                    profile.profile_image = f"/static/uploads/{unique_filename}"
        
        img_url = request.form.get("profile_image", "").strip()
        if img_url and ("profile_photo" not in request.files or not request.files["profile_photo"].filename):
            profile.profile_image = img_url

        # Visibility settings map
        def is_on(key):
            return request.form.get(key) in ("1", "true", "on")

        visibility = {
            "show_photo": is_on("show_photo"),
            "show_lineage": is_on("show_lineage"),
            "show_bio": is_on("show_bio"),
            "show_secondary_bio": is_on("show_secondary_bio"),
            "show_stats": is_on("show_stats"),
            "show_experience": is_on("show_experience"),
            "show_consultations": is_on("show_consultations"),
            "show_pujas": is_on("show_pujas"),
            "show_cta_button": is_on("show_cta_button"),
            "show_darshan": is_on("show_darshan"),
            "show_ashram": is_on("show_ashram"),
            "show_contact": is_on("show_contact"),
        }
        profile.visibility_settings = visibility

        db.session.commit()

        AuditService.log(
            action="GURUJI_PROFILE_UPDATE",
            module="content",
            actor_email=user.email,
            actor_user_id=user.id,
            entity_type="GurujiProfile",
            entity_id=str(profile.id),
        )
        flash("Guruji's profile and display visibility updated successfully.", "success")

    return render_template("content/guruji.html", current_user=user, profile=profile, active_page="guruji")


# -------------------------------------------------------------
# Media Library
# -------------------------------------------------------------
@content_bp.route("/media")
@login_required
@permission_required("media", "view")
def media_list():
    user = get_current_admin()
    media_files = MediaFile.query.order_by(MediaFile.created_at.desc()).all()
    return render_template("content/media.html", current_user=user, media_files=media_files, active_page="media")


@content_bp.route("/media/upload", methods=["POST"])
@login_required
@permission_required("media", "upload")
def media_upload():
    user = get_current_admin()
    if "file" not in request.files:
        flash("No file part in the request.", "danger")
        return redirect(url_for("content.media_list"))

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected.", "danger")
        return redirect(url_for("content.media_list"))

    orig_name = secure_filename(file.filename)
    ext = orig_name.rsplit(".", 1)[-1].lower() if "." in orig_name else ""
    allowed = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", {"jpg", "jpeg", "png", "webp", "svg", "pdf"})

    if ext not in allowed:
        flash(f"File type '.{ext}' is not permitted.", "danger")
        return redirect(url_for("content.media_list"))

    unique_filename = f"{uuid.uuid4().hex[:12]}_{orig_name}"
    upload_folder = current_app.config.get("UPLOAD_FOLDER")
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, unique_filename)
    file.save(save_path)

    size = os.path.getsize(save_path)
    media = MediaFile(
        filename=unique_filename,
        original_name=orig_name,
        file_path=f"/static/uploads/{unique_filename}",
        file_size=size,
        mime_type=file.mimetype or "image/jpeg",
        uploaded_by_id=user.id,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(media)
    db.session.commit()

    AuditService.log(
        action="MEDIA_UPLOAD",
        module="content",
        actor_email=user.email,
        actor_user_id=user.id,
        entity_type="MediaFile",
        entity_id=str(media.id),
        details={"filename": unique_filename, "size": size},
    )
    flash("Asset uploaded successfully.", "success")
    return redirect(url_for("content.media_list"))
