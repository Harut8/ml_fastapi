#!/bin/bash
alembic upgrade head
echo "Applied database migrations !!!!!!!!!"
exec "$@"
