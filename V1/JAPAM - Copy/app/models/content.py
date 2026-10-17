from datetime import datetime, timezone
from app.extensions import db


class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(280), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(500), nullable=True)
    author_name = db.Column(db.String(150), default="Spiritual Editorial Team", nullable=False)
    category = db.Column(db.String(100), default="Vedic Wisdom", nullable=False)
    tags = db.Column(db.String(255), nullable=True)
    is_published = db.Column(db.Boolean, default=True, nullable=False, index=True)
    views_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<BlogPost {self.title}>"


class Testimonial(db.Model):
    __tablename__ = "testimonials"

    id = db.Column(db.Integer, primary_key=True)
    devotee_name = db.Column(db.String(150), nullable=False)
    devotee_city = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Integer, default=5, nullable=False)
    photo_url = db.Column(db.String(500), nullable=True)
    service_or_product = db.Column(db.String(150), nullable=True)
    blessing_text = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Testimonial {self.devotee_name}>"


class GurujiProfile(db.Model):
    __tablename__ = "guruji_profile"

    id = db.Column(db.Integer, primary_key=True)
    full_title = db.Column(db.String(255), nullable=False)
    spiritual_lineage = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=False)
    secondary_bio = db.Column(db.Text, nullable=True)
    experience_years = db.Column(db.String(50), default="25+", nullable=True)
    consultations_count = db.Column(db.String(50), default="10K+", nullable=True)
    pujas_count = db.Column(db.String(50), default="5000+", nullable=True)
    button_text = db.Column(db.String(100), default="Book Consultation →", nullable=True)
    button_url = db.Column(db.String(255), default="#jyotish", nullable=True)
    darshan_timings = db.Column(db.String(255), nullable=True)
    ashram_address = db.Column(db.Text, nullable=True)
    contact_phone = db.Column(db.String(50), nullable=True)
    contact_email = db.Column(db.String(255), nullable=True)
    profile_image = db.Column(db.String(500), nullable=True)
    visibility_settings = db.Column(db.JSON, default=dict, nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    @property
    def visibility(self):
        defaults = {
            "show_photo": True,
            "show_lineage": True,
            "show_bio": True,
            "show_secondary_bio": True,
            "show_stats": True,
            "show_experience": True,
            "show_consultations": True,
            "show_pujas": True,
            "show_cta_button": True,
            "show_darshan": False,
            "show_ashram": False,
            "show_contact": False,
        }
        if self.visibility_settings and isinstance(self.visibility_settings, dict):
            defaults.update(self.visibility_settings)
        return defaults

    def __repr__(self):
        return f"<GurujiProfile {self.full_title}>"



class MediaFile(db.Model):
    __tablename__ = "media_files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    mime_type = db.Column(db.String(100), nullable=False)
    file_category = db.Column(db.String(50), default="general", nullable=False)  # product, puja, blog, guruji
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    def __repr__(self):
        return f"<MediaFile {self.filename}>"


class Banner(db.Model):
    __tablename__ = "banners"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    link_url = db.Column(db.String(500), nullable=True)
    position = db.Column(db.String(50), default="hero", nullable=False, index=True)  # hero, announcement, promo
    button_text = db.Column(db.String(100), nullable=True)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Banner {self.title}>"

