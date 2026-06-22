import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200


def test_home_page_contains_form(client):
    response = client.get('/')
    assert b'cv_file' in response.data
    assert b'job_description' in response.data


def test_analyze_no_file(client):
    response = client.post('/analyze', data={
        'job_description': 'Some job description'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_analyze_no_job_description(client):
    response = client.post('/analyze', data={}, follow_redirects=True)
    assert response.status_code == 200