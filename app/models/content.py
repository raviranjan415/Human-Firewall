"""Learning content models: paths, modules, lessons, videos, comics, games."""

from app.extensions import db
from app.models.user import TimestampMixin

# Content workflow states (section 20 of the specification).
CONTENT_STATES = ("draft", "review", "published", "archived")

DIFFICULTY_LEVELS = ("beginner", "intermediate", "advanced", "expert")


class LearningPath(db.Model, TimestampMixin):
    __tablename__ = "learning_paths"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_hi = db.Column(db.String(200))
    description_en = db.Column(db.Text)
    description_hi = db.Column(db.Text)
    level = db.Column(db.String(24), default="beginner", nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    state = db.Column(db.String(24), default="published", nullable=False)

    modules = db.relationship(
        "Module", back_populates="path", order_by="Module.order_index", cascade="all, delete-orphan"
    )


class Module(db.Model, TimestampMixin):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)
    path_id = db.Column(db.Integer, db.ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False)
    slug = db.Column(db.String(120), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    title_hi = db.Column(db.String(200))
    summary_en = db.Column(db.Text)
    summary_hi = db.Column(db.Text)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    state = db.Column(db.String(24), default="published", nullable=False)

    path = db.relationship("LearningPath", back_populates="modules")
    lessons = db.relationship(
        "Lesson", back_populates="module", order_by="Lesson.order_index", cascade="all, delete-orphan"
    )

    __table_args__ = (db.UniqueConstraint("path_id", "slug", name="uq_module_slug_per_path"),)


class Lesson(db.Model, TimestampMixin):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    slug = db.Column(db.String(140), nullable=False)
    title_en = db.Column(db.String(220), nullable=False)
    title_hi = db.Column(db.String(220))
    summary_en = db.Column(db.Text)
    summary_hi = db.Column(db.Text)
    category = db.Column(db.String(80), index=True)
    difficulty = db.Column(db.String(24), default="beginner", nullable=False, index=True)
    duration_minutes = db.Column(db.Integer, default=5, nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    state = db.Column(db.String(24), default="published", nullable=False)

    module = db.relationship("Module", back_populates="lessons")
    video_assets = db.relationship("VideoAsset", back_populates="lesson", cascade="all, delete-orphan")
    questions = db.relationship("Question", back_populates="lesson", cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint("module_id", "slug", name="uq_lesson_slug_per_module"),)


class VideoAsset(db.Model, TimestampMixin):
    """A video lesson. Rendered media may not exist yet — the record, script
    and prototype flag are always honest about what is available."""

    __tablename__ = "video_assets"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    title_en = db.Column(db.String(220), nullable=False)
    title_hi = db.Column(db.String(220))
    # Script, storyboard and narration are authored for every lesson even when
    # rendered media is not yet produced.
    script_en = db.Column(db.Text)
    script_hi = db.Column(db.Text)
    narration_en = db.Column(db.Text)
    narration_hi = db.Column(db.Text)
    thumbnail_url = db.Column(db.String(500))
    duration_seconds = db.Column(db.Integer, default=0, nullable=False)
    is_prototype = db.Column(db.Boolean, default=True, nullable=False)
    available_languages = db.Column(db.String(32), default="en", nullable=False)
    transcript_en = db.Column(db.Text)
    transcript_hi = db.Column(db.Text)
    captions_en_url = db.Column(db.String(500))
    captions_hi_url = db.Column(db.String(500))
    order_index = db.Column(db.Integer, default=0, nullable=False)

    lesson = db.relationship("Lesson", back_populates="video_assets")
    tracks = db.relationship(
        "VideoLanguageTrack", back_populates="video", cascade="all, delete-orphan"
    )

    @property
    def languages(self) -> list[str]:
        return [lang.strip() for lang in (self.available_languages or "").split(",") if lang.strip()]


class VideoLanguageTrack(db.Model):
    __tablename__ = "video_language_tracks"

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video_assets.id", ondelete="CASCADE"), nullable=False)
    language = db.Column(db.String(8), nullable=False)
    media_url = db.Column(db.String(500))
    captions_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=False, nullable=False)

    video = db.relationship("VideoAsset", back_populates="tracks")

    __table_args__ = (db.UniqueConstraint("video_id", "language", name="uq_video_language"),)


class Comic(db.Model, TimestampMixin):
    __tablename__ = "comics"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    collection = db.Column(db.String(140), index=True)
    title_en = db.Column(db.String(220), nullable=False)
    title_hi = db.Column(db.String(220))
    character = db.Column(db.String(140))
    situation_en = db.Column(db.Text)
    situation_hi = db.Column(db.Text)
    problem_en = db.Column(db.Text)
    problem_hi = db.Column(db.Text)
    decision_en = db.Column(db.Text)
    decision_hi = db.Column(db.Text)
    resolution_en = db.Column(db.Text)
    resolution_hi = db.Column(db.Text)
    lesson_1_en = db.Column(db.Text)
    lesson_2_en = db.Column(db.Text)
    lesson_3_en = db.Column(db.Text)
    lesson_1_hi = db.Column(db.Text)
    lesson_2_hi = db.Column(db.Text)
    lesson_3_hi = db.Column(db.Text)
    related_lab_id = db.Column(db.Integer, db.ForeignKey("labs.id"))
    badge_name = db.Column(db.String(120))
    difficulty = db.Column(db.String(24), default="beginner", nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    state = db.Column(db.String(24), default="published", nullable=False)

    panels = db.relationship(
        "ComicPanel", back_populates="comic", order_by="ComicPanel.order_index", cascade="all, delete-orphan"
    )


class ComicPanel(db.Model):
    __tablename__ = "comic_panels"

    id = db.Column(db.Integer, primary_key=True)
    comic_id = db.Column(db.Integer, db.ForeignKey("comics.id", ondelete="CASCADE"), nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    image_url = db.Column(db.String(500))
    caption_en = db.Column(db.Text)
    caption_hi = db.Column(db.Text)
    dialogue_en = db.Column(db.Text)
    dialogue_hi = db.Column(db.Text)
    alt_text_en = db.Column(db.String(400))
    alt_text_hi = db.Column(db.String(400))

    comic = db.relationship("Comic", back_populates="panels")


class Game(db.Model, TimestampMixin):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_hi = db.Column(db.String(200))
    instructions_en = db.Column(db.Text)
    instructions_hi = db.Column(db.Text)
    debrief_en = db.Column(db.Text)
    debrief_hi = db.Column(db.Text)
    difficulty = db.Column(db.String(24), default="beginner", nullable=False)
    timed = db.Column(db.Boolean, default=False, nullable=False)
    time_limit_seconds = db.Column(db.Integer)
    xp_reward = db.Column(db.Integer, default=25, nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    state = db.Column(db.String(24), default="published", nullable=False)

    scenarios = db.relationship(
        "GameScenario", back_populates="game", order_by="GameScenario.order_index", cascade="all, delete-orphan"
    )


class GameScenario(db.Model, TimestampMixin):
    __tablename__ = "game_scenarios"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    scenario_type = db.Column(db.String(40), default="email", nullable=False)  # email|sms|call|page|chat
    sender = db.Column(db.String(200))
    subject_en = db.Column(db.String(300))
    subject_hi = db.Column(db.String(300))
    body_en = db.Column(db.Text)
    body_hi = db.Column(db.Text)
    meta_json = db.Column(db.Text)  # links, attachments, etc. (JSON string)
    is_threat = db.Column(db.Boolean, default=True, nullable=False)
    difficulty = db.Column(db.String(24), default="beginner", nullable=False)
    explanation_en = db.Column(db.Text)
    explanation_hi = db.Column(db.Text)
    warning_signs_en = db.Column(db.Text)
    warning_signs_hi = db.Column(db.Text)
    xp_value = db.Column(db.Integer, default=10, nullable=False)

    game = db.relationship("Game", back_populates="scenarios")
    choices = db.relationship(
        "ScenarioChoice", back_populates="scenario", order_by="ScenarioChoice.order_index",
        cascade="all, delete-orphan",
    )


class ScenarioChoice(db.Model):
    __tablename__ = "scenario_choices"

    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey("game_scenarios.id", ondelete="CASCADE"), nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    text_en = db.Column(db.String(300), nullable=False)
    text_hi = db.Column(db.String(300))
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
    feedback_en = db.Column(db.Text)
    feedback_hi = db.Column(db.Text)

    scenario = db.relationship("GameScenario", back_populates="choices")


class Question(db.Model, TimestampMixin):
    """Assessment question used for baseline / post / retention checks."""

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id", ondelete="CASCADE"))
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id", ondelete="CASCADE"))
    topic = db.Column(db.String(120), index=True)
    phase = db.Column(db.String(24), default="knowledge_check", nullable=False)
    # knowledge_check | baseline | post | retention
    text_en = db.Column(db.Text, nullable=False)
    text_hi = db.Column(db.Text)
    options_json = db.Column(db.Text, nullable=False)  # JSON list of {en, hi}
    correct_index = db.Column(db.Integer, nullable=False)
    explanation_en = db.Column(db.Text)
    explanation_hi = db.Column(db.Text)
    order_index = db.Column(db.Integer, default=0, nullable=False)

    lesson = db.relationship("Lesson", back_populates="questions")

    def options(self, locale: str = "en") -> list[str]:
        import json

        try:
            raw = json.loads(self.options_json or "[]")
        except ValueError:
            return []
        result = []
        for option in raw:
            if isinstance(option, dict):
                result.append(option.get(locale) or option.get("en") or "")
            else:
                result.append(str(option))
        return result
