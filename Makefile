D = docker
DC = docker compose
PROJECT = deploy/logs.yaml
STORAGE_FILE = deploy/storage.yaml

.PHONY: project
project-build:
	${DC} -f ${PROJECT} up --build -d

.PHONY: stop-project
stop-project:
	${DC} -f ${PROJECT} stop

.PHONY: down-project
down-project:
	${DC} -f ${PROJECT} down

.PHONY: kill-project
kill-project:
	make down-project && make prune-volume-all

.PHONY: logs-project
logs-project:
	${DC} -f ${PROJECT} logs -f


.PHONY: storage
storage:
	${DC} -f ${STORAGE_FILE} up --build -d

.PHONY: down-storage
down-storage:
	${DC} -f ${STORAGE_FILE} down

.PHONY: kill-storage
kill-storage:
	make down-storage && make prune-volume-all
