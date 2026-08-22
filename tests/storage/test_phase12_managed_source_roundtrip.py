import io
import json
import os
import sys
import uuid

from pathlib import Path


# ==========================================================
# PHASE 12.18 - THE ORIGINAL SOURCE SURVIVES END TO END
# ==========================================================
#
# RELEASE BLOCKER 2, and the release rule attached to it:
#
#   "Do NOT declare VIGILOX deployment ready if a NEW
#    successfully completed document still cannot display its
#    original uploaded source image."
#
# So this walks the whole path with a real API, a real worker,
# real managed storage and a real database, and then asks the
# image endpoint for the bytes back:
#
#   POST /api/v1/document-jobs      original bytes
#     -> pending job source storage
#     -> worker claims the job
#     -> FAKE pipeline               <- no OCR, no Groq
#     -> real PersistenceService
#     -> managed source storage
#     -> documents row
#     -> GET /api/v1/documents/{id}/image
#     -> byte-for-byte comparison
#
# ZERO REAL GROQ CALLS. The pipeline is injected and returns a
# literal, so the provider is never contacted. That is
# deliberate: the release brief forbids spending quota on these
# fixes, and the question here is whether STORAGE preserves
# bytes, which OCR and extraction have nothing to do with.
#
#
# WHY NOT REUSE AN EXISTING DOCUMENT
# ----------------------------------------------------------
# The brief is explicit, and it is right: an old row whose file
# is missing proves nothing about whether new persistence
# works, and an old row whose file is present proves nothing
# either -- it was written by whatever the code did then.
#
# This creates its own document and deletes it again.
#
#
# WHAT IT TOUCHES
# ----------------------------------------------------------
# Only rows and files it created. The job id, the document id
# and the pending source name are all recorded as they are
# made and removed in a finally block. There are real user
# documents in this database and this test must not go near
# them.
# ==========================================================


PROJECT_ROOT = (
    Path(
        __file__
    )
    .resolve()
    .parents[2]
)

if str(
    PROJECT_ROOT
) not in sys.path:

    sys.path.insert(
        0,
        str(
            PROJECT_ROOT
        ),
    )


from dotenv import load_dotenv  # noqa: E402

load_dotenv(
    PROJECT_ROOT
    / ".env"
)

# The API process must not build a pipeline: this test injects
# its own into the worker and the API never runs OCR here.
os.environ["VIGILOX_API_EAGER_PIPELINE"] = "false"

from fastapi.testclient import TestClient  # noqa: E402

from backend.app.main import app  # noqa: E402


# ==========================================================
# ASSERTIONS
# ==========================================================

def assert_equal(
    actual,
    expected,
    message: str,
) -> None:

    if actual != expected:

        raise AssertionError(
            f"{message}\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}"
        )


def assert_true(
    value,
    message: str,
) -> None:

    if not value:
        raise AssertionError(
            message
        )


def section(
    title: str,
) -> None:

    print()
    print(
        "-" * 74
    )
    print(
        title
    )
    print(
        "-" * 74
    )


def ok(
    message: str,
) -> None:

    print(
        f"[PASS] {message}"
    )


# ==========================================================
# A SYNTHETIC SOURCE
# ==========================================================
#
# A real, decodable PNG built here rather than read from
# samples/. samples/ is gitignored and one of its files is a
# photograph of an apparently real identity card; a test that
# depended on it would not run on a clean checkout and would
# be handling a real person's document.
#
# Pillow is already a dependency -- the pipeline uses it -- so
# this costs nothing.
# ==========================================================

def synthetic_png(
    *,
    marker: str,
) -> bytes:

    from PIL import Image, ImageDraw

    image = Image.new(
        "RGB",
        (
            420,
            260,
        ),
        (
            250,
            250,
252,
        ),
    )

    draw = ImageDraw.Draw(
        image
    )

    # Content that varies per run, so a comparison cannot
    # accidentally pass against a cached or wrong file.
    draw.rectangle(
        [
            10,
            10,
            410,
            250,
        ],
        outline=(
            30,
            60,
            120,
        ),
        width=4,
    )

    draw.text(
        (
            28,
            40,
        ),
        f"VIGILOX SYNTHETIC {marker}",
        fill=(
            20,
            20,
            30,
        ),
    )

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG",
    )

    return buffer.getvalue()


# ==========================================================
# A PIPELINE THAT NEVER CALLS A PROVIDER
# ==========================================================

class FakePipeline:

    """
    Returns a valid analysis without touching OCR or Groq.

    The shape matches what PersistenceService reads. Nothing
    here is about extraction quality -- the question is whether
    the ORIGINAL BYTES reach managed storage and come back, and
    that is decided entirely by the storage and persistence
    layers.
    """

    def __init__(
        self,
    ) -> None:

        self.calls = 0

        self.paths: list[str] = []


    def process(
        self,
        image_path,
        reference_date=None,
        timer=None,
    ):

        self.calls += 1

        self.paths.append(
            str(
                image_path
            )
        )

        return {
            "extraction": {
                "document_type": "guard_license",
                "fields": {
                    "full_name": "SAMPLE,JANE",
                    "licence_number": "GL-0000001",
                    "expiry_date": "2030-01-01",
                    "issuer": "TX DPS",
                },
            },
            "ocr_lines": [],
            "evidence_flags": {},
            "field_confidence": {},
            "date_validation": {},
            "anomaly_validation": {},
            "review_decision": {
                "decision": "REVIEW_REQUIRED",
                "review_required": True,
                "priority": "MEDIUM",
            },
        }


# ==========================================================
# THE TEST
# ==========================================================

def main() -> int:

    print(
        "=" * 74
    )
    print(
        "PHASE 12.18 - MANAGED SOURCE ROUND TRIP "
        "(NO PROVIDER CALLS)"
    )
    print(
        "=" * 74
    )

    from backend.app.services.document_storage_service import (
        DocumentStorageService,
    )
    from backend.app.services.document_worker import (
        DocumentWorker,
    )
    from backend.app.services.job_source_store import (
        JobSourceStore,
    )
    from database.database import SessionLocal
    from database.job_repositories import (
        DocumentJobRepository,
    )
    from database.models import DocumentJobModel

    marker = uuid.uuid4().hex[:8]

    source_bytes = synthetic_png(
        marker=marker,
    )

    print(
        f"  synthetic source: {len(source_bytes)} bytes, "
        f"marker {marker}"
    )

    job_id = None
    document_id = None

    # The CONTEXT MANAGER form, deliberately.
    #
    # TestClient(app) without it never runs the lifespan, so
    # app.state.jobs is never built and every job route fails
    # with AttributeError -> 500. That is what the first run of
    # this test did, and the 500 said nothing about the code
    # under test.
    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    client.__enter__()

    try:

        # ==============================================
        # 1. UPLOAD -> PENDING SOURCE STORAGE
        # ==============================================

        section(
            "STEP 1 - THE UPLOAD LANDS IN PENDING STORAGE"
        )

        response = client.post(
            "/api/v1/document-jobs",
            files={
                "file": (
                    f"synthetic-{marker}.png",
                    io.BytesIO(
                        source_bytes
                    ),
                    "image/png",
                ),
            },
        )

        assert_equal(
            response.status_code,
            202,
            (
                "A job creation must return 202 Accepted.\n"
                f"{response.text[:400]}"
            ),
        )

        created = response.json()

        job_id = created["job_id"]

        assert_equal(
            created["status"],
            "QUEUED",
            "A new job starts QUEUED.",
        )

        ok(
            f"job {job_id[:8]} created, status QUEUED"
        )

        # The pending bytes must be on disk and identical.
        pending_root = JobSourceStore().pending_root

        with SessionLocal() as session:

            row = session.get(
                DocumentJobModel,
                job_id,
            )

            source_name = row.source_name

        pending_path = pending_root / source_name

        assert_true(
            pending_path.is_file(),
            (
                "The uploaded bytes must be in pending "
                "storage before the worker ever runs."
            ),
        )

        assert_equal(
            pending_path.read_bytes(),
            source_bytes,
            (
                "Pending storage must hold the ORIGINAL "
                "bytes, unmodified. Everything downstream "
                "copies from here."
            ),
        )

        ok(
            f"pending source is byte-identical "
            f"({pending_path.stat().st_size} bytes)"
        )

        # ==============================================
        # 2. THE WORKER, WITH A FAKE PIPELINE
        # ==============================================

        section(
            "STEP 2 - THE WORKER PROCESSES IT WITHOUT A "
            "PROVIDER"
        )

        pipeline = FakePipeline()

        worker = DocumentWorker(
            worker_id=f"managed-source-{marker}",
            pipeline=pipeline,
        )

        # only_job_ids so this cannot claim a real upload
        # waiting in the queue. There are user jobs in this
        # database.
        claimed = worker.process_one(
            only_job_ids=job_id,
        )

        assert_true(
            claimed,
            (
                "The worker must claim and process the job "
                "this test created."
            ),
        )

        assert_equal(
            pipeline.calls,
            1,
            (
                "The injected pipeline must have been called "
                "exactly once -- and it is the only pipeline "
                "in play, which is what makes this run cost "
                "no provider quota."
            ),
        )

        ok(
            "the worker processed the job through an injected "
            "pipeline: zero OCR passes, zero provider calls"
        )

        # ==============================================
        # 3. THE JOB COMPLETED AND NAMED A DOCUMENT
        # ==============================================

        status = client.get(
            f"/api/v1/document-jobs/{job_id}"
        ).json()

        assert_equal(
            status["status"],
            "COMPLETED",
            (
                "The job must be COMPLETED.\n"
                f"{json.dumps(status)[:400]}"
            ),
        )

        document_id = status["document_id"]

        assert_true(
            bool(
                document_id
            ),
            (
                "A completed job must name the document it "
                "produced."
            ),
        )

        ok(
            f"job COMPLETED and produced document "
            f"{document_id[:8]}"
        )

        # ==============================================
        # 4. MANAGED STORAGE HOLDS THE ORIGINAL
        # ==============================================

        section(
            "STEP 3 - MANAGED STORAGE HOLDS THE ORIGINAL "
            "BYTES"
        )

        storage = DocumentStorageService()

        original_path = storage.get_original_path(
            document_id=document_id,
            content_type="image/png",
        )

        assert_true(
            original_path.is_file(),
            (
                "The original must be in managed storage "
                "after a successful completion. This is the "
                "invariant the release blocker is about."
            ),
        )

        stored = original_path.read_bytes()

        assert_equal(
            len(
                stored
            ),
            len(
                source_bytes
            ),
            (
                "The managed original must be the same size "
                "as what was uploaded."
            ),
        )

        assert_true(
            stored == source_bytes,
            (
                "The managed original must be BYTE-IDENTICAL "
                "to the upload. Same length but different "
                "content would mean the pipeline wrote a "
                "processed image over the source."
            ),
        )

        ok(
            f"managed original is byte-identical to the "
            f"upload ({len(stored)} bytes)"
        )

        # ==============================================
        # 5. THE IMAGE ENDPOINT RETURNS IT
        # ==============================================

        section(
            "STEP 4 - THE IMAGE ENDPOINT RETURNS THE "
            "ORIGINAL"
        )

        image = client.get(
            f"/api/v1/documents/{document_id}/image"
        )

        assert_equal(
            image.status_code,
            200,
            (
                "The image endpoint must return 200 for a "
                "document whose source exists.\n"
                f"{image.text[:300]}"
            ),
        )

        content_type = image.headers.get(
            "content-type",
            "",
        )

        assert_true(
            content_type.startswith(
                "image/png"
            ),
            (
                "The response must carry the real content "
                "type. A browser handed the wrong type is "
                "one of the ways an <img> fails to decode.\n"
                f"got: {content_type!r}"
            ),
        )

        assert_true(
            image.content == source_bytes,
            (
                "The endpoint must return the ORIGINAL bytes. "
                "This is the byte-preservation guarantee the "
                "workspace depends on."
            ),
        )

        ok(
            f"GET image returned 200, {content_type}, "
            f"{len(image.content)} bytes, byte-identical to "
            "the upload"
        )

        # ------------------------------------------
        # AND IT IS A DECODABLE IMAGE
        # ------------------------------------------
        #
        # Byte equality is not quite the whole claim. The
        # workspace needs the BROWSER to decode it, so the
        # bytes are put through a decoder here.

        from PIL import Image as PillowImage

        decoded = PillowImage.open(
            io.BytesIO(
                image.content
            )
        )

        decoded.load()

        assert_equal(
            decoded.format,
            "PNG",
            "The returned bytes must decode as PNG.",
        )

        assert_true(
            decoded.width > 0 and decoded.height > 0,
            (
                "The decoded image must have a real intrinsic "
                "size -- every evidence box is a percentage "
                "of it."
            ),
        )

        ok(
            f"the returned bytes decode as "
            f"{decoded.format} {decoded.width}x"
            f"{decoded.height}, so a browser can render them "
            "and evidence has a size to work against"
        )

        # ==============================================
        # 6. THE DOCUMENT READ PATH AGREES
        # ==============================================

        section(
            "STEP 5 - THE WORKSPACE PAYLOAD POINTS AT IT"
        )

        detail = client.get(
            f"/api/v1/documents/{document_id}"
        )

        assert_equal(
            detail.status_code,
            200,
            "The document detail must load.",
        )

        payload = detail.json()

        # document_id, not id. The detail payload names it
        # explicitly; reading `id` here was a guess and it was
        # wrong.
        assert_equal(
            payload["document"]["document_id"],
            document_id,
            "The detail must be for this document.",
        )

        assert_equal(
            payload["document"]["content_type"],
            "image/png",
            (
                "The stored content type must match what was "
                "uploaded -- it is what the image endpoint "
                "serves the file as."
            ),
        )

        ok(
            "the document detail loads and its content type "
            "matches the served image"
        )

        # ==============================================
        # 7. PENDING SOURCE WAS CLEANED UP
        # ==============================================

        assert_true(
            not pending_path.exists(),
            (
                "A completed job must not leave its pending "
                "source behind. The bytes now live in managed "
                "storage; a second copy is a slow leak of the "
                "pending volume."
            ),
        )

        ok(
            "the pending source was removed once the original "
            "reached managed storage"
        )

        print()
        print(
            "=" * 74
        )
        print(
            "[PASS] A NEW COMPLETED DOCUMENT SERVES ITS "
            "ORIGINAL SOURCE IMAGE"
        )
        print(
            "=" * 74
        )

        return 0

    finally:

        # ==============================================
        # CLEAN UP ONLY WHAT THIS TEST MADE
        # ==============================================
        #
        # There are real user documents and real queued jobs
        # in this database. Named ids only -- nothing
        # wildcarded, nothing truncated.

        removed = []

        if document_id:

            try:
                from backend.app.services.document_deletion_service import (  # noqa: E501
                    DocumentDeletionService,
                )

                DocumentDeletionService().delete_document(
                    document_id
                )

                removed.append(
                    f"document {document_id[:8]}"
                )

            except Exception as error:

                print(
                    f"       (could not delete document: "
                    f"{type(error).__name__}: {error})"
                )

        if job_id:

            try:
                with SessionLocal() as session:

                    deleted = session.query(
                        DocumentJobModel
                    ).filter(
                        DocumentJobModel.id == job_id
                    ).delete()

                    session.commit()

                if deleted:
                    removed.append(
                        f"job {job_id[:8]}"
                    )

            except Exception as error:

                print(
                    f"       (could not delete job: "
                    f"{type(error).__name__}: {error})"
                )

        print()
        print(
            "  cleaned up: "
            + (
                ", ".join(
                    removed
                )
                if removed
                else "nothing to remove"
            )
        )

        client.__exit__(
            None,
            None,
            None,
        )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
