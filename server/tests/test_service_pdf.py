import pytest
from unittest.mock import patch, MagicMock
from server.services.PdfService import PdfService
from server.models.models import PdfFile

@pytest.mark.anyio
async def test_pdf_progress_calculation(db_session):
    # Manually add some PDFs to the test DB
    user_id = 1
    p1 = PdfFile(filename="1.pdf", filepath="p1", user_id=user_id, completed=True)
    p2 = PdfFile(filename="2.pdf", filepath="p2", user_id=user_id, completed=False)
    db_session.add_all([p1, p2])
    db_session.commit()

    total, completed, percent = PdfService.get_progress(db_session, user_id)
    
    assert total == 2
    assert completed == 1
    assert percent == 50.0

@pytest.mark.anyio
async def test_toggle_pdf_completion(db_session):
    user_id = 99
    pdf = PdfFile(filename="test.pdf", filepath="path", user_id=user_id, completed=False)
    db_session.add(pdf)
    db_session.commit()

    # Toggle to true
    updated = PdfService.mark_pdf_completed(db_session, pdf.id, user_id)
    assert updated.completed is True
    assert updated.completed_at is not None

    # Toggle back to false
    updated = PdfService.mark_pdf_completed(db_session, pdf.id, user_id)
    assert updated.completed is False
    assert updated.completed_at is None