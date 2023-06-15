if IN_DOCKER: # type: ignore
    print("RUNNING IN DOCKER...")
    assert MIDDLEWARE[:1] == [  # type: ignore # noqa: F821
        'django.middleware.security.SecurityMiddleware'
    ]
else:
    print("RUNNING IN LOCAL...")
